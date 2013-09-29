$(function() {
    var datetimepickerOptions = {
        autoclose: true,
        minView: 0,
        minuteStep: 15,
        startDate: (new Date())
    };

    $('#voting_deadline').datetimepicker(datetimepickerOptions);
    $('#voting_option_0').datetimepicker(datetimepickerOptions).on('changeDate', function() {
        $('#add-datepair').attr('disabled', null);
    });

    $('#add-datepair').on('click', function() {
        var $datepickers = $('.voting-option'),
            template = Mustache.template('datetimepicker'),
            $previous = $datepickers.last(),
            html = template.render({
                nr: $datepickers.length,
                previous: $previous.find('[name=voting_options]').val()
            });

        $(html).insertAfter($previous);
        $('#voting_option_' + $datepickers.length).datetimepicker(
            datetimepickerOptions);

        $('.remove').click(function () {
            $(this).parent().remove();
        });

        return false;
    });

    $('#id_emails').tagsinput({
        tagClass: function(item) {
            return (/(.+)@(.+){2,}\.(.+){2,}/.test(item) ? 'label label-success' : 'label label-danger');
        }
    });
});

