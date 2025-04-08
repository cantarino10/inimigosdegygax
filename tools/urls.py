from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   
    path('roll_dice',views.roll_dice, name='roll_dice'),
    path('stats_builder',views.stats_builder, name='stats_builder'),
    path('char_builder',views.char_builder, name='char_builder'),
    path('encounter_calculate',views.encounter_calculate, name='encounter'),
    path('item_randomize',views.item_randomize,name='item_randomize'),
    path('item_randomize',views.item_randomize,name='item_randomize'),

    
]
