'use strict';

$(function () {
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
  });
});
