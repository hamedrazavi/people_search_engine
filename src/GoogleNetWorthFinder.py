import requests
from lxml.html import fromstring
import re

request_headers = {
    'Host': 'www.google.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/',
    'Cookie': 'CGIC=CgZ1YnVudHUaAmZzIj90ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSwqLyo7cT0wLjg; NID=148=Y86IbdMjcEVSEB54j6xuSJ4egvUsAu-dQtO8mSJAyhUD-lleDNAUBd_24MxLjQAJimHRv_2BllrY1__8CZqzLDT6-Il_y-6puSviY-65Oz39ZDl80J-lNTrskF2_k8w_Swp79m7bdViop52F48LTHjWF6JIorkgbYYUIWuBtbyDM5OeF22jOjs18wJa1IfYckJbv7w; 1P_JAR=2018-11-25-12; OGP=-5061451:; CONSENT=YES+CH.en-GB+V9; _ga=GA1.1.1453439703.1530718155; OGPC=873035776-22:; S=billing-ui-v3=d7JEzTMIFLIgi3aoOiJ8OxLap2VVnhHR:billing-ui-v3-efe=d7JEzTMIFLIgi3aoOiJ8OxLap2VVnhHR; _gcl_au=1.1.190702646.1539697537; DV=A2OnfgRjC38SgJ14QZ6ztebOFTOudBY',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

class GoogleNetWorthFinder:
    """
    Use extract_net_worth(person) method to get the best estimate of google of the net worth
    of the person. 'person' is a instant of the Person class. 
    """
    def __init__(self):
        pass
    
    def __find_decimal(self, s):
        return ''.join(re.findall('\d+\.?\d+', s))

    def __get_parser(self, person):
        url_worth = "https://www.google.com/search?&q=What+is+{}+{}+net+worth".format(person.first_name, person.last_name)
        response = requests.get(url_worth, headers = request_headers)
        parser = fromstring(response.content)
        el = parser.xpath('//div[@class="HwtpBd kno-fb-ctx"]//div[@class="Z0LcW"]/text()')
        if not el:
            el = parser.xpath('//div[@class="LGOjhe"]//span//b/text()')
        if not el:
            el = parser.xpath('//b/text()')
        return el
            
    def extract_net_worth(self, person):
        el = self.__get_parser(person)
        try:
            value = self.__find_decimal(el[0])
            unit = 'USD'
            if (re.findall('billion', el[0], re.IGNORECASE) != []):
                unit = 'billion USD'
            elif (re.findall('million', el[0], re.IGNORECASE) != []):
                unit = 'million USD'
            person.net_worth = value + ' ' + unit
            person.set_raw()
        except:
            pass