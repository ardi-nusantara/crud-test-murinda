from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from preorder.models import PreOrder
from terima_barang.forms import TerimaBarangForm
from terima_barang.models import TerimaBarang


def get_preorder_qty_po(request, id):
    preorder = get_object_or_404(PreOrder, pk=id)
    return JsonResponse({'qty_po': preorder.qty_po})


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

    def form_valid(self, form):
        with transaction.atomic():
            qty_terima = form.cleaned_data['qty_terima']
            preorder = PreOrder.objects.get(pk=form.cleaned_data['pemasok'].pk)
            preorder.qty_po = preorder.qty_po - qty_terima
            preorder.qty_terima = preorder.qty_terima + qty_terima
            preorder.save()
        return super().form_valid(form)


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
