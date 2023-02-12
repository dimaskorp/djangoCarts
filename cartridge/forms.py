{% extends 'cartridge/base.html' %}

{% block title %}Смена местоположения картриджей с помощью сканера штрих-кодов{% endblock %}

{% block submenu %}Картриджи / Смена местоположения картриджей с помощью сканера штрих-кодов{% endblock %}

{% block content %}
    <div class="row">
        <div class="large-4 columns" style="display: {{ display }}">
            <ul class="error_msg" style="display: {{ display }}">
                <li class="success">{{ message }}</li>
            </ul>
        </div>
    </div>
    <div class="row">
        <div class="large-5 columns">
            <form action="{% url 'massive_change_room' %}" method="get">
                <div class="row">
                    <div class="large-12 columns">
                        <label>Отсканированный штрихкод</label>
                        {#                       {{ form.barcode }}#}
                    </div>
                </div>
                <div class="marginTop"></div>
                <div class="row">
                    <div class="large-12 columns">
                        <label>Ввести номер картриджа вручную</label>
                        <div class="input_row">
                            {#                            {{ form.barcode }}#}
                            {#                            <input type="search" name="barcode" id="id_barcodeNumber" class="manual_number" autofocus="autofocus" onkeyup="return lengthBarcode()" required="">#}
                            <input class="manual_number" type="search" autofocus="autofocus" aria-label="Search"
                                   name="search">
                            <script>
                                function lengthBarcode() {
                                    var col = document.getElementById("id_barcodeNumber").value.length
                                    if (col === 0)
                                        document.getElementById('id_placeNumber').disabled = true;
                                    if (col === 13)
                                        document.getElementById('id_placeNumber').disabled = false;
                                    document.getElementById('id_placeNumber').focus();
                                    return true;
                                }
                            </script>
                            <button class="button small-move" type="submit">Поиск</button>
                            {#                            <a title="Найти по номеру" type="submit" class="button no_follow add-session-move-barcode search-zoom" href=""></a>#}

                        </div>
                    </div>
                </div>
            </form>
            <form action="{% url 'massive_change_room' %}" method="post">
                {% csrf_token %}
                <div class="marginTop"></div>
                <div class="row">
                    <div class="large-12 columns">
                        <label class="required">Помещение</label>
                        {#                        {{ form_place.barcode }}#}
                        <a class="dj_button" href="{% url 'tree_list' %}" title="Добавить название помещения"></a>

                        <div class="form_error_text cart_sklad_error">Поле должно быть выбрано</div>
                    </div>
                </div>

                <div class="marginTop55"></div>
                <div class="row">
                    <div class="large-12 columns">
                        <a class="button no_follow set_focus small-focus">Сфокусировать</a>
                        <button class="button small-move" type="submit">Передать</button>
                        {#                        <a class="button small-move" href="">Переместить</a>&nbsp;&nbsp;&nbsp;#}
                        <img class="spinner" src="static/img/loader.gif">
                    </div>
                </div>
            </form>
        </div>
        <div class="large-5 columns">
            <div class="marginTop wrapper_add_scanner_items" style="display:block">
                <a class="button remove-move-item no_follow small-delete-row">Удалить элемент</a>
                <a class="button clear-move-session no_follow small-clear">Очистить сессию</a>
                <span class="count_objects_wrapper">Кол-во:
                    <span class="count_objects">0</span>
                </span>
                <img class="session_spinner" src="static/img/loader.gif">
            </div>
            <div class="marginTop"></div>
            <div class="session-wrapper">
                <div class="p_checkboxes cart_item_${pk}">

                    {% for cart in carts %}
                        <p>{{ forloop.counter }}. {{ cart.barcode }}</p>
                        <p>{{ cart.cartName }}</p>
                        <p>{{ cart.placeName }}</p>
                    {% endfor %}
                    {#                        <input class="checkbox" type='checkbox' name='cart_number' value='${pk}'>#}
                    {#                        {{ queryset_form_cart }}&nbsp;&nbsp;&nbsp;{{ queryset_form_cart }}&nbsp;&nbsp;&nbsp;#}
                    {#                        <span class="ballon">{{ queryset_form_cart }}</span>#}

                    <hr/>
                </div>
            </div>
        </div>
        <div class="large-2 columns"></div>
    </div>
{% endblock %}
