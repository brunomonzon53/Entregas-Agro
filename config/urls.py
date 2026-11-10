from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "iniciar-sesion/",
        auth_views.LoginView.as_view(
            template_name="gestion/login.html",
            redirect_authenticated_user=True
        ),
        name="login"
    ),
    path(
        "cerrar-sesion/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),
    path("admin/", admin.site.urls),
    path("", include("gestion.urls")),
]