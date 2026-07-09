from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('hospital/', views.hospital_dashboard, name='hospital_dashboard'),
    path('bloodbank/', views.bloodbank_dashboard, name='bloodbank_dashboard'),
    path('donor/', views.donor_dashboard, name='donor_dashboard'),
    path('board/', views.request_board, name='request_board'),
    path('fulfill/<int:request_id>/', views.fulfill_request, name='fulfill_request'),
]
path('donor-respond/<int:request_id>/', views.donor_respond, name='donor_respond'),