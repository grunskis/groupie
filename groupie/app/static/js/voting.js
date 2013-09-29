$(function () {
    var update_popovers = function () {
        $('.nr_of_votes').each(function () {
            var $option = $(this),
                template = Mustache.template('voters'),
                voters = $option.data('voters').split(',');

            voters = voters.filter(function(e) {
                return e;
            });

            $option.popover('destroy').popover({
                'trigger': 'hover',
                'content': template.render({'voters': voters}),
                'html': true
            });
        });
    };

    update_popovers();

    $('.thumbnail').click(function () {
        var $this = $(this),
            $option = $('input[value=' + $this.data('option') + ']'),
            $votes = $(this).next('.nr_of_votes'),
            nr_of_votes = parseInt($votes.data('nr-of-votes'), 10),
            voters = $votes.data('voters').split(',');

        if ($this.hasClass('vote-yes')) {
            nr_of_votes = nr_of_votes - 1;
            $this.removeClass('vote-yes').addClass('vote-no');
            voters.splice(voters.indexOf('You'), 1);
        } else {
            nr_of_votes = nr_of_votes + 1;
            $this.removeClass('vote-no').addClass('vote-yes');
            voters[0] = 'You';
        }

        $option.trigger('click');

        $votes.text(nr_of_votes + ' ' + owl.pluralize('vote', nr_of_votes));
        $votes.data('nr-of-votes', nr_of_votes);
        $votes.data('voters', voters.join(','));

        update_popovers();
    });
});
