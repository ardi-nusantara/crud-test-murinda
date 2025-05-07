from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from terima_barang.forms import TerimaBarangForm
from terima_barang.models import TerimaBarang


class TerimaBarangListView(SuccessMessageMixin, ListView):
    model = TerimaBarang
    template_name = 'terima_barang.html'


class TerimaBarangDetailView(SuccessMessageMixin, DetailView):
    model = TerimaBarang
    template_name = 'terima_barang_detail.html'


class TerimaBarangCreateView(SuccessMessageMixin, CreateView):
    form_class = TerimaBarangForm
    template_name = 'terima_barang_form.html'
    success_url = reverse_lazy('terima-barang:terima-barang')
    success_message = 'Terima Barang Berhasil Ditambahkan!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_type'] = 'create'
        context['submit_url'] = reverse('terima-barang:terima-barang-create')
        return context


class TerimaBarangUpdateView(SuccessMessageMixin, UpdateView):
    model = TerimaBarang
    form_class = TerimaBarangForm
    template_name = 'terima_barang_form.html'
    success_url = reverse_lazy('terima-barang:terima-barang')
    success_message = 'Terima Barang Berhasil Diubah!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_type'] = 'update'
        context['submit_url'] = reverse('terima-barang:terima-barang-update', kwargs={'pk': self.object.pk})
        return context


class TerimaBarangDeleteView(SuccessMessageMixin, DeleteView):
    model = TerimaBarang
    success_url = reverse_lazy('terima-barang:terima-barang')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, 'Terima Barang Berhasil Dihapus!')
        self.object.delete()
        return redirect(self.get_success_url())
