from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.create, name="create"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('all_customers/', views.all_customers, name="all_customers"),
    path('confirm_pickup/<int:customer_id>/', views.confirm_pickup, name="confirm_pickup"),
    path('filter_by_day/<int:id>/', views.filter_by_day, name="filter_by_day"),
]