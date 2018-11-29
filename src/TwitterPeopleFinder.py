from Person import Person
import tweepy
from geopy import geocoders
from datetime import datetime
import re
import pandas as pd
from collections import defaultdict
from geopy.exc import GeocoderTimedOut
from nameparser import HumanName

geocoders.options.default_user_agent = 'HamedRazavi/'
gn = geocoders.Nominatim() 
gy = geocoders.Yandex(lang='en')

fl = open('../data/occupations.csv', 'r')
occupations_raw = fl.read()
occupations = occupations_raw.split('\n')
occupations.remove('')
occupations = [word.lower() for word in occupations]

class TwitterPeopleFinder:
    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET):
        """
        """
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        self.api = tweepy.API(auth)
    
    def find_users(self, person, page_number=1):
        """
        Returns the users list the exact output of the Twitter api.
        """
        first_name = person.first_name
        last_name = person.last_name
        users = self.api.search_users(first_name + " " + last_name, page = page_number)
        return users
    
    def is_listedname_similar(self, person, listed_name):
        """
        Check if the user listed name in Twitter mataches the first
        and last names of the person.
        """
        first_name = person.first_name.lower()
        last_name = person.last_name.lower()
        listed_name_lower = listed_name.lower()
        i_f = listed_name_lower.find(first_name)
        i_l = listed_name_lower.find(last_name)
        return (not i_f == -1) & (not i_l == -1)
    
    def get_user_map(self, user):
        user_map = {
            'id_str': [user.id_str],
            'listed_name': [user.name],
            'screen_name': [user.screen_name],
            'location': [user.location],
            'description': [user.description],
            'created_at': [user.created_at],
            'verified': [user.verified],
            'followers_count': [user.followers_count],
            'followings_count': [user.friends_count], # number of pepole the user follows
            'listed_count': [user.listed_count], # number of public lists the user is a member of
            'favourites_count': [user.favourites_count], # the number of Tweets the user has liked
            'statuses_count': [user.statuses_count], # number of Tweets (including retweets) issued by the user (maybe devide by how old the account is to get a better feature),
            'contributors_enabled': [user.contributors_enabled], 
            'default_profile': [user.default_profile],
            'protected': [user.protected],
            'url': [user.url],
        }
        return user_map 
    
    def find_users_as_df(self, person, page_number=1):
        """
        Returns the Twitter raw users data, but as a Pandas dataframe
        """
        users = self.find_users(person, page_number=page_number)
        users_map = defaultdict(list)
        for user in users:
            user_map = self.get_user_map(user)
            for key in user_map.keys():
                users_map[key].append(user_map[key][0])
        df_users = pd.DataFrame(users_map)
        return df_users
        
    
    def get_country_code_old(self, location):
        loc = None
        try:
            loc = gn.geocode(language='en', exactly_one=True, query=location, extratags=True, addressdetails=True)
        except Exception as e:
            print("Geocoder connection issue?", e)
            pass
        if loc:
            country_code = loc.raw['address']['country_code']
            return country_code.upper()
        else:
            return ''
        
    def get_country_code(self, location):
        location = location.replace('Greater', '')
        loc = None
        try:
            loc = gy.geocode(query=location, timeout=2)
        except GeocoderTimedOut:
            loc = gy.geocode(query=location)
        except Exception as e:
            print("Geocoder connection issue?", e)
            pass
        if loc:
            try:
                country_code = loc.raw['metaDataProperty']['GeocoderMetaData']['Address']['country_code']
                return country_code.upper()
            except:
                return ''
        else:
            return ''
        
    def get_middle_name(self, person, listed_name):
        """
        listed_name is the listed name of the user, i.e. user.name
        """
        try:
            first_name = person.first_name.lower()
            last_name = person.last_name.lower()
            i_f = listed_name.lower().find(first_name) + len(first_name)
            i_l = listed_name.lower().find(last_name)
            if self.is_listedname_similar(person, listed_name):
                return (''.join(listed_name[i_f + 1:i_l])).strip().lower().capitalize()
            else:
                return ''
        except:
            return ''
        
    def get_account_age(self, created_at):
        now = datetime.now()
        how_old = max(((now - created_at).days) / 365, 1)  # how old the account is in years
        return how_old
    
    def extract_occupation(self, text, occupations):
        """
        Extracts occupation which exists in the list occupations from the text.
        Returns a list of occupations in the text.
        """
        occu_list = []
        text = text.lower()
        for occupation in occupations:
            if re.search(r'\b{}\b'.format(occupation), text):
                occu_list.append(occupation)
        return ', '.join(occu_list)
    
    def is_famous(self, user):
        try: 
            followers_net = user.followers_count - user.friends_count
            follow_ratio = user.followers_count / (user.friends_count + 1)
            followers_net_normalized = followers_net / self.get_account_age(user.created_at)
            cond1 = (followers_net > 1000) & (follow_ratio > 100) & (user.verified == 1)
            cond2 = (followers_net_normalized > 10000) & (follow_ratio > 1000)
            is_famous = cond1 | cond2
            return is_famous
        except Exception as e:
            print(e)
            return ''        

    def user_to_person(self, user):
        """
        Converts Twitter api generic user output to person as 
        an instance of the Person class
        """
        person = Person()
        name_split = HumanName(user.name)
        person.first_name = name_split.first
        person.middle_name = name_split.middle
        person.last_name = name_split.last
        person.domicile = self.get_country_code(user.location)
        person.description = user.description
        person.occupation = self.extract_occupation(user.description, occupations)
        person.is_famous = self.is_famous(user)
        person.set_raw()
        return person

    def __is_match(self, person, p, strict_match):
        """
        Check if the optional fields of given 'person', such as middle name, 
        domicile and nationality matches with the person 'p' found.
        Note that "listed name" is already checked before calling this function in 
        the 'find' method.
        """
        cond1 = person.domicile.lower() == p.domicile.lower()
        cond2 = person.domicile.lower() == p.nationality.lower()
        cond3 = (p.domicile == '') & (p.nationality == '')
        cond4 = True
        if strict_match:
            cond4 =  (person.first_name.lower() == p.first_name.lower()) & (person.last_name.lower() == p.last_name.lower())
        if (cond1 | cond2 | cond3) & cond4:
            return True
        else:
            return False

    def find(self, person, strict_match=0, page_number=1):
        """
        Note that the given 'person' nationality and domicile either should
        be empty or based on ISO 3166 alpha 2 coding. (e.g., US for United States
        of America and not USA)
        If strict_match=1 then the first name and last name of the found users
        must match with the given person. 
        Returns the users which match 'person' as a list of Person() class
        """
        users = self.find_users(person, page_number=page_number)
        persons = []
        for user in users:
            if self.is_listedname_similar(person, user.name):
                p = self.user_to_person(user)
                if self.__is_match(person, p, strict_match):
                    persons.append(p)
        return persons
    
    def find_as_df(self, person, strict_match=0, page_number=1):
        """
        Returns the users which match 'person' as a Pandas dataframe. 
        """
        persons = self.find(person, strict_match, page_number=page_number)
        df = pd.DataFrame()
        for person in persons:
            dfperson = person.to_df(pd)
            df = pd.concat([df, dfperson], axis = 0)
        df = df.reset_index().drop('index', axis = 1)
        return df        