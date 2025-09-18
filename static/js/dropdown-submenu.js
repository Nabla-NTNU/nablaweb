function startToggleUtlaanListener() {
    // Toggle submenu only when clicking "Utlån"
    document.querySelectorAll('.dropdown-submenu > .dropdown-toggle').forEach(function(toggle) {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();   // don’t follow "#"
            e.stopPropagation();  // don’t close the parent dropdown

            let submenu = this.nextElementSibling;

            // Toggle current submenu
            submenu.classList.toggle('show');
        });
    });

    // Automatically close all submenus when main dropdown closes
    document.querySelectorAll('.dropdown').forEach(function(dropdown) {
        dropdown.addEventListener('hide.bs.dropdown', function () {
            dropdown.querySelectorAll('.dropdown-menu.show').forEach(function(submenu) {
                submenu.classList.remove('show');
            });
        });
    });
}



/*
function startCloseUtlaanListener() {
    document.querySelectorAll('dropdown-menu').forEach(function(toggle) {
        toggle.addEventListener('click', function() {
            console.log('Hei mikkel')

            let submenu = document.querySelectorAll('.dropdown-submenu');

            // Toggle current submenu
            submenu.classList.remove('show');
        });
    })
}

document.addEventListener("DOMContentLoaded", startToggleUtlaanListener);
document.addEventListener("DOMContentLoaded", startCloseUtlaanListener);
 */