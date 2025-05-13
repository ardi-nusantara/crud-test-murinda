from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from preorder.forms import PreorderForm, PreorderDetailForm
from preorder.models import PreOrder, PreOrderDetail


class PreorderListView(SuccessMessageMixin, ListView):
    model = PreOrder
    template_name = 'preorder.html'


class PreorderDetailView(SuccessMessageMixin, DetailView):
    model = PreOrder
    template_name = 'preorder_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['details'] = PreOrderDetail.objects.filter(preorder=self.object)
        return context


class PreorderCreateView(SuccessMessageMixin, CreateView):
    form_class = PreorderForm
    template_name = 'preorder_form.html'
    success_url = reverse_lazy('preorder:preorder')
    success_message = 'Preorder Berhasil Ditambahkan!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_type'] = 'create'
        context['submit_url'] = reverse('preorder:preorder-create')

        PreorderFormSet = inlineformset_factory(PreOrder, PreOrderDetail, form=PreorderDetailForm, extra=1,
                                                can_delete=True)

        if self.request.POST:
            context['PreorderFormSet'] = PreorderFormSet(self.request.POST)
        else:
            context['PreorderFormSet'] = PreorderFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        preorder_formset = context['PreorderFormSet']

        if preorder_formset.is_valid():
            preorder = form.save()
            preorder_formset.instance = preorder
            preorder_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


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

        PreorderFormSet = inlineformset_factory(PreOrder, PreOrderDetail, form=PreorderDetailForm, extra=0,
                                                can_delete=True)

        if self.request.POST:
            context['PreorderFormSet'] = PreorderFormSet(self.request.POST, instance=self.object)
        else:
            context['PreorderFormSet'] = PreorderFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        preorder_formset = context['PreorderFormSet']

        if preorder_formset.is_valid():
            preorder = form.save()
            preorder_formset.instance = preorder
            preorder_formset.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class PreorderDeleteView(SuccessMessageMixin, DeleteView):
    model = PreOrder
    success_url = reverse_lazy('preorder:preorder')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, 'Preorder Berhasil Dihapus!')
        self.object.delete()
        return redirect(self.get_success_url())
