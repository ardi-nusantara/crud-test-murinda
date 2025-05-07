from django.urls import path

from barang.views import MasterBarangListView, MasterBarangDetailView, MasterBarangCreateView, MasterBarangUpdateView, \
    MasterBarangDeleteView, get_induk_choices

urlpatterns = [
    path('', MasterBarangListView.as_view(), name='master-barang'),
    path('detail/<int:pk>/', MasterBarangDetailView.as_view(), name='master-barang-detail'),
    path('create/', MasterBarangCreateView.as_view(), name='master-barang-create'),
    path('update/<int:pk>/', MasterBarangUpdateView.as_view(), name='master-barang-update'),
    path('delete/<int:pk>/', MasterBarangDeleteView.as_view(), name='master-barang-delete'),
    path('get_induk_choices/', get_induk_choices, name='get_induk_choices'),
]
