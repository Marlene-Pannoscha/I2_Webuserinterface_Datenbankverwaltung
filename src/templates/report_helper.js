
/** Wenn die Seite faculty.html vollständig geladen wurde, wird ein GET-Request an app.py gesendet, um
 * Fakultäts-Daten aus der Datenbank abzufragen. Wenn die Daten geladen wurde, werden diese an die Funktion
 * insertFac übergeben.
*/
$(document).on('DOMContentLoaded', () => {
    $.ajax({
        type: 'GET',
        url: '/loader/faculty'
    })
        .done((data) => {
           insertFac(data);
        });
});


/** Wenn der GET-Request die Fakultäts-Informationen aus der Datenbank geladen hat, wird per HTML eine Tabelle mit den Inhalten erzeugt.
  * 
  * @param {{de: string, en: string, agreements: int}} allFaculties --enthält die Namen der Fakultät in Deutsch und Englisch sowie die Anzahl der mit dieser Fakultät bestehenden Verträge
  */
function insertFac(allFaculties) {
    
    const mySelect = $('#select-faculty-for-report');
    allFaculties.forEach(entity => {
        //mySelect.append("<tr><th>" + entity['de'] + "</th><th>" + entity['eng'] + "</th><th>" + entity['agreements'] + "</th></tr>");
        let opt = document.createElement("option");
        opt.value = entity['id'];
        opt.text = entity['de'];
        mySelect.append(opt);
    });    

    /*
    mySelect.on('change', function() {
        listReport(this.value) // on.('change', ...) verweist auf aktuelle Auswahl --> gibt aktuelle id zurück
    });
    */

}

/*
function loadAll() {
    $.get('/get/reports_fac', function (data) {
        // load institutes from database
        sessionStorage.setItem('admin', JSON.stringify(data[2]['admin']));
        insertInstitutes(data);
    })
        .then(checkAdmin());
}
*/


function listReport(faculty_id) {

    let repoHTML = $('#report-list')
    repoHTML.html('');

    let faculty_related_reports = ["basic", "special"];

    /*
    let reports = [
        {'<button id=' + faculty_related_reports[0] + '>' + faculty_related_reports[0] + '</button>'},
        {"name": "bericht1", "title": "Bericht 1"},
        {"name": "bericht2", "title": "Bericht 2"},
        {"name": "bericht3", "title": "Bericht 3"},
        {"name": "bericht4", "title": "Bericht 4"},
        {"name": "bericht5", "title": "Bericht 5"}
    ];
    */

    const list = $('ul#report-list');

    for(let element of faculty_related_reports){
        let button = document.createElement("button");
        button.id = faculty_related_reports[element];
        //button.class = "btn btn-outline-primary me-3";
        button.innerHTML = "<style>background-color: blue; border: 2px; font-size: 20px; padding: 32px, 16px; width: 25%</style>"
        button.textContent = faculty_related_reports[element];
        /*
        let li = document.createElement("li");
        li.textContent = element["title"];
        list.append(li);
        */
       list.append(button);
    }
}

function createPDF(type, id) {

    let url;
    let erasmus = '0001';
    let institute = '0002';

    if(type == 'pdf1') {
        url = '/pdf/fac_report/' + id;
    } else if (type == 'pdf2') {
        url = '/pdf/erasmus_report/' + erasmus;
    } else if (type == 'pdf3') {
        url = '/pdf/institute_report/' + institute;
    }
    
    //console.log(url);
    window.open(url);
}


