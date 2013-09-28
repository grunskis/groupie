$(function() {
    $('#add-datepair').on('click', function() {
        var $datepair = $('.datepair'),
            $datepairs = $datepair.find('.time'),
            template = Mustache.template('add_datepair'),
            html = template.render({nr: $datepairs.length});

        $datepair.append(html);
        $datepair.timepicker();

        return false;
    });

    $('#rem-dates').on('click', function() {
        if( i > 2 ) {
            $(this).parents('p').remove();
            i--;
        }
        return false;
    });
});
