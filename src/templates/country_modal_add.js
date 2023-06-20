function insertCountry() {
    $('.new_country').on('click', () => {
    $.ajax({
        method: 'POST',
        url: '/add/Country',
        data: $('#country_add_form').serialize()
    })
        .done((data) => {
            console.log(data);
            // wenn einfügen erfolgreich war, Modal wieder ausgeblendet
            // sonst Fehlermeldung in Modal anzeigen
           $('#modal_add_country').toggle();
           location.reload();
        });

    });
}

