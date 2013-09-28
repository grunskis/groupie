$(function() {
    $('#datetimepicker_0').datetimepicker({autoclose: true});

    $('#add-datepair').on('click', function() {
        var $datepickers = $('.date'),
            template = Mustache.template('datetimepicker'),
            html = template.render({nr: $datepickers.length});

        $(html).insertAfter($datepickers.last());
        $('#datetimepicker_' + $datepickers.length).datetimepicker({
            autoclose: true
        });

        return false;
    });

    $('.datetimepicker .remove').on('click', function () {
        $(this).remove();
    });
});
