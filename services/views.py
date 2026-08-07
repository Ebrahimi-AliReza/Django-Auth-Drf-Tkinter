from django.shortcuts import render,get_object_or_404
#from django.shortcuts import render,get_object_or_404
from .models import *
from django.views.generic import ListView,DetailView
from accounts.models import User


class ServicesView(ListView):
    model=Services
    template_name='services/services.html'
    context_object_name='services'
    
    def get_queryset(self):
        if self.request.GET.get('search'):
            services=Services.objects.filter(description__contains=self.request.GET.get('search'))
        elif self.kwargs.get('category'):
            services=Services.objects.filter(category__name=self.kwargs.get('category'))
        elif self.kwargs.get('tag'):
            services=Services.objects.filter(tags__title=self.kwargs.get('tag'))
        
        else:
             services=Services.objects.all()
        return services
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['user']=User.objects.get(email='admin@admin.com')
        return context
        

# def services(request,*args,**kwargs):
#     if kwargs.get('category'):
#         services=Services.objects.filter(category__name=kwargs.get('category'))
#     elif kwargs.get('tag'):
#         services=Services.objects.filter(tags__title=kwargs.get('tag'))
#     elif request.GET.get('search'):
#         services=Services.objects.filter(description__contains=request.GET.get('search'))
#     else:
#         services=Services.objects.filter()
#     #
#     context={
#         'services':services
#     }
#     return render(request,"services/services.html",context)

class ServiceDetailView(DetailView):
    model = Services
    template_name='services/service-details.html'
    context_object_name='service'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['user']=User.objects.get(email='admin@admin.com')
        return context







# def services_detail(request,id):
#     # id=request.GET.get('id') 
#     # try:
#     #     service=Services.objects.get(id=id)
#     # except:
#     #     return render(request,"services/404.html")
#     service=get_object_or_404(Services,id=id)
#     #id=request.GET.get('id')
#     #service=get_object_or_404(Services,id=id)
#     context={"service":service}
#     return render(request,"services/service-details.html",context)

# Create your views here.
