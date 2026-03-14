from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Produto
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def calcular_total(carrinho):
    produtos = Produto.objects.filter(id__in=carrinho.keys())

    total = 0

    for produto in produtos:
        quantidade = carrinho[str(produto.id)]
        total +=  produto.preco * quantidade

    return total

def home(request):
    return render(request, 'home.html')

def produtos(request):
    produtos = Produto.objects.filter(ativo=True)
    return render(request, 'produtos.html', {"produtos":produtos})

def produto_detalhe(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'produto_detalhe.html', {'produto':produto})

def comprar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'compra_produto.html', {'produto':produto})

def adicionar_carrinho(request, id):
    carrinho = request.session.get("carrinho", {})

    id = str(id)
    if id in carrinho:
        carrinho[id] += 1
    else:
        carrinho[id] = 1
    request.session["carrinho"] = carrinho

    return redirect("ver_carrinho")

def cadastro_usuario(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        user.save()
        login(request, user)
        return redirect("home")
    
    return render(request, 'cadastro_usuario.html')

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
    return render(request, "login.html")

def logout_usuario(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("home")
    return render(request, "logout_usuario.html")

def ver_carrinho(request):
    carrinho = request.session.get("carrinho", {})
    produtos = Produto.objects.filter(id__in=carrinho.keys())

    produtos_carrinho = []

    for produto in produtos:
        quantidade = carrinho[str(produto.id)]

        produtos_carrinho.append({
            "produto":produto,
            "quantidade":quantidade
        })
    return render(request, "carrinho.html", {"produtos": produtos_carrinho})

def deletar_item(request, id):
    carrinho = request.session.get("carrinho", {})

    if str(id) in carrinho:
        del carrinho[str(id)]

    request.session["carrinho"] = carrinho

    return redirect("ver_carrinho")

def diminuir_quantidade(request, id):
    carrinho = request.session.get("carrinho", {})

    if str(id) in carrinho:
        carrinho[str(id)] -= 1

        if carrinho[str(id)] <= 0:
            del carrinho[str(id)]
    
    request.session["carrinho"] = carrinho

    return redirect("ver_carrinho")

def checkout_carrinho(request):
    carrinho = request.session.get("carrinho", {})

    total = calcular_total(carrinho)

    return render(request, "checkout_carrinho.html", {
        "total": total
        })

def pagamento(request):
    carrinho = request.session.get("carrinho", {})
    total = calcular_total(carrinho)

    if request.method == "POST":

        metodo = request.POST.get("pagamento")

        if metodo == "pix":
            total = 0
            request.session["carrinho"] = {}

            return redirect("home")
        
    return render(request, 'pagamentos.html', {
        "total": total
    })

def adicionar_produto(request):
    if not request.user.is_staff:
        return redirect("home")
    
    if request.method == 'POST':
        nome_produto = request.POST.get("nome_produto")
        descricao_produto = request.POST.get("descricao_produto")
        preco_produto = request.POST.get("preco_produto")
        ativo_produto = request.POST.get("ativo_produto")

        if ativo_produto == "ativo":
            ativo = True
        else:
            ativo = False

        produto_novo = Produto.objects.create(
            nome=nome_produto, 
            descricao=descricao_produto, 
            preco=preco_produto, 
            ativo=ativo)
        produto_novo.save()



    return render(request, "adicionar_produto.html")