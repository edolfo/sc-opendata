from django.db import models

# Create your models here.
import datetime

class Crime(models.Model):
    ObjectID = models.IntegerField(default = 0)
    CaseNum = models.CharField(max_length=200)
    #ID = models.CharField(max_length=200)
    CM_ID = models.CharField(max_length=200)
    CM_AGENCY = models.CharField(max_length=200)
    DateOccurred1 = models.DateTimeField('date occurred')
    TimeOccurred1 = models.DateTimeField('time occurred')
    UcrCrime = models.CharField(max_length=200)
    UcrCrimeHierarchy = models.CharField(max_length=200)
    Description = models.CharField(max_length=500)
    UCR1 = models.CharField(max_length=200)
    CM_LEGEND = models.CharField(max_length=200)
    StrNumber = models.CharField(max_length=200)
    Street = models.CharField(max_length=200)
    Zip = models.CharField(max_length=200)
    Intersection = models.CharField(max_length=200)
    CVADDRESS = models.CharField(max_length=200)
    BLOCK_ADDRESS = models.CharField(max_length=200)
    CVDATE = models.CharField(max_length=200)
    CVDOW = models.CharField(max_length=200)
    CVTIME = models.CharField(max_length=200)
    iwGeoName = models.CharField(max_length=200)
    iwStep = models.CharField(max_length=200)
    Status = models.CharField(max_length=200)
    Score = models.CharField(max_length=200)
    X = models.CharField(max_length=200)
    Y = models.CharField(max_length=200)
    Stan_Addr = models.CharField(max_length=200)
    pointProperty = models.CharField(max_length=200)
    DomViolMeth = models.CharField(max_length=200)
    Side = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.Description

    """
    ================================
    === Custom queries
    ================================
    """
    def recent(self, days):
        return self.DateOccurred1 >= datetime.datetime.now() - datetime.timedelta(days=days)
        
    def crimeType(self, title):
        return self.objects.filter(CM_LEGEND__startswith=title)