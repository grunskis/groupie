$(function () {
    $('.thumbnail').click(function () {
        var $this = $(this),
            $option = $('input[value=' + $this.data('option') + ']');

        if ($this.hasClass('vote-yes')) {
            $this.removeClass('vote-yes').addClass('vote-no');
        } else {
            $this.removeClass('vote-no').addClass('vote-yes');
        }

        $option.trigger('click');
    });

    $('.nr_of_votes').each(function () {
        var $option = $(this),
            template = Mustache.template('voters'),
            voters = $option.data('voters');
            
        $option.popover({
            'trigger': 'hover',
            'content': template.render({'voters': voters}),
            'html': true
        });
    });
});
