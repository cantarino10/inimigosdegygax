
from math import log2,ceil
def calc(play:list,mons:list):

  party_level = []
  number_player = sum(list(map(int,play[1])))

  encounter_level = 0
 
  for i in range(6):
    encounter_level += power_level(float(mons[0][i]),int(mons[1][i]))
    if play[0][i] != '0' and play[1][i] != '0':
     party_level.append(int(play[0][i]) * int(play[1][i]))

  encounter_level = (2 * log2(encounter_level))  

  if encounter_level < 1 :
    encounter_level=1
  encounter_level = round(encounter_level)  

  party_level = ceil(sum(party_level)/ number_player)

  xp =  int(calculate_xp(encounter_level,int(party_level)))

  return xp,encounter_level,party_level,int(xp/number_player)


 


def calculate_xp(cr,plvl) -> int:
  
  if plvl == 1:
    if cr > 3:
      return 1350 * (1 + ((cr - 4)/2))
    else:
      return 300*cr  
  else:
    gap_or = cr-plvl

    if gap_or < -7:
      return 0
    gap = 0-gap_or 
    xp = (plvl * 300) 
    
    if gap % 2 != 1: 
      calc_fator =(pow(2,gap * 0.5) )       
    else:
      calc_fator =(pow(2,(gap+1) * 0.5) ) + (pow(2,(gap-1) * 0.5) )     
      calc_fator = calc_fator/2
    if gap_or >= 0:  
      total_xp = xp /  calc_fator     
   
    else:
      total_xp = xp*  calc_fator
    return int(total_xp)

def power_level(cr:float,number:float) -> float:

  if cr <= 1 : 
    return cr * number
  else:   
    return round(pow(2,cr/2) * number,3)

def set_dificult(el:int,pl:int) -> str  :
  dif = el - pl
  
  if dif <= -8:
    return "No challenge"
  elif dif < -2:
    return "Easy"
  elif dif < 0:
    return "Easy if handled properly"  
  elif dif == 0:
    return "Challenging"
  elif dif <= 4:
    return "Very difficult"  
  
  return "Overpowering"  
  

def set_treasure(lv):
  treasure = [300, 600, 900, 1200, 1600, 2000, 2600, 3400, 4500, 5800, 7500, 9800, 13000, 17000, 22000, 28000, 36000, 47000, 61000, 80000, 87000, 96000, 106000, 116000, 128000, 141000, 155000, 170000, 187000, 206000,
               227000, 249000, 274000, 302000, 332000, 365000, 401000, 442000, 486000, 534000]
  return treasure[lv]
 
