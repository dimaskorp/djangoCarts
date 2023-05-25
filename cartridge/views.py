from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from .models import Cartridges, Placements, NameСartridge, Manufacturer, ChangeLog
from .forms import ManufacturerForm, NameСartridgeForm, PlacementsForm, CartridgesForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from io import BytesIO
import datetime
import barcode
import random
import json

list_checks = []
numbers = []


class CartListView(ListView):
    model = Cartridges
    template_name = 'cartridge/stock.html'

    def get_context_data(self, **kwargs):
        context = super(CartListView, self).get_context_data(**kwargs)
        context['cartridge_list_view'] = Cartridges.objects.filter(placeName=2)
        context['qs_json'] = json.dumps(list(Cartridges.objects.values()), cls=DjangoJSONEncoder)
        return context


class UseListView(ListView):
    model = Cartridges
    template_name = 'cartridge/use.html'

    def post(self, request, *args, **kwargs):
        checks = request.POST.getlist('check')
        if self.request.POST:
            for num in checks:
                Cartridges.objects.filter(barcode=num).update(placeName='0')
            return render(request, 'cartridge/use.html')

    def get_context_data(self, **kwargs):
        context = super(UseListView, self).get_context_data(**kwargs)
        context['cartridge_list_view'] = Cartridges.objects.exclude(placeName=0).exclude(placeName=1).exclude(placeName=2).exclude(placeName=3)
        context['qs_json'] = json.dumps(list(Cartridges.objects.values()), cls=DjangoJSONEncoder)
        return context


class EmptyListView(ListView):
    model = Cartridges
    template_name = 'cartridge/empty.html'

    def get_context_data(self, **kwargs):
        context = super(EmptyListView, self).get_context_data(**kwargs)
        context['empty_carts'] = Cartridges.objects.filter(placeName=0)
        return context


class WorkedfirmsListView(ListView):
    model = Cartridges
    template_name = 'cartridge/worked_firms.html'

    def get_context_data(self, **kwargs):
        context = super(WorkedfirmsListView, self).get_context_data(**kwargs)
        context['worked_carts'] = Cartridges.objects.filter(placeName=1)
        return context


class BasketListView(ListView):
    model = Cartridges
    template_name = 'cartridge/basket.html'

    def get_context_data(self, **kwargs):
        context = super(BasketListView, self).get_context_data(**kwargs)
        context['basket'] = Cartridges.objects.filter(placeName=3)
        return context


class CartDetailView(DetailView):
    model = Cartridges
    template_name = 'cartridge/details_view.html'
    context_object_name = 'cartridge_details_view'
    success_url = reverse_lazy('add_items')

    def get_context_data(self, **kwargs):
        context = super(CartDetailView, self).get_context_data(**kwargs)
        history = ChangeLog.objects.filter(barcode_h=kwargs['object'].barcode)
        context['history'] = history
        return context


class EditUpdateView(UpdateView):
    model = Cartridges
    form_class = CartridgesForm
    template_name = 'cartridge/edit_cartridge_info.html'
    success_url = reverse_lazy('stock')


class CartDeleteView(DeleteView):
    model = Cartridges
    template_name = 'cartridge/stock.html'
    success_url = reverse_lazy('stock')


def massive_change_room(request):
    carts = ''
    message = ''
    display_error_msg = 'none'
    display_success_msg = 'none'
    display = 'none'
    autofocus = 'autofocus'
    display_form = 'none'

    if request.GET:
        search_post = request.GET.get('search')
        if len(search_post) > 13:
            display_error_msg = 'block'
            message = 'Максимальная длина номера 13 символов'
            autofocus = 'autofocus'
        elif len(search_post) == 0:
            display_error_msg = 'none'
            autofocus = 'autofocus'
        else:
            carts = Cartridges.objects.filter(barcode=search_post)
            if carts:
                display_form = 'block'
                numbers.append(search_post)
                autofocus = ''
            else:
                display_error_msg = 'block'
                message = 'Такого номера нет в базе'
                autofocus = 'autofocus'

    cart = CartridgesForm()
    place = PlacementsForm()

    if request.POST:

        place = PlacementsForm(request.POST)
        barcode_place = place.data['barcode']

        if len(barcode_place) > 13:
            display_error_msg = 'block'
            message = 'Максимальная длина номера 13 символов'
        elif len(barcode_place) == 0:
            display_error_msg = 'none'
        else:
            places = Placements.objects.filter(barcode=barcode_place)
            if places:  # если номер есть в базе
                place_id = [i.pk for i in places][0]  # получаем id помещения
                if numbers:  # если картридж отсканирован
                    Cartridges.objects.filter(barcode=numbers[0]).update(placeName=place_id, date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

                    p = Placements.objects.get(id=place_id)
                    ChangeLog.objects.create(barcode_h=numbers[0], placeName_h=p, date_h=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), comments_h=f'Картридж {numbers[0]} передан на {p}')  # запись в журнал изменений

                    display_success_msg = 'block'
                    message = 'Картридж передан'
                    carts = Cartridges.objects.filter(barcode=numbers[0])
                    numbers.clear()
                    place = PlacementsForm(None)
                    autofocus = 'autofocus'
                    display_form = 'none'
                else:
                    display_error_msg = 'block'
                    message = 'Не выбран картридж'
                    place = PlacementsForm(None)
                    autofocus = 'autofocus'
                    display_form = 'none'
            else:
                if numbers:
                    carts = Cartridges.objects.filter(barcode=numbers[0])
                    display_error_msg = 'block'
                    message = 'Такого помещения нет в базе'
                    place = PlacementsForm(None)
                    autofocus = ''
                    display_form = 'block'

    data = {
        'message': message,
        'carts': carts,
        'display': display,
        'display_error_msg': display_error_msg,
        'display_success_msg': display_success_msg,
        'cart': cart,
        'place': place,
        'page': massive_change_room,
        'autofocus': autofocus,
        'display_form': display_form
    }
    return render(request, 'cartridge/massive_change_room.html', data)


def transfer(request):
    checks = request.POST.getlist('check')
    carts_all = Cartridges.objects.all()
    list_checks.append(checks)
    message = ''
    display_error_msg = 'none'
    display_success_msg = 'none'
    display = 'none'
    nam = ''
    manuf = ''
    form = ''
    if request.POST:
        form = CartridgesForm(request.POST)['placeName']
        id_name = form.data
        if id_name:
            p = Placements.objects.get(id=id_name)
            for i in list_checks[0]:
                Cartridges.objects.filter(barcode=i).update(placeName=id_name, date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

                ChangeLog.objects.create(barcode_h=i, placeName_h=p, date_h=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), comments_h=f'Картридж {i} передан на {p}')

            list_checks.clear()
            return redirect('stock')
    data = {
        'carts': carts_all,
        'checks': checks,
        'form': form,
        'nam': nam,
        'manuf': manuf,
        'message': message,
        'display': display,
        'display_error_msg': display_error_msg,
        'display_success_msg': display_success_msg,
    }
    return render(request, 'cartridge/transfer_for_use.html', data)


def basket(request):
    return render(request, 'cartridge/basket.html')


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

            n = form.data['name']
            ChangeLog.objects.create(cartName_h=n, date_h=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), comments_h=f'Добавлена модель {n}')  # запись в журнал изменений

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
    place = Placements.objects.order_by('name').exclude(id=1)
    count = Placements.objects.count()
    error = ''
    display = 'none'
    name = ''
    msg_display = 'none'
    err_display = 'none'
    if request.POST:
        form = PlacementsForm(request.POST)
        bar = form.data["barcode"]
        if bar == '':
            random_num = random.randint(1111111111111, 9999999999999)
            updated_data = request.POST.copy()
            updated_data.update({'barcode': random_num})
            form = PlacementsForm(data=updated_data)
        else:
            updated_data = request.POST.copy()
            updated_data.update({'barcode': bar})
            form = PlacementsForm(data=updated_data)
        if form.is_valid():
            form.save()

            b = form.data['barcode']
            p = form.data['name']
            ChangeLog.objects.create(barcode_h=b, placeName_h=p, date_h=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), comments_h=f'Добавлено помещение(статус) {p} с кодом {b}')  # запись в журнал изменений

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

            m = form.data['manufacturer']
            ChangeLog.objects.create(manufacturerName_h=m, date_h=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), comments_h=f'Добавлен производитель {m}')  # запись в журнал изменений

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


@csrf_protect
@ensure_csrf_cookie
def add_items(request):
    count = Cartridges.objects.count()
    name_cart = Cartridges.objects.order_by('-date')
    msg_display = 'none'
    err_display = 'none'
    display = 'none'
    random_num = ''
    error = ''
    if request.POST:
        form = CartridgesForm(request.POST)
        bar = form.data["barcode"]
        if bar == '':
            random_num = random.randint(1111111111111, 9999999999999)
            updated_data = request.POST.copy()
            updated_data.update({'barcode': random_num})
            form = CartridgesForm(data=updated_data)
        else:
            updated_data = request.POST.copy()
            updated_data.update({'barcode': bar})
            form = CartridgesForm(data=updated_data)
        if form.is_valid():
            form.save()

            b = form.data['barcode']
            c = NameСartridge.objects.get(id=form.data['cartName'])
            m = Manufacturer.objects.get(id=form.data['manufacturerName'])
            p = Placements.objects.get(id=form.data['placeName'])
            ChangeLog.objects.create(barcode_h=b, cartName_h=c, placeName_h=p, manufacturerName_h=m, date_h=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), comments_h=f'Добавлен картридж {m} {c} с кодом {b} в статусе "{p}"')  # запись в журнал изменений

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
        'msg_display': msg_display,
        'err_display': err_display,
        'display': display,
        'carts': name_cart,
        'random_num': str(random_num),
        'count': count
    }
    return render(request, 'cartridge/add_items.html', data)


def print_pl(request):
    checks = request.POST.getlist('check')
    svg_all = []
    for num in checks:
        pl = Placements.objects.get(barcode=num).name
        rv = BytesIO()
        EAN = barcode.get_barcode_class('code39')
        svg = EAN(num, add_checksum=False)
        svg.write(rv, {"module_width": 0.17, "module_height": 8, "font_size": 16, "text_distance": 5, "quiet_zone": 4.5, "human": pl})
        encoded_output = rv.getvalue()
        rv.close()
        svg_all.append(encoded_output.decode('utf-8'))

    data = {
        'barcode_img': svg_all
    }
    return render(request, 'cartridge/print_pl.html', data)


def print_cart(request):
    checks = request.POST.getlist('check')
    svg_all = []
    for num in checks:
        rv = BytesIO()
        EAN = barcode.get_barcode_class('code39')
        svg = EAN(num, add_checksum=False)
        svg.write(rv, {"module_width": 0.17, "module_height": 6, "font_size": 7, "text_distance": 3, "quiet_zone": 3.8})
        encoded_output = rv.getvalue()
        rv.close()
        svg_all.append(encoded_output.decode('utf-8'))

    data = {
        'barcode_img': svg_all
    }
    return render(request, 'cartridge/print_cart.html', data)


def to_firm(request):
    checks = request.POST.getlist('check')
    if request.POST:
        for num in checks:
            Cartridges.objects.filter(barcode=num).update(placeName='1', date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
            p = Placements.objects.get(id=1)
            ChangeLog.objects.create(placeName_h=p, date_h=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), comments_h=f'Картридж {num} передан на {p}')  # запись в журнал изменений

    data = {
    }
    return render(request, 'cartridge/empty.html', data)


def from_firm(request):
    checks = request.POST.getlist('check')
    if request.POST:
        for num in checks:
            Cartridges.objects.filter(barcode=num).update(placeName='2', date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

            p = Placements.objects.get(id=2)
            ChangeLog.objects.create(placeName_h=p, date_h=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), comments_h=f'Картридж {num} передан на {p}')  # запись в журнал изменений

            cl = Cartridges.objects.get(barcode=num)
            if cl.col is None:
                cl.col = 1
            else:
                cl.col += 1
            cl.save()
    data = {
    }
    return render(request, 'cartridge/worked_firms.html', data)



