$(function () {
    $('.thumbnail').click(function () {
        var $this = $(this),
            $option = $('input[value=' + $this.data('option') + ']'),
            $votes = $(this).next('.nr_of_votes'),
            nr_of_votes = parseInt($votes.data('nr-of-votes'), 10),
            plus_minus = 0;

        if ($this.hasClass('vote-yes')) {
            nr_of_votes = nr_of_votes - 1;
            $this.removeClass('vote-yes').addClass('vote-no');
        } else {
            nr_of_votes = nr_of_votes + 1;
            $this.removeClass('vote-no').addClass('vote-yes');
        }

        $option.trigger('click');

        $votes.text(nr_of_votes + ' ' + owl.pluralize('vote', nr_of_votes));
        $votes.data('nr-of-votes', nr_of_votes);
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
