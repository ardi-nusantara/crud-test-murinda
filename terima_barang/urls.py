from django.urls import path

from terima_barang.views import TerimaBarangListView, TerimaBarangDetailView, TerimaBarangCreateView, \
    TerimaBarangUpdateView, TerimaBarangDeleteView, get_preorder_qty_po, get_barang_by_preorder

urlpatterns = [
    path('', TerimaBarangListView.as_view(), name='terima-barang'),
    path('detail/<int:pk>/', TerimaBarangDetailView.as_view(), name='terima-barang-detail'),
    path('create/', TerimaBarangCreateView.as_view(), name='terima-barang-create'),
    path('update/<int:pk>/', TerimaBarangUpdateView.as_view(), name='terima-barang-update'),
    path('delete/<int:pk>/', TerimaBarangDeleteView.as_view(), name='terima-barang-delete'),
    path('preorder/<int:id>/', get_preorder_qty_po, name='get-preorder-qty-po'),
    path('preorder/<int:preorder_id>/barang/', get_barang_by_preorder, name='get-barang-by-preorder'),

]
