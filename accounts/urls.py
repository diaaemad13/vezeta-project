from django.urls import path
from . import views
from .views import *
app_name = 'accounts'


app_name = 'accounts'
urlpatterns = [
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('login/', views.user_login, name='login'),
    path('myprofile/', views.my_profile, name='myprofile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('signup/', views.signup, name='signup'),
    path('<slug:slug>/', views.doctors_detail, name='doctors_detail'),
#################################################################################
    path('api/doctors/', DoctorListView.as_view(), name='doctor_list_api'),
    path('api/doctors/<slug:slug>/', DoctorDetailView.as_view(), name='doctors_detail_api'),
    path('api/login/', user_login_api, name='login_api'),
    path('api/myprofile/', my_profile_api, name='myprofile_api'),
    path('api/update_profile/', update_profile_api, name='update_profile_api'),
    path('api/signup/', SignupView.as_view(), name='signup_api'),
]



