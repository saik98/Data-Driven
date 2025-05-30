from django.db import models

# Create your models here.
class RegisterModel(models.Model):
    firstname=models.CharField(max_length=300)
    lastname=models.CharField(max_length=200)
    userid=models.CharField(max_length=200)
    password=models.IntegerField()
    mblenum=models.BigIntegerField()
    email=models.EmailField(max_length=400)
    gender=models.CharField(max_length=200)

class BlockModel(models.Model):
    usid=models.ForeignKey(RegisterModel)
    block=models.CharField(max_length=200)
    flow=models.CharField(max_length=200)

class add_detailsModel(models.Model):
    usids=models.ForeignKey(RegisterModel)
    bls=models.CharField(max_length=200)
    fls=models.CharField(max_length=200)
    minimum_capacity=models.IntegerField()
    maximum_capacity=models.IntegerField()
    status=models.CharField(max_length=200,default="OFF")

class AnalysisModel(models.Model):
    blk=models.CharField(max_length=100)
    sts=models.CharField(max_length=100)