
from django import forms
from .models import Handbooks,Classes,Races,Items,Feats,Spells,favorites_spells,Race,Magic_Enhancement


class Entryhb(forms.ModelForm):
  class Meta:
    model = Handbooks
    fields = ['text','link','category','edition']
    labels = {'text' : 'Handbook'}

class EntryClasses(forms.ModelForm):
  class Meta:
    model = Classes  
    fields = ['text','link', 'handbook']
    labels = {'text' : 'Class Name', 'link' : 'Link','handbook' : 'Source Book' }

class EntryRaces(forms.ModelForm):
  class Meta :
    model = Races 
    fields = ['text','link','handbook']
    labels = {'text' : 'Race', 'link' : 'Link', 'handbook' : 'Source Book'}

class EntryItems(forms.ModelForm):
  class Meta:
    model = Items
    fields = ['text','link','handbook','slot','family','price']
    labels = {'text' : 'Item', 'link' : 'Link','price' : 'Price (In GP)', 'handbook' : 'Source Book', 'family':'Type', 'slot':'Slot'}

class EntryFeat(forms.ModelForm):
  class Meta:
    model = Feats
    fields = ['name','handbook','shortdescript','type','version','page','requisite','required','description','special']
    labels  ={'name' : 'Feat Name','version':'Edition','page':'Page','type' : 'Category','handbook' : 'Source Book','requisite' : 'Pré Requisites','required' : 'Required For','description' : 'Feat Benefit','special':'Special'}
    widgets = {'Benefit' : forms.Textarea(attrs={'cols': 150}),'Special' : forms.Textarea(attrs={'cols': 150})}

  
class EntrySpells(forms.ModelForm):
  class Meta:
    model = Spells
    fields = ['name','handbook','category','area','school','components','casting_time','range','duration','save_throw','Edition','descript']
    widgets = {'descript' : forms.Textarea(attrs={'cols': 150})}

class FavoriteSpells(forms.ModelForm):
  class Meta:
    model = favorites_spells
    fields=['spell_id','user']

class EntryRaces(forms.ModelForm):
  class Meta:
    model = Race
    fields = ['Race','Size', 'Speed',  'Space', 'Reach','level_adjstument','weapons', 'Languages', 'traits', 'description']
    labels = {'Speed' : 'Base Speed (FT)','Space' : 'Space (FT)', 'Reach' : 'Reach (FT)', 'level_adjstument' : 'Level Adjustment', 'traits' : 'Racial Traits','weapons' : 'Weapons Proficiency', 'description' : 'Description'}    

class EntryEnhancement(forms.ModelForm):
  class Meta:
    model = Magic_Enhancement
    fields = ['name','price','slot','book','caster_level']
    labels = {'name' : 'Enhancement Name','price' : 'Price', 'slot' : 'Equipment', 'book' : 'Handbook', 'caster_level' : 'Caster Level'}    

