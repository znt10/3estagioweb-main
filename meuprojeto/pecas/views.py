
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
from .models import Perfil

from django.views import View
from django.shortcuts import redirect, get_object_or_404
from .models import Produto

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')  # redireciona se já estiver logado
        return render(request, 'pecas/login.html')

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = authenticate(request, username=email, password=senha)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'pecas/login.html', {
                'erro': 'Email ou senha inválidos.'
            })






class AddNoCarrinho(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('login')

        produto = get_object_or_404(Produto, pk=pk)
    
        carrinho = request.session.get('carrinho', [])
        carrinho.append(produto.id)
        request.session['carrinho'] = carrinho
        return redirect('carrinho')

class remover_do_carrinho(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('login')

        produto = get_object_or_404(Produto, pk=pk)
    
        carrinho = request.session.get('carrinho', [])
        if produto.id in carrinho:
            carrinho.remove(produto.id)
            request.session['carrinho'] = carrinho
        return redirect('carrinho')

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


class KitUpgradeListView(ListView):
    model = Produto
    queryset = Produto.objects.filter(categoria__nome='Kit Upgrade')
    paginate_by = 6
    template_name = 'pecas/kitupgrade.html'
    context_object_name = 'kits'

class monitor(ListView):
    model = Produto
    queryset = Produto.objects.filter(categoria__nome='Monitor')
    paginate_by = 6
    template_name = 'pecas/monitor.html'
    context_object_name = 'monitores'

class promocao(ListView):
    model = Produto
    queryset = Produto.objects.filter(categoria__nome='Monitor')
    paginate_by = 6
    template_name = 'pecas/promocao.html'
    context_object_name = 'produtos_promocao'

class atendimento(ListView):
    model = Produto
    template_name = 'pecas/atendimento.html'
    context_object_name = 'atendimento'
    
class notebook(ListView):
    model = Produto
    queryset = Produto.objects.filter(categoria__nome='Notebook')
    paginate_by = 6
    template_name = 'pecas/notebook.html'
    context_object_name = 'notebooks'
    

class pcgamer(ListView):
    model = Produto
    queryset = Produto.objects.filter(categoria__nome='PC Gamer')
    paginate_by = 6
    template_name = 'pecas/pcgamer.html'
    context_object_name = 'pcs'

class hardwares(ListView):
    model = Produto
    queryset = Produto.objects.filter(categoria__nome='Hardware')
    paginate_by = 6
    template_name = 'pecas/hardware.html'
    context_object_name = 'hardwares'

class carrinho(ListView):
    model = Produto
    template_name = 'pecas/carrinho.html'
    context_object_name = 'produtos'

    def get_queryset(self):
        carrinho_ids = self.request.session.get('carrinho', [])
        return Produto.objects.filter(id__in=carrinho_ids)


class CriarContaView(View):
    def get(self, request):
        return render(request, 'pecas/cadastro.html')

    def post(self, request):
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf', '').replace('.', '').replace('-', '').strip()
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
