'use strict';

let app = angular.module('app', []);

app.controller('MainCtrl', function ($scope, $timeout, $http) {
  // инициализация формы начальными значениями
  $scope.pk = pk;
  $scope.number = number;
  $scope.restorations_count = restorations_count;
  $scope.printed_pages = printed_pages;
  $scope.doc_contract = doc_contract[0];
  $scope.hour_minute = hour_minute;

  function hide_errors() {
    $scope.cart.name.er = false;
    $scope.cart.place.er = false;
    $scope.cart.number.er = false;
    $scope.cart.restorations_count.er = false;
    $scope.cart.printed_pages.er = false;
    $scope.cart.hour_minute.er = false;
  }

  $scope.edit = function (event) {
    $('.spinner').show();
    let btn = $(event.currentTarget);
    if (btn.hasClass('disabled')) {
      return;
    }
    btn.addClass('disabled');
    $('.success_msg').hide();
    let data = {};
    data['name'] = $('.cart_names option:selected').val();
    data['number'] = $scope.number;
    data['place'] = $('.rooms_list option:selected').val();
    data['set_date'] = $('#id_set_date').val();
    data['hour_minute'] = $('#id_hour_minute').val();
    data['printed_pages'] = $scope.printed_pages;
    data['restorations_count'] = $scope.restorations_count;
    data['doc'] = $('#id_doc option:selected').val();
    data['pk'] = $scope.pk;

    let url = url_data['index:edit_info'];
    let csrftoken = getCookie('csrftoken');
    let config = {
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
    };

    data = $.param(data);
    hide_errors();
    $http.post(url, data, config).then(function (data) {
      $('.spinner').hide();
      $('.error_msg').hide();
      btn.removeClass('disabled');
      let error = data.data.error;
      let text = data.data.text;
      hide_errors();
      if (error === 0) {
        $('.error_msg').hide();
        $('.success_msg').show();
        $('.success_msg').html(text);
      }
      if (error === 1) {
        if (text.name) {
          $scope.cart.name.er = text.name[0];
        }
        if (text.place) {
          $scope.cart.place.er = text.place[0];
        }
        if (text.number) {
          $scope.cart.number.er = text.number[0];
        }
        if (text.printed_pages) {
          $scope.cart.printed_pages.er = text.printed_pages[0];
        }
        if (text.restorations_count) {
          $scope.cart.restorations_count.er = text.restorations_count[0];
        }
        if (text.hour_minute) {
          $scope.cart.hour_minute.er = text.hour_minute[0];
        }
      }
      if (error === 2) {
        $('.error_msg').show();
        $('.error_msg').html(text);
      }
    }, function (data) {
      btn.removeClass('disabled');
      $('.spinner').hide();
      $('.error_msg').show();
      $('.error_msg').html('Ошибка');
    });

  }

});


$(function () {
  // $('.cart_names').select2({
  //   dropdownAutoWidth: true,
  //   width: 'calc(100% - 38px)',
  //   ajax: {
  //     url: url_data['index:get_all_names_select2'],
  //     dataType: 'json',
  //     method: 'POST',
  //     delay: 250,
  //     beforeSend: function (xhr, settings) {
  //       let csrftoken = getCookie('csrftoken');
  //       if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
  //         xhr.setRequestHeader('X-CSRFToken', csrftoken);
  //       }
  //     },
  //     data: function (params) {
  //       return {q: params.term};
  //     },
  //     processResults: function (data, params) {
  //       return {results: data.results};
  //     },
  //     cache: false,
  //   },
  // });

  // $('.branch_list').on('select2:select', function (e) {
  //   $('.rooms_list').val(null).trigger('change');
  // });

  // $('.rooms_list').select2({
  //   dropdownAutoWidth: true,
  //   width: 'calc(100% - 38px)',
  //   ajax: {
  //     url: url_data['organizations:get_all_rooms_select2'],
  //     dataType: 'json',
  //     method: 'POST',
  //     delay: 250,
  //     beforeSend: function (xhr, settings) {
  //       let csrftoken = getCookie('csrftoken');
  //       if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
  //         xhr.setRequestHeader('X-CSRFToken', csrftoken);
  //       }
  //     },
  //     data: function (params) {
  //       return {branch: $('.branch_list').val(), q: params.term};
  //     },
  //     processResults: function (data, params) {
  //       return {results: data.results};
  //     },
  //     cache: false,
  //   },
  // });

  // $('.doc_contract').select2({
  //   dropdownAutoWidth: true,
  //   width: 'calc(100% - 38px)',
  //   ajax: {
  //     url: url_data['docs:deliveres_contracts'],
  //     dataType: 'json',
  //     method: 'POST',
  //     delay: 250,
  //     allowClear: true,
  //     beforeSend: function (xhr, settings) {
  //       let csrftoken = getCookie('csrftoken');
  //       if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
  //         xhr.setRequestHeader('X-CSRFToken', csrftoken);
  //       }
  //     },
  //     data: function (params) {
  //       return {q: params.term};
  //     },
  //     processResults: function (data, params) {
  //       return {results: data.results};
  //     },
  //     cache: false,
  //   },
  // });
  $('#id_hour_minute').timepicker({
    show2400: true,
    timeFormat: 'H:i',
    step: 1,
    scrollDefault: '11:00',
  });
  if (typeof pk !== 'undefined') {
    $('.cart_names').append($('<option></option>')
      .attr('value', names[0]['pk'])
      .text(names[0]['name']))
      .val(names[0]['pk']);

    $('.rooms_list').append($('<option></option>')
      .attr('value', rooms[0]['pk'])
      .text(rooms[0]['name']))
      .val(rooms[0]['pk']);

    $('.doc_contract').append($('<option></option>')
      .attr('value', doc_contract[0]['pk'])
      .text(doc_contract[0]['name']))
      .val(doc_contract[0]['pk']);

    $('.branch_list').append($('<option></option>')
      .attr('value', branch[0]['pk'])
      .text(branch[0]['name']))
      .val(branch[0]['pk']);

  } else {
    $('#id_hour_minute').val('11:00').trigger('change'); // set 11:00
  }

  $('.add_items').click(function (e) {
    /* Выполняем проверку на принадлежность орг. юниту*/
    if ($(this).hasClass('disabled')) {
      return false;
    }
    let cart_name = $('#id_cartName option:selected').val();
    let place = $('#id_place option:selected').val();
    let docum = $('#id_doc option:selected').val();
    let cont = parseInt($('#id_cartCount').val());
    let cart_type = $(this).attr('data');
    let cart_number = $('#id_manualNumber').val();
    let set_date = $('#id_set_date').val();
    let set_time = $('#id_hour_minute').val();
    let tumbler = $('.cmn-toggle-1').is(':checked');

    let tumbler_2 = $('.cmn-toggle-2').is(':checked');

    if (tumbler && !cart_number) {
      $('.cart_number_error').show();
    } else {
      $('.cart_number_error').hide();
    }

    if (tumbler_2 && !set_time) {
      $('.time_error').show();
    } else {
      $('.time_error').hide();
    }

    if (!cart_name) {
      $('.cart_name_error').show();
    } else {
      $('.cart_name_error').hide();
    }  // cart_count_error

    if (!cont) {
      $('.cart_count_error').show();
    } else {
      $('.cart_count_error').hide();
    }
    if (place === '0') {
      $('.cart_sklad_error').show();
      place = false;
    } else {
      $('.cart_sklad_error').hide();
    }
    if (!place) {
      $('.cart_sklad_error').show();
    } else {
      $('.cart_sklad_error').hide();
    }

    // далее идёт сложная логическая функция описанная в файле /static/other/table.xls
    let flag = cart_name && place && cont && ((!tumbler && !cart_number) || (!tumbler && cart_number) || (tumbler && cart_number && !cont) || (tumbler && cart_number))
    // старое значение cart_name && cont && cart_sklad
    // flag - отправляем данные на сервер, если значение булевой функции Истина
    if (flag) {
      if (tumbler) {
        tumbler = 1;
      } else {
        tumbler = 0;
      }

      if (tumbler_2) {
        tumbler_2 = 1;
      } else {
        tumbler_2 = 0;
      }
      let send_dict = {}; // странспортный словарь для передачи данных на сервер
      send_dict['cartName'] = cart_name;
      send_dict['doc'] = docum;
      send_dict['cartCount'] = cont;
      send_dict['cart_type'] = cart_type;
      send_dict['place'] = place;
      send_dict['cart_number'] = cart_number;
      send_dict['tumbler'] = tumbler;
      send_dict['tumbler_2'] = tumbler_2;
      send_dict['hour_minute'] = set_time;
      send_dict['set_date'] = set_date;
      $(this).addClass('disabled');
      let btn = $(this);
      $.ajax({
        method: 'POST',
        url: url_data['index:ajax_add_session_items'],
        data: send_dict,
        beforeSend: function (xhr, settings) {
          $('.spinner').show();
          let csrftoken = getCookie('csrftoken');
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
          }
        },
        success: function (msg) {
          // Прячем ссылку закачки pdf файлов
          $('.download_pdf').hide();
          if (msg.error === '1') {
            $('.spinner').hide();
            $('.success_msg').hide();
            $('.error_msg').show();
            $('.error_msg').html(msg.mes);
          }
          if (msg.error === '0') {
            $('.spinner').hide();
            $('.error_msg').hide();
            $('.session_data').html(msg.html);
            $('.success_msg').show();
            $('.success_msg').html(msg.mes);
          }
          setTimeout(function () {
            btn.removeClass('disabled');
          }, 2000);
        },
        error: function () {
          $('.error_msg').show();
          $('.error_msg').html('Ошибка на стороне сервера');
          $('.spinner').hide();
          btn.removeClass('disabled');
        },
      });
    }
  });

  // $('.branch_list').select2({
  //   dropdownAutoWidth: true,
  //   width: 'calc(100% - 38px)',
  //   ajax: {
  //     url: url_data['organizations:get_br_select2'],
  //     dataType: 'json',
  //     method: 'POST',
  //     delay: 250,
  //     beforeSend: function (xhr, settings) {
  //       let csrftoken = getCookie('csrftoken');
  //       if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
  //         xhr.setRequestHeader('X-CSRFToken', csrftoken);
  //       }
  //     },
  //     data: function (params) {
  //       return {org: $('#id_org').val(), q: params.term};
  //     },
  //     processResults: function (data, params) {
  //       return {results: data.results};
  //     },
  //     cache: false,
  //   },
  // });

  $('.branch_list').on("select2:select", function (e) {
    $('.rooms_list').val(null).trigger('change');
  });

  $('.remove_item').click(function () {
    // удаление объекта в сессионной корзине
    let selected = [];
    let session_var = $(this).attr('session_var');
    $('.p_checkboxes input:checked').each(function () {
      if ($(this).attr('value')) {
        selected.push($(this).attr('value'));
      }
    });
    if (selected.length === 0) {
      return;
    }
    $.ajax({
      method: 'POST',
      url: url_data["index:clear_basket_session"],
      data: {'selected[]': selected, 'session_var': session_var},
      beforeSend: function (xhr, settings) {
        $('.session_spinner').show();
        let csrftoken = getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
      },
      success: function (msg) {
        $('.session_spinner').hide();
        if (msg.error === '0') {
          let class_name = '';
          $('.count_carts').html(msg.count_carts);
          if (msg.text) {
            for (let i = 0; i < msg.text.length; i++) {
              class_name = '.cart_item_' + msg.text[i];
              $(class_name).remove();
            }
          } else {
            $('.p_checkboxes').each(function () {
              $('.wrapper_add_scanner_items').hide();
              $(this).remove();
              $('.count_carts').html(0);
            });
          }
        }

      },
      error: function (msg) {
        $('.session_spinner').hide();
        console.log(msg);
      },
    });

  });


  let add_new_cart_from_barcode = $('.add_cart_from_barcode');
  // Если происходит добавления новых картриджей с помощью
  // сканера штрихкодов.
  if (add_new_cart_from_barcode.length) {
    $(window).keydown(function (event) {
      // устанавливаем перехватчик нажатий клавиши Enter для сканеров
      // штрих кодов которые добавляют символ перевода строки
      // самостоятельно
      if (event.keyCode == 13) {
        event.preventDefault();
        return false;
      }
    });
    $('#id_cartNumber').focus();
    $('.set_focus').click(function () {
      $('#id_cartNumber').focus();
      $('#id_scan_number').focus();
    });

    let pressed = false;
    let chars = [];
    $('#id_cartNumber').keypress(function (e) {
      chars.push(String.fromCharCode(e.which));
      if (pressed == false) {
        setTimeout(function () {
          if (chars.length >= 1) {
            let barcode = chars.join("");
            //console.log("Barcode Scanned: " + barcode);
            $("#id_cartNumber").val(barcode);
            add_elememts_in_sessions();
          }
          chars = [];
          pressed = false;
        }, 500);
      }
      pressed = true;
    });
  }

  $('.add_items_from_barcode').click(function () {
    // добавление пустых или новых на склад
    if ($(this).hasClass('disabled')) {
      return;
    }
    let session_var = $(this).attr('session_var');
    $(this).addClass('disabled');
    let button = $(this);
    $.ajax({
      method: 'POST',
      url: url_data["index:add_items_in_stock_from_session_basket"],
      data: {'session_var': session_var},
      beforeSend: function (xhr, settings) {
        $('.session_spinner').show();
        const csrftoken = getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
      },
      success: function (msg) {
        $('.session_spinner').hide();
        if (msg.error == '0') {
          $('.success_msg').show();
          $('.success_msg').text(msg.text);
          $('.error_msg').hide();
          $('.p_checkboxes').each(function () {
            $('.wrapper_add_scanner_items').hide();
            $(this).remove();
          });
        }
        if (msg.error == '1') {
          $('.success_msg').hide();
          $('.error_msg').show();
          $('.error_msg').text(msg.text);
        }
        setTimeout(function () {
          button.removeClass('disabled');
        }, 2000);

      },
      error: function (msg) {
        $('.session_spinner').hide();
        console.log(msg);
      },
    });

  });


  function add_elememts_in_sessions() {
    /*  Добавление едениц расходных материалов с сканер штрихкода  */
    let cart_number = $('#id_cartNumber').val();
    let cart_name = $('#id_cartName option:selected').val();
    let cart_sklad = $('#id_place option:selected').val();
    let docum = $('#id_doc option:selected').val();
    let cart_type = $('#id_cartNumber').attr('data');

    let tumbler = $('.cmn-toggle-2').is(':checked');

    let valid_date_time = false;
    let set_date = '';
    let set_time = '';

    if (tumbler) {
      set_date = $('#id_set_date').val();
      set_time = $('#id_hour_minute').val();
      if (set_time) {
        $('.time_error').hide();
      } else {
        $('.time_error').show();
      }
      if (set_date) {
        $('.date_error').hide();
      } else {
        $('.date_error').show();
      }

      // если данные введены, то разрешаем отправку формы
      if (set_date && set_time) {
        valid_date_time = true;
      }

    } else {
      let currentdate = new Date();
      let date_str = currentdate.getDate() + "." + (currentdate.getMonth() + 1) + "." + currentdate.getFullYear();
      let time_str = currentdate.getHours() + ":" + currentdate.getMinutes();
      valid_date_time = true;
      set_date = date_str;
      set_time = time_str;
    }

    if (!cart_number) {
      $('.cart_number_error').show();
    } else {
      $('.cart_number_error').hide();
    }

    if (!cart_name) {
      $('.cart_name_error').show();
    } else {
      $('.cart_name_error').hide();
    }

    if (!cart_sklad) {
      $('.cart_sklad_error').show();
    } else {
      $('.cart_sklad_error').hide();
    }

    if (!(cart_name && cart_sklad && cart_number && valid_date_time)) {
      return;
    }
    let send_dict = {};
    send_dict['cartNumber'] = cart_number;
    send_dict['cartName'] = cart_name;
    send_dict['doc'] = docum;
    send_dict['cart_type'] = cart_type;
    send_dict['place'] = cart_sklad;
    send_dict['set_date'] = set_date;
    send_dict['hour_minute'] = set_time;
    send_dict['tumbler'] = tumbler;
    $.ajax({
      method: 'POST',
      url: url_data['index:ajax_add_session_items_from_barcode'],
      data: send_dict,
      beforeSend: function (xhr, settings) {
        $('.spinner').show();
        const csrftoken = getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
      },
      success: function (msg) {
        // Прячем ссылку закачки pdf файлов
        $('#id_cartNumber').val('');
        $('.download_pdf').hide();
        $("#id_cartNumber").focus();
        if (msg.error == '1') {
          $('.spinner').hide();
          $('.success_msg').hide();
          $('.error_msg').show();
          $('.error_msg').html(msg.mes);
        }

        if (msg.error == '0') {
          $('.spinner').hide();
          $('.error_msg').hide();
          $('.count_carts').html(msg.count_carts);
          $('.session_data').html(msg.html);
          $('.success_msg').show();
          $('.success_msg').html(msg.mes);
          $('.add_cart_from_barcode').html(msg.html);
          $('.wrapper_add_scanner_items').show();
          $('div.p_checkboxes').click(function (event) {
            // TODO: улучшитель юзабилити таблиц, при клике по
            // строке выбирается чекбокс
            if (event.target.type !== 'checkbox') {
              $(':checkbox', this).trigger('click');
            }

            if (event.target.type !== 'radio') {
              $(':radio', this).trigger('click');
            }

          });
        }
      },
      error: function () {
        $("#id_cartNumber").focus();
        $('.error_msg').show();
        $('.error_msg').html('Server error :(');
        $('.spinner').hide();
      },
    });
    return false;
  }

  $('.generate_pdf').click(function () {
    $('.download_pdf').hide();
    let cart_type = $(this).attr('data');
    $.ajax({
      method: 'POST',
      url: url_data['docs:generate_pdf'],
      data: {'cart_type': cart_type},
      beforeSend: function (xhr, settings) {
        $('.spinner_pdf').show();
        const csrftoken = getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
      },
      success: function (msg) {
        $('.spinner_pdf').hide();
        if (msg.url) {
          $('.download_pdf').show();
          $('.download_pdf').attr('href', msg.url)
        }
      },
      error: function () {
        $('.ajax_messages').show();
        $('.success_msg').html('Error');
        $('.spinner_pdf').hide();
      },
    });
  })

  $('.cmn-toggle-2').click(function () {
    /* переключатель для ручного ввода даты РМ */
    if ($('.cmn-toggle-2').is(':checked')) {
      $('.wrapper-manual-datetime').show('slow');
      $('#id_date').focus();
      // On

    } else {
      // Off
      $('.wrapper-manual-datetime').hide('slow');

      $('#id_filter_ca').focus();
      let now = new Date();
      let cmonth = now.getMonth() + 1;
      let prepare_str = '';
      if (cmonth < 10) {
        prepare_str = now.getDate() + '/0' + cmonth + '/' + now.getFullYear();
      } else {
        prepare_str = now.getDate() + '/' + cmonth + '/' + now.getFullYear();
      }

      $('#id_date').val(prepare_str);
    }
    // очищаем и прячем диагностические сообщения
    $('.success_msg').html('');
    $('.error_msg').html('');
    $('.success_msg').hide();
    $('.error_msg').hide();

  });

  $('.clear_session').click(function () {
    let cart_type = $(this).attr('data');
    $.ajax({
      method: 'POST',
      url: url_data['index:clear_session'],
      data: {'cart_type': cart_type},
      beforeSend: function (xhr, settings) {
        $('.spinner_pdf').show();
        const csrftoken = getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
      },
      success: function (msg) {
        $('.spinner_pdf').hide();
        $('.download_pdf').hide();
        $('.session_data').html('');
        $('.wrapper_add_scanner_items').hide();
        $('.count_carts').html(0);
        // TODO унифицировать html классы для разных шаблонов
        $('.add_cart_from_barcode').html('');
        $('.ajax_messages').show();
        $('.success_msg').html(msg.mes);
      },
      error: function () {
        $('.ajax_messages').show();
        $('.success_msg').html('Server error :(');
        $('.spinner_pdf').hide();
      },
    });
  });


});
