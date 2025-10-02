
// $ runs the function through jQuery for it to be compatible with Bootstrap
$(document).ready(function() {

    $(".dropdown-submenu > .dropdown-toggle").on("click", function(e) {
        e.preventDefault();   
        e.stopPropagation();  

        const $submenu = $(this).next(".dropdown-menu");
        const isOpen = $submenu.hasClass("show");

        // Toggle submenu
        $submenu.toggleClass("show");

        // Update aria-expanded for accessibility
        $(this).attr("aria-expanded", !isOpen);
    });

    // Close all submenus when the main dropdown closes
    $(".dropdown").on("hide.bs.dropdown", function() {
        $(this).find(".dropdown-submenu > .dropdown-menu.show").removeClass("show");

        // Reset aria-expanded for all submenu toggles
        $(this).find(".dropdown-submenu > .dropdown-toggle").attr("aria-expanded", "false");
    });
});
