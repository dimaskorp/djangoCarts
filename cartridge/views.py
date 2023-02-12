from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from .models import Cartridges, Placements
from .forms import ManufacturerForm, NameСartridgeForm, PlacementsForm, CartridgesForm, PlaceUpdateForm


# Create your views here.
@csrf_protect
@ensure_csrf_cookie
def stock(request):
    form = CartridgesForm()
    cart = Cartridges.objects.order_by('-date')
    count = Cartridges.objects.count()
    cart_name = ''
    manufacturer_name = ''
    place_name = ''
    if request.POST:
        form = CartridgesForm(request.POST)
        cart_name = form.instance.cartName
        manufacturer_name = form.instance.manufacturerName
        place_name = form.instance.placeName
    data = {
        'form': form,
        'cart_name': cart_name,
        'manufacturer_name': manufacturer_name,
        'place_name': place_name,
        'cart': cart,
        'count': count
    }
    return render(request, 'cartridge/stock.html', data)


def use(request):
    return render(request, 'cartridge/use.html')


def empty(request):
    return render(request, 'cartridge/empty.html')


def worked_firms(request):
    return render(request, 'cartridge/worked_firms.html')


def basket(request):
    return render(request, 'cartridge/basket.html')


def massive_change_room(request):
    carts = ''
    message = ''
    display = 'none'
    if request.GET:
        search_post = request.GET.get('search')
        if len(search_post) == 13:
            carts = Cartridges.objects.filter(Q(barcode__icontains=search_post))
            if not carts:
                display = 'block'
                message = 'Такого номера нет в базе'
        else:
            display = 'block'
            message = 'Необходимо ввести 13-значный код'

    form = PlaceUpdateForm()
    # if request.POST:
    #     form = PlaceUpdateForm(request.POST)
    #     barcode_form_cart = form['barcode'].data
    #     barcode_form_place = form['barcode'].data
    #
    #     queryset_form_cart = Cartridges.objects.filter(barcode=barcode_form_cart).values('barcode').values()
    #     queryset_form_place = Placements.objects.filter(barcode=barcode_form_place)

    data = {
        'form': form,
        'message': message,
        'carts': carts,
        'display': display
    }
    return render(request, 'cartridge/massive_change_room.html', data)

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
