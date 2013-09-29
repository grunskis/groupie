$(function () {
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
