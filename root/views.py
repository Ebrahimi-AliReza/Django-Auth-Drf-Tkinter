from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Contact, Skills,Agent,Testimonial
from services.models import Services
from .forms import ContactUsForm
from django.contrib import messages
from django.views.generic import TemplateView,RedirectView




# context={
#     'name':'Alireza',
#     'family':'Ebrahimi',
#     'phone':'09388091057',
#     "adress":'Arak Gerdoo Street'
# }

def home(request):
    # skills = Skills.objects.all()
    # print(skills)
    # for obj in skills:
    #     print(obj.title,obj.rating)
    # context = {'skills':skills}
    
    agents=Agent.objects.filter(status=True).order_by("?")[:3]
    services=Services.objects.all().order_by('?')[:3]
    testimonials=Testimonial.objects.filter(status=True)
    context={'agents':agents,
             'testimonials':testimonials,
             'services':services
             
             }
    return render(request, "root/index.html",context=context)

# def about(request):
#    return render(request, "root/about.html")
class AboutView(TemplateView):
    template_name= 'root/about.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['test']=  +989388091057
        return context
class Soft98(RedirectView):
    url='https://soft98.ir'

def contact(request):
        if request.method=="GET":
            return render(request, "root/contact.html")
        elif request.method == 'POST':
            form = ContactUsForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your message has been sent successfully!')
                return redirect(request.path_info)  # Redirect to the same page after successful submission      
            else:
                messages.error(request, 'There was an error sending your message. Please try again.')
                return redirect(request.path_info)
        
            # name=request.POST.get('name')
            # email=request.POST.get('email')
            # subject=request.POST.get('subject')
            # message=request.POST.get('message')
            # contact=Contact(name=name,email=email,subject=subject,message=message)
            # contact.save()
            # print(name,email,subject,message)
            # print(request.POST.get('name'))
            # print(request.POST.get('email'))
            # print(request.POST.get('subject'))
            # print(request.POST.get('message'))
            # return render(request, "root/contact.html")



def agents(request):
    agents=Agent.objects.filter(status=1)
    context = {'agents':agents}
    return render(request,'root/agents.html',context=context)

