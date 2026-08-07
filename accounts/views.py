from django.shortcuts import render,redirect
from .forms import loginForm, registerForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import User
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from django.views.generic import FormView
from django.views.generic import FormView
from django.views.generic.edit import CreateView 

class Login_view(FormView):
    form_class=loginForm
    template_name='accounts/login.html'
    success_url='/'
    def form_valid(self,form):
        email=self.request.POST.get('email')
        password=self.request.POST.get('password')
        try:
            user=User.objects.get(email=email)
        except:
            messages.error(self.request, 'Invalid Email')
            return redirect('accounts:login')
        email=user.email
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            print(self.request.user)
            print(email)
            print(password)
            return redirect('root:home')
        else:
            messages.error(self.request, 'Invalid Email or password')
            return redirect('accounts:login')
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid  input (Email or password)')
        return super().form_invalid(form)

# def login_view(request):
#     if request.method == 'GET':
#         return render(request, 'accounts/login.html')
#     else:
#         form = loginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             try:
#                 user=User.objects.get(email=email)
#             except:
#                 messages.error(request, 'Invalid phone number')
#                 return redirect('accounts:login')
#             email=user.email
               
#             user = authenticate(request, username=email, password=password)
#             print(user)
#             print(email)
#             print(password)
#             if user is not None:
#                 login(request, user)
#                 print(request.user)
#                 return redirect('root:home')
#             else:
#                 messages.error(request, 'Invalid username or password')
#                 return redirect('accounts:login')
#         else:
#             messages.error(request, 'Invalid form submission')
#             return redirect('accounts:login')   

class Regester_view(CreateView):
        template_name = 'accounts/register.html'
        form_class = registerForm
        success_url = '/accounts/login/'
        def form_valid(self, form):
            form.save()
            messages.success(self.request, 'Account created successfully')
            return super().form_valid(form)

        def form_invalid(self, form):
            messages.error(self.request, 'Invalid input submission')
            return super().form_invalid(form)
     
    

def register_view(request):
    if request.method == 'GET':
        return render(request, 'accounts/register.html')
    else:
        form = registerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('accounts:login')

        else:
            messages.error(request, 'Invalid input submission')
            return redirect(request.path_info)  # Redirect to the same page if the form is invalid

@login_required
def logout_view(request):
    print(request.user)
    logout(request) 
    print(request.user)
    return redirect('root:home')



@login_required
def change_password(request):
    if request.method=='GET':
        return render(request,'accounts/change-pass.html')
    else:
        form=changepasswordForm(request.POST)
        if form.is_valid():
            current_password=form.cleaned_data['current_password']
            password1=form.cleaned_data['password1']
            password2=form.cleaned_data['password2']
        
            if(request.user.check_password(current_password))and (password1==password2)and not(request.user.check_password(password1)):
                try :
                    password_validation.validate_password(password1)
                    user=request.user
                    user.set_password(password1)
                    user.save()
                    login(request,user)
                    messages.success(request,'password change successfully')
                    return redirect(request.path_info
                                    )
                except ValidationError as e :
                    for message in e.messages:
                        message.error(request,message)
                        return redirect(request.path_info)
            else:
                messages.error(request,'pass1 =! pass2 & newpass =! oldpass & oldpass is incurrent')
                return redirect(request.path_info)    
        else:
             messages.error(request,'input current entry in fields(validate data)')
             return redirect(request.path_info)   
                
                
                
def reset_password(request):
    if request.method == 'GET':
        return render(request,'accounts/reset-password.html')
    else:
        form=ResetPasswordForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            user=User.objects.get(email=email)
            token , create =Token.objects.get_or_create(user=user)
            print(token,create)
            send_mail(
                'reset-password',
                f'http://127.0.0.1:8000/accounts/reset-password-confirm/{token.key}',
                'alireza.ebrahimi',
                [user.email],
                fail_silently=True  
            )
            return redirect('accounts:reset-password-done')
        
            

def reset_password_done(request):
    return render(request,'accounts/reset-password-done.html')

def reset_password_confirm(request,token):
    if request.method == 'GET':
        return render(request, 'accounts/reset-password-confirm.html')
    else:
        form=ResetPasswordForm(request.POST)
        if form.is_valid():
            password1=form.cleaned_data['password1']
            password2=form.cleaned_data['password2']
            user=Token.objects.get(key=token).user
            if(password1==password2)and not(user.check_password(password1)):
                try :
                    password_validation.validate_password(password1)
                    user.set_password(password1)
                    user.save()
                    return redirect('accounts:reset-password-complete')
                
                                   
                except ValidationError as e :
                    for message in e.messages:
                        message.error(request,message)
                        return redirect(request.path_info)
            else:
                messages.error(request,'pass1 =! pass2 ')
                return redirect(request.path_info)    
        else:
            messages.error(request,'input current entry in fields(validate data)')
            return redirect(request.path_info)  
        

def reset_password_complete(request):
   return render(request, 'accounts/reset-password-complete.html')