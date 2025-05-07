from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from barang.forms import MasterBarangForm
from barang.models import MasterBarang


def get_induk_choices(request):
    """
    Fetch induk choices based on kode and level from the request.
    """
    kode = request.GET.get('kode')
    level = request.GET.get('level')

    if not kode or not level:
        return JsonResponse({'induk_choices': []})  # No data if inputs are missing

    try:
        # Determine the parent level (level - 1)
        parent_level = int(level) - 1
        if parent_level < 1:
            return JsonResponse({'induk_choices': []})  # No valid parent level

        # Extract induk base from kode
        induk_code = ".".join(kode.split(".")[:parent_level])

        # Query database for possible induk options (parent level items)
        induk_queryset = MasterBarang.objects.filter(
            kode__startswith=induk_code,
            level=str(parent_level)
        )

        # Prepare choices as a list of tuples (value, label)
        induk_choices = [
            (item.kode, f"{item.kode} - {item.nama}") for item in induk_queryset
        ]
        print(induk_choices)
        return JsonResponse({'induk_choices': induk_choices})
    except Exception as e:
        return JsonResponse({'induk_choices': [], 'error': str(e)}, status=400)


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
