from main.models import *
from tools.models import *
from .func import *
from random import choice,randint
abilities = ['STR','DEX','CON','INT','WIS','CHA']

class Character:
  def __init__(self) -> None:
       self.shield = None
 
  def adjust(self,request):
    atributes = []
    self.level= set_level(request.POST.get('level'))  
    self.set_race(request.POST.get("Race"),request.POST.get('adjust_lvl'))    
    for i in range(6):
      try:  
        atributes.append(int(request.POST.get(f'atribute{i}')))
      except :
         atributes.append('')

    self.generate_atributes(atributes)       
    self.set_race_adjust()  
    self.set_hair(request.POST.get('hair')) 
    self.set_alignment(request.POST.get('aligment'))
    self.set_skin(request.POST.get('skin')) 
    self.set_class(request.POST.get('classes'),request.POST.get('book'))  

    if int(self.level) > 3:
      self.add_stats(request.POST.get('prefered_stats'))
    else:
      self.modify = modf(self.atributes)   

    self.gold = set_gold(self.level,self.classe)    
    self.gender = request.POST.get('gender')     
    self.abilities = self.abilities[:int(self.level)] 
    self.set_numfeats()
    self.set_pv()        

    if request.POST.get('name') == "":
       self.name = ' '
    else:
       self.name = request.POST.get('name')  

    self.ini = self.modify[2]
    self.pv += self.modify[1] * self.level
    self.set_bba()
    self.set_atributes()   
    self.fort,self.ref,self.will = self.set_save([int(self.modify[2]),int(self.modify[1]),int(self.modify[4])])
    self.weapon1 = self.set_weapon()   
    self.armor,self.gold = set_armor(self.classe,self.level,self.gold)
    self.weapon2 = self.set_weapon()
    self.weapon1.set_bba(self.level,self.classe.BBA,self.modify[0],self.modify[1],self.race.Size)
    self.weapon2.set_bba(self.level,self.classe.BBA,self.modify[0],self.modify[1],self.race.Size)
    self.damage1 = self.set_damage(self.weapon1,int(self.modify[0]))
    self.damage2 = self.set_damage(self.weapon2,int(self.modify[0]))   

    if 'Shield' in self.weapon1.name :
       shield = Shield.objects.filter(shield__contains = self.weapon1.name[-5:]).first()     
       self.set_shield(shield = shield) 
    elif self.weapon1.category == 'One Hand':
        self.set_shield()   

    self.set_item()          
    self.ca = 10 + self.modify[1]    
    self.set_ca()     

    if self.armor:     
      if self.armor.penalty_speed:
        self.speed = change_speed(self.speed)     
    self.totalskill,self.skills = set_skills(self.classe.classSkills,self.classe.Skills,self.level,self.penalty,list(self.modify),self.race )

    if self.race.Size == 'Small':   
       self.ca +=1
  
    self.gear = set_gear(self.level)
    self.set_weight()
    self.set_load()
    self.set_spells()
    self.set_feats()
    self.set_language()  


  def set_weight(self):
     self.weight = int(self.weapon1.weight + self.weapon2.weight    )
     if self.armor != '':
        self.weight+= self.armor.weight
     if self.shield:
        self.weight+= self.shield.weight

       
     
  def add_stats(self,fixed):  
   points = int(self.level/4)
   if fixed != '':           
      self.atributes[int(fixed)] += points

   key1 = self.classe.key1
   key2 = self.classe.key2
  
   for i in range(points):
      if points == 0:
         break  
      if  key1 == key2:
         self.atributes[key1] += points
         return      
      elif (self.atributes[key1] % 2) == 1:
         self.atributes[key1] +=1
         points -= 1  
      elif  (self.atributes[key2] % 2) == 1:
         self.atributes[key1] +=1
         points -= 1  
      elif self.atributes[2] % 2 ==1:
         self.atributes[2] += 1
         points -=1
      else:        
         self.atributes[choice([key1,key1,key2])] +=1
         points -= 1     
   
   self.modify = modf(self.atributes)

  

  def generate_atributes(self,atr:list):
   roll = False
   at = atr.copy() 

   for i in range(6):
      if at[i] == '':
         roll = True

   if roll == True :     
      for i in range(6):   
         if at[i] == '':
            at[i] = int(random_at())   
            at[i]   
   
         if at[i] >= 14:
            roll = False      
      if roll == True:
         self.generate_atributes(atr)   
  
   self.atributes =  at
   self.modify = modf(at)   


  def set_hair(self,hair):
   color = ["White","Blond","Red","Gray","Brown","Black"]
   if hair == '':
      hair = color[randint(0,5)]

   self.hair =  hair


  def set_alignment(self,alignment:str) -> str:  
   algm = ["Lawful/Good","Lawful/Neutral","Lawful/Evil","Neutral/Good","True Neutral","Neutral/Evil","Chaotic/Good",
            "Chaotic/Neutral","Chaotic/Evil"]
   if alignment == None:
         alignment = algm[randint(0,8)]

   self.alignment = alignment


  def set_skin(self,skin:str) -> str:
   color = ["White","Pale","Yellow","Gray","Brown","Black"]
   if skin == '':
      skin = color[randint(0,4)]

   self.skin= skin 

  def set_class(self,class_name:str,book):
   if class_name != '':
      classe = Classe.objects.get(Class = class_name) 
   elif book != '':
      classe = choice(Classe.objects.filter(book = book))     
   else:
      classe = rand_class(self.atributes)   
      
   abilities = classe.Abilities.split('|')   
   self.classe =  classe
   self.abilities = abilities

  def set_bba(self) -> None:
   fbba = []
   rbba = []
   mbba=[]
   classe = self.classe.BBA
   strg = self.modify[0]
   dex = self.modify[1]

   if classe == 'Poor':
      bba =BBA.objects.get(level = self.level).Poor
   elif classe == 'Medium':
      bba = BBA.objects.get(level = self.level).Medium
   else:
       bba = BBA.objects.get(level = self.level).Good

   if bba < 6:
      self.bba = str(f'+{bba}')
      self.meele = str(f'+{bba + strg}')
      self.ranged = str(f'+{bba + dex}')   
      return None
   
   for i in range(5) :
       
         fbba.append(str(f'+{bba - (5 * i) }'))
         mbba.append(str(f'+{bba - (5 * i) + strg}'))
         rbba.append(str(f'+{bba - (5 * i) + dex}'))
         if bba / ((i+1)*5) < 1:
            break

   self.bba = '/'.join(fbba)
   self.meele = '/'.join(mbba)
   self.ranged = '/'.join(rbba) 


  def set_shield(self,shield = None) -> None:
   gold = self.gold
 
   if not shield:   
      shields = self.classe.shields.split('|')
      shield = Shield.objects.filter(shield__in=shields)   
      try:
        shield  = choice(shield)
      except:
         return 
   
   shield = SetShield(shield)

   if gold > 150:
         while True:
          magic = magic_possibility(self.level)
        
          if magic == 'MW':
            shield.magic = 'MW'
            gold = gold - 150
            break 
          if magic * magic * 1000 <= gold:
            gold = gold - magic * magic * 1000
            break
         if magic:
           shield.set_magic(magic)
           shield.adjust()

   self.shield = shield
   self.gold = gold 

  def set_pv(self,)->None:
   hd = self.classe.HitDice
   pv = hd
   for i in range(self.level - 1):
      pv += randint(1,hd)      

   self.pv = pv  

  def set_save(self,abilities:list[int]) -> list:
   bases = []
   save = []
   saves = self.classe.Saves.split(',')
   self.extra_save = 0

   if self.race.Race == 'Halfling':        
         self.extra_save += 1
   if self.classe.Class == 'Paladin' and self.level > 1:
      self.extra_save += int(self.cha_mod)

   for i in range(3):
      if saves[i] == 'Poor':
         base = int(self.level/3)
         sa =int(abilities[i] + (self.level/3) )
      else:
         sa = int(abilities[i] + (self.level/2) + 2 )
         base = int(self.level/2) +2
          
      bases.append(base)
      save.append(sa + self.extra_save )
   self.fort_base,self.ref_base,self.will_base = bases
   return save
  
  def set_weapon(self):
    gold = self.gold
    parameter1 = self.classe.weapons.split(',')
    parameter2 = self.classe.weapons_name.split('|')
    if self.race.weapons:
      
       for weapon in self.race.weapons.split('|'):
          parameter2.append(weapon)
         
    weapons = Weapons.objects.filter(designation__in = parameter1 ) | Weapons.objects.filter(weapon__in = parameter2 )  
  
    if weapons and gold > 0:
       weapon = SetWeapons(choice(weapons))

       if gold > 300 and weapon.name != 'Unarmed Strike' :
         while True:
           magic = magic_possibility(self.level)
            
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
         self.gold = gold
         return weapon    
       self.gold = gold
       return weapon   
    return SetWeapons(Weapons.objects.get(weapon__contains = 'Unarmed'))
  
  def set_damage(self,weapon,str:int) -> int:
   
   if weapon.category == 'Two Hand':
      return int(str*1.5) + weapon.enhancement
   elif weapon.category == 'One Hand' or 'Composite' in weapon.name:
      return str  + weapon.enhancement
   else:
      return 0  + weapon.enhancement 

  def set_item(self,):
   gold = self.gold
   number_item = set_number_item(self.level)  
   items = []

   for i in range(number_item):
      if gold < 8:
         break
      item = Items.objects.filter(price__gt = 0,price__lte = gold, family__in=['Ring','Wondrous','Cursed','Universal Items'])
      item = choice(item)
      item.price = int(item.price)
      items.append(item)
      gold -= item.price

   self.items = items
   self.gold = gold  

  def set_ca(self):
   dex = self.modify[1]
   armor = self.armor
   shield = self.shield
   maxdex = 100
   armorca = 0
   shieldca = 0
   penalty = 0

   if armor != None and armor != '':
      maxdex = armor.maxdex 
      armorca = armor.ca
      penalty += armor.penalty

   if shield != '' and shield != None:
      if maxdex > shield.maxdex:
         maxdex = shield.maxdex  
         penalty += shield.penalty 
      shieldca = shield.ca
     
   if maxdex > dex:
      self.ca = (10 + armorca + dex + shieldca)
      self.penalty = penalty
      self.maxdex = maxdex
      self.touch_ca = 10 + dex
      if 'Uncanny dodge' in self.abilities:
          self.flat = self.ca
      else:
         self.flat = self.ca - dex     
         
      return
   
   self.ca = (10 + armorca + shieldca + maxdex)
   self.penalty  = penalty
   self.maxdex = maxdex
   self.touch_ca = 10 + maxdex

   if 'Uncanny dodge' in self.abilities:
          self.flat = self.ca
   else:
      self.flat = self.ca - maxdex      

  def set_load(self):
     if self.atributes[0]>29:
        self.carrying = 'Light'
        return
        
     table =  Carrying.objects.get(str = self.atributes[0])
     if self.weight <= int(table.light):
        self.carrying = 'Light'
              
     elif self.weight <= int(table.medium.split('-')[1] ):
        self.carrying = 'Medium'
        self.set_speed()  
        self.penalty -=3
        if self.maxdex > 3:
           self.maxdex = 3      
     else:
        self.carrying = 'Heavy'
        if self.maxdex > 1:
           self.maxdex = 1 
        self.penalty -=6
             
        self.set_speed()
        
  def set_speed(self):
     if self.speed == 30:
      self.speed = 20
     elif self.speed == 20:
        self.speed = 15
     else:
        self.speed = 10       
        
  def set_spells(self)  :
     allspells = {'0': [],'1': [],'2':[],'3':[],'4':[],'5':[],'6':[],'7':[],'8':[],'9':[],

     }
     self.insuficiente = False
     key_ab = int(self.modify[self.classe.key1])
     
     self.spell_key = abilities[self.classe.key1]
     if self.classe.spells == 'None':
        self.spells = None
        return
     
     spell_data = self.classe.spells.split('||')
     spells = spell_data[self.level-1]
     if spells == '':      
        self.spells = None
        return
     
     for spell in spells.split(','):
        quanty_spells = int(spell[2])
        
        if key_ab >= int(spell[0]):
           quanty_spells += 1 + int((key_ab - int(spell[0]))/4)
        for i in range(quanty_spells):
           
           spells =  Spells.objects.filter(level__contains= f'{self.classe} {spell[0]}' )
          
           if spells.exists():
            spl = choice(spells)
          
            if int(self.atributes[self.classe.key1]) - 10 < int(spell[0]):
               spl.name = spl.name + '*'
               self.insuficiente = True
            allspells[f'{spell[0]}'].append(spl)

     self.spells = allspells   

  def set_numfeats(self) :
     self.feat = int(self.level/3) + 1
     if self.race.Race == 'Human':
        self.feat+=1

  def set_feats(self):
      self.feats = []
      for i in range(self.feat):
         self.feats.append(choice(Feats.objects.filter(requisite = ' ')))
       
  def set_race_adjust(self):
   for adjust,i in zip(self.race.Adjustment.split(','),range(6)):
      self.atributes[i] += int(adjust)

   self.speed = self.race.Speed
   self.languages = self.race.Languages
   
   if self.race.level_adjstument:
         if self.level <= self.race.level_adjstument:
            self.level = 1
            self.Adjustment_level = self.race.level_adjstument + 1
         else:   
            self.Adjustment_level = self.level
            self.level -= self.race.level_adjstument
   else:
      self.Adjustment_level = False
    
   self.link = Races.objects.filter(text = self.race.Race).first().link


     
  def set_atributes(self):
     self.str = self.atributes[0]
     self.dex = self.atributes[1]
     self.con = self.atributes[2]
     self.int = self.atributes[3]
     self.wis = self.atributes[4]
     self.cha = self.atributes[5]
    
     self.str_mod = self.modify[0]
     self.dex_mod = self.modify[1]
     self.con_mod = self.modify[2]
     self.int_mod = self.modify[3]
     self.wis_mod = self.modify[4]
     self.cha_mod = self.modify[5]

  def set_language(self):
   self.languages = self.race.Languages.split(",")
   if self.int_mod > 0:
      for i in range(self.int_mod):
          l =choice(Languages.objects.exclude(language__in = self.languages))
          self.languages.append(l.language)
  

        
  def set_race(self,race_name:str,lvladjust):
   if race_name =='None':
       if  not lvladjust:
         races = list(Race.objects.exclude(level_adjstument__gte = 1))
       else:
         races = list(Race.objects.all())          

       self.race = choice(races)
   else:      
      self.race = Race.objects.get(Race = race_name)  
  
     
 
   
   


   