from django.urls import path

from preorder.views import PreorderListView, PreorderDetailView, PreorderCreateView, PreorderUpdateView, \
    PreorderDeleteView

urlpatterns = [
    path('', PreorderListView.as_view(), name='preorder'),
    path('detail/<int:pk>/', PreorderDetailView.as_view(), name='preorder-detail'),
    path('create/', PreorderCreateView.as_view(), name='preorder-create'),
    path('update/<int:pk>/', PreorderUpdateView.as_view(), name='preorder-update'),
    path('delete/<int:pk>/', PreorderDeleteView.as_view(), name='preorder-delete'),
]
