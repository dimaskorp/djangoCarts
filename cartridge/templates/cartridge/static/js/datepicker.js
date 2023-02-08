'use strict';

$(function() {
  let code = 'ru-ru';

  let date_format = 'dd.mm.yy';
  if (code === 'ru-ru') {
    date_format = 'dd.mm.yy';
  }

  if (code === 'en-us') {
    date_format = 'mm/dd/yy';
  }

  $('.datepicker').datepicker({
    dateFormat: date_format,
    showOn: "button",
    buttonImage: "/static/img/calendar.png",
    buttonImageOnly: true,
    buttonText: 'Выберите дату',
  });


  // init calendar widget
  $('.datepicker').datepicker();

});
