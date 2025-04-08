from django.http import HttpResponseRedirect
from django.urls import reverse


def super_user(function):

  def wrap(request,*args,**kwargs):
 
   if not request.user.is_superuser:
    return HttpResponseRedirect(reverse('index'))
   return function(request,*args,**kwargs)

  return wrap


