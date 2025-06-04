
from .models import Produto
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User


class ProdutoListView(ListView):
    model = Produto
    template_name = 'pecas/index.html'
    context_object_name = 'produtos'
    paginate_by = 6

    def get_queryset(self, *args, **kwargs):
        queryset = Produto.objects.all()
        ordenar = self.request.GET.get('ordenar_por')
        pesquisar = self.request.GET.get('q')

        if pesquisar:
            queryset = queryset.filter(nome__icontains=pesquisar)  # corrigido: 'titulo' → 'nome'
        if ordenar:
            queryset = queryset.order_by(ordenar)
        return queryset

class ProdutoDetailView(DetailView):
    model = Produto
    template_name = 'pecas/produto_detail.html'
    context_object_name = 'produto_detalhe'

from .models import Perfil

class CriarContaView(View):
    def get(self, request):
        return render(request, 'pecas/cadastro.html')

    def post(self, request):
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        genero = request.POST.get('genero')
        data = request.POST.get('data')  # deve estar no formato yyyy-mm-dd
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar = request.POST.get('confirmar')

        if senha != confirmar:
            return render(request, 'pecas/cadastro.html', {
                'erro': 'As senhas não coincidem.'
            })

        if User.objects.filter(username=email).exists():
            return render(request, 'pecas/cadastro.html', {
                'erro': 'Este e-mail já está em uso.'
            })

        # Cria o usuário
        user = User.objects.create_user(username=email, email=email, password=senha)
        user.first_name = nome
        user.save()

        # Cria o perfil vinculado ao usuário
        Perfil.objects.create(
            user=user,
            cpf=cpf,
            genero=genero,
            data_nascimento=data,
            telefone=telefone
        )

        return redirect('home')


class LoginView(View):
    def get(self, request):
        return render(request, 'pecas/login.html')

    def post(self, request):
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = authenticate(request, username=email, password=senha)

        if user is not None:
            login(request, user)
            return redirect('home')  # ou a rota que você quiser
        else:
            return render(request, 'pecas/login.html', {
                'erro': 'Email ou senha inválidos.'
            })




class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    fields = ['nome', 'descricao', 'preco', 'imagem', 'categoria']
    template_name = 'pecas/produto_form.html'

    def form_valid(self, form):
        form.instance.vendedor = self.request.user
        return super().form_valid(form)
    


class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    fields = ['nome', 'descricao', 'preco', 'imagem', 'categoria']
    template_name = 'pecas/produto_form.html'

    def get_queryset(self):
        return Produto.objects.filter(vendedor=self.request.user)
    


class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = 'pecas/produto_confirm_delete.html'
    success_url = reverse_lazy('produto-list')  # redireciona para a lista após deletar

    def get_queryset(self):
        return Produto.objects.filter(vendedor=self.request.user)
