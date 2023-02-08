$( function(){
    $(document).bind('keydown', 'return', function() {
        $('.add_items').click();
        $('.add_items_from_barcode').click();

        $('.force_move_to_transfer').click();

    });

    $(document).bind('keydown', 'esc', function() {
        $('.close_modal_win').click();
    });
});
