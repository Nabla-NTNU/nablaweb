
(function (doors) {
    doors.on("click", function() {
        door = $(this);
        if (door.attr("data-open") == "True") {

            if (!door.hasClass('advent-door-open')) {

               door.addClass('advent-door-open');
               return false;

            } else {

                door.removeClass('advent-door-open');
                return true;

            }
        } else {
            alert("Ikke åpen enda.");
        }
    });

})($('.advent-door'));


