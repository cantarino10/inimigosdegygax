from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from main.api import viewset as featviewset

route = routers.DefaultRouter()

route.register(r'feats',featviewset.FeatsViewSet, basename= 'Feat')




urlpatterns = [

    path('', views.index, name='index'),
    path('handbooks', views.handbooks, name='handbooks'),
    path('handbook/<book>', views.handbook, name='handbook'),
    path('races', views.races, name='races'),
    path('classes', views.classes, name='classes'),
    path('classes/<classe>', views.classes, name='classe'),
    path('class_filter/<classe>',views.class_filter,name='class_filter'),
    path('items', views.items, name='items'),
    path('register_books',views.register_books, name='register_books'),
    path('register_classes',views.register_classes,name='register_classes'),
    path('register_races',views.register_races,name='register_races'),
    path('register_items',views.register_items,name='register_items'),
    path('feats', views.feats,name='feats'),
    path('api/', include(route.urls),name = 'apis'),
    path('feat/<feat_id>',views.feat,name='feat'),
    path('callfeat/<feat_name>',views.callfeat,name='call_feat'),
    path('register_feats',views.register_feats,name='register_feats'),
    path('spells',views.spells,name='spells'),
    path('spells/<spells_name>',views.spells,name='spells'),
    path('spell/<spell_id>',views.spell,name='spell'),    
    path('register_spells',views.register_spells,name='register_spells'),
    path('favorite_spell/<spell_id>',views.favorite_spell, name='favorite_spell'),
    path('favorite_feat/<feat_id>',views.favorite_feat, name='favorite_feat'),
    path('favorites/',views.favorites, name='favorites'),
    path('favorites/',views.favorites, name='favorites'),
    path('enhancements/',views.enhancements, name='enhancements'),
    path('enhancement/<enhancement_name>',views.enhancement, name='enhancement'),
    path('define_type/<name>',views.define_type, name='define'),
    path('googlea135415e434a0e29.html',views.google_verif, name='google_verif'),
    path('token/',TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
 


  
]

