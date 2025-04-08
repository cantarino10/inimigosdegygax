
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm,PasswordResetForm
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField

from django.core.exceptions import ValidationError   # importa do django para mostrar erros de validação
User = get_user_model()

class Loginform(forms.Form):

  username = forms.CharField(max_length=30)   #cria um campo com o nome login
  password = forms.CharField(max_length=20, widget=forms.PasswordInput()) #Cria o campo com o nome password , widget indica que o campo é uma senha e oculta

  
  def clean_login(self):

    name = self.cleaned_data['username']    #registra o campo login em name
     
    if not (name.isalnum()) :
        raise ValidationError("O nome de usuário não pode ter caracter especaa")          #validation serve para retornar o motivo do erro
    else:
       raise ValidationError("asd") 
    #return name

class UserRegistrationFormm(UserCreationForm):
   email = forms.EmailField(help_text='A valid email addres', required=True)
   captcha = CaptchaField()
   class Meta:
      model = get_user_model()
      fields =['username','password1','password2', 'email']
      def save(self, commit=True):
         user = super(UserRegistrationFormm, self).save(commit=False)
         user.email = self.cleaned_data['email']
         if commit:
            user.save()
         return user   

class SetPasswordForm(SetPasswordForm):
   class Meta:
      model = get_user_model()
      fields = ['new_password1','new_password2']      

class PasswordResetForm(PasswordResetForm):
   def __init__(self, *args, **kwargs):
      super(PasswordResetForm, self).__init__(*args, *kwargs)

