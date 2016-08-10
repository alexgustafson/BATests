from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic import TemplateView


from .models import Process


class CreateProcess(CreateView):
    model = Process
    fields = ('title', 'description',)


class UpdateProcess(UpdateView):
    model = Process


class ListProcess(ListView):
    model = Process
    paginate_by = 20


class DeleteProcess(DeleteView):
    model = Process


class ProcessDetail(DetailView):
    model = Process


class Controller(TemplateView):

    template_name = 'process/controller.jade'