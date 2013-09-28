$(function() {
    var datetimepickerOptions = {
        autoclose: true,
        minView: 1
    };

    $('#voting_deadline').datetimepicker(datetimepickerOptions);
    $('#voting_option_0').datetimepicker(datetimepickerOptions);

    $('#add-datepair').on('click', function() {
        var $datepickers = $('.voting-option'),
            template = Mustache.template('datetimepicker'),
            html = template.render({nr: $datepickers.length});

        $(html).insertAfter($datepickers.last());
        $('#voting_option_' + $datepickers.length).datetimepicker(
            datetimepickerOptions);

        $('.remove').click(function () {
            $(this).parent().remove();
        });

        return false;
    });

});
