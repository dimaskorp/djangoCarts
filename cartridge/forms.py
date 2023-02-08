from .models import Cartridges, Manufacturer, NameСartridge, Placements
from django.forms import ModelForm, TextInput, Textarea, Select, NumberInput, DateTimeInput, DateField, DateTimeField


class ManufacturerForm(ModelForm):  # форма Производитель
    class Meta:
        model = Manufacturer
        fields = ['manufacturer', 'comments']
        widgets = {
            'manufacturer': TextInput(attrs={
                'name': 'name',
                'maxlength': "256",
                'required': "",
                'id': "id_name"
            }),
            'comments': Textarea(attrs={
                'name': 'comment',
                'cols': '40',
                'rows': '10',
                'id': "id_comment"
            })
        }


class PlacementsForm(ModelForm):  # форма Помещения
    class Meta:
        model = Placements
        fields = ['barcode', 'name', 'branch']
        widgets = {
            'name': TextInput(attrs={
                'required': "True",
            }),
            'branch': TextInput(attrs={
                'required': "False",
            }),
            'barcode': NumberInput(attrs={
                'name': 'number_barcode',
                'id': "id_barcode"
            })
        }


class CartridgesForm(ModelForm):  # Картриджи
    class Meta:
        model = Cartridges
        date = DateTimeField()
        fields = ['barcode', 'cartName', 'placeName', 'manufacturerName', 'date']
        dateTimeOptions = {
            'format': 'dd/mm/yyyy HH:ii P',
            'autoclose': True,
            'showMeridian': True
        }
        widgets = {
            'barcode': NumberInput(attrs={
                'name': 'manualNumber',
                'id': "id_manualNumber"
            }),
            'cartName': Select(attrs={
                'id': "id_cartName",
                'required': "True",
                'class': 'select-selection--single',
                'style': "width: calc(100% - 38px);"
            }),
            'placeName': Select(attrs={
                'id': 'id_place',
                'name': 'place',
                'required': "True",
                'class': 'select-selection--single',
                'style': "width: calc(100% - 38px);"
            }),
            'manufacturerName': Select(attrs={
                'id': 'id_manufacturer',
                'name': 'manufacturer',
                'required': "True",
                'class': 'select-selection--single',
                'style': "width: calc(100% - 38px);"
            }),
            # 'date': DateTimeField(attrs={
            #     'id': 'id_set_dat',
            #     'name': 'set_dat',
            #     'required': "True",
            #     'style': "width: calc(100% - 38px);"
            # }, input_formats=['%d.%m.%Y %H:%M'])

        }


class NameСartridgeForm(ModelForm):  # форма Названия картриджей
    class Meta:
        model = NameСartridge
        fields = ['name', 'comments']
        widgets = {
            'name': TextInput(attrs={
                'required': "True",
                'id': "id_cart_name"
            }),
            'comments': Textarea(attrs={
                'name': 'comment',
                'cols': '40',
                'rows': '10',
                'id': "id_comment"
            })
        }