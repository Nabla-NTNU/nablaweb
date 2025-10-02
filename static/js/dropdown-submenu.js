// Script to handle dropdown submenus
// $ runs the function through jQuery for it to be compatible with Bootstrap

$(document).ready(function() {

    $(".dropdown-submenu > .dropdown-toggle").on("click", function(e) {
        e.preventDefault();   
        e.stopPropagation();  

        const submenu = $(this).next(".dropdown-menu");
        const isOpen = submenu.hasClass("show");

        submenu.toggleClass("show");

        $(this).attr("aria-expanded", !isOpen);
    });

    // Close all submenus when the main dropdown closes
    $(".dropdown").on("hide.bs.dropdown", function() {

        $(this).find(".dropdown-submenu > .dropdown-menu.show").removeClass("show");

        $(this).find(".dropdown-submenu > .dropdown-toggle").attr("aria-expanded", "false");
    });
});
