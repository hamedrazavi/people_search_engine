import requests
import re
import pandas as pd
import random
from collections import defaultdict
from Person import Person
from nameparser import HumanName
from geopy import geocoders
from geopy.exc import GeocoderTimedOut
from time import sleep

user_agents = {}
user_agents[0] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
user_agents[1] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
user_agents[2] = 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'
user_agents[3] = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'
user_agents[4] = 'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18'
user_agents[5] = 'Mozilla/5.0 (Linux; U; Android 4.0.4; pt-br; MZ608 Build/7.7.1-141-7-FLEM-UMTS-LA) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30'
user_agents[6] = 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; WT19M-FI Build/KTU84Q)'
user_agents[7] = 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; LG-L38C Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MMS/LG-Android-MMS-V1.0/1.2'

accept_lang = {}
accept_lang[0] = 'en-US,en;q=0.9,fa;q=0.8,fr;q=0.7'
accept_lang[1] = 'en-US,en;q=0.9;q=0.8;q=0.7'
accept_lang[2] = 'en-US, en'

dnt_status = ['0', '1']

request_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': accept_lang[2],
    'cache-control': 'max-age=0',
    'cookie': 'bcookie="v=2&e2b334d5-7bd4-40ac-818d-4d8cbda0b965"; bscookie="v=1&201810161905207570283f-ddb6-4bf4-89b8-28fbf0374ed8AQE2LYO2WS8xcHO64GBsUe5FX-x0YDYK"; _ga=GA1.2.1412527673.1539716986; _guid=562fb94e-964b-4d11-9af0-d143a967275d; visit="v=1&M"; spectroscopyId=886774b9-f892-4098-9626-c48cf2f6e375; PLAY_SESSION=4e360b9c03e09f73f941a400077a9cfa7a35da6b-jobsEmailMember=1; lil-lang=en_US; __utmc=226841088; UserMatchHistory=AQK31IcBpqP6cAAAAWcsr-0p3gZ3n-ko8ZjJcuSAG7k_-kpWudcXZpf-vr1yZKeliy-tDLRwmTAzc-zNGfI3bK6S46JSXNkb3QrJZmk; li_oatml=AQH2SpjfVdo0aQAAAWcsr-8kySdjIJXRnLoosGSWDyv55fwmGyKoEwgKkaObfAhsfhgmyC7BZEeeV8stKlIG5qPNVOAaLKJq; utag_main=v_id:0166b67c39d1000b328aa91b497903079002207100ac2$_sn:34$_ss:0$_st:1542646226879$_se:12$ses_id:1542642986879%3Bexp-session$_pn:2%3Bexp-session; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; _lipt=CwEAAAFnQkO_oWkCOMbzpIbmgztYQEwrf1-juyYZfsWNPVry4Hf1ozofzz_P73JOacuyrP04MMoNkHvg_bHOFkhGBAj1NNtph72SJ7cLGAXvVFfpansmw3WhXjPIdXjOjJxHGKjxfYfzIQo6VToDtDY74XniDSY9sgIWPkTO4QjYotzzApkE0ntcRTuaTrF_O_6fySQWzYkrpiVONYNDOJuqxue2xl-xtSWh3CVhRwkPDIadp1lGzV1Ds0rFepXUmur6sIxJX4jzGXCUjJtGzCFQed4QgvLIwYetVPaB56t1j0gLm7H4FIpvvW-N5mdzy8JP_DomX3LgFN8KdKH25iTGDjf7SZ2t4vDvd0NlQIDeIhdUSMNlcOLWaqjMQKChU0TAcCs3O5YBQISHDBWedxs0DbzehqVHL5HKYCP86uNf_LB8W4-A2BaBhLk0csR7i3vjBkB41tV8GdQIK2vrwEdDhjK0j9FmOihpaoGEfNrIH3NxXBGWDrCexovGGKiKsONOlrxi1Z4yMuzGuDqLbOwVjz37EIjj1inUZw; lang="v=2&lang=en-us"; JSESSIONID="ajax:5606231106206409384"; lidc="b=TGST01:g=1276:u=1:i=1543045671:t=1543132071:s=AQF2isHXU93iYpPIVlxgzTriC2cxkS7z"; __utma=226841088.1412527673.1539716986.1542960600.1543045691.3; __utmz=226841088.1543045691.3.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); fid=AQHCB3CjiaFpswAAAWdEsQ5HC2WXcZXXMsEy9JK4NX0sGMEPWjx4ARD9MUHsssf1cugFJUEYJvHUTw; fcookie=AQHKPvQFw8o1NQAAAWdEsXOIT0auigEtJcwVzd3KnR1BeHPTrgJrgKC0snCh7YHejVYJB0UJ29Sl5bB1eG28-2o3Yl5JVIeoZM6LjNBeHv9BPsEQDuatCxzMK0k5kImxdsv90dRa7BAld1CBjef9u0iGNVPbdIbOGGmMvPuCLY4xWnBp27ycf03A9c_cly300XOLcC4JnASPiXycy7pQC+g2Itx44975sKXzqom6+CwsbWpaQfJNEyiywZ1Rqton+P0tk3Te/0mk07pODiLLlUj+RslHG95CFDRV5py61w==; __utmb=226841088.4.10.1543045691',
    'dnt': dnt_status[0],
    'upgrade-insecure-requests': '1',
    'user-agent': user_agents[2],
    }

geocoders.options.default_user_agent = 'HamedRazavi2/'
gn = geocoders.Nominatim() 
gy = geocoders.Yandex(lang = 'en')


fl = open('../data/occupations.csv', 'r')
occupations_raw = fl.read()
occupations = occupations_raw.split('\n')
occupations.remove('')
occupations = [word.lower() for word in occupations]

res = requests.get('https://proxyscrape.com/proxies/HTTP_Elite_Proxies.txt')
proxies_list = (res.text).splitlines()
n = len(proxies_list)

# i = random.randint(0, n - 1)
# proxies = {'https': proxies_list[-1]}

class LinkedinPeopleFinder:
    
    def __init__(self):
        pass
    
    def get_url(self, person):
        base_url = "https://www.linkedin.com/pub/dir/"
        url = base_url + person.first_name + '/' + person.last_name
        response = requests.get(url, headers = request_headers) # proxies = proxies helps to avoid robot detection
        return response.text
        
    def read_from_file(self, path):
        """
        'path' is the path to the downloaded .html file. 
        """
        fl = open(path, 'r')
        text = fl.read()
        fl.close()
        return text
    
    def get_profile_indices(self, text):
        """
        'text' is the raw html text of the linedin public directory
        Returns a list of indices pointing to start of each Linkedin user profile
        """
        re_iter = re.finditer('Public Profile</a>', text)
        pp_index = [m.start() for m in re_iter]
        pp_index.append(len(text))
        return pp_index
    
    def __find_between(self, text, first, last):
        """
        'text', 'first', and 'last' are strings
        Returns the substring between the first and last strings.
        """
        try:
            start = text.index(first) + len(first)
            end = text.index(last, start)
            return text[start:end]
        except ValueError:
            return ""
     
    def extract_profile_info(self, single_listing):
        ch = '"'
        link= self.__find_between(single_listing, ch, ch)
        name_iter = re.finditer(link, single_listing)
        name_index = [m.end() for m in name_iter]

        ch1 = '>'
        ch2 = '</a>'
        listed_name = self.__find_between(single_listing[name_index[1]:], ch1, ch2)

        ch1 = '<p class="headline">'
        ch2 = '</p>'
        headline= self.__find_between(single_listing, ch1, ch2)

        ch1 = '<dt>Location</dt><dd>'
        ch2 = '</dd>'
        location= self.__find_between(single_listing, ch1, ch2)

        ch1 = '<dt>Industry</dt><dd>'
        ch2 = '</dd>'
        industry= self.__find_between(single_listing, ch1, ch2)

        ch1 = '<th>Current</th><td>'
        ch2 = '</td>'
        current = self.__find_between(single_listing, ch1, ch2)

        ch1 = '<th>Education</th><td>'
        ch2 = '</td>'
        education = self.__find_between(single_listing, ch1, ch2)

        ch1 = '<th>Past</th><td>'
        ch2 = '</td>'
        past = self.__find_between(single_listing, ch1, ch2)

        ch1 = '<th>Summary</th><td>'
        ch2 = '</td>'
        summary = self.__find_between(single_listing, ch1, ch2)
        
        user_map = { 
                  'listed_name' : listed_name, 
                  'headline' : headline, 
                  'location' : location, 
                  'industry' : industry,
                  'current' : current,
                  'past' : past,
                  'education': education,
                  'summary': summary,
                  'link': link
                 }
        return user_map
        
    def get_country_code_old(self, location):
        loc = None
        try:
            loc = gn.geocode(language='en', exactly_one=True, query=location, addressdetails=True, timeout=2)
        except GeocoderTimedOut:
            loc = gn.geocode(language='en', exactly_one=True, query=location, addressdetails=True)
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
        
    def user_map_to_person(self, user_map):
        person = Person()
        name_split = HumanName(user_map['listed_name'])
        person.first_name = name_split.first
        person.middle_name = name_split.middle
        person.last_name = name_split.last
        person.domicile = self.get_country_code(user_map['location'])
        if (user_map['current'].strip() == '') & (user_map['past'].strip() == ''):
            person.occupation = user_map['industry']
        else:
            person.occupation = 'current: ' + user_map['current'] + '; past: ' + user_map['past']
        if user_map['summary'].strip() == '':
            person.description = user_map['education'] + '; ' + user_map['headline']
        else:
            person.description = user_map['education'] + '; ' + user_map['summary']
        person.set_raw()
        return person
    
    def find_users(self, person, path='', offline=1):
        """
        Allows both online and offline Linkedin scarping. 
        If 'offline = 1', then the 'path' to the downloaded
        html file must be given. 
        'person' is an instant of the Person class
        Returns the raw Linkedin users matching 'person' as a list of maps
        """
        if offline:
            try:
                text = self.read_from_file(path)
            except: 
                return ''
        else:
            try:
                text = self.get_url(person)
            except:
                return ''
        users_map = defaultdict(list)
        try:
            pp_index = self.get_profile_indices(text)
            for i in range(len(pp_index) - 1):
                single_listing = text[pp_index[i]:pp_index[i+1]]
                single_map = self.extract_profile_info(single_listing)
                for key in single_map.keys():
                    users_map[key].append(single_map[key])
            return users_map
        except:
            return ''
    
    def find_users_as_df(self, person, path='', offline=1):
        """
        Allows both online and offline Linkedin scarping. 
        If 'offline = 1', then the 'path' to the downloaded
        html file must be given. 
        'person' is an instant of the Person class
        Returns the raw Linkedin users matching 'person' as a Pandas dataframe
        """
        try:
            users_map = self.find_users(person, path, offline)
            return pd.DataFrame(users_map)
        except:
            return ''
    
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

    def find(self, person, path='', offline=1, strict_match=0):
        """
        Allows both online and offline Linkedin scarping. 
        If 'offline = 1', then the 'path' to the downloaded
        html file must be given. 
        'person' is an instant of the Person class
        If strict_match=1 then the first name and last name of the found users
        must match with the given person. 
        Returns the raw users data matching 'person' as a list of Person class
        """
        try:
            users_map = self.find_users(person, path, offline)
        except Exception as e:
            print(e)
            return ''
        n = len(users_map['listed_name'])
        keys = users_map.keys()
        persons = []
        try:
            for i in range(n):
                user_map = {key:users_map[key][i] for key in keys}
                if self.is_listedname_similar(person, user_map['listed_name']):
                    p = self.user_map_to_person(user_map)
                    if self.__is_match(person, p, strict_match):
                        persons.append(p)
            return persons
        except:
            return ''
    
    def find_as_df(self, person, path='', offline=1, strict_match=0):
        """
        Allows both online and offline Linkedin scarping. 
        If 'offline = 1', then the 'path' to the downloaded
        html file must be given. 
        'person' is an instant of the Person class
        If strict_match=1 then the first name and last name of the found users
        must match with the given person. 
        Returns the users matching 'person' a Pandas dataframe
        """
        try:
            persons = self.find(person, path, offline, strict_match)
        except:
            return ''
        keys = person.keys()
        persons_map = {key:[] for key in keys}
        for p in persons:
            for key in keys:
                persons_map[key].append(p.raw[key])
        return pd.DataFrame(persons_map)