from django.shortcuts import render,redirect

# Create your views here.
from django.shortcuts import render
from .models import Service

def service_list(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'services': services})
from .forms import ServiceForm

def add_service(request):
    form = ServiceForm()

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)  # 🔥 IMPORTANT
        if form.is_valid():
            form.save()
            return redirect('service_list')

    return render(request, 'add_service.html', {'form': form})
def edit_service(request, id):
    service = Service.objects.get(id=id)
    form = ServiceForm(instance=service)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)  # 🔥 IMPORTANT
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')

    return render(request, 'edit_service.html', {'form': form, 'service': service})
def delete_service(request, id):
    service = Service.objects.get(id=id)
    service.delete()
    return redirect('admin_dashboard')