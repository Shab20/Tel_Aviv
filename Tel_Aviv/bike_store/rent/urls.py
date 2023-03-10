from django.urls import path
from . import views
from .views import hello_world, rental_list_view, RentalListView, RentalDetailView, CustomerDetailView, VehicleDetailView, return_vehicle, RentalCreateView, CustomerDetailView, RentalDetailView, CustomerCreateView, VehicleListView, VehicleDetailView, VehicleCreateView, RentalUpdateView, CustomerUpdateView, VehicleUpdateView, RentalDeleteView, CustomerDeleteView, VehicleDeleteView

app_name = 'rental'

urlpatterns = [
    path('', hello_world),
    path('rental/', views.RentalListView.as_view(), name='rental_list'),
    path('rentals/', rental_list_view, name='rental_list'),
    path('rental/<int:pk>/', views.RentalDetailView.as_view(), name='rental_detail'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('vehicles/<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
    path('rentals/<int:pk>/return/', return_vehicle, name='return-vehicle'),
    path('rentals/add/', RentalCreateView.as_view(), name='rental-create'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('rentals/<int:pk>/', RentalDetailView.as_view(), name='rental-detail'),
    path('customers/add/', CustomerCreateView.as_view(), name='customer-create'),
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicles/<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
    path('vehicles/add/', VehicleCreateView.as_view(), name='vehicle-create'),
    path('rentals/<int:pk>/edit/', RentalUpdateView.as_view(), name='rental-update'),
    path('customers/<int:pk>/edit/', CustomerUpdateView.as_view(), name='customer-update'),
    path('vehicles/<int:pk>/edit/', VehicleUpdateView.as_view(), name='vehicle-update'),
    path('rentals/<int:pk>/delete/', RentalDeleteView.as_view(), name='rental-delete'),
    path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer-delete'),
    path('vehicles/<int:pk>/delete/', VehicleDeleteView.as_view(), name='vehicle-delete'),
]