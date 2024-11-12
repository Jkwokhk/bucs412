# voter_analytics/models.py
from django.db import models
import csv
from datetime import datetime
from django.conf import settings
from django.db import models

# Create your models here.
class Voter(models.Model):
    '''encapsualtes an idea of a Voter'''
    voter_id = models.CharField(max_length= 12)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10, blank=True, null=True)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=1)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

def load_data():
    '''function to load data records from csv file into django model instances'''
    Voter.objects.all().delete()
    filename = '/Users/jasonk/Desktop/newton_voters.csv'
    f = open(filename)
    f.readline() #discard headers
    for row in f:
        # line = f.readline().strip()
        fields = row.split(',')
        # show which value in each field
        try:
        # create instance of Result object with this record
            voter = Voter(
                voter_id = fields[0],
                last_name = fields[1],
                first_name = fields[2],
                street_number = fields[3],
                street_name = fields[4],
                apartment_number = fields[5] if fields[5].strip() else None,
                zip_code = fields[6],
                date_of_birth = fields[7],
                date_of_registration = fields[8],
                party_affiliation = fields[9],
                precinct_number = fields[10],
                v20state = fields[11].strip().lower() == 'true',
                v21town = fields[12].strip().lower() == 'true',
                v21primary = fields[13].strip().lower() == 'true',
                v22general = fields[14].strip().lower() == 'true',
                v23town = fields[15].strip().lower() == 'true',
                voter_score = fields[16],
            )
            voter.save() 
            # commit to database
            print(f' Created result: {voter}')
        except:
            print(f"Skipped {fields}")
    print(f'Done. Created all Voters')
    