"""
URL configuration for crud_test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = \
    [
        path('admin/', admin.site.urls),
        path('', include(('app.urls', 'app'), namespace='app')),
        path('master-gudang/', include(('gudang.urls', 'gudang'), namespace='gudang')),
        path('master-barang/', include(('barang.urls', 'barang'), namespace='barang')),
        path('preorder/', include(('preorder.urls', 'preorder'), namespace='preorder')),
        path('terima-barang/', include(('terima_barang.urls', 'terima-barang'), namespace='terima-barang')),
    ]
