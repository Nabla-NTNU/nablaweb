
(function (doors) {
    doors.on("click", function() {
        door = $(this);
        if (!door.hasClass('advent-door-open')) {

           door.addClass('advent-door-open');
           return false;

        } else {

            door.removeClass('advent-door-open');
            return true;

        }
    });

})($('.advent-door'));


