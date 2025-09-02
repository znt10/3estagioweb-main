from django.test import TestCase
from pecas.models import Categoria, Produto

class TestCategoria(TestCase):
    def test_str_categoria(self):
        categoria = Categoria.objects.create(nome="Eletrônicos")
        self.assertEqual(str(categoria), "Eletrônicos")


class TestProduto(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Eletrônicos")
        self.produto = Produto.objects.create(
            nome="Smartphone",
            descricao="Um smartphone moderno",
            preco=1500.00,
            categoria=self.categoria,
            imagem="produtos/teste.jpg"
        )

    def test_str_produto(self):
        self.assertEqual(str(self.produto), "Smartphone")

    def test_preco_positivo(self):
        self.assertGreater(self.produto.preco, 0)
