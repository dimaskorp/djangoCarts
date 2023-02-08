'use strict';

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie != '') {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      let cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function add_button_event_handler() {
  $('a.add').each(function () {
    let plus_button = $(this);
    plus_button.bind('click', function (event) {
      $('.add-iframe-modal').contents().find('body').html('');
      event.preventDefault();
      event.stopPropagation();
      const url = plus_button.attr('href') + '?modal=1';
      const show_dialog = Boolean(plus_button.attr('href'));
      let title_str = plus_button.attr('title');
      $('.add-dictionary-modal').css('display', 'block');
      // $('.add-dictionary-modal').dialog({
      //   autoOpen: false,
      //   width: 600,
      //   height: 500,
      //   modal: true,
      //   title: title_str,
      //   open: function (ev, ui) {
      //     $('.add-iframe-modal').attr('src', url);
      //   },
      // });
      // if (show_dialog) {
      //   $('.add-dictionary-modal').dialog('open');
      // }
    });
  });
}

$(function () {
  $('.set_focus').click(function () {
    $('#id_cartNumber').focus();
    $('#id_scan_number').focus();
  });


  $('.back').click(function () {
    window.history.back();
  });

  add_button_event_handler();

});


let getUrlParameter = function getUrlParameter(sParam) {
  // http://stackoverflow.com/questions/19491336/get-url-parameter-jquery
  var sPageURL = decodeURIComponent(window.location.search.substring(1)),
    sURLVariables = sPageURL.split('&'),
    sParameterName,
    i;

  for (let i = 0; i < sURLVariables.length; i++) {
    sParameterName = sURLVariables[i].split('=');

    if (sParameterName[0] === sParam) {
      return sParameterName[1] === undefined ? true : sParameterName[1];
    }
  }
};


window.addEventListener('error', (event) => {
  $.ajax({
    method: 'POST',
    url: url_data['service:js_errors'],
    data: {
      'msg': event.message,
      'colno': event.colno,
      'filename': event.filename,
      'page': window.location.href,
    },
    beforeSend: function (xhr, settings) {
      let csrftoken = getCookie('csrftoken');
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
      }
    },
    success: function (msg) {},
    error: function () {},
  });

});


$(function () {

  /* checkbox and radiobutton widget */
  $('table.checkboxes tr:not(:first), \
        table.users-list tr:not(:first), \
        table.transfer_list_to_firm tr:not(:first)').click(function (event) {
    // улучшитель юзабилити таблиц, при клике по строке выбирается чекбокс
    var input_obj = $(this).find('input');
    if (input_obj.prop('checked')) {
      input_obj.prop('checked', false);
    } else {
      input_obj.prop('checked', true);
    }
    $('tr input[type="radio"]').each(function () {
      $(this).parent().parent().removeClass('selected');
    });
    input_obj.parent().parent().toggleClass('selected');
    event.defaultPrevented;
  });

  $('input.checkbox, input:radio').click(function (event) {
    var input_type = $(this).attr('type');
    if (input_type === 'radio') {
      $('table.checkboxes tr').each(function () {
        $(this).removeClass('selected');
      })
    }
    $(this).parent().parent().toggleClass('selected');
    event.stopPropagation();
  });

  /* end checkbox and radiobutton widget */

  $('.no_follow').click(function (event) {
    event.preventDefault();
    event.stopPropagation();
    return false;
  });

  $('.cmn-toggle-1').click(function () {
    if ($('.cmn-toggle-1').is(':checked')) {
      $('.wrapper-manual-number').show('slow');
      $('.wrapper-counter-items').hide('slow');
      $('#id_manualNumber').focus();
      $('#id_cartCount').val(1);
      // On
    } else {
      // Off
      $('.wrapper-manual-number').hide('slow');
      $('.wrapper-counter-items').show('slow');
      $('#id_filter_ca').focus();
      $('#id_cartCount').val(0);
    }
    $('.success_msg').html('');
    $('.error_msg').html('');
    $('.success_msg').hide();
    $('.error_msg').hide();

  });

  $('div.p_checkboxes').click(function (event) {
    // улучшитель юзабилити таблиц, при клике по строке выбирается чекбокс
    if (event.target.type !== 'checkbox') {
      $(':checkbox', this).trigger('click');
    }

    if (event.target.type !== 'radio') {
      $(':radio', this).trigger('click');
    }

  });

});

function parse_grid(grid) {
  // функция помощник для облегчения доступа к значениям
  // фильтруемых строк ui-grid.
  let filter_terms = new Object();
  for (let i = 0; i <= grid.columns.length; ++i) {
    if (grid.columns[i]) {
      let key = grid.columns[i].field;
      let value = grid.columns[i].filters[0].term;
      filter_terms[key] = value;
    }
  }
  return filter_terms;
}

function scrolling_ui_grid() {
  let leftPos = $('.ui-grid-canvas').scrollLeft();

  document.onkeydown = function (e) {
    let maxWidth2 = $('.ui-grid-canvas').width();

    switch (e.which) {
      case 37: // left
        leftPos -= 20
        if (leftPos <= 0) {
          leftPos = 0;
        }
        $('.ui-grid-viewport').animate({scrollLeft: leftPos}, 10);
        break;

      case 38: // up
        break;

      case 39: // right
        leftPos += 20;
        if (leftPos >= maxWidth2) {
          leftPos = maxWidth2;
        }
        $('.ui-grid-viewport').animate({scrollLeft: leftPos}, 10);
        break;

      case 40: // down
        break;

      default:
        return; 
    }
  };
}
