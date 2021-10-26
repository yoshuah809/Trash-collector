from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Employee
# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

def index(request):
    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        today = date.today()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        Customer = apps.get_model('customers.Customer')
        all_customers = Customer.objects.all()
        customers_in_zipcode =  all_customers.filter(zip_code = logged_in_employee.zip_code)
        customers_pickup_day = customers_in_zipcode.filter(Q(weekly_pickup = days[date.weekday(today)]) | Q(one_time_pickup = today))
        customers_not_suspended = customers_pickup_day.exclude(Q(suspend_start__lt=today) & Q(suspend_end__gt=today))
        customers_need_pickup = customers_not_suspended.exclude(date_of_last_pickup = today)


        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'customers_need_pickup' : customers_need_pickup
        }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))

# def index(request):
#     # This line will get the Customer model from the other app, it can now be used to query the db for Customers
#     Customer = apps.get_model('customers.Customer')

#     return render(request, 'employees/index.html')

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user, zip_code=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        zip_from_form = request.POST.get('zip_code')
        logged_in_employee.name = name_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)

def all_customers(request):
    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        Customer = apps.get_model('customers.Customer')
        all_customers = Customer.objects.all()

        context = {
            'logged_in_employee': logged_in_employee,
            'all_customers' : all_customers,
        }
        return render(request, 'employees/all_customers.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))