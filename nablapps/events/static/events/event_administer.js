$(document).ready(function(){
    // Select all checboxes in registrationTable
    $( '#registrationTable .toggle-all' ).click( function () {
        $('#registrationTable input[type="checkbox"]' ).prop('checked', this.checked);
  })
});

function copy_mail_list(){
    let textarea = document.getElementById("epostliste-text");
    textarea.select();
    document.execCommand("copy");
}
