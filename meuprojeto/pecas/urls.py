from django.urls import path
from .views import (
    ProdutoListView, ProdutoDetailView, ProdutoCreateView, ProdutoUpdateView,
    ProdutoDeleteView, CriarContaView,remover_do_carrinho ,KitUpgradeListView,carrinho,AddNoCarrinho ,LoginView, pcgamer,hardwares,notebook,monitor,
    promocao,atendimento,remover_do_carrinho,gerenciar_produtos,DadosUsuarioView,EditarEmailView
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', ProdutoListView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'), 
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('produto/<int:pk>/', ProdutoDetailView.as_view(), name='produto-detail'),
    path('produto/novo/', ProdutoCreateView.as_view(), name='produto-create'),
    path('produto/<int:pk>/editar/', ProdutoUpdateView.as_view(), name='produto-update'),
    path('produto/<int:pk>/deletar/', ProdutoDeleteView.as_view(), name='produto-delete'),

    path('criar-conta/', CriarContaView.as_view(), name='criar-conta'),
    path('kitupgrade/', KitUpgradeListView.as_view(), name='kitupgrade'),
    path('pc-gamer/', pcgamer.as_view(), name='pc_gamer'),
    path('hardwares/', hardwares.as_view(), name='hardwares'),
    path('monitor/', monitor.as_view(), name='monitor'),
    path('promocao/', promocao.as_view(), name='promocao'),
    path('atendimento/', atendimento.as_view(), name='atendimento'),
    path('notebook/', notebook.as_view(), name='notebook'),
    path('add-no-carrinho/<int:pk>/', AddNoCarrinho.as_view(), name='add_no_carrinho'),
    path('carrinho/', carrinho.as_view(), name='carrinho'),
    path('remover-do-carrinho/<int:pk>/', remover_do_carrinho.as_view(), name='remover'),
    path('gerenciar-produtos/', gerenciar_produtos.as_view(), name='gerenciar_produtos'),
    path('dados-usuario/', DadosUsuarioView.as_view(), name='dados_usuario'),
    path('editar-email/', EditarEmailView.as_view(), name='editar_email'),


    
]
