from django.contrib import admin
from django.urls import path
from .views import ProdutoListView, ProdutoDetailView, ProdutoCreateView, ProdutoUpdateView, ProdutoDeleteView, CriarContaView,KitUpgradeListView, dadosView,pedidosdetail
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProdutoListView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='pecas/login.html'),
    name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', ProdutoListView.as_view(), name='produto-list'),
    path('produto/<int:pk>/', ProdutoDetailView.as_view(), name='produto-detail'),
    path('produto/novo/', ProdutoCreateView.as_view(), name='produto-create'),
    path('produto/<int:pk>/editar/', ProdutoUpdateView.as_view(), name='produto-update'),
    path('produto/<int:pk>/deletar/', ProdutoDeleteView.as_view(), name='produto-delete'),
    path('criar-conta/', CriarContaView.as_view(), name='criar-conta'),
    path('kitupgrade/', KitUpgradeListView.as_view(), name='kitupgrade'),
    path('pedidos/', pedidosdetail.as_view(), name='favoritos'),
    path('meus-dados/', dadosView.as_view(), name='meus-dados'),
]
