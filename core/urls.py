from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('produtos/', views.produtos, name='produtos'),
    path('produtos/<int:id>/', views.produto_detalhe, name='produto_detalhe'),
    path('comprar_produto/<int:id>/', views.comprar_produto, name='comprar_produto'),
    path('adicionar_carrinho/<int:id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('cadastro_usuario/', views.cadastro_usuario, name='cadastro_usuario'),
    path('login_usuario/', views.login_usuario, name='login_usuario'),
    path('logout_usuario/', views.logout_usuario, name='logout_usuario'),
    path('ver_carrinho', views.ver_carrinho, name="ver_carrinho"),
    path('deletar_item/<int:id>', views.deletar_item, name='deletar_item'),
    path('diminuir_quantidade_carrinho/<int:id>', views.diminuir_quantidade, name='diminuir_item'),
    path('checkout_carrinho/', views.checkout_carrinho, name="checkout_carrinho"),
    path('pagamento/', views.pagamento, name='pagamento'),
    path('adicionar_produto/', views.adicionar_produto, name="adicionar_produto")
]