from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('',views.customerpage,name="customerpage"),
   path('base/',views.baseCustomer,name="base"),
   path('Success/',views.app_successifully,name="Success"),
   path("login/", auth_views.LoginView.as_view(template_name="customerPrjcts/login.html"), name="login"),
   path("logout/", auth_views.LogoutView.as_view(), name="logout"),
   path("register/", views.register, name="register"),
]
