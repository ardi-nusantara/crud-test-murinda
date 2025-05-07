from django.urls import path

from app.views import MasterPemasokListView, DashboardView, MasterPemasokCreateView, MasterPemasokUpdateView, \
    MasterPemasokDetailView, MasterPemasokDeleteView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('master-pemasok/', MasterPemasokListView.as_view(), name='master-pemasok'),
    path('master-pemasok/detail/<int:pk>/', MasterPemasokDetailView.as_view(), name='master-pemasok-detail'),
    path('master-pemasok/create/', MasterPemasokCreateView.as_view(), name='master-pemasok-create'),
    path('master-pemasok/update/<int:pk>/', MasterPemasokUpdateView.as_view(), name='master-pemasok-update'),
    path('master-pemasok/delete/<int:pk>/', MasterPemasokDeleteView.as_view(), name='master-pemasok-delete'),
]
