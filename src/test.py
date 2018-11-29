#!/anaconda3/envs/envPy36/bin/python

# this is a test script (a main.py) which is executable. To run this code in the command line
# as executable first make this script execubtable by the command 'chmod +x test.py', then
# type ./test.py 
# Make sure that you have the proper tokens in the tokens folder

from Person import Person
from TwitterPeopleFinder import TwitterPeopleFinder
from LinkedinPeopleFinder import LinkedinPeopleFinder

def main():

  # It is assumed that your authorization keys are stored in 'twitter_tokens.csv' with space between the keys and their values
  # Make sure the path to your twitter_tokens.csv is correct. 
  fl = open('../../tokens/twitter_tokens.csv', 'r')
  lines = fl.readlines()
  tokens = {line.split()[0]:line.split()[1] for line in lines}

  # You could also simply copy paste your keys directly here
  CONSUMER_KEY = tokens['CONSUMER_KEY']
  CONSUMER_SECRET = tokens['CONSUMER_SECRET']
  OAUTH_TOKEN = tokens['OAUTH_TOKEN']
  OAUTH_TOKEN_SECRET = tokens['OAUTH_TOKEN_SECRET']
  person = Person(first_name="John", last_name="Smith", domicile='US')

  twitterfinder = TwitterPeopleFinder(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
  df = twitterfinder.find_as_df(person, strict_match=1)
  print(df)

  linkedfinder = LinkedinPeopleFinder()
  df = linkedfinder.find_as_df(person, path='../data/sample_linkedin_html/66800_John_Smith_profiles _ LinkedIn.html', strict_match=1)
  print(df)

if __name__ == '__main__':
  main()