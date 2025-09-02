
from urllib import request
from .models import Produto,Perfil
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from .forms import EmailUpdateForm
from django.views.generic import TemplateView




class CriarContaView(View):
    def get(self, request):
        return render(request, 'pecas/crud/cadastro.html')

    def post(self, request):
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf', '').replace('.', '').replace('-', '').strip()
        genero = request.POST.get('genero')
        data = request.POST.get('data')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar = request.POST.get('confirmar')
        vendedor = request.POST.get('origem')



        if Perfil.objects.filter(cpf=cpf).exists():
            return render(request, 'pecas/crud/cadastro.html', {
                'erro': 'CPF já cadastrado.'
            })
        
        if vendedor not in ["sim", "nao"]:
            return render(request, 'pecas/crud/cadastro.html', {
                'erro': 'Seleção inválida para vendedor.'
            })
        

        if len(cpf) != 11 or not cpf.isdigit():
            return render(request, 'pecas/crud/cadastro.html', {
                'erro': 'CPF inválido. Deve conter 11 dígitos numéricos.'
            })


        if senha != confirmar:
            return render(request, 'pecas/crud/cadastro.html', {
                'erro': 'As senhas não coincidem.'
            })

        if User.objects.filter(username=email).exists():
            return render(request, 'pecas/crud/cadastro.html', {
                'erro': 'Este e-mail já está em uso.'
            })
        

        user = User.objects.create_user(username=email, email=email, password=senha)
        user.first_name = nome

        is_vendedor = False
        if vendedor == "Sim":
            is_vendedor = True 
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
        
        user.save()

        Perfil.objects.create(
            user=user,
            cpf=cpf,
            genero=genero,
            data_nascimento=data,
            telefone=telefone,
            is_vendedor=is_vendedor
        )
        return redirect('home')




class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dados_usuario')
        return render(request, 'pecas/crud/login.html')

    def post(self, request):

        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = authenticate(request, username=email, password=senha)

        if user is not None:
            login(request, user)
            return redirect('dados_usuario')
        else:
            return render(request, 'pecas/crud/login.html', {
                'erro': 'Email ou senha inválidos.',
            })



class EditarEmailView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'pecas/editar_dados.html')

    def post(self, request):
        email = request.POST.get('email') 
        if User.objects.filter(email=email).exclude(id=request.user.id).exists():
            return render(request, 'pecas/editar_dados.html', {
                'erro': 'Este e-mail já está em uso por outro usuário.'
            })
        request.user.email = email
        request.user.username = email
        request.user.save()
        return redirect('dados_usuario')


class DadosUsuarioView(LoginRequiredMixin, View):
    def get(self, request):
        perfil = request.user.perfil
        return render(request, 'pecas/dados.html', {'perfil': perfil})







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
            queryset = queryset.filter(nome__icontains=pesquisar)  
        if ordenar:
            queryset = queryset.order_by(ordenar)
        return queryset


class painel_vendedor(LoginRequiredMixin, View):
    def get(self, request):
        if not hasattr(request.user, 'perfil') or not request.user.perfil.is_vendedor:
            return redirect('home')  

        return render(request, 'pecas/painel_vendedor.html')


class ProdutoDetailView(DetailView):
    model = Produto
    template_name = 'pecas/protudos/produto_detail.html'
    context_object_name = 'produto_detalhe'





class KitUpgradeListView(ListView):
    model = Produto
    queryset = Produto.objects.filter(categoria__nome='Kit Upgrade')
    paginate_by = 6
    template_name = 'pecas/protudos/kitupgrade.html'
    context_object_name = 'kits'

class monitor(ListView):
    model = Produto
    queryset = Produto.objects.filter(categoria__nome='Monitor')
    paginate_by = 6
    template_name = 'pecas/protudos/monitor.html'
    context_object_name = 'monitores'

class promocao(ListView):
    model = Produto
    queryset = Produto.objects.filter(categoria__nome='Monitor')
    paginate_by = 6
    template_name = 'pecas/protudos/promocao.html'
    context_object_name = 'produtos_promocao'

class atendimento(ListView):
    model = Produto
    template_name = 'pecas/protudos/atendimento.html'
    context_object_name = 'atendimento'
    
class notebook(ListView):
    model = Produto
    queryset = Produto.objects.filter(categoria__nome='Notebook')
    paginate_by = 6
    template_name = 'pecas/protudos/notebook.html'
    context_object_name = 'notebooks'
    

class pcgamer(ListView):
    model = Produto
    queryset = Produto.objects.filter(categoria__nome='PC Gamer')
    paginate_by = 6
    template_name = 'pecas/protudos/pcgamer.html'
    context_object_name = 'pcs'

class hardwares(ListView):
    model = Produto
    queryset = Produto.objects.filter(categoria__nome='Hardware')
    paginate_by = 6
    template_name = 'pecas/protudos/hardware.html'
    context_object_name = 'hardwares'

class carrinho(ListView):
    model = Produto
    template_name = 'pecas/protudos/carrinho.html'
    context_object_name = 'produtos'

    def get_queryset(self):
        carrinho_ids = self.request.session.get('carrinho', [])
        return Produto.objects.filter(id__in=carrinho_ids)



class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    fields = ['nome', 'descricao', 'preco', 'imagem', 'categoria']
    template_name = 'pecas/criar.html'
    success_url = reverse_lazy('gerenciar_produtos')  

class gerenciar_produtos(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'pecas/gerenciar.html'
    context_object_name = 'produtos'


class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    fields = ['nome', 'descricao', 'preco', 'imagem', 'categoria']
    template_name = 'pecas/editar.html'
    success_url = reverse_lazy('gerenciar_produtos')  


class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = 'pecas/deletar.html'
    success_url = reverse_lazy('gerenciar_produtos')  

