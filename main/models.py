from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class Handbooks(models.Model):
 
  text = models.CharField(max_length=50)
  link = models.URLField(max_length=200, null=True)
  edition = models.CharField(max_length=3, null=True)
  date = models.DateTimeField(auto_now_add=True)
  category = models.CharField(max_length=100, null=True)
  region = models.CharField(max_length=50,null=True)

  def __str__(self) -> str:
    return self.text

class Classes(models.Model):
  text = models.CharField(max_length=50)
  link = models.URLField(max_length=200, null=True)
  date = models.DateTimeField(auto_now_add=True)
  category = models.CharField(max_length=10, null=True)
  handbook = models.CharField(max_length=30, null=True)
  
  def __str__(self) -> str:
    return self.text
  
class Races(models.Model)  :
  text = models.CharField(max_length=30)
  link = models.URLField(max_length=200, null=True)
  date = models.DateField(auto_now_add=True)
  handbook = models.CharField(max_length=30, null=True)

  def __str__(self) -> str:
    return self.text

class Items(models.Model) :
  text = models.CharField(max_length=50)
  link = models.URLField(max_length=200, null=True)
  date = models.DateField(auto_now_add=True)
  price=models.FloatField(null=True)
  handbook = models.CharField(max_length=20,null=True)
  family = models.CharField(max_length=30,null=True)
  slot = models.CharField(max_length=20)

  def __str__(self):
    return self.text
  
class Feats(models.Model)  :
  
  name = models.CharField(max_length=50)
  version = models.CharField(max_length=5)
  shortdescript = models.CharField(max_length=300,null=True)
  page = models.CharField(max_length=5, null=True)
  type = models.CharField(max_length=50)
  handbook = models.CharField(max_length=50)
  requisite = models.TextField(max_length=5000, blank=True)
  required = models.TextField(max_length=1000,blank=True)
  description = models.TextField()
  special = models.TextField(blank=True)


  def __str__(self) -> str:
    return self.name
  


class Spells(models.Model):

    name = models.CharField(max_length=50)
    Edition = models.CharField(max_length=5)
    handbook = models.CharField(max_length=50)
    school = models.CharField(max_length=50)
    components = models.CharField(max_length=500,null=True)
    level = models.CharField(max_length=200)
    casting_time =models.CharField(max_length=100)
    range = models.CharField(max_length=50)
    duration = models.CharField(max_length=20,null=True)
    category =  models.CharField(max_length=100)
    save_throw =  models.CharField(max_length=10)
    descript = models.TextField()
    spellresistance = models.CharField(max_length=10, default='Yes')
    area = models.CharField(max_length=50)
  
    
    def __str__(self) -> str:
     return self.name    

class favorites_spells(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  spell_id = models.CharField(max_length=5000)

class favorites_feats(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  feat_id = models.CharField(max_length=5000)

class Classe(models.Model):
  Class = models.CharField(max_length=50)
  link = models.URLField(max_length=200, null=True)
  BBA = models.CharField(max_length=10)
  HitDice = models.IntegerField()
  gold = models.CharField(max_length=10)
  Saves = models.CharField(max_length=20)
  Abilities = models.CharField(max_length=5000)
  Skills = models.IntegerField()
  classSkills = models.CharField(max_length=1000)
  armors = models.CharField(max_length=1000)
  amors_name =  models.CharField(max_length=1000)
  weapons =  models.CharField(max_length=1000)
  weapons_name =  models.CharField(max_length=1000)
  shields =  models.CharField(max_length=1000)
  book = models.CharField(max_length=100)
  spells = models.CharField(max_length=2000)
  Abilities = models.CharField(max_length=5000)
  key1 = models.IntegerField()
  key2 = models.IntegerField()

  def __str__(self) -> str:
     return self.Class    

class Race(models.Model):
   Race = models.CharField(max_length=50)
   Adjustment = models.CharField(max_length=100) 
   SkillBonus = models.CharField(max_length=200, null=True)
   Speed = models.IntegerField(default=30)
   Size = models.CharField(max_length=10, default='Medium')
   Space = models.IntegerField(default=5)
   Reach = models.IntegerField(default=5)
   Languages = models.CharField(max_length=100)
   level_adjstument = models.IntegerField(default=0)
   description = models.TextField(max_length=5000)
   traits = models.TextField(max_length=5000) 
   weapons = models.CharField(max_length=1000, null=True)
   book = models.CharField(max_length=100)

   
   def __str__(self) -> str:
     return self.Race   
   
class Weapons(models.Model):
   weapon = models.CharField(max_length=50)
   damage_medium = models.CharField(max_length=10)
   damage_small = models.CharField(max_length=10)
   critical = models.CharField(max_length=10)
   reach = models.IntegerField()
   weight = models.FloatField()
   type = models.CharField(max_length=20)
   category = models.CharField(max_length=20)
   designation = models.CharField(max_length=10)

   def __str__(self) -> str:
     return self.weapon

class Armor(models.Model):
   armor = models.CharField(max_length=20)
   ca = models.IntegerField()
   maxdex = models.IntegerField()
   penalty = models.IntegerField()
   penalty_speed = models.BooleanField()
   category = models.CharField(choices=(('Light','Light'),('Medium', 'Medium'), ('Heavy', 'Heavy')), max_length=10)
   weight = models.FloatField()

   def __str__(self) -> str:
     return self.armor

class Shield(models.Model):
   shield = models.CharField(max_length=30)
   ca = models.IntegerField()
   maxdex = models.IntegerField()
   penalty = models.IntegerField()
   weight = models.FloatField()
   
   def __str__(self) -> str:
     return self.shield

class Skills(models.Model):
  skills = models.CharField(max_length=30)
  atribute = models.CharField(max_length=3)
  amorpenalty = models.BooleanField()
  trained = models.BooleanField()
  sinergy = models.CharField(max_length=500)
  description = models.TextField(max_length=20000)

  def __str__(self) -> str:
     return self.skills  

class Magic_Enhancement(models.Model):
  name = models.CharField(max_length=50)
  price  = models.CharField(max_length=50)
  slot = models.CharField(max_length=20)
  book = models.CharField(max_length=100)
  page = models.IntegerField(null=True)
  caster_level = models.IntegerField()
  aura = models.CharField(max_length=200, null=True)
  activation  = models.CharField(max_length=50,null=True)
  sinergy = models.CharField(max_length=50,null=True)
  description = models.CharField(max_length=1000)
  absolute_price= models.IntegerField(null=True)
  cost_create = models.CharField(max_length=50,null=True)
  requirements = models.CharField(max_length=50,null=True)


  def __str__(self) -> str:
    return self.name

