from django.contrib import admin
from .models import Categoria, Produto, Perfil

admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Perfil)