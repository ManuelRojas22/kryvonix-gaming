from django.urls import path
from apps.staff.views.base import StaffLoginView, DashboardView, DashboardStatsView

app_name = 'staff'

urlpatterns = [
    path('login/', StaffLoginView.as_view(), name='login'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
]