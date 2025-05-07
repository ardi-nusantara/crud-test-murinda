from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from preorder.forms import PreorderForm
from preorder.models import PreOrder


class PreorderListView(SuccessMessageMixin, ListView):
    model = PreOrder
    template_name = 'preorder.html'


class PreorderDetailView(SuccessMessageMixin, DetailView):
    model = PreOrder
    template_name = 'preorder_detail.html'


class PreorderCreateView(SuccessMessageMixin, CreateView):
    form_class = PreorderForm
    template_name = 'preorder_form.html'
    success_url = reverse_lazy('preorder:preorder')
    success_message = 'Preorder Berhasil Ditambahkan!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_type'] = 'create'
        context['submit_url'] = reverse('preorder:preorder-create')
        return context


class PreorderUpdateView(SuccessMessageMixin, UpdateView):
    model = PreOrder
    form_class = PreorderForm
    template_name = 'preorder_form.html'
    success_url = reverse_lazy('preorder:preorder')
    success_message = 'Preorder Berhasil Diubah!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_type'] = 'update'
        context['submit_url'] = reverse('preorder:preorder-update', kwargs={'pk': self.object.pk})
        return context


class PreorderDeleteView(SuccessMessageMixin, DeleteView):
    model = PreOrder
    success_url = reverse_lazy('preorder:preorder')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, 'Preorder Berhasil Dihapus!')
        self.object.delete()
        return redirect(self.get_success_url())
