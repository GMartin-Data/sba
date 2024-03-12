from django.db import models

from .enums import *

    
class LoanApplication(models.Model):
    State = models.CharField(max_length=2, choices=USState.choices(), null=False, blank=False)
    Bank = models.CharField(max_length=50, null=False, blank=False)
    BankState = models.CharField(max_length=2, choices=USState.choices(), null=False, blank=False)
    NAICS = models.CharField(max_length=100, choices=Naics.choices(), null=False, blank=False)
    Term = models.IntegerField(null=False, blank=False)
    NewExist = models.CharField(max_length=1, choices=YesNo.choices(), null=False, blank=False)
    NoEmp = models.IntegerField(null=False, blank=False)
    CreateJob = models.IntegerField(null=False, blank=False)
    RetainedJob = models.IntegerField(null=False, blank=False)
    Franchise = models.CharField(max_length=1, choices=YesNo.choices(), null=False, blank=False)
    UrbanRural = models.CharField(max_length=1, choices=UrbanRural.choices(), null=False, blank=False)
    RevLineCr = models.CharField(max_length=7, choices=YesNo.choices(), null=False, blank=False)
    GrAppv = models.FloatField(null=False, blank=False)
    SBA_Appv = models.FloatField(null=False, blank=False)
    # Prediction Fields
    Verdict = models.CharField(max_length=8)
    Percentage = models.FloatField()
