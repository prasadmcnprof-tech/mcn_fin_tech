from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import CustomerRequest, RequestDocument

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class CustomerRequestForm(forms.ModelForm):
    class Meta:
        model = CustomerRequest
        fields = ["customer_name", "email", "phone", "company_name", "city", "business_type", "customer_notes"]
        widgets = {"customer_notes": forms.Textarea(attrs={"rows": 4})}

class RequestDocumentForm(forms.ModelForm):
    class Meta:
        model = RequestDocument
        fields = ["document_name", "file"]

class StaffRequestEditForm(forms.ModelForm):
    class Meta:
        model = CustomerRequest
        fields = ["status", "payment_status", "assigned_to", "admin_notes"]
        widgets = {"admin_notes": forms.Textarea(attrs={"rows": 4})}

class AdminUserEditForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_active", "is_staff", "is_superuser", "groups"]
