from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import F
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from barang.models import MasterBarang
from preorder.models import PreOrder, PreOrderDetail
from terima_barang.forms import TerimaBarangForm, TerimaBarangDetailForm
from terima_barang.models import TerimaBarang, TerimaBarangDetail


def get_preorder_qty_po(request, id):
    preorder = get_object_or_404(PreOrder, pk=id)
    return JsonResponse({'qty_po': preorder.qty_po})


def get_barang_by_preorder(request, preorder_id):
    # Get all barang associated with the selected PreOrder and with qtystok >= 1
    details = PreOrderDetail.objects.filter(preorder_id=preorder_id, kode_barang__qtystok__gte=1)
    result = [
        {"id": detail.kode_barang.pk, "kode": detail.kode_barang.kode, "nama": detail.kode_barang.nama, "qtystok": detail.kode_barang.qtystok}
        for detail in details
    ]
    return JsonResponse({"barang": result})


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

        TerimaBarangFormSet = inlineformset_factory(TerimaBarang, TerimaBarangDetail, form=TerimaBarangDetailForm,
                                                    extra=1, can_delete=True)

        if self.request.POST:
            context['TerimaBarangFormSet'] = TerimaBarangFormSet(self.request.POST)
        else:
            context['TerimaBarangFormSet'] = TerimaBarangFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        terima_barang_formset = context['TerimaBarangFormSet']

        if terima_barang_formset.is_valid():
            with transaction.atomic():
                terima_barang = form.save()
                terima_barang_formset.instance = terima_barang
                terima_barang_formset.save()

                # Update related PreOrderDetail and MasterBarang
                for detail in terima_barang_formset.cleaned_data:
                    kode_barang = detail['kode_barang']
                    qty_terima = detail['qty_terima']

                    # Update PreOrderDetail
                    PreOrderDetail.objects.filter(preorder=form.cleaned_data['preorder'], kode_barang=kode_barang).update(
                        qty_terima=F('qty_terima') + qty_terima)

                    # Update MasterBarang stock
                    MasterBarang.objects.filter(kode=kode_barang.kode).update(qtystok=F('qtystok') - qty_terima)

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


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
