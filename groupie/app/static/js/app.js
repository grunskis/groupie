$(function() {
        var scntDiv = $('#date-picker');
        var i = $('#add-dates p').size() + 1;

        $('#add-dates').on('click', function() {
                
                
                $('<p id="date-picker' + i +'" class="datepair" data-language="javascript"><input id="date-' + i +' " name="date-' + i +'" type="text" class="date"><input id="time-" name="time-" type="text" class="time"><a href="#" id="rem-dates">Remove</a></p>').insertAfter(scntDiv);
                i++;
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