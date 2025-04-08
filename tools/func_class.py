from main.models import Classe,Race,Weapons,Armor,Shield,Skills,Magic_Enhancement,Items
from tools.models import BBA
from random import choice,randint


class SetWeapons:
  def __init__(self,weapon):
    self.name = weapon.weapon
    self.critical = weapon.critical
    self.reach = weapon.reach
    self.weight = weapon.weight
    self.type = weapon.type
    self.category = weapon.category
    self.damage_medium = weapon.damage_medium
    self.damage_small = weapon.damage_small
    self.designation = weapon.designation
    self.magic = 0
    self.enhancement =0
    self.property = 0
    self.fixed_property =''
    self.properties = []
    self.bonus = 0
    self.bba = 0 
   
  def adjust(self):
    if self.magic =='MW':
      self.bonus +=1
    else :  
     self.bonus += self.enhancement 


  def set_magic(self,magic)  :
    self.magic = magic
    to_enhance = magic - 1
    property = 0
    bonus = 1
 
    for i in range(to_enhance):
      chance = choice([1,2])
      if chance == 1 or bonus == 5:
          property +=1
      else:
        bonus +=1

    self.enhancement = bonus
    self.property = property

    while property > 0 :
        rand = randint(1,property)
        property -= rand
        self.properties.append(f'{choice(Magic_Enhancement.objects.filter(price__contains = f'+{rand}',slot = 'Weapon')).name} (+{rand  })')
    self.magic = f'{magic} (+{self.enhancement}/+{self.property})'    
    
    
    
    
  
  def set_bba(self,level,classe,strg,dex,size):
      
   if classe == 'Poor':
      bba =BBA.objects.get(level = level).Poor
   elif classe == 'Medium':
      bba = BBA.objects.get(level = level).Medium
   else:
       bba = BBA.objects.get(level = level).Good

   base = []

   if size == 'Small':
     bba +=1
   for i in range(5):
     base.append(bba - ((i) * 5))
     if bba / ((i+1)*5) < 1:
         break     
     
   bba = [i+self.bonus for i in base]    

   if self.category == 'Ranged':
      bba = [f'+{i+self.bonus+dex}' for i in base]  
   else:
     bba = [f'+{i+self.bonus+strg}' for i in base]  

   self.bba =  '/'.join(bba)

class SetArmor:
  def __init__(self,armor):
    self.name = armor.armor
    self.ca = armor.ca
    self.maxdex = armor.maxdex
    self.penalty = armor.penalty
    self.penalty_speed = armor.penalty_speed
    self.category = armor.category
    self.magic = 0
    self.enhancement =0
    self.property = 0
    self.properties = []
    self.weight = int(armor.weight)  

    
  def adjust(self):
    if self.magic !='MW':
           
     self.ca += self.enhancement 

  def set_magic(self,magic:int)  :
    if self.penalty > 0:
        self.penalty -=1
    self.magic = magic
    if magic == 'MW':
      self.magic = 'MW'
      return
    
    to_enhance = magic - 1
    property = 0
    bonus = 1
 
    for i in range(to_enhance):
      chance = choice([1,2])
      if chance == 1 or bonus == 5:
          property +=1
      else:
        bonus +=1

    self.enhancement = bonus
    self.property = property

    while property > 0 :
        rand = randint(1,property)
        property -= rand
        self.properties.append(f'{choice(Magic_Enhancement.objects.filter(price__contains = f'+{rand}',slot__contains = 'Armor')).name} (+{rand  })')
    self.magic = f'{magic} (+{self.enhancement}/+{self.property})' 
           
  
       


class SetShield:
  def __init__(self,shield):
    self.name = shield.shield
    self.ca = shield.ca
    self.maxdex = shield.maxdex
    self.penalty = shield.penalty
    self.magic = 0
    self.enhancement =0
    self.property = 0
    self.properties = []
    self.weight = int(shield.weight)

 
  def adjust(self):
    if self.magic !='MW':       
     self.ca += self.enhancement 

  def set_magic(self,magic:int)  :
    if self.penalty > 0:
        self.penalty -=1
    self.magic = magic
 
    if magic == 'MW':
      self.magic = 'MW'
      return
    
    to_enhance = magic - 1
    property = 0
    bonus = 1
 
    for i in range(to_enhance):
      chance = choice([1,2])
      if chance == 1 or bonus == 5:
          property +=1
      else:
        bonus +=1
    self.enhancement = bonus
    self.property = property

    while property > 0 :
        rand = randint(1,2)
        property -= rand
        self.properties.append(f'{choice(Magic_Enhancement.objects.filter(price__contains = f'+{rand}',slot__contains = 'Shield')).name} (+{rand  })')
    self.magic = f'{magic} (+{self.enhancement}/+{self.property})' 
           



  