# People Search Engine

This project includes the Python classes for finding people online given their first and last names. There are overall 3 different people finder classes: `WikiPeopleFinder, TwitterPeopleFinder` and `LinkedinPeopleFinder`.  Moreover, the class `GoogleNetWorthFinder` finds the net worth of a person given the first and last names, if such information exist in the google main search results. Also, a `Person` class is defined to handle the input and output of the people finders easier. The attributes of the `Person` class include `first_name, middle_name, last_name, nationality (ISO 3166 alpha 2), domicile (ISO 3166 alpha 2), dob (date of birth), is_famous (True or False), net_worth (in USD), description (summary) `. 

**Note:** To use the `TwitterPeopleFinder` you need to provide your `CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET`. If you don't have these credentials head to [here](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html). If you don't have an already existing app, it may take a day or more to get your tokens.

The people finder classes here have mostly similar interfaces. Below you can find a quick example on how to use the`WikiPeopleFinder` class. Also, the notebook `main.ipynb` includes more examples and instructions on how to use the people finder classes. 

## Installation 

Please follow the instructions in [packages_list.md](./packages_list.md), to install the required classes.

## Quick Start

`WikiPeopleFinder` example:

```python
# Import
from Person import Person
from WikiPeopleFinder import WikiPeopleFinder

# Instantiate the Person class
person = Person("Jim", "Carrey")

# Instantiate the WikiPeopleFinderClass
wikifinder = WikiPeopleFinder()

# Find the person in wikipedia (and wikidata)
wikifinder.find(person) # This will update the attributes of the person class

# Show the output
print(person.raw)

# Find the person and display the result as a Pandas dataframe
wikifinder.find_as_df(person)
```

`TwitterPeopleFinder` example:

```python
# Import
from Person import Person
from TwitterPeopleFinder import TwitterPeopleFinder

# Copy-paste your Twitter api keys and tokens 
CONSUMER_KEY = tokens['CONSUMER_KEY']
CONSUMER_SECRET = tokens['CONSUMER_SECRET']
OAUTH_TOKEN = tokens['OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = tokens['OAUTH_TOKEN_SECRET']

twitterfinder = TwitterPeopleFinder(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# Instantiate the Person class (note the location condition)
person = Person(first_name="Jim", last_name="Carrey", domicile='US')

# Find the person in Twitter users and display the result as a Pandas dataframe
twitterfinder.find_as_df(person)
```

