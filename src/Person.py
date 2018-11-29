class Person:
    def __init__(self, first_name='', last_name='', domicile = '', nationality = ''):
        self.first_name = first_name.capitalize()
        self.last_name = last_name.capitalize()
        self.middle_name = ''
        self.nationality = nationality
        self.domicile = domicile
        self.dob = '' # Date of birth
        self.occupation = ''
        self.net_worth = ''
        self.is_famous = ''
        self.description = ''
        self.raw = {
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'nationality': self.nationality,
            'domicile': self.domicile,
            'date_of_birth': self.dob,
            'occupation': self.occupation,
            'net_worth': self.net_worth, # in USD
            'is_famous': self.is_famous,
            'description': self.description
        }
        
    def name(self):
        if self.middle_name:
            return self.first_name + ' ' + self.middle_name + ' '+ self.last_name
        else:
            return self.first_name + ' ' + self.last_name
    
    def set_raw(self):
        self.raw = {
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'nationality': self.nationality,
            'domicile': self.domicile,
            'date_of_birth': self.dob,
            'occupation': self.occupation,
            'net_worth': self.net_worth,
            'is_famous': self.is_famous,
            'description': self.description
        }
        
    def keys(self):
        return self.raw.keys()
    
    def to_df(self, pandas):
        """
        pandas package as input.
        Returns the Person.raw as a Pandas dataframe
        """
        self.set_raw()
        dfmap = {key:[self.raw[key]] for key in self.keys()}
        return pandas.DataFrame(dfmap)