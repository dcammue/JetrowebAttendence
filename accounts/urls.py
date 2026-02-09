from django.urls import path
from .views import LoginView, LogoutView
from .views import StartStopView
from .views import today_dashboard
from .views import monthly_summary
from .views import admin_dashboard
from .views import user_dashboard
from .views import monthly_payroll_pdf


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('work/', StartStopView.as_view()),
    path('today/', today_dashboard),
    path("monthly/", monthly_summary),
    path("admin-dashboard/", admin_dashboard),
    path("user-dashboard/", user_dashboard),
    path("admin/payroll-pdf/", monthly_payroll_pdf),

]

