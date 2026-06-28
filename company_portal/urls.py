from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from requirements_app import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("services/", views.service_list, name="service_list"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="requirements_app/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.customer_dashboard, name="customer_dashboard"),
    path("requests/create/<slug:service_slug>/", views.create_customer_request, name="create_customer_request"),
    path("requests/<int:request_id>/", views.customer_request_detail, name="customer_request_detail"),
    path("requests/<int:request_id>/upload-document/", views.upload_document, name="upload_document"),
    path("staff-dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("staff/requests/", views.staff_request_list, name="staff_request_list"),
    path("staff/requests/<int:request_id>/edit/", views.staff_request_edit, name="staff_request_edit"),
    path("admin-users/", views.admin_user_list, name="admin_user_list"),
    path("admin-users/<int:user_id>/edit/", views.admin_user_edit, name="admin_user_edit"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
