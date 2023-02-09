from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from .models import Cartridges, Manufacturer, NameСartridge, Placements
from .forms import ManufacturerForm, NameСartridgeForm, PlacementsForm, CartridgesForm


# Create your views here.
def stock(request):
    cart = Cartridges.objects.order_by('-date')
    count = Cartridges.objects.count()
    return render(request, 'cartridge/stock.html', {'cart': cart, 'count': count})


def use(request):
    return render(request, 'cartridge/use.html')


def empty(request):
    return render(request, 'cartridge/empty.html')


def worked_firms(request):
    return render(request, 'cartridge/worked_firms.html')


def basket(request):
    return render(request, 'cartridge/basket.html')


def massive_change_room(request):
    return render(request, 'cartridge/massive_change_room.html')


@csrf_protect
@ensure_csrf_cookie
def add_items(request):
    name_cart = Cartridges.objects.order_by('-date')
    count = Cartridges.objects.count()
    error = ''
    display = 'none'
    barcode_text = ''
    cart_name = ''
    manufacturer_name = ''
    msg_display = 'none'
    err_display = 'none'
    if request.POST:
        form = CartridgesForm(request.POST)
        if form. is_valid():
            form.save()
            barcode_text = form['barcode'].data
            cart_name = form.instance.cartName
            manufacturer_name = form.instance.manufacturerName
            count = Cartridges.objects.count()
            display = 'block'
            msg_display = 'block'
        elif form.errors:
            error = form.errors
            display = 'block'
            err_display = 'block'
        else:
            display = 'none'
    form = CartridgesForm()
    data = {
        'form': form,
        'error': error,
        'display': display,
        'msg_display': msg_display,
        'err_display': err_display,
        'barcode_text': barcode_text,
        'cart_name': cart_name,
        'manufacturer_name': manufacturer_name,
        'name_cart': name_cart,
        'count': count
    }
    return render(request, 'cartridge/add_items.html', data)


@csrf_protect
@ensure_csrf_cookie
def add_name(request):
    error = ''
    display = 'none'
    name = ''
    if request.POST:
        form = NameСartridgeForm(request.POST)
        if form.is_valid():
            form.save()
            name = form['name'].data
            display = 'block'
        else:
            error = 'block'
    form = NameСartridgeForm()
    data = {
        'form': form,
        'error': error,
        'display': display,
        'name': name,
    }
    return render(request, 'cartridge/add_name.html', data)


@csrf_protect
@ensure_csrf_cookie
def tree_list(request):
    place = Placements.objects.order_by('name')
    count = Placements.objects.count()
    error = ''
    display = 'none'
    name = ''
    msg_display = 'none'
    err_display = 'none'
    if request.POST:
        form = PlacementsForm(request.POST)
        if form.is_valid():
            form.save()
            name = form['name'].data
            count = Placements.objects.count()
            display = 'block'
            msg_display = 'block'
        elif form.errors:
            error = form.errors
            display = 'block'
            err_display = 'block'
        else:
            display = 'none'
    form = PlacementsForm()
    data = {
        'form': form,
        'error': error,
        'display': display,
        'msg_display': msg_display,
        'err_display': err_display,
        'name': name,
        'place': place,
        'count': count
    }
    return render(request, 'cartridge/tree_list.html', data)


@csrf_protect
@ensure_csrf_cookie
def add_manufacture(request):
    error = ''
    display = 'none'
    name = ''
    if request.POST:
        form = ManufacturerForm(request.POST)
        if form.is_valid():
            form.save()
            name = form['manufacturer'].data
            display = 'block'

        else:
            error = 'block'
    form = ManufacturerForm()
    data = {
        'form': form,
        'error': error,
        'display': display,
        'name': name
    }
    return render(request, 'cartridge/add_manufacture.html', data)


def add_cartridge_from_barcode_scanner(request):
    return render(request, 'cartridge/add_cartridge_from_barcode_scanner.html')
