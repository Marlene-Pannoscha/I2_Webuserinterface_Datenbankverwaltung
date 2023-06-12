 function facultyButtonFunctionality() {
 // HAUPTANSICHT: Fakultät -> Fakultät ANLEGEN BUTTON
 $('#add_faculty_btn').on('click', function (){
    $('.modal_form_add').trigger("reset");
    $('#modal_add_faculty').toggle();
    setBlur();
    
});

  // MODAL: Fakultät BEARBEITEN -> ABBRECHEN / X BUTTON
  $(' .close_modal_add').on('click', function (){
    $('#modal_add_faculty').toggle();
    $('#mod_add_faculty_save_btn').attr('disabled', 'true');
    unsetBlur();
});


}

function insertFaculty() {
  $('#mod_add_faculty_save_btn').on('click', () => {
    $.ajax({
      method: 'POST',
      url: '/add/Faculty',
      data: $('#form_add_faculty').serialize()
    })
      .done((data) => {
        console.log(data);
        // Wenn das Einfügen erfolgreich war, das Modal ausblenden und die Seite neu laden
        // Ansonsten Fehlermeldung im Modal anzeigen
        $('#modal_add_faculty').toggle();
        location.reload();
      });
  });

  
}
