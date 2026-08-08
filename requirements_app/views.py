from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Service, CustomerRequest
from .forms import RegisterForm, CustomerRequestForm, RequestDocumentForm, StaffRequestEditForm, AdminUserEditForm

from django.db import connection
from django.http import HttpResponse

def codeql_test(request):
    username = request.GET.get("username", "")

    with connection.cursor() as cursor:
        query = "SELECT * FROM auth_user WHERE username = '%s'" % username
        cursor.execute(query)

    return HttpResponse("CodeQL test")

def home(request):
    return render(request, "requirements_app/home.html", {"services": Service.objects.filter(is_active=True)[:6]})
def about(request): return render(request, "requirements_app/about.html")
def contact(request): return render(request, "requirements_app/contact.html")
def service_list(request): return render(request, "requirements_app/service_list.html", {"services": Service.objects.filter(is_active=True)})
def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    related_services = Service.objects.filter(is_active=True).exclude(id=service.id)[:3]
    return render(request, "requirements_app/service_detail.html", {"service": service, "related_services": related_services})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("customer_dashboard")
    else:
        form = RegisterForm()
    return render(request, "requirements_app/register.html", {"form": form})

@login_required
def customer_dashboard(request):
    return render(request, "requirements_app/customer_dashboard.html", {"requests": CustomerRequest.objects.filter(user=request.user)})

@login_required
def create_customer_request(request, service_slug):
    service = get_object_or_404(Service, slug=service_slug, is_active=True)
    if request.method == "POST":
        form = CustomerRequestForm(request.POST)
        if form.is_valid():
            cr = form.save(commit=False)
            cr.user = request.user
            cr.service = service
            cr.save()
            messages.success(request, f"Request {cr.request_number} created successfully.")
            return redirect("customer_request_detail", request_id=cr.id)
    else:
        form = CustomerRequestForm(initial={"customer_name": request.user.get_full_name() or request.user.username, "email": request.user.email})
    return render(request, "requirements_app/request_form.html", {"form": form, "service": service})

@login_required
def customer_request_detail(request, request_id):
    if request.user.is_staff:
        cr = get_object_or_404(CustomerRequest, id=request_id)
    else:
        cr = get_object_or_404(CustomerRequest, id=request_id, user=request.user)
    return render(request, "requirements_app/request_detail.html", {"customer_request": cr})

@login_required
def upload_document(request, request_id):
    if request.user.is_staff:
        cr = get_object_or_404(CustomerRequest, id=request_id)
    else:
        cr = get_object_or_404(CustomerRequest, id=request_id, user=request.user)
    if request.method == "POST":
        form = RequestDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.customer_request = cr
            doc.uploaded_by = request.user
            doc.save()
            messages.success(request, "Document uploaded successfully.")
            return redirect("customer_request_detail", request_id=cr.id)
    else:
        form = RequestDocumentForm()
    return render(request, "requirements_app/document_upload.html", {"form": form, "customer_request": cr})

def staff_required(user): return user.is_authenticated and user.is_staff
@login_required
@user_passes_test(staff_required)
def staff_dashboard(request):
    total = CustomerRequest.objects.count()
    active = CustomerRequest.objects.exclude(status__in=["COMPLETED", "CANCELLED"]).count()
    completed = CustomerRequest.objects.filter(status="COMPLETED").count()
    recent = CustomerRequest.objects.select_related("service", "user").all()[:10]
    return render(request, "requirements_app/staff_dashboard.html", {"total_requests": total, "active_requests": active, "completed_requests": completed, "recent_requests": recent})
@login_required
@user_passes_test(staff_required)
def staff_request_list(request):
    return render(request, "requirements_app/staff_request_list.html", {"requests": CustomerRequest.objects.select_related("service", "user").all()})
@login_required
@user_passes_test(staff_required)
def staff_request_edit(request, request_id):
    cr = get_object_or_404(CustomerRequest, id=request_id)
    if request.method == "POST":
        form = StaffRequestEditForm(request.POST, instance=cr)
        if form.is_valid():
            form.save()
            messages.success(request, f"Request {cr.request_number} updated.")
            return redirect("staff_request_list")
    else:
        form = StaffRequestEditForm(instance=cr)
    return render(request, "requirements_app/staff_request_edit.html", {"form": form, "customer_request": cr})

def superuser_required(user): return user.is_authenticated and user.is_superuser
@login_required
@user_passes_test(superuser_required)
def admin_user_list(request):
    return render(request, "requirements_app/admin_user_list.html", {"users": User.objects.all().order_by("username")})
@login_required
@user_passes_test(superuser_required)
def admin_user_edit(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = AdminUserEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"User {user_obj.username} updated successfully.")
            return redirect("admin_user_list")
    else:
        form = AdminUserEditForm(instance=user_obj)
    return render(request, "requirements_app/admin_user_edit.html", {"form": form, "user_obj": user_obj})
    


