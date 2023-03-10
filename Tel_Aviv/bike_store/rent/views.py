from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import RentalForm, CustomerForm, VehicleForm
from .models import Customer, Vehicle, Rental, VehicleType, VehicleSize, RentalRate
from itertools import groupby
from django.utils import timezone
from django import forms
from django.http import HttpResponse

def hello_world (request):
    return HttpResponse ('Hello Arnold')

class RentalListView(ListView):
    model = Rental
    queryset = Rental.objects.order_by('return_date', 'rental_date')
    template_name = 'rental/rental_list.html'

    def get(self, request, *args, **kwargs):
        rental_list = self.get_queryset()
        context = {'rental_list': rental_list}
        return render(request, self.template_name, context)

class RentalDetailView(DetailView):
    model = Rental
    template_name = 'rental/rental_detail.html'

class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'vehicle/vehicle_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rentals = self.object.rentals.order_by('-rental_date')
        rental_status = 'Not yet returned'
        if rentals.filter(return_date__isnull=False).exists():
            last_returned_rental = rentals.filter(return_date__isnull=False).first()
            rental_status = f'Returned on: {last_returned_rental.return_date}'
        context['rentals'] = rentals
        context['rental_status'] = rental_status
        return context

class RentalCreateView(View):
    def get(self, request):
        form = RentalForm()
        return render(request, 'rental/rental_form.html', {'form': form})

    def post(self, request):
        form = RentalForm(request.POST)
        if form.is_valid():
            customer_id = form.cleaned_data['customer_id']
            vehicle_id = form.cleaned_data['vehicle_id']
            customer = get_object_or_404(Customer, pk=customer_id)
            vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
            if vehicle.is_rented():
                error_msg = f'The vehicle {vehicle} is already rented.'
                return render(request, 'rental/rental_form.html', {'form': form, 'error_msg': error_msg})
            rental = Rental.objects.create(customer=customer, vehicle=vehicle)
            return redirect('rental_detail', pk=rental.pk)
        else:
            return render(request, 'rental/rental_form.html', {'form': form})

class RentalAddView(View):
    def get(self, request):
        customers = Customer.objects.all()
        vehicles = Vehicle.objects.filter(rental__isnull=True)
        context = {'customers': customers, 'vehicles': vehicles}
        return render(request, 'rental/rental_add.html', context)

    def post(self, request):
        customer_id = request.POST.get('customer_id')
        vehicle_id = request.POST.get('vehicle_id')
        if not customer_id or not vehicle_id:
            error_message = "Please select both a customer and a vehicle."
            return render(request, 'rental/rental_add.html', {'error_message': error_message})

        customer = get_object_or_404(Customer, pk=customer_id)
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)

        if vehicle.is_rented():
            error_message = f"{vehicle} is currently being rented and is not available."
            return render(request, 'rental/rental_add.html', {'error_message': error_message})

        rental = Rental.objects.create(customer=customer, vehicle=vehicle)
        return redirect('rental_detail', pk=rental.pk)

class CustomerDetailView(View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        return render(request, 'rental/customer_detail.html', {'customer': customer})
    
class CustomerListView(View):
    def get(self, request):
        customers = Customer.objects.all().order_by('name')
        return render(request, 'rental/customer_list.html', {'customers': customers})

class CustomerCreateView(View):
    def get(self, request):
        form = CustomerForm()
        return render(request, 'rental/customer_form.html', {'form': form})

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return redirect('customer_detail', pk=customer.pk)
        else:
            return render(request, 'rental/customer_form.html', {'form': form})
        
def vehicle_list(request):
    vehicles = Vehicle.objects.order_by('vehicle_type__name')
    grouped_vehicles = {}
    for key, group in groupby(vehicles, lambda x: x.vehicle_type.name):
        grouped_vehicles[key] = list(group)

    return render(request, 'rental/vehicle_list.html', {'grouped_vehicles': grouped_vehicles})

def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    active_rentals = Rental.objects.filter(vehicle=vehicle, return_date__isnull=True)
    rental_status = "Available"
    if active_rentals:
        rental_status = f"Rented until {active_rentals[0].return_date.strftime('%m/%d/%Y')}"

    return render(request, 'rental/vehicle_detail.html', {'vehicle': vehicle, 'rental_status': rental_status})

def vehicle_add(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm()

    return render(request, 'rental/vehicle_add.html', {'form': form})

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ('name', 'vehicle_type', 'size', 'real_cost')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle_type'].queryset = VehicleType.objects.all()
        self.fields['size'].queryset = VehicleSize.objects.all()
