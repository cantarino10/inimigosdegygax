from django.shortcuts import render
from .func import *
from main.models import Classe,Race,Handbooks
from .models import Wealth
from .char_info import Character
from .xp_calc import *
from time import time
# Create your views here.
atrb = ['STR','DEX','CON','INT','WIS','CHA']
def roll_dice(request):
  standard_dices = ['d4','d6','d8','d10','d12','d20','d100']
  
  if request.method == "POST":

    a = dict(request.POST)   
    print(a)
    result,sume,dices = roll_dices(a)
    result = zip(result,sume,dices)   
    context = {'choices' : zip(request.POST.getlist('number_dices'),request.POST.getlist('Dice'),range(7)),'results' : result, 'sum' : sum(sume)}
    return render(request,'tools/roll_dice.html', context)

  context = {'choices' : zip([0,0,0,0,0,0,0],standard_dices,range(7))}
  return render(request,'tools/roll_dice.html', context)

def stats_builder(request,atributes = False):
  stats,mod = random_atributes()

  if request.method == "POST":
    modf(request)

  atributes = zip(stats,mod,['str','dex','con','int','wis','cha'])
  context = {'range' : range(6),'atributes' : atributes,'total' : sum(stats)}
  return render(request, 'tools/stats_builder.html', context)


def char_builder(request):
  
  if request.method == "POST":
    char = Character()   
    char.adjust(request)       
    context = {'char':char,'weapons' : zip([char.weapon1,char.weapon2],[char.damage1,char.damage2]), 'modify' : char.modify,'stats' : zip(char.atributes,char.modify,atrb),'totalatributes' : sum(char.atributes),
               'abilities':zip(char.abilities,range(1,21)),'books': 2}    
    return render(request, 'tools/show_char.html', context)
  
  books = Classe.objects.all().values_list('book',flat=True).distinct().order_by('book')  
  classe = Classe.objects.all()
  race = Race.objects.all()
  context = {'classes': classe,'races': race,'atributes' : zip(range(6),atrb),'books' : books}
  return render(request, 'tools/char_builder.html', context)




def encounter_calculate(request):

  if request.POST.get('button') == 'reset' or request.method == "GET":
    zero = [0,0,0,0,0,0]
    zeros = zip(zero,zero)
    context = {'monsters':zeros,'players':zip(zero,zero),'range' : range(6)}
    return render(request,"tools/xp_calculate.html",context)    
  
  players = [request.POST.getlist('plvl'), request.POST.getlist('pnumber')]
  monsters = [request.POST.getlist('mlvl'), request.POST.getlist('mnumber')]

  if set(players[0]) == {'0'} or set(players[1]) == {'0'} or set(monsters[0]) == {'0'} or set(monsters[1]) == {'0'}:
    zero = [0,0,0,0,0,0]
    zeros = zip(zero,zero)
    context = {'monsters':zeros,'players':zip(zero,zero),'range' : range(6),'message' : "Select at least 1 group of monsters and 1 group of players"}
    return render(request,"tools/xp_calculate.html",context)    

  xp,el,pl,each_xp = calc(players,monsters)
  if el < 25:
      treasure = set_treasure(el)

  dificult = set_dificult(el,pl)    
  context = {'monsters': zip(request.POST.getlist('mlvl'),request.POST.getlist('mnumber')), 'players' : zip(request.POST.getlist('plvl'),request.POST.getlist('pnumber')),
               'xp' : xp, 'el' : el,'pl' : pl,'each_xp' : each_xp, 'difficult' : dificult,'treasure':treasure}
  return render(request,"tools/xp_calculate.html", context)


def item_randomize(request):
  context = {}
  message = None

  if request.method == "POST":

    if request.POST.get('item_category') != "":
      item = set_item(request.POST.get('item_category'))
      book = Handbooks.objects.filter(text = item.handbook)
    else:
      item = Items.objects.filter(price__gte = request.POST.get('min_value'), price__lte= request.POST.get('max_value'))
      try:
        item = choice(item)
      except:
        item = None  
        book = None
        message = f'Could not find an item between {request.POST.get('min_value')}gp and {request.POST.get('max_value')}gp '
      else:  
        book = Handbooks.objects.filter(text = item.handbook)
    context = {'item' : item,'book' : book ,'message':message}    
    
  return render(request, "tools/random_item.html", context)

def set_item(category):
  prices  = {
    'Minor' : [200,7400,],
    'Medium':[7500,28000],
    'Major':[28000,99999999]

  }

  price = prices[f'{category}']
  item = Items.objects.filter(price__gte = price[0], price__lte= price[1])
  return choice(item)



  