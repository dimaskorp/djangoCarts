'use strict';

$(function () {
  $(document).foundation();
  $('.filter_room').click( function() {
    $('.room-filter-modal').foundation('reveal', 'open');

    new Promise(function(resolve, reject) {
      let send_dict = {
        'branch': $('.branch_list_filter_room option:selected').val()
      };
      let result = get_tree_structure(send_dict);
      resolve(result);
    }).then(function(result) {
      $('#jstree_rooms').jstree({
        'core': {
          'data': result
        }
      });
    })
  });

  $('a.close-room-filter-modal').on('click', function() {
    $('.room-filter-modal').foundation('reveal', 'close');
    $(window).unbind('keydown');
  });

  // $('.branch_list_filter_room').select2({
  //   dropdownAutoWidth : true,
  //   width: '100%',
  //   ajax: {
  //     url: url_data['organizations:get_br_select2'],
  //     dataType: 'json',
  //     method: 'POST',
  //     delay: 250,
  //     beforeSend: function( xhr, settings ){
  //       const csrftoken = getCookie('csrftoken');
  //       if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
  //         xhr.setRequestHeader('X-CSRFToken', csrftoken);
  //       }
  //     },
  //     data: function (params) {
  //       return {};
  //     },
  //     processResults: function (data, params) {
  //       return { results: data.results };
  //     },
  //     cache: false,
  //   },
  // });

  // $('.branch_list_filter_room').on("select2:select", function(e) {
  //   new Promise(function(resolve, reject) {
  //     let data = e.params.data;
  //     let send_dict = {
  //       'branch': data.id
  //     };
  //     let result = get_tree_structure(send_dict);
  //     resolve(result);
  //   }).then(function(result) {
  //     $('#jstree_rooms').jstree(true).settings.core.data = result;
  //     $('#jstree_rooms').jstree(true).refresh();
  //   })
  // });

  $('.add-filter-room').click(function(event) {
    let select_room = $('#jstree_rooms').jstree('get_selected');
    if (!select_room.length) return;
    select_room = select_room[0];

    let btn = $(event.currentTarget);
    if (btn.hasClass('disabled')) { return; }
    btn.addClass('disabled');

    $.ajax({
      url: url_data['organizations:set_filter_room'],
      type: 'POST',
      data: {select_room: select_room},
      beforeSend: function( xhr, settings ){
        const csrftoken = getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
      },
      success: function (result) {
        if (result.success) {
          location.reload();
        }
      }
    })
  });

  $('.clear-filter-room').click(function(event) {
    let btn = $(event.currentTarget);
    if (btn.hasClass('disabled')) { return; }
    btn.addClass('disabled');

    $.ajax({
      url: url_data['organizations:clear_filter_room'],
      type: 'POST',
      data: {},
      beforeSend: function( xhr, settings ){
        const csrftoken = getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
      },
      success: function (result) {
        if (result.success) {
          btn.removeClass('disabled');
          location.reload();
        }
      }
    })
  });

  $('.find-by-room-name').click(function() {
    new Promise(function(resolve, reject) {
      let send_dict = {
        'branch': $('.branch_list_filter_room option:selected').val(),
        'room': $('.room-name').val()
      };
      let result = get_tree_structure(send_dict);
      resolve(result);
    }).then(function(result) {
      $('#jstree_rooms').jstree(true).settings.core.data = result;
      $('#jstree_rooms').jstree(true).refresh();
    })
  });

  async function get_tree_structure(send_dict) {
    let promise = new Promise((resolve, reject) => {
      $.ajax({
        url: url_data["organizations:get_jstree"],
        type: 'POST',
        data: send_dict,
        beforeSend: function( xhr, settings ){
          const csrftoken = getCookie('csrftoken');
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
          }
        },
        success: function (res) {
          if (res.success === false) {
            console.log(res);
            resolve([]);
          }
          if (res.success === true) {
            resolve(res.rendered);
          }
        }
      })
    });
    let result = await promise;
    return result;
  }

});
