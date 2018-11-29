#!/anaconda3/envs/envPy36/bin/python
# this is a test script (a main.py) which is executable. To run this code in the command line
# type ./test.py 
# Make sure that you have the proper tokens in the tokens folder

from Person import Person
from TwitterPeopleFinder import TwitterPeopleFinder

def main():

  # It is assumed that your authorization keys are stored in 'twitter_tokens.csv' with space between the keys and their values
  fl = open('../../tokens/twitter_tokens.csv', 'r')
  lines = fl.readlines()
  tokens = {line.split()[0]:line.split()[1] for line in lines}

  # You could also simply copy paste your keys directly here
  CONSUMER_KEY = tokens['CONSUMER_KEY']
  CONSUMER_SECRET = tokens['CONSUMER_SECRET']
  OAUTH_TOKEN = tokens['OAUTH_TOKEN']
  OAUTH_TOKEN_SECRET = tokens['OAUTH_TOKEN_SECRET']
  person = Person("Jim", "Carrey")

  twitterfinder = TwitterPeopleFinder(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
  df = twitterfinder.find_as_df(person)
  print(df)

if __name__ == '__main__':
  main()