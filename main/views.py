from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from time import sleep
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import Entryhb,EntryClasses,EntryRaces,EntryItems,EntryFeat,EntrySpells,EntryRaces
from .models import Handbooks,Classes,Races,Items,Feats, Spells,favorites_spells,favorites_feats,Skills,Magic_Enhancement
from django.contrib.auth.decorators import login_required      #metodo para restringer os logins
#decorator são para alterar o comportamento da função sem mudar a função
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator

import pandas as pd
from django.shortcuts import get_object_or_404
import re,json,requests

### 'result' variables are here to store search data even after page refresh
resulthb = []  

def index(request): #Function to the main site
 return render(request, 'main/index.html')

def handbooks(request): #Function to search for handbooks
  global resulthb
  if request.method == 'GET':
        class_paginator = Paginator(resulthb,20)
        try:
          pag_num = request.GET['page']  #check if the method return a valid page
        except:
           return render(request, "main/handbooks.html")
  else:
    try:
      searchh = request.POST['searchh']
    except:
      return render(request, "index.html")  
    resulthb = Handbooks.objects.filter(text__contains= searchh,edition__contains=request.POST['version']).order_by('text')
    class_paginator = Paginator(resulthb,20)    
    pag_num = request.POST.get('page') 
  page = class_paginator.get_page(pag_num)
  context = { 'pag' : page, 'method' : request.method}
  return render(request, "main/handbooks.html", context)

@user_passes_test(lambda u: u.is_superuser) # check if user is a super user to register new books
def register_books(request):  
  if request.method != 'POST':    
    form = Entryhb()
  else:
    form = Entryhb(data=request.POST) 
    if form.is_valid() :
      new_entry = form.save()
      new_entry.text = request.POST.get('handbook')     
      new_entry.save()
      return HttpResponseRedirect(reverse('index'))
  context = {'form' : form}  
  return render(request, 'main/register_books.html', context)


def handbook(request, book: str):

  hbook = Handbooks.objects.get(text = book) 
  return HttpResponseRedirect(hbook.link)


resultcl = []
def classes(request,classe = False):
  global resultcl
  if request.method == 'POST':
    try:  
     searchclasses = request.POST['searchclasses']  #check if method sends a valid class
    except:
      return render(request,'main/classes.html') 
    resultcl = Classes.objects.filter(text__contains=searchclasses,category__contains=request.POST['classtype']).order_by('text')
    class_paginator = Paginator(resultcl,20)
    pag_num = request.POST.get('page')
  
  else:
      if classe:
        resultcl = Classes.objects.filter(text=classe).order_by('text')
        class_paginator = Paginator(resultcl,20)
        pag_num = request.GET.get('pag')
        page = class_paginator.get_page(pag_num)
        context = { 'pag' : page, 'method' : request.method}
        return render(request, 'main/classes.html', context)  
      class_paginator = Paginator(resultcl,20)
      try:
          pag_num = request.GET['page']
      except:
           return render(request, 'main/classes.html')
  page = class_paginator.get_page(pag_num)
  
  context = { 'pag' : page, 'method' : request.method}
  return render(request, 'main/classes.html', context)  

@user_passes_test(lambda u: u.is_superuser)
def register_classes(request):  
  if request.method != 'POST':    
    form = EntryClasses()
  else:
    form = EntryClasses(data=request.POST) 
    if form.is_valid() :
      new_entry = form.save()
      new_entry.category = request.POST.get('classtype')
      new_entry.save()     
      return HttpResponseRedirect(reverse('index'))
  context = {'form' : form}  
  return render(request, 'main/register_classes.html', context)


resultrc = []
def races(request):
    global resultrc
    if request.method =='GET':
        class_paginator = Paginator(resultrc,20)
        try:
          pag_num = request.GET['page']
        except:
            return render(request, "main/races.html")
    else:
      try:
        racesname = request.POST['racesname']
      except:
        return render(request, "main/races.html")  
      resultrc = Races.objects.filter(text__contains=racesname,handbook__contains=request.POST['racesbook']).order_by('text')
      class_paginator = Paginator(resultrc,20)
      pag_num = request.POST.get('page')
    page = class_paginator.get_page(pag_num)
    context = { 'pag' : page, 'method' : request.method}
    return render(request, "main/races.html", context)
 
@user_passes_test(lambda u: u.is_superuser)

def register_races(request):
  atributes  = ['STR','DEX','CON', 'INT','WIS','CHA']
  atr = []
  skills = []
  if request.method != 'POST':
    form = EntryRaces()
  else:
    form = EntryRaces(data=request.POST) 
    if form.is_valid() :
      new_entry = form.save()
      for i in range(6):
        if request.POST.get(f'atr{i}') != '0':
          value = request.POST.get(f'atr{i}')
          atr.append(str(value + ' ' + atributes[i]))
        
        if request.POST.get(f'skills{i}') != '' and  request.POST.get(f'skill_input{i}') != '':
           skillvalue = request.POST.get(f'skill_input{i}')
           skills.append(str( skillvalue + ' ' +  request.POST.get(f'skills{i}')))
        
      new_entry.Adjustment = ','.join(atr)
      new_entry.SkillBonus = ','.join(skills)
      new_entry.save()
      return render(request, 'main/register_races.html')
  atributes  = ['STR','DEX','CON', 'INT','WIS','CHA']
  skill = Skills.objects.all()
 
  ziped = zip(atributes,range(6))
  context = {'form' : form,'zip' : ziped,'skills' : skill, 'range' : range(6)}  
  return render(request, 'main/register_races.html', context)

resultit = []
def items(request):
    global resultit
    if request.method == 'GET':
        class_paginator = Paginator(resultit,20)
        try:
          pag_num = request.GET['page']
        except:
           return render(request, "main/items.html")
    else:    
        try:        
         itemsname = request.POST['itemname']
        except:
          return render(request, "main/items.html")  
        if request.POST['itemprice'] == '':
          itemsprice = 9999999
        else:
          itemsprice = request.POST['itemprice']  
        
        resultit = Items.objects.filter(text__contains=itemsname,handbook__contains=request.POST['itemhandbook'],slot__contains=request.POST['itemslot'],price__lte=itemsprice).order_by('slot')
        class_paginator = Paginator(resultit,20)
        pag_num = request.GET.get('page')
    page = class_paginator.get_page(pag_num) 
    context = { 'pag' : page, 'method' : request.method}
    return render(request, "main/items.html", context) 


@user_passes_test(lambda u: u.is_superuser)
def register_items(request):
 
  if request.method != 'POST':
    form = EntryItems()
  else:
    form = EntryItems(data=request.POST) 
    if form.is_valid() :
      new_entry = form.save()   
     
      return HttpResponseRedirect(reverse('register_items'))
  context = {'form' : form}  
  return render(request, 'main/register_items.html', context)

resultft = []
def feats(request):
  global resultft
  if request.method == 'GET':
        class_paginator = Paginator(resultft,20)
        try:
          pag_num = request.GET['page']
        except:
           return render(request, "main/feats.html")
  else:      
    try: 
      featname = request.POST['featname']
    except:
      return render(request, 'main/feats.html')   
    resultft = Feats.objects.filter(name__contains=featname,handbook__contains=request.POST['feathandbook'],requisite__contains=request.POST['featrequisite'],type__contains=request.POST['feattype']).order_by('name')
    class_paginator = Paginator(resultft,20)
    pag_num = request.POST.get('page')
  page = class_paginator.get_page(pag_num) 
  context = { 'pag' : page, 'method' : request.method}  
  return render(request, "main/feats.html", context)


  
@user_passes_test(lambda u: u.is_superuser) 
def register_feats(request):
 
  if request.method != 'POST':
    form = EntryFeat()
  else:
    form = EntryFeat(data=request.POST) 
    if form.is_valid():
      form.save()
      return HttpResponseRedirect(reverse('register_feats'))
  context = {'form' : form}  
  return render(request, 'main/register_feats.html', context)



def feat(request,feat_id):
  requisites = []
  isfavorite= 'False'
 # response = requests.get(f"https://enemysofgygax-production.up.railway.app/api/feats/{feat_id}")
  feat = Feats.objects.get(id = feat_id)
  try:
    book = Handbooks.objects.get(text = feat.handbook)
  except:
    book = ''  
  try:
    otherfeats = Feats.objects.filter(name = feat.name)
  except:
    otherfeats = ''  
  if feat.required != ' ':
    feat.required = feat.required.split(',') 
  if feat.requisite != ' ':
    feat.requisite = feat.requisite.split(',')    
  feat.requisite = feat.requisite[:-1]
  for i in feat.requisite:

      b = i.split(' (')
      b = b[0].strip()
      a = Feats.objects.filter(name__contains = b).first()
      requisites.append(a)
  if request.user.is_authenticated:
    if favorites_feats.objects.get(user_id=request.user.id):
      sp = favorites_feats.objects.get(user_id=request.user.id)
      if feat_id in sp.feat_id.split(','):
        isfavorite = 'True'
  requisites = zip(feat.requisite,requisites)    
  context = {'isfavorite': isfavorite,'requisites' : requisites,'otherfeats':otherfeats,'feat'  : feat,'book' : book, 'method' : request.method}
  return render(request, 'main/feat.html', context)



def callfeat(request,feat_name):
  feats = Feats.objects.filter(name=feat_name).first()
  id = str(feats.id)
  return feat(request,id)
resultsp=[]

def spells(request,spells_name=False):
    global resultsp
    if spells_name:
      resultsp = Spells.objects.filter(level__contains=spells_name).order_by('name')
      class_paginator = Paginator(resultsp,20)
      pag_num = request.GET.get('pag')
      page = class_paginator.get_page(pag_num)
      context = { 'pag' : page, 'method' : request.method}
      return render(request, 'main/spells.html', context)  
    
    if request.method == 'GET':
        class_paginator = Paginator(resultsp,20)
        try:
          pag_num = request.GET['page']
        except:
           return render(request, 'main/spells.html') 
    else:    
        try: 
          spellname = request.POST['spellname']
        except:
            return render(request,'main/spells.html') 

        classlvl = request.POST['spellclass'] + ' ' + request.POST['spelllevel']
        resultsp = Spells.objects.filter(name__contains=spellname,handbook__contains=request.POST['spellhandbook'],level__contains=classlvl,Edition__contains=request.POST['spellversion'],school__contains=request.POST['spellschool'],spellresistance__contains=request.POST['spellresistance']).order_by('name')
        class_paginator = Paginator(resultsp,20)
        pag_num = request.POST.get('page')
    page = class_paginator.get_page(pag_num) 
    context = {'pag' : page, 'method' : request.method}
    return render(request, 'main/spells.html', context)
  
@user_passes_test(lambda u: u.is_superuser)   
def register_spells(request):
  if request.method != 'POST':
     form = EntrySpells()
  else:
    form = EntrySpells(data=request.POST) 
    if form.is_valid() :
      new_entry = form.save()
      return HttpResponseRedirect(reverse(f'index'))
  context = {'form' : form}  
  return render(request, 'main/register_spells.html', context)
classes_len = Classes.objects.filter(text__contains ='').count()


def spell(request,spell_id):
  j = 0
  global classes_len
  spell = Spells.objects.get(id = spell_id)
  classes =[]
  level = []
  isfavorite = 'False'
  try:
    book = Handbooks.objects.get(text = spell.handbook)
  except:
    book = ''  
  try:
    otherspells = Spells.objects.filter(name = spell.name)
  except:
    otherspells = ''  
  info = str(spell.level).split(',') 
  for j in info:
      if j != "":
        text2 = str(re.findall(r"[A-Z].*[0-9]", j))[2:-4]
        lvl = str(re.findall(r"\d",j))[2]
        classes.append(text2)
        level.append(lvl)
  if request.user.is_authenticated:
    if favorites_spells.objects.get(user_id=request.user.id):
      sp = favorites_spells.objects.get(user_id=request.user.id)
      if spell_id in sp.spell_id.split(','):
        isfavorite = 'True'
  classlvl = zip(classes,level)      
  context = {'isfavorite' : isfavorite,'spell'  : spell,'book' : book, 'method' : request.method,'classes' : classlvl, 'j' : j,'otherspells' : otherspells,'level': level}
  return render(request, 'main/spell.html', context)



def class_filter(request, classe):
 
  classe = str(classe)
  classe = classe.split(',')
  for i in range(len(classe)):
    if i <1:
     classe[i] = classe[i][:-2]
    else:
      classe[i] = classe[i][1:-2]
  classe = classe[:-1]
  result = Classes.objects.filter(text__in=classe).order_by('text')
  class_paginator = Paginator(result,20)
  pag_num = request.GET.get('page')
  page = class_paginator.get_page(pag_num) 
  context = { 'pag' : page, 'method' : request.method}
  return render(request, 'main/classes.html', context)  


def favorite_spell(request,spell_id):
    if not request.user.is_authenticated:
      return redirect('login')    
    if   favorites_spells.objects.filter(user_id=request.user.id):
      user = favorites_spells.objects.filter(user_id=request.user.id).first()
      ids = str(user.spell_id).split(',')[:-1]    
      if spell_id in ids:       
       ids.remove(spell_id) 
       if len(ids) > 0:     
        ids = ','.join(ids)
        ids = ids + ','   
       else:
         ids ='' 
       favorites_spells.objects.filter(user_id=request.user.id).update(spell_id= ids)
      else:
        ids.append(f'{spell_id},')
        ids = ','.join(ids)
        favorites_spells.objects.filter(user_id=request.user.id).update(spell_id= ids)
    else:   
      favorites_spells.objects.create(user_id=request.user.id,spell_id =f'{spell_id},')           
    return redirect(request.META.get('HTTP_REFERER'))



def favorite_feat(request,feat_id):
    if not request.user.is_authenticated:
      return redirect('login')    
    if   favorites_feats.objects.filter(user_id=request.user.id):
      user = favorites_feats.objects.filter(user_id=request.user.id).first()
      ids = str(user.feat_id).split(',')[:-1]    
      if feat_id in ids:       
       ids.remove(feat_id) 
       if len(ids) > 0:   
        ids = ','.join(ids)
        ids = ids + ','  
       else:
         ids = ''  
       favorites_feats.objects.filter(user_id=request.user.id).update(feat_id= ids)
      else:
        ids.append(f'{feat_id},')
        ids = ','.join(ids)
        favorites_feats.objects.filter(user_id=request.user.id).update(feat_id= ids)

          
    return redirect(request.META.get('HTTP_REFERER'))

def favorites(request):
  fav_spell = []
  fav_feat = []
  spells = favorites_spells.objects.get(user_id=request.user.id)
  spell = spells.spell_id.split(',')[:-1]
  for i in spell:
    fav_spell.append(Spells.objects.get(id = i))
  feats =  favorites_feats.objects.get(user_id=request.user.id)
  feat = feats.feat_id.split(',')[:-1]
  for i in feat:
    fav_feat.append(Feats.objects.get(id = i))  
  context = {'fav_spells':fav_spell,'fav_feats':fav_feat}
  return render(request,'main/favorites.html', context)





resulten = []
def enhancements(request):
  global resulten
  handbooks = Magic_Enhancement.objects.values('book').distinct().order_by('book')
  handbook= []
  for i in handbooks:          
    handbook.append(i.popitem()[1])
  if request.method == 'GET':
    class_paginator = Paginator(resulten,20)    
    try:
       pag_num = request.GET['page']
    except:         
       return render(request, "main/enhancements.html",{'handbooks' : handbook})
  else:   
    try : 
      enhance_name = request.POST['name']  
    except:   
      return render(request, 'main/enhancements.html')
    if request.POST.get('property_select') == 'bonus':
      resulten = Magic_Enhancement.objects.filter(name__contains = request.POST['name'] ,price__contains = request.POST['bonus'], slot__contains=request.POST['equip'], book__contains=request.POST['book'])
    else:
      resulten = Magic_Enhancement.objects.filter(name__contains = request.POST['name'] ,absolute_price__gte= request.POST['value_min'], absolute_price__lte=request.POST['value_max'] , slot__contains=request.POST['equip'], book__contains=request.POST['book'])      
    class_paginator = Paginator(resulten,20)
    pag_num = request.POST.get('page') 
  page = class_paginator.get_page(pag_num)
  context = {'pag' : page, 'method' : request.method, 'handbooks': handbook}
  return render(request, 'main/enhancements.html', context)


def enhancement(request,enhancement_name:str):
  if '(+' in enhancement_name:
    enhancement_name = enhancement_name[:-5]
  enhancement = Magic_Enhancement.objects.filter(name = enhancement_name).first()
  requirement = enhancement.requirements.split(',')
  return render(request, 'main/enhancement.html', {'enhance' : enhancement,'require' : requirement})

def define_type(request,name:str): 
  value = Feats.objects.filter(name = name.strip()).first()
  if value == None:
    value = Spells.objects.filter(name = name.strip()).first()
    if value == None:
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    return spell(request, value.id)
  return feat(request,value.id) 


def google_verif(request):
  return render(request ,"main/googlea135415e434a0e29.html")
