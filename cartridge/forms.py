from .models import Cartridges, Manufacturer, NameСartridge, Placements
from django.forms import ModelForm, TextInput, Textarea, Select, NumberInput, DateTimeInput


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
                'name': 'branch',
            }),
            'barcode': NumberInput(attrs={
                'name': 'number_barcode',
                'id': "id_barcode"
            })
        }


class CartridgesForm(ModelForm):  # Картриджи
    class Meta:
        model = Cartridges
        fields = ['barcode', 'cartName', 'placeName', 'manufacturerName', 'date']
        widgets = {
            'barcode': NumberInput(attrs={
                'id': "id_manualNumber",
                'style': "width: calc(100% - 38px);",
            }),
            'cartName': Select(attrs={
                'id': "id_cartName",
                'required': "True",
                'class': 'select-selection--single',
                'style': "width: calc(100% - 38px);"
            }),
            'placeName': Select(attrs={
                'id': 'id_place',
                'required': "True",
                'class': 'select-selection--single',
                'style': "width: calc(100% - 38px);"
            }),
            'manufacturerName': Select(attrs={
                'id': 'id_manufacturer',
                'required': "True",
                'class': 'select-selection--single',
                'style': "width: calc(100% - 38px);"
            }),
            'date': DateTimeInput(attrs={
                'id': 'datetimepicker4',
                'required': "True"
            })
        }


class PlaceUpdateForm(ModelForm):  # Картриджи
    class Meta:
        model = Cartridges
        fields = ['placeName']
        widgets = {
             'placeName': NumberInput(attrs={
                'id': 'id_place',
                'required': "True",
                'style': "width: calc(100% - 38px);"
            })
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
