from django.urls import path

from gudang.views import MasterGudangListView, MasterGudangDeleteView, MasterGudangUpdateView, MasterGudangCreateView, \
    MasterGudangDetailView

urlpatterns = [
    path('', MasterGudangListView.as_view(), name='master-gudang'),
    path('detail/<int:pk>/', MasterGudangDetailView.as_view(), name='master-gudang-detail'),
    path('create/', MasterGudangCreateView.as_view(), name='master-gudang-create'),
    path('update/<int:pk>/', MasterGudangUpdateView.as_view(), name='master-gudang-update'),
    path('delete/<int:pk>/', MasterGudangDeleteView.as_view(), name='master-gudang-delete'),
]
