from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from gudang.forms import MasterGudangForm
from gudang.models import MasterGudang


class MasterGudangListView(SuccessMessageMixin, ListView):
    model = MasterGudang
    template_name = 'master_gudang.html'


class MasterGudangDetailView(SuccessMessageMixin, DetailView):
    model = MasterGudang
    template_name = 'master_gudang_detail.html'


class MasterGudangCreateView(SuccessMessageMixin, CreateView):
    form_class = MasterGudangForm
    template_name = 'master_gudang_form.html'
    success_url = reverse_lazy('gudang:master-gudang')
    success_message = 'Master Gudang Berhasil Ditambahkan!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_type'] = 'create'
        context['submit_url'] = reverse('gudang:master-gudang-create')
        return context


class MasterGudangUpdateView(SuccessMessageMixin, UpdateView):
    model = MasterGudang
    form_class = MasterGudangForm
    template_name = 'master_gudang_form.html'
    success_url = reverse_lazy('gudang:master-gudang')
    success_message = 'Master Gudang Berhasil Diubah!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_type'] = 'update'
        context['submit_url'] = reverse('gudang:master-gudang-update', kwargs={'pk': self.object.pk})
        return context


class MasterGudangDeleteView(SuccessMessageMixin, DeleteView):
    model = MasterGudang
    success_url = reverse_lazy('gudang:master-gudang')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, 'Master Gudang Berhasil Dihapus!')
        self.object.delete()
        return redirect(self.get_success_url())
