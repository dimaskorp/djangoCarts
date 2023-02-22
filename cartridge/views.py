from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from .models import Cartridges, Placements
from .forms import ManufacturerForm, NameСartridgeForm, PlacementsForm, CartridgesForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class AddCreateView(CreateView):
    form_class = CartridgesForm
    template_name = 'cartridge/add_items.html'
    success_url = reverse_lazy('add_items')
    count = Cartridges.objects.count()
    name_cart = Cartridges.objects.order_by('-date')

    def form_valid(self, form):
        super(AddCreateView, self).form_valid(form)
        return render(self.request, self.template_name, self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        rez = super(AddCreateView, self).get_context_data(**kwargs)
        rez['col'] = self.count
        rez['carts'] = self.name_cart
        return rez


class CartListView(ListView):
    model = Cartridges
    template_name = 'cartridge/stock.html'
    context_object_name = 'cartridge_list_view'

    # def get_context_data(self, **kwargs):
    #     rez = super(CartListView, self).get_context_data(**kwargs)
    #     model = Placements
    #     rez['place'] = model.objects.all()
    #     return rez




class CartDetailView(DetailView):
    model = Cartridges
    template_name = 'cartridge/details_view.html'
    context_object_name = 'cartridge_details_view'
    success_url = reverse_lazy('add_items')


class EditUpdateView(UpdateView):
    model = Cartridges
    form_class = CartridgesForm
    template_name = 'cartridge/edit_cartridge_info.html'
    success_url = reverse_lazy('stock')


class CartDeleteView(DeleteView):
    model = Cartridges
    template_name = 'cartridge/stock.html'
    success_url = reverse_lazy('stock')


numbers = []


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
                    Cartridges.objects.filter(barcode=numbers[0]).update(placeName=place_id)  # получаем id картриджа
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
    checks = ''
    nam = ''
    manuf = ''
    carts = CartridgesForm()
    if request.POST:
        checks = request.POST.getlist('checks')
        for i in checks:
            cart = Cartridges.objects.filter(barcode=i)

            print(cart)


    data = {
        'carts': carts,
        'checks': checks,
        'nam': nam,
        'manuf': manuf

    }
    return render(request, 'cartridge/transfer_for_use.html', data)


def use(request):
    return render(request, 'cartridge/use.html')


def empty(request):
    return render(request, 'cartridge/empty.html')


def worked_firms(request):
    return render(request, 'cartridge/worked_firms.html')


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
