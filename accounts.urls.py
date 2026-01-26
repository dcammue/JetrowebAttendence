from .views import today_dashboard

urlpatterns += [
    path('today/', today_dashboard),
]
