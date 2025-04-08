from random import randint
from random import choice,choices
from main.models import Classe,Race,Weapons,Armor,Shield,Skills,Magic_Enhancement,Items
from .func_class import SetWeapons,SetArmor,SetShield
from tools.models import BBA
from .models import Wealth
from django.db.models import Q
from time import time



def roll_dices(dict: dict):
  dices = dict['Dice']
  number = dict['number_dices']
  dice = []
  result = []
  sume = []

  for i in range(6):    
    if range(int(number[i]) > 0):
      t_result=[]

      for j in range(int(number[i])):     
        t_result.append(randint(1,int(dices[i][1:])))

      result.append(t_result)
      sume.append(sum(t_result))
      dice.append(str(number[i]) + str(dices[i]))      
  return result,sume,dice

def random_atributes():
    mod = []
    roll = True

    while roll == True:
      total = []  

      for j in range(6):  
        sume = []

        for i in range(4) :
             sume.append(randint(1,6))

        sume.sort()
        sume = sume[-3::]
        sumat = sum(sume)
     
        if sumat >= 14:
         roll = False

        total.append(sumat)  
    mod = modf(total)     
    return total,mod

def modf(atributes:list[int]) -> list:
   mod= []

   for i in atributes:     
       if i >= 10:
          mod.append(int((i - 10) / 2))
       else:
          mod.append(int((i-11) / 2))  

   return mod


def random_at() -> int:
   sume = [randint(1,6) for i in range(4)]
   sume.sort()   
   return sum(sume[-3::])




def set_class(class_name:str,atrb:list):

   if class_name == '':
      classe = rand_class(atrb)   
   else:
      classe = Classe.objects.get(Class = class_name) 

   abilities = classe.Abilities.split('|')   
   return classe,abilities

def rand_class(atrb:list):
   atributes = list(atrb).copy()
   keys1 = atributes.index(max(atributes))  
   atributes[keys1] = 0
   keys2 = atributes.index(max(atributes))
   atributes[keys2] = 0
   sort = randint(0,100)

   while True:            
       if sort < 45:
         classe = Classe.objects.filter(key1 = keys1, key2=keys2)
         if classe:
            break
         sort = randint(45,100)
       elif sort < 65:
         classe = Classe.objects.filter(key1 = keys2, key2 = keys1)
         if classe:
            break
         sort = randint(65,100)
       elif sort < 80:
          classe = Classe.objects.filter(key1 = keys1)
          if classe:
            break
          sort = randint(80,100)
       elif  sort < 87: 
          classe = Classe.objects.filter(key1 = keys2)
          if classe:
               break
          sort = randint(87,100)  
       elif sort < 93:  
          classe = Classe.objects.filter(key2 = keys1)
          if classe:
            break
          sort = randint(93,100)
       elif sort < 98:  
          classe = Classe.objects.filter(key2 = keys2)
          if classe:
            break
          sort = 100
       else:  
          classe = Classe.objects.all()
          break
       
   classe = choice(classe)
   return classe



def set_level(level:int)->int:

   if level == '':      
      level = randint(1,20)
   else:
      level = int(level)  

      if level > 20:
         level = 20
      elif level < 1:
         level = 1   

   return level





def set_gold(level:int,classe)  -> float :
   
   if level > 1:
    max_gold = int(Wealth.objects.get(id=2).Wealth.split(',')[level-1])
    gold = randint(int(max_gold/2),int(max_gold))
    return gold
   
   starting = classe.gold.split(' ')
   gold = []

   for i in range(int(starting[0][0])):
      gold.append(randint(1,int(starting[0][2]))) 

   gold = sum(gold) * int(starting[2])     
   return gold


def set_weapon(classe,race,level:int,gold:float):
    parameter1 = classe.weapons.split(',')
    parameter2 = classe.weapons_name.split(',')
    weapons = Weapons.objects.filter(designation__in = parameter1 ) | Weapons.objects.filter(weapon__in = parameter2 )  

    if weapons and gold > 0:
       weapon = SetWeapons(choice(weapons))

       if gold > 300 and weapon.name != 'Unarmed Strike' :

         while True:
           magic = magic_possibility(level)

           if magic == 'MW':
              weapon.magic = 'MW'
              gold = gold-300
              break
           
           if (magic*magic*2*1000) <= gold:
              gold = gold - magic*magic*2*1000

              if magic > 1:
               fixed = Magic_Enhancement.objects.exclude(price__contains='bonus', slot__contains=['Armor','SHield'])               
               fixed = choice(fixed)
               weapon.set_magic(magic)     

               if fixed.absolute_price <= gold:
                  weapon.fixed_property = fixed.name
                  gold = gold - fixed.absolute_price    

              break         
         weapon.adjust()             
         return weapon,gold    
       return weapon,gold   
    
    

def magic_possibility(level:int) -> int:

   magic = ((level/2) * randint(1,100)) / 100 
   if 1 > magic > 0.49:
      return 'MW'
   return int(magic)

    
    


def set_armor(classe,level:int,gold:float):
   if gold < 0:
      return '',gold
   magic = ''
   armors = classe.armors.split(',')
   armorn = classe.amors_name.split(',')
   armor =  Armor.objects.filter(armor__in= armorn) | Armor.objects.filter(category__in = armors)
   if not armor :
      return '',gold
   armor = SetArmor(choice(armor))
   if gold > 1000:
      while True:
       magic = magic_possibility(level)
       if magic == 'MW':
          armor.magic = 'MW'
          gold = gold - 150
          break 
       if magic * magic * 1000 <= gold:
          gold = gold - magic * magic * 1000
          break
   if magic:
      armor.set_magic(magic)
      armor.adjust()
   return  armor,gold

def change_speed(speed:int) -> int:
   if speed == 30:
      return 20
   return 15      

at = {
      'STR' : 0,
      'DEX' : 1,
      'CON' : 2,
      'INT' : 3,
      'WIS' : 4,
      'CHA' : 5,      
   }   

def set_skills(classe,nskills:str,level:int,penalty:int,mod:int,race):  
   global at  
   armorpenalty = penalty
   tot = 0
   skill_list = {
      'Alchemy' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Animal Empathy' : { 'atribute' : 'CHA','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Appraise' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Autohypnosis' : { 'atribute' : 'WIS','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Balance' : { 'atribute' : 'DEX','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 1,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Bluff' : { 'atribute' : 'CHA','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'Diplomacy, Disguise, Sleight of Hand','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Climb' : { 'atribute' : 'STR','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 1,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Concentration' : { 'atribute' : 'CON','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'Autohypnosis','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Control Shape' : { 'atribute' : 'WIS','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Craft' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Decipher Script' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Diplomacy' : { 'atribute' : 'CHA','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Disable Device' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Disguise' : { 'atribute' : 'CHA','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Escape Artist' : { 'atribute' : 'DEX','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 1,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Forgery' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Gather Information' : { 'atribute' : 'CHA','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Handle Animal' : { 'atribute' : 'CHA','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'Ride','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Heal' : { 'atribute' : 'WIS','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Hide' : { 'atribute' : 'DEX','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 1,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Iaijutsu Focus' : { 'atribute' : 'CHA','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Innuendo' : { 'atribute' : 'WIS','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Intimidate' : { 'atribute' : 'CHA','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Intuit Direction' : { 'atribute' : 'WIS','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Jump' : { 'atribute' : 'STR','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 1,'sinergy' :'Tumble','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Knowledge (arcana)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'Spellcraft','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (architecture and engineering)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (barbarian lore)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (code of martial honor)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (dungeoneering)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (geography)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'Survival','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (history)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (law)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (local)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'Gather Information','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (nature)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'Survival','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (nobility and royalty)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'Diplomacy','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (psionics)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'Psicraft','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (religion)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (Shadowlands)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (spirits)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (tactics)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (the planes)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (War)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Knowledge (weaponry)' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Listen' : { 'atribute' : 'WIS','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Lucid Dreaming' : { 'atribute' : 'WIS','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Martial Lore' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Move Silently' : { 'atribute' : 'DEX','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 1,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Open Lock' : { 'atribute' : 'DEX','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Perform' : { 'atribute' : 'CHA','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Pick Pocket' : { 'atribute' : 'DEX','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 1,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Profession' : { 'atribute' : 'WIS','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Psicraft' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'Use Psionic Device','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Read Lips' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Ride' : { 'atribute' : 'DEX','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Scry' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Search' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Sense Motive' : { 'atribute' : 'WIS','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'Diplomacy','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Sleight of Hand' : { 'atribute' : 'DEX','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 1,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Speak Language' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Spellcraft' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Spot' : { 'atribute' : 'WIS','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Survival' : { 'atribute' : 'WIS','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'Knowledge (nature)','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Swim' : { 'atribute' : 'STR','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 1,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Truespeak' : { 'atribute' : 'INT','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Tumble' : { 'atribute' : 'DEX','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 1,'sinergy' :'Balance','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Use Magic Device' : { 'atribute' : 'CHA','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Use Psionic Device' : { 'atribute' : 'CHA','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'Psicraft','sinergies' : 0,'trained' : True, 'inclasse' : False },
      'Use Rope' : { 'atribute' : 'DEX','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
      'Wilderness Lore' : { 'atribute' : 'WIS','total' : tot,'graduation' : 0,'modificator' : 0,'amorpenalty' : 0,'sinergy' :'-','sinergies' : 0,'trained' : False, 'inclasse' : False },
     
   }
   global at
   
   class_skills = classe.split('||')  
   try:
      class_skills.remove('Speak Language') 
   except:   
      pass

   max_skill = level +3
   tot_sp = (mod[3] + nskills) * max_skill
   totalsp = tot_sp
   finalskills = {}

   while tot_sp > 0:
      skl = choice(class_skills)   
      spent = randint(1,max_skill - skill_list[skl]['graduation'])

      if spent > tot_sp:         
         spent = tot_sp

      skill_list[skl]['graduation'] += spent
      tot_sp -= spent

      if skill_list[skl]['graduation'] >= max_skill:
         class_skills.remove(skl)

   if race.SkillBonus:
      racial_skills = race.SkillBonus.split(',')

      for racial in racial_skills:
         skill_list[racial[2:]]['sinergies'] = int(racial[0])
         skill_list[racial[2:]]['total'] = int(racial[0])

   if race.Size == 'Small':        
       skill_list['Hide']['sinergies'] +=4
       skill_list['Hide']['total'] +=4      
         
   for i,j in skill_list.items():   
      skill_list[i]['total'] += skill_list[i]['graduation'] 

      if skill_list[i]['graduation'] >= 5:
         if skill_list[i]['sinergy'] != '-':
            sin = (skill_list[i]['sinergy']).split(',')
        
            for h in sin:              
               skill_list[h.strip()]['total'] += 2
               skill_list[h.strip()]['sinergies'] += 2

      if skill_list[i]['amorpenalty'] == 1:
         skill_list[i]['total'] -= armorpenalty
         skill_list[i]['amorpenalty'] = armorpenalty
      else:
         skill_list[i]['amorpenalty'] = ''   
    
      skill_list[i]['total'] += mod[at[ skill_list[i]['atribute']]]
      skill_list[i]['modificator'] += mod[at[ skill_list[i]['atribute']]]     

      if i in classe.split('||') and skill_list[i]['graduation'] > 0:
             skill_list[i]['inclasse'] = True  
             finalskills[i] = j

      elif skill_list[i]['trained'] != True:          
          finalskills[i] = j    
 
   return totalsp,dict(sorted(finalskills.items()))


 

def set_number_item(level:int) -> int:
  number = int(level/5)
  probab = level * 4
  for i in range(4):
    probab_num = randint(0,100)
    if probab_num < probab:
      number +=1
    else:
      return number
  return number    

 
def set_gear(level):
   gear = ['Backpack (empty)', 'Barrel (empty)', 'Basket (empty)', 'Bedroll', 'Bell', 'Blanket, winter', 'Block and tackle', 'Bottle, wine, glass', 'Bucket (empty)', 'Caltrops', 'Candle', 'Canvas (sq. yd.)', 'Case, map or scroll', 'Chain (10 ft.)', 'Chalk, 1 piece', 'Chest (empty)', 'Crowbar', 'Firewood (per day)', 'Fishhook', 'Fishing net, 25 sq. ft.', 'Flask (empty)', 'Flint and steel', 'Grappling hook', 'Hammer', 'Ink (1 oz. vial)', 'Inkpen', 'Jug, clay', 'Ladder, 10-foot', 'Lamp, common', 'Lantern, bullseye', 'Lantern, hooded', 'Lock (very simple)', 'Lock (average)', 'Lock (good)', 'Lock (amazing)', 'Manacles', 'Manacles, masterwork', 'Mirror, small steel', 'Mug/Tankard, clay', 'Oil (1-pint flask)', 'Paper (sheet)', 'Parchment (sheet)', 'Pick, miner’s', 'Pitcher, clay', 'Piton', 'Pole, 10-foot', 'Pot, iron', 'Pouch, belt (empty)', 
      'Ram, portable', 'Rations, trail (per day)', 'Rope, hempen (50 ft.)', 'Rope, silk (50 ft.)', 'Sack (empty)', 'Sealing wax', 'Sewing needle', 'Signal whistle', 'Signet ring', 'Sledge', 'Soap (per lb.)', 'Spade or shovel', 'Spyglass', 'Tent', 'Torch', 'Vial, ink or potion', 'Waterskin', 'Whetstone']
   number = int( (level /5)  * 4) + level + 1
  
   return choices(gear,k=number)




