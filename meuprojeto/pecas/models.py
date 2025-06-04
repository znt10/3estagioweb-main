from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True)
    genero = models.CharField(max_length=20)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.nome
    

    
class Review(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='reviews')
    autor = models.CharField(max_length=100)
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.produto.nome}"

class Comentario(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.CharField(max_length=100)
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor}"