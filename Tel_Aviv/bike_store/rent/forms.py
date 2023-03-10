from django import forms
from django.shortcuts import render
from .forms import CustomerForm

class RentalForm(forms.Form):
    customer_id = forms.IntegerField()
    vehicle_id = forms.IntegerField()

def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to success page or return success response
    else:
        form = CustomerForm()
    return render(request, 'customer_form.html', {'form': form})
