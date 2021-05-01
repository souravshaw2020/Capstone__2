from django.db import models
class Capstone(models.Model):
    mname = models.CharField(max_length=100)
    mgenre = models.CharField(max_length=200)
    mreview = models.TextField()
    
class Calculate(models.Model):
    mname = models.CharField(max_length=100)
    mgenre = models.CharField(max_length=200)
    mreview = models.TextField()
    mscore = models.IntegerField()

class AvgScore(models.Model):
    mname = models.CharField(max_length=100)
    mgenre = models.CharField(max_length=200)
    mscore = models.FloatField()

# Create your models here.
