from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from barang.models import MasterBarang
from preorder.models import PreOrderDetail
from terima_barang.forms import TerimaBarangForm, TerimaBarangDetailForm
from terima_barang.models import TerimaBarang, TerimaBarangDetail


def get_barang_by_preorder(request, preorder_id):
    # Get all barang associated with the selected PreOrder and with qtystok >= 1
    details = PreOrderDetail.objects.filter(preorder_id=preorder_id, kode_barang__qtystok__gte=1)
    result = [
        {"id": detail.kode_barang.pk, "kode": detail.kode_barang.kode, "nama": detail.kode_barang.nama,
         "qty_po": detail.qty_po, "qty_terima": detail.qty_terima, "qtystok": detail.kode_barang.qtystok}
        for detail in details
    ]
    return JsonResponse({"barang": result})


class TerimaBarangListView(SuccessMessageMixin, ListView):
    model = TerimaBarang
    template_name = 'terima_barang.html'


class TerimaBarangDetailView(SuccessMessageMixin, DetailView):
    model = TerimaBarang
    template_name = 'terima_barang_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['details'] = TerimaBarangDetail.objects.filter(terima_barang=self.object)
        return context


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
        terima_barang_details = context['TerimaBarangFormSet']
        preorder = form.instance.preorder

        with transaction.atomic():
            # Save the main form instance
            self.object = form.save()

            # Process the formset
            if terima_barang_details.is_valid():
                for detail_form in terima_barang_details:
                    detail = detail_form.save(commit=False)

                    # Fetch PreOrderDetail and validate qty_terima
                    preorder_detail = get_object_or_404(
                        PreOrderDetail, preorder=preorder, kode_barang=detail.kode_barang
                    )
                    remaining_qty = preorder_detail.qty_po - preorder_detail.qty_terima

                    if detail.qty_terima > remaining_qty:
                        raise ValidationError(
                            f"Qty Terima ({detail.qty_terima}) exceeds the remaining allowed quantity ({remaining_qty}) for {detail.kode_barang.nama}."
                        )

                    # Update PreOrderDetail and MasterBarang
                    preorder_detail.qty_terima += detail.qty_terima
                    preorder_detail.save()

                    master_barang = get_object_or_404(MasterBarang, pk=detail.kode_barang.pk)
                    master_barang.qtystok += detail.qty_terima
                    master_barang.save()

                    # Save the detail instance
                    detail.terima_barang = self.object
                    detail.save()

            else:
                return self.form_invalid(form)

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

        TerimaBarangFormSet = inlineformset_factory(TerimaBarang, TerimaBarangDetail, form=TerimaBarangDetailForm,
                                                    extra=0, can_delete=True)
        if self.request.POST:
            context['TerimaBarangFormSet'] = TerimaBarangFormSet(self.request.POST, instance=self.object)
        else:
            context['TerimaBarangFormSet'] = TerimaBarangFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['TerimaBarangFormSet']

        if formset.is_valid():
            with transaction.atomic():
                self.object = form.save()

                # Get the original details before updating
                original_details = TerimaBarangDetail.objects.filter(terima_barang=self.object)
                original_data = {
                    detail.kode_barang_id: detail.qty_terima for detail in original_details
                }

                # Save the updated details
                formset.instance = self.object
                formset.save()

                # Adjust stocks based on the differences
                updated_details = TerimaBarangDetail.objects.filter(terima_barang=self.object)
                for detail in updated_details:
                    barang = detail.kode_barang
                    original_qty = original_data.get(barang.id, 0)
                    updated_qty = detail.qty_terima
                    delta_qty = updated_qty - original_qty

                    # Adjust MasterBarang stock
                    barang.qtystok += delta_qty
                    barang.save()

                    # Adjust PreOrderDetail qty_terima
                    preorder_detail = PreOrderDetail.objects.get(
                        preorder=self.object.preorder, kode_barang=barang
                    )
                    preorder_detail.qty_terima += delta_qty
                    preorder_detail.save()

                # Handle deletions from the formset
                for barang_id, original_qty in original_data.items():
                    if barang_id not in [detail.kode_barang_id for detail in updated_details]:
                        barang = MasterBarang.objects.get(id=barang_id)
                        barang.qtystok -= original_qty
                        barang.save()

                        preorder_detail = PreOrderDetail.objects.get(
                            preorder=self.object.preorder, kode_barang=barang
                        )
                        preorder_detail.qty_terima -= original_qty
                        preorder_detail.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class TerimaBarangDeleteView(SuccessMessageMixin, DeleteView):
    model = TerimaBarang
    success_url = reverse_lazy('terima-barang:terima-barang')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Reverse related stocks and PreOrderDetails
        terima_barang_details = TerimaBarangDetail.objects.filter(terima_barang=self.object)

        with transaction.atomic():
            for detail in terima_barang_details:
                barang = detail.kode_barang

                # Reverse MasterBarang stock
                barang.qtystok -= detail.qty_terima
                barang.save()

                # Reverse PreOrderDetail qty_terima
                preorder_detail = PreOrderDetail.objects.get(
                    preorder=self.object.preorder,
                    kode_barang=barang
                )
                preorder_detail.qty_terima -= detail.qty_terima
                preorder_detail.save()

            # Delete the main object and details
            self.object.delete()

        messages.success(request, 'Terima Barang Berhasil Dihapus!')
        return redirect(self.get_success_url())
