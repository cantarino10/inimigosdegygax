from django.db import models
from django import forms

class BBA(models.Model):
  level = models.IntegerField()
  Poor = models.IntegerField()
  Medium = models.IntegerField()
  Good = models.IntegerField()

  def __str__(self):
    return 'BBA'

class Wealth(models.Model):
  type = models.CharField(max_length=5)
  Wealth = models.CharField(max_length=500)

  def __str__(self) :
    return self.type
# Create your models here.

class Carrying(models.Model):
  str = models.IntegerField()
  light = models.CharField(max_length=15)
  medium = models.CharField(max_length=15)
  heavy = models.CharField(max_length=15)

  def __str__(self):
    return 'Carrying'

class Languages(models.Model):
  language = models.CharField(max_length=30)
  speakers = models.CharField(max_length=100)
  Alphabet = models.CharField(max_length=20)

  def __str__(self):
    return self.language