from django.urls import path

from terima_barang.views import TerimaBarangListView, TerimaBarangDetailView, TerimaBarangCreateView, \
    TerimaBarangUpdateView, TerimaBarangDeleteView

urlpatterns = [
    path('', TerimaBarangListView.as_view(), name='terima-barang'),
    path('detail/<int:pk>/', TerimaBarangDetailView.as_view(), name='terima-barang-detail'),
    path('create/', TerimaBarangCreateView.as_view(), name='terima-barang-create'),
    path('update/<int:pk>/', TerimaBarangUpdateView.as_view(), name='terima-barang-update'),
    path('delete/<int:pk>/', TerimaBarangDeleteView.as_view(), name='terima-barang-delete'),
]
