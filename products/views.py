from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Min
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .facade import get_product, get_from_category
from .forms import CategoryForm, ProductForm, VariationForm, \
    ProductVariationForm
from .models import ProductVariation, Category, Product, Variation


@login_required
def products_list(request):
    produtos = Product.objects.all().order_by('category__name', 'name')

    produtos_simples = produtos.filter(productvariation__isnull=True)

    variacoes = ProductVariation.objects.all()

    context = {
        'produtos_simples': produtos_simples,
        'variacoes': variacoes,
    }
    return render(request, 'products/list_products.html', context=context)


@login_required
def product_new(request):
    product_form = Product()
    variations_formset = inlineformset_factory(Product, ProductVariation,
                                               form=ProductVariationForm,
                                               extra=1)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product_form, prefix='main')
        formset = variations_formset(request.POST, instance=product_form,
                                     prefix='product')

        if form.is_valid() and formset.is_valid():
            novo_produto = form.save(commit=False)
            novo_produto.save()
            formset.save()
            messages.success(request, "Novo produto cadastrado.")
            return redirect(products_list)
    else:
        form = ProductForm(instance=product_form, prefix='main')
        formset = variations_formset(instance=product_form, prefix='product')

    return render(request, 'products/product_new.html', {'form': form,
                                                         'formset': formset})


def two_flavors(request):
    variacoes = ProductVariation.objects.all()
    min_price_broto = ProductVariation.objects.filter(
        variation__name='Broto').aggregate(Min('price'))
    min_price_grande = ProductVariation.objects.filter(
        variation__name='Grande').aggregate(Min('price'))
    context = {
        'variacoes': variacoes,
        'min_price_broto': min_price_broto['price__min'],
        'min_price_grande': min_price_grande['price__min']
    }
    return render(request, 'products/sliced.html', context=context)


@login_required
def categories_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}

    return render(request, 'products/list_categories.html', context)


@login_required
def category_new(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nova categoria cadastrada.")
            return redirect(categories_list)
    else:
        form = CategoryForm()

    return render(request, 'products/category_new.html', {'form': form})


@login_required
def variations_list(request):
    variacoes = Variation.objects.all()
    context = {'variacoes': variacoes}

    return render(request, 'products/list_variations.html', context)


@login_required
def variation_new(request):
    if request.method == "POST":
        form = VariationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nova variação cadastrada.")
            return redirect(variations_list)
    else:
        form = VariationForm()

    return render(request, 'products/variation_new.html', {'form': form})


@login_required
def import_from_woocommerce(request, product_id):
    product = get_product(product_id=product_id)
    return JsonResponse(product.json())


@login_required
def import_all_from_woocommerce_category(request, category_id):
    products = get_from_category(category_id)
    return JsonResponse(products)
