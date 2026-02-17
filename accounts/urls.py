from django.urls import path
from .views import LoginView, LogoutView
from .views import StartStopView
from .views import today_dashboard
from .views import monthly_summary
from .views import admin_dashboard
from .views import user_dashboard
from .views import monthly_payroll_pdf
from .views import test_pdf
from .views import CustomAuthToken
from .views import register
from .views import delete_account
from .views import forgot_password
from .views import reset_password
from .views import forgot_page
from . import views
from .views import dashboard



urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('work/', StartStopView.as_view()),
    path('today/', today_dashboard),
    path("monthly/", monthly_summary),
    path("admin-dashboard/", admin_dashboard),
    path("user-dashboard/", user_dashboard),
    path('monthly_payroll_pdf/', monthly_payroll_pdf, name='monthly_payroll_pdf'),
    path('test_pdf/', test_pdf, name='test_pdf'),
    path('api/accounts/login/', CustomAuthToken.as_view(), name='api-login'),
    path('register/', register),
    path('delete-account/', delete_account),
    path('', views.login_page, name='login'),         # /api/accounts/
    path('reset/', views.reset_page, name='reset'),    # /api/accounts/reset/
    path('forgot-password/', forgot_password),  # your API view for forgot password
    path('reset-password/', reset_password),    # your API view for reset password
    path('forgot-page/' , forgot_page),
    path("dashboard/", dashboard, name="dashboard"),
]


