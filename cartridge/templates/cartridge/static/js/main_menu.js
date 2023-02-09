'use strict';

$(function () {
    loadAjaxMenu();

    function _getState() {
        let state = [];
        $('.menu').find('li > ul').each(function (index) {
            if ($(this).closest('li').hasClass('active')) {
                state.push(index);
            }
        });
        return state;
    }

    function saveMenuState() {
        let state = _getState();
        $('auroramenu', JSON.stringify(state), {expires: 7, path: '/'});
    }

    function clearMenuState() {
        let state = _getState();
        $('auroramenu', JSON.stringify(state), {expires: 7, path: '/'});
    }

    function loadMenuState() {
        let cookie = $.cookie('auroramenu');
        if (!cookie) return;

        let state = JSON.parse(cookie);
        for (let i = 0; i < state.length; ++i) {
            let ul = $('.menu').find('li > ul').eq(state[i]);
            ul.closest('li').addClass('active');
            ul.slideDown({
                complete: function () {
                    set_scroll();
                }
            });
        }
    }

    // let loadAjaxMenu = $.ajax({
    //   method: 'POST',
    //   url: url_data['common:vertical_menu'],
    //   data:  {},
    //   beforeSend: function( xhr, settings ){
    //     let csrftoken = getCookie('csrftoken');
    //     if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
    //       xhr.setRequestHeader('X-CSRFToken', csrftoken);
    //     }
    //   },
    //   success: function(msg) {
    //     if (msg.success) {
    //       $('.left-sidebar').html(msg.menu);
    //     }
    //   },
    //   error: function() {
    //     ;
    //   },
    // });
    function loadAjaxMenu() {
        $('ul.menu > li > span').click(function () {
            $('ul.menu li').removeClass('active');
            $(this).closest('li').addClass('active');
            let checkElement = $(this).next();
            if ((checkElement.is('ul')) && (checkElement.is(':visible'))) {
                $(this).closest('li').removeClass('active');
                checkElement.slideUp('normal');
                clearMenuState();
            }
            if ((checkElement.is('ul')) && (!checkElement.is(':visible'))) {
                $('ul.menu ul:visible').slideUp('normal');
                checkElement.slideDown('normal');
                saveMenuState();
            }
        });
        $('ul.menu > li > ul > li > span').click(function () {
            $('ul.menu > li > ul > li > ul').removeClass('active');
            $(this).closest('li').addClass('active');
            let checkElement = $(this).next();
            if ((checkElement.is('ul')) && (checkElement.is(':visible'))) {
                $(this).closest('li').removeClass('active');
                checkElement.slideUp('normal');
                clearMenuState();
            }
            if ((checkElement.is('ul')) && (!checkElement.is(':visible'))) {
                checkElement.slideDown('normal');
                saveMenuState();
            }
        });

        // loadMenuState();
        bind_scroll_event();
    }

    function bind_scroll_event() {
        let last_start = false;
        $('ul.menu').scroll(function () {
            if (last_start) {
                let scrolled = $(this).scrollTop();
                $.removeCookie("scroll_position");
                $.cookie("scroll_position", scrolled, {expires: 7, path: '/'});
            }
            last_start = true;
        });
    }

    // function set_scroll() {
    //     let scrolled = $.cookie("scroll_position");
    //     if (scrolled) {
    //         $('ul.menu').scrollTop(scrolled);
    //     }
    // }

});
