from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from .models import Cartridges, Placements
from .forms import ManufacturerForm, NameСartridgeForm, PlacementsForm, CartridgesForm, PlaceUpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.db.models import Q


class CartListView(ListView):
    model = Cartridges
    template_name = 'cartridge/stock.html'
    context_object_name = 'cartridge_list_view'


class CartDetailView(DetailView):
    model = Cartridges
    template_name = 'cartridge/details_view.html'
    context_object_name = 'cartridge_details_view'


def use(request):
    return render(request, 'cartridge/use.html')


def empty(request):
    return render(request, 'cartridge/empty.html')


def worked_firms(request):
    return render(request, 'cartridge/worked_firms.html')


def basket(request):
    return render(request, 'cartridge/basket.html')


class PlaceUpdateView(UpdateView):
    model = Cartridges
    template_name = 'cartridge/massive_change_room.html'

def massive_change_room(request):
    carts = ''
    message = ''
    display = 'none'
    display_msg = 'none'
    if request.GET:
        search_post = request.GET.get('search')
        if len(search_post) == 13:
            carts = Cartridges.objects.filter(Q(barcode__icontains=search_post))
            if not carts:
                display_msg = 'block'
                message = 'Такого номера нет в базе'
            else:
                display = 'block'
        elif len(search_post) == 0:
            display_msg = 'none'
        else:
            display_msg = 'block'
            message = 'Необходимо ввести 13-значный код'
    form = PlaceUpdateView()
    cart = CartridgesForm()
    place = Placements.objects.all()

    if request.POST:
        form = PlaceUpdateView(request.POST)
        barcode_place = form.data['place_number']
        child_detail = Placements.objects.get(barcode=barcode_place)
        detail = Cartridges.objects.filter(placeName=child_detail)
        #
        if detail.exists():
            print("Ok")
        else:
            print("Такого номера нет в базе")

    data = {
        'form': form,
        'message': message,
        'carts': carts,
        'display_msg': display_msg,
        'display': display,
        'cart': cart
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
        if form.is_valid():
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
