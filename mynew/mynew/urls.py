from django.contrib import admin
from django.urls import path
from myapps import views  # Import views from your app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),  # Corrected view import and syntax
    path('login/', views.login_user, name='Login'),  # Corrected view import and syntax

]
