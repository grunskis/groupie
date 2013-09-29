$(function() {
    var datetimepickerOptions = {
        autoclose: true,
        minView: 0,
        minuteStep: 15,
        startDate: (new Date())
    };

    $('#voting_deadline').datetimepicker(datetimepickerOptions);
    $('#voting_option_0').datetimepicker(datetimepickerOptions);

    $('#add-datepair').on('click', function() {
        var $datepickers = $('.voting-option'),
            template = Mustache.template('datetimepicker'),
            $previous = $datepickers.last(),
            html = template.render({
                nr: $datepickers.length,
                previous: $previous.find('[name=voting_options]').val()
            });

        $(html).insertAfter($('#initial_option'));
        $('#voting_option_' + $datepickers.length).datetimepicker(
            datetimepickerOptions);

        $('.remove').click(function () {
            $(this).parent().parent().remove();
        });

        return false;
    });

    $('#id_emails').tagsinput({
        tagClass: function(item) {
            return (/(.+)@(.+){2,}\.(.+){2,}/.test(item) ? 'label label-success' : 'label label-danger');
        }
    });
});

