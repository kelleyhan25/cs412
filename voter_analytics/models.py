# voter_analytics/models.py 
# Kelley Han kelhan@bu.edu
# this includes the model definition of a Voter and all its attributes, and the function to load data from the CSV file
from django.db import models

# Create your models here.
class Voter(models.Model):
    '''stores/represents the data from one voter '''

    last_name = models.TextField()
    first_name = models.TextField()
    street_num = models.IntegerField()
    street_name = models.TextField()
    apt_num = models.TextField()
    zip_code = models.TextField()
    dob = models.TextField()
    dor = models.TextField()
    party = models.CharField(max_length=1)
    precinct_num = models.TextField()
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}'
    

def load_data(): 
    '''function to load data records from the newton_voters csv file into Django model instances.'''
    Voter.objects.all().delete()
    
    filename = '/Users/khan/Desktop/django/newton_voters.csv'
    f = open(filename)
    f.readline()

   
    
    for line in f: 
    
        fields = line.split(',')
       
        def convert_to_boolean(value):
            '''converts the "TRUE" and "FALSE" values to a Boolean.'''
            return value == "TRUE"
        


        try: 
            
            # create a new instance of Voter object with this record from CSV 
            voter = Voter(last_name=fields[1],
                        first_name=fields[2],
                        street_num=fields[3],
                        street_name=fields[4],
                        apt_num=fields[5],
                        zip_code=fields[6],
                        dob=fields[7],
                        dor=fields[8],
                        party=fields[9],
                        precinct_num=fields[10],
                        v20state=convert_to_boolean(fields[11]),
                        v21town=convert_to_boolean(fields[12]),
                        v21primary=convert_to_boolean(fields[13]),
                        v22general=convert_to_boolean(fields[14]),
                        v23town=convert_to_boolean(fields[15]),
                        voter_score=fields[16])
            voter.save() 
        except: 
            print(f"Skipped: {voter}")
       
    print(f'Done. Created {len(Voter.objects.all())} Voters.')

