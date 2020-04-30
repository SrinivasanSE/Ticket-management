from administer.models import User
from django import forms
"""
class TicketCreateForm(forms.Form):
    technicians = User.objects.filter(is_technician=True)
    technicians = list(technicians)
    Choices = []
    for technician in technicians:
        Choices.append((technician, technician))

    content = forms.CharField(label='Enter the problem', max_length=100)
    customer = forms.CharField(label='Enter the customer name', max_length=20)
    technicians = forms.ChoiceField(label='Available technicians',choices=Choices,widget=forms.RadioSelect())

    class Meta:
        fields=['content','customer','technicians']

    field_order = ['content','customer','technicians'] """

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget= forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)