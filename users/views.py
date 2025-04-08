from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,logout,get_user_model,login    #esse metodo verifica se o usuario existe e bate com a senha
from django.contrib.auth import login as auth_login  #metodo para abrir uma sessão para o usuário
from django.contrib.auth.forms import UserCreationForm  #importa o formulario de ciração de usuarios
from .forms import Loginform,UserRegistrationFormm,SetPasswordForm,PasswordResetForm
from main.models import favorites_feats,favorites_spells
from .tokens import account_activation_token

def activate(request,uidb64, token):
  User = get_user_model()
  try:
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
  except:
    user = None

  if user is not None and  account_activation_token.check_token(user, token):    
    user.is_active= True
    user.save()
    messages.success(request, "Thanks for being another Gygax enemy, now you can login",extra_tags='safe')

    return redirect('login')
  else:
    messages.error(request,"Activation link is invalid",extra_tags='safe')
  return redirect('index')

def activateEmail(request,user,to_email):
  mail_subject = "Activate your user account"
  message = render_to_string("users/template_activate_account.html",{
    'user': user.username,
    'domain' : get_current_site(request).domain,
    'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
    'token':account_activation_token.make_token(user),
    'protocol' : 'https' if request.is_secure() else 'http'
  })
  email = EmailMessage(mail_subject,message,to=[to_email])
 
  if email.send():
    messages.success(request, f'Dear <b>{user}</b>, a confirmation has been sent to your email, please click on activion link to activate your account. <b> Check your spam folder also</b>',extra_tags= 'safe')
  else:
    messages.error(request, f'Problem sending email to{to_email}, check if its correct',extra_tags='safe')  

def login(request):
  if request.user.is_authenticated:
    return HttpResponseRedirect(reverse('index'))
  error = False
  if request.method != 'POST':    #Verifica se o metodo é posto
    form = Loginform()    #Caso seja retorna o formulario em branco
  else:
    form = Loginform(data=request.POST)  
    if form.is_valid():    #Verifica se os dados são validos
      username = request.POST.get('username')   #pega o campo de POST que possui os dados de username
      password = request.POST.get('password')
      user = authenticate(username=username,password=password)    # compara usuario com senha
      if user:
        auth_login(request, user)
        return HttpResponseRedirect(reverse('index'))   #redireciona para a pagina principal 
      else:
       
        for error in list(form.errors.values()):
          messages.error(request, error)
        error = True
  context = {'form' : form, 'error': error}       #armazena o formulario em context
  return render(request, 'users/login.html', context)  #retorna pra pagina com o context

@login_required
def logout_view(request):
  logout(request)
  messages.info(request,'Logged out sucessfully')

  return HttpResponseRedirect(reverse('index'))

def register(request) :  #cadastrar novo usuário
  if request.user.is_authenticated:
    return HttpResponseRedirect(reverse('index'))
  if request.method != 'POST': #Exibe o formulário de cadastro em branco
    form = UserRegistrationFormm()
  else: #processa se o formulário foi preenchido
    form = UserRegistrationFormm(data=request.POST)
    if form.is_valid():
      new_user = form.save(commit=False)
    
      new_user.is_active = False
      new_user.email = request.POST.get('email')
      new_user.save()
      favorites_feats.objects.create(user_id=new_user.id) 
      favorites_spells.objects.create(user_id=new_user.id) 
      activateEmail(request, new_user, form.cleaned_data.get('email'))     
      return HttpResponseRedirect(reverse('index'))
    
  context = {'form' : form}  
  return render(request, 'users/register.html', context)

@login_required
def password_change(request):
  user = request.user
  if request.method == 'POST':
    form = SetPasswordForm(user, request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, "Your paassword has been changed",extra_tags='safe')
      return redirect('login')
    else:
      for error in list(form.errors.values()):
        messages.error(request, error)
  form = SetPasswordForm(user)      
  return render(request, 'users/password_reset_confirm.html', {'form': form})
    
def password_reset(request):

 if request.method == 'POST':
  form = PasswordResetForm(request.POST)


  if form.is_valid():
    user_email = form.cleaned_data['email']
    associated_user = get_user_model().objects.filter(Q(email=user_email)).first()

    if associated_user:
    
      subject ="Password Reset Quest"
      message = render_to_string("users/template_reset_password.html",{
        'user': associated_user,
        'domain' : get_current_site(request).domain,
        'uid' : urlsafe_base64_encode(force_bytes(associated_user.pk)),
        'token':account_activation_token.make_token(associated_user),
        'protocol' : 'https' if request.is_secure() else 'http'
      })
      email = EmailMessage(subject,message,to=[user_email])

      if email.send():
        messages.success(request,
                      """
                      <h2 style='color : white'>Password reset sent</h2><hr> 
                      <p style='color : white'>
                        We've emailed you instructions for setting your password if an account exists with the email you entered.
                        You should receive them shortly,<br>If you don't receive an email, please make sure you've entered the address correctly
                        and check your spam folder.
                      </p>
                        
                      """,extra_tags='safe')
      else:
        messages.error(request, "Problem Sending your password <b>SERVER PROBLEM</b>",extra_tags='safe')
    else:
          messages.error(request, "Couldn't find an account associated with this email",extra_tags='safe')
  return redirect('password_reset')  
     
 form = PasswordResetForm()   
 return render(
   request=request,
   template_name='users/password_reset.html',
   context={'form': form}
 )

def password_reset_confirm(request, uidb64, token):
  User = get_user_model()
  try:
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
  except:
    user = None

  if user is not None and  account_activation_token.check_token(user, token):    
    if request.method == 'POST':
      form = SetPasswordForm(user, request.POST)
      if form.is_valid():
     
        form.save()
        messages.success(request, "You password has been reset. You may now go an <b>log in </b>",extra_tags='safe')
        return redirect('login')
      else: 
        for error in list(form.errors.values())  :
          messages.error(request, error)
    form = SetPasswordForm(user)      
    return render(request, 'users/password_reset_confirm.html', {'form' : form})
  else:
    messages.error(request,"Link is expired")

  messages.error(request, 'Something went wrong, redirecting back to Homepage',extra_tags='safe')  
  return redirect('index')


