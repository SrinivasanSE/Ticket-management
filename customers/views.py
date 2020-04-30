from django.shortcuts import render, redirect
from administer.admin import UserCreationForm
from django.contrib import messages
from administer.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import LoginForm
from .decorators import admin_login_required, customer_login_required, technician_login_required
from administer.models import Ticket
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate,login
from customermanagement.settings import EMAIL_HOST_USER

from django.core.mail import send_mail
"""Signup form"""


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            subject="Successfully Created Account"
            message="Thankyou for registering!. Hope You have a Good Experience"
            send_mail(subject, message, EMAIL_HOST_USER, [email], fail_silently=False)
            messages.success(request, f'Account created for {username}! Now you can login')
            user = form.save()
            user.is_customer = True
            user.save()
            print(user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'customers/register.html', {'form': form})


@admin_login_required
def technician_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = form.save()
            user.is_technician = True
            user.save()
            print(user)
            return redirect('admin')
    else:
        form = UserCreationForm()
    return render(request, 'customers/register.html', {'form': form})


"""Login form"""

"""
class CustomLoginView(SuccessMessageMixin, LoginView):
    success_message = "You were successfully logged in"
    template_name = 'customers/login.html'

    def get_success_url(self):
        user = User.objects.get(username=self.request.user)
        if user.is_customer:
            return '/customer/home'
        elif user.is_technician:
            return '/technician/'
        else:
            return '/webadmin/'
"""


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(
                        0)  # <-- Here if the remember me is False, that is why expiry is set to 0 seconds. So it will automatically close the session after the browser is closed.
                # else browser session will be as long as the session  cookie time "SESSION_COOKIE_AGE"
                if user.is_customer:
                    return redirect('home')
                elif user.is_technician:
                    return redirect('technician')
                else:
                    return redirect('admin')
            else:
                return render(request, 'customers/login.html', {'form': form,'error':'Username or Password is Incorrect.Both are Case_sensitve'})
    else:
        form = LoginForm()
    return render(request, 'customers/login.html', {'form': form})


"""admin"""


@admin_login_required
def admin(request):
    technicians = User.objects.filter(is_technician=True)
    tickets = Ticket.objects.all()
    length = len(list(tickets))
    return render(request, 'customers/admin.html', {'tickets': tickets, 'technicians': technicians, 'length': length})


@admin_login_required
def ticket_assign(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    try:
        ticket.technician = request.POST['tech']  # technician name from form
    except:
        technicians = User.objects.filter(is_technician=True)
        return render(request, 'customers/admin.html', {'tickets': Ticket.objects.all(), 'technicians': technicians,
                                                        'error': 'You did not select a choice'})
    else:
        ticket.status = "Technician assigned"
        ticket.save()
        return redirect('admin')


@admin_login_required
def admin_ticket(request):
    customers = User.objects.filter(is_customer=True)
    technicians = User.objects.filter(is_technician=True)
    if request.method == "POST":
        try:
            customer = User.objects.get(username=request.POST['dropdown'])
        except:
            return render(request, 'customers/admin_ticket.html',
                          {'technicians': technicians, 'customers': customers, 'error': 'Customername Not Entered'})
        else:
            try:
                customer.ticket_set.create(content=request.POST['content'], technician=request.POST['tech'],
                                           status='Technician assigned')
            except:
                return render(request, 'customers/admin_ticket.html',
                              {'technicians': technicians, 'customers': customers, 'error': 'Technician not selected'})
            else:
                return redirect('admin')
    return render(request, 'customers/admin_ticket.html', {'technicians': technicians, 'customers': customers})


"""customers"""


class TicketCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Ticket
    fields = ['content']
    template_name = 'customers/customer.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return '/customer/query'

    def test_func(self):
        if self.request.user.is_customer:
            return True
        return False


@customer_login_required
def customer_query(request):
    Tickets = Ticket.objects.filter(user_id=request.user.id)
    length = len(Tickets)
    return render(request, 'customers/customerqueries.html', {'Tickets': Tickets, 'length': length})


"""technician"""


@technician_login_required
def technicia(request):
    Tickets = Ticket.objects.filter(technician=request.user.username)
    length = len(list(Tickets))
    return render(request, 'customers/technician.html', {'tickets': Tickets, 'length': length})


@technician_login_required
def resolve(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.status = "resolved"
    ticket.save()
    return redirect('technician')


"""home page"""


def home(request):
    return render(request, 'customers/home.html')


"""error page"""


def error(request):
    return render(request, 'customers/error.html')


"""
def admin_ticket(request):
    if request.method == "POST":
        form = TicketCreateForm(request.POST)
        if form.is_valid():
            try:
                c = form.cleaned_data
                u = User.objects.get(username=c['customer'])
                u.ticket_set.create(content=c['content'], technician=c['technicians'],status="Technician assigned")

            except:
                error = "Check whether all the fields are entered correctly"
                return render(request, 'customers/admin_ticket.html', {'form': form, 'error': error})
            else:
                return redirect('admin')
    else:
        technicians = User.objects.filter(is_technician=True)
    return render(request, 'customers/admin_ticket.html', {'technicians': technicians})
"""
