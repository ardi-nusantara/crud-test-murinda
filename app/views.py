from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from app.forms import MasterPemasokForm
from app.models import MasterPemasok


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        # Redirect to the desired URL or view
        return redirect('app:master-pemasok')


class MasterPemasokListView(SuccessMessageMixin, ListView):
    model = MasterPemasok
    template_name = 'master_pemasok.html'


class MasterPemasokDetailView(SuccessMessageMixin, DetailView):
    model = MasterPemasok
    template_name = 'master_pemasok_detail.html'


class MasterPemasokCreateView(SuccessMessageMixin, CreateView):
    form_class = MasterPemasokForm
    template_name = 'master_pemasok_form.html'
    success_url = reverse_lazy('app:master-pemasok')
    success_message = 'Master Pemasok Berhasil Ditambahkan!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_type'] = 'create'
        context['submit_url'] = reverse('app:master-pemasok-create')
        return context


class MasterPemasokUpdateView(SuccessMessageMixin, UpdateView):
    model = MasterPemasok
    form_class = MasterPemasokForm
    template_name = 'master_pemasok_form.html'
    success_url = reverse_lazy('app:master-pemasok')
    success_message = 'Master Pemasok Berhasil Diubah!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_type'] = 'update'
        context['submit_url'] = reverse('app:master-pemasok-update', kwargs={'pk': self.object.pk})
        return context


class MasterPemasokDeleteView(SuccessMessageMixin, DeleteView):
    model = MasterPemasok
    success_url = reverse_lazy('app:master-pemasok')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, 'Master Pemasok Berhasil Dihapus!')
        self.object.delete()
        return redirect(self.get_success_url())
