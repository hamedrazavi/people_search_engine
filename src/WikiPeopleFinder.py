import requests
from datetime import datetime
import pandas as pd
import wikipedia
import wikidata
from wikidata.client import Client

class WikiPeopleFinder:
    
    def __init__(self):
        self.wikipedia = wikipedia
        self.client = Client()
        
    def find_page(self, person):
        try:
            page = self.wikipedia.page(person.first_name + " " + person.last_name, auto_suggest=False, preload=True)
            return page
        except self.wikipedia.DisambiguationError as e:
            print("Diasmbiguation error: To show Wikipedia results select one of the followings")
            print(list(set(e.options)))
            return
        except self.wikipedia.PageError:
            print("Wikipedia does not have a page with the name \"{} {}\".".format(person.first_name, person.last_name)) # should skip to the end of code
            return
    
    def get_entity_id(self, title):
        try:
            base_api = "https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&format=json&titles="
            name_api = base_api + title
            name_json = requests.get(name_api).json()['query']['pages']
            for k, v in name_json.items():
                val = v
            entity_id = val['pageprops']['wikibase_item']
            return entity_id
        except:
            return ''
    
    def get_entity(self, entity_id):
        try:
            entity = self.client.get(entity_id, load=True)
        except:
            print("Entity id of the page not found. Please check the exact name of the page.")
            entity = ''
        return entity
    
    def to_datetime(self, wiki_date):
        try:
            date = datetime.strptime(wiki_date, '+%Y-%m-%dT%H:%M:%SZ')
            return date
        except:
            return ''
    
    def get_value(self, entity, Pid, index):
        """
        Pid is the wikidata property id
        """
        value = entity.data['claims'][Pid][index]['mainsnak']['datavalue']['value']
        return value
    
    def get_birthday(self, entity):
        """
        Returns birthday in day-month-year format, e.g. 14-12-1955
        """
        try:
            Pid = 'P569'
            birthday = self.get_value(entity, Pid, 0)['time']
            birthdate = self.to_datetime(birthday)
            return datetime.strftime(birthdate, '%d-%m-%Y')
        except Exception as e:
            print(e)
            return ''
    
    def get_birth_name(self, entity):
        try:
            Pid = 'P1477'
            birth_name = self.get_value(entity, Pid, 0)['text']
            return birth_name
        except:
            return 
    
    def get_middle_name(self, name, person):
        try:
            first_name = person.first_name
            last_name = person.last_name
            i_f = name.find(first_name) + len(first_name)
            i_l = name.find(last_name)
            return (''.join(name[i_f + 1:i_l])).strip()
        except:
            return ''
    
    def get_networth(self, entity):
        try:
            Pid = 'P2218'
            net_worth = self.get_value(entity, Pid, 0)['amount']
            return net_worth
        except:
            return ''
    
    def get_birthplace_id(self, entity):
        try:
            Pid = 'P19'
            birthplace_Qid = self.get_value(entity, Pid, 0)['id']
            return birthplace_Qid
        except:
            return ''
    
    def get_birthcountry_id(self, entity):
        try:
            entity = self.client.get(self.get_birthplace_id(entity), load = True)
            country_Pid = 'P17'
            birthcountry_Qid = self.get_value(entity, Pid, 0)['id']
            return birthcountry_Qid
        except:
            return ''
    
    def get_country_code(self, Qid):
        try:
            entity = self.client.get(Qid, load = True)
            Pid = 'P297'
            return self.get_value(entity, Pid, 0)
        except:
            return ''
    
    def get_birthcountry(self, entity):
        try:
            Qid = self.get_birthcountry_id(entity)
            return self.get_country_code(Qid)
        except:
            return ''
    
    def get_occupation_id(self, entity):
        occupation_Qid = []
        try:
            occupation_Pid = 'P106'
            occ_list = entity.data['claims'][occupation_Pid]
            n = len(occ_list)
            for i in range(min(n, 10)):
                occupation_Qid.append(occ_list[i]['mainsnak']['datavalue']['value']['id'])
            return occupation_Qid
        except:
            return ''

    def get_occupation(self, entity):
        try:
            occ_id_list = self.get_occupation_id(entity)
            occupation = []
            for Qid in occ_id_list:
                entity = self.client.get(Qid, load=True)
                occupation.append(entity.attributes['labels']['en']['value'])
            return ', '.join(occupation)
        except:
            return ''
    
    def get_country_of_citizenship_id(self, entity):
        try:
            Pid = 'P27'
            citizenship_Qid = self.get_value(entity, Pid, 0)['id']
            return citizenship_Qid
        except:
            return ''

    def get_country_of_citizenship(self, entity):
        try:
            Qid = self.get_country_of_citizenship_id(entity)
            return self.get_country_code(Qid)
        except:
            return ''
    
    def get_residence_id(self, entity):
        try:
            Pid = 'P551'
            residence_Qid = self.get_value(entity, Pid, 0)['id']
            return residence_Qid
        except:
            return ''

    def get_residencecountry_id(self, entity):
        try:
            entity = self.client.get(self.get_residence_id(entity), load = True)
            Pid = 'P17'
            residencecountry_Qid = self.get_value(entity, Pid, 0)['id']
            return residencecountry_Qid
        except:
            return ''
    
    def get_domicile(self, entity):
        try:
            Qid = self.get_residencecountry_id(entity)
            return self.get_country_code(Qid)
        except:
            return ''
    
    def find(self, person):
        """
        'person' is an istant of Person() class. Updates the 'person' attributes. 
        """
        page = self.find_page(person)
        try:
            entity_id = self.get_entity_id(page.title)
            entity = self.get_entity(entity_id)
            person.dob = self.get_birthday(entity)
            person.occupation = self.get_occupation(entity)
            person.nationality = self.get_country_of_citizenship(entity)
            res_domicile = self.get_domicile(entity)
            if res_domicile:
                person.domicile = res_domicile
            elif person.nationality == self.get_birthcountry(entity):
                person.domicile = person.nationality # this is an assumption!
            birth_name = self.get_birth_name(entity)
            person.middle_name = self.get_middle_name(birth_name, person)
            if page:
                person.is_famous = 'True'
            else:
                person.is_famous = ''
            person.net_worth = self.get_networth(entity)
            person.description = page.summary
            person.set_raw()
        except:
            pass
        
    def find_as_df(self, person):
        """
        person: an istant of Person() class.
        Returns a Pandas data frame.
        """
        try:
            self.find(person)
            return person.to_df(pd)
        except:
            pass