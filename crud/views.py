from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import PessoaForm
from .models import Pessoa

class PessoaList(ListView):
    model = Pessoa
    template_name = 'pessoas.html'
    context_object_name = 'pessoas'

class PessoaCreate(CreateView):
    model = Pessoa
    form_class = PessoaForm
    template_name = 'form.html'
    success_url = reverse_lazy('list')
    
    def form_valid(self, form):
        cpf = form.cleaned_data['cpf']
        if Pessoa.objects.filter(cpf=cpf).exists():
            form.add_error('cpf', 'CPF já cadastrado.')
            return self.form_invalid(form)
        return super().form_valid(form)

class PessoaUpdate(UpdateView):
    model = Pessoa
    form_class = PessoaForm
    template_name = 'form_update.html'
    success_url = reverse_lazy('list')

class PessoaDelete(DeleteView):
    model = Pessoa
    form_class = PessoaForm
    template_name = 'pessoas_delete.html'
    success_url = reverse_lazy('list')
