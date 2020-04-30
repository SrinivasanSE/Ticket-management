from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('home/', views.home, name='home'),
    path('customer/register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('customer/home', views.TicketCreateView.as_view(), name='customerhome'),
    path('customer/query', views.customer_query, name='customerquery'),
    path('webadmin/', views.admin, name='admin'),
    path('webadmin/assign/<int:ticket_id>/', views.ticket_assign, name='ticketassign'),
    path('webadmin/ticket/', views.admin_ticket, name='admin_ticket'),
    path('technician/', views.technicia, name='technician'),
    path('technician/resolve/<int:ticket_id>/', views.resolve, name='resolve'),
    path('error/', views.error, name='error'),
    path('technician/signup', views.technician_register, name='technician_signup')
]
