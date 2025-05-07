from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from barang.forms import MasterBarangForm
from barang.models import MasterBarang


def get_induk_choices(request):
    level = int(request.GET.get('level', 0))
    tipe = request.GET.get('tipe', '')
    induk_choices = MasterBarang.objects.filter(level=level, tipe=tipe).values('id', 'kode', 'nama')
    return JsonResponse({'induk_choices': list(induk_choices)})


class MasterBarangListView(SuccessMessageMixin, ListView):
    model = MasterBarang
    template_name = 'master_barang.html'


class MasterBarangDetailView(SuccessMessageMixin, DetailView):
    model = MasterBarang
    template_name = 'master_barang_detail.html'


class MasterBarangCreateView(SuccessMessageMixin, CreateView):
    form_class = MasterBarangForm
    template_name = 'master_barang_form.html'
    success_url = reverse_lazy('barang:master-barang')
    success_message = 'Master Barang Berhasil Ditambahkan!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_type'] = 'create'
        context['submit_url'] = reverse('barang:master-barang-create')
        return context


class MasterBarangUpdateView(SuccessMessageMixin, UpdateView):
    model = MasterBarang
    form_class = MasterBarangForm
    template_name = 'master_barang_form.html'
    success_url = reverse_lazy('barang:master-barang')
    success_message = 'Master Barang Berhasil Diubah!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_type'] = 'update'
        context['submit_url'] = reverse('barang:master-barang-update', kwargs={'pk': self.object.pk})
        return context


class MasterBarangDeleteView(SuccessMessageMixin, DeleteView):
    model = MasterBarang
    success_url = reverse_lazy('barang:master-barang')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, 'Master Barang Berhasil Dihapus!')
        self.object.delete()
        return redirect(self.get_success_url())
