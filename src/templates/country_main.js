$(document).on('DOMContentLoaded', loadCountry);


function loadCountry(){
    $.ajax({
        type: 'GET',
        url: '/loader/country'
    })
        .done((data) => {
            countryInsert(data);
            cacheCountry(data);
        });

    trackCountryChange(); 
    countryButtonFunctionality();

}

function cacheCountry(countryArray) {    
    const mentArr = [];
    $.each(countryArray, (index) => {
        let cur = countryArray[index];
        let obj = {
            country_ID: cur['ID'],
            alpha2: cur['alpha2'],
            de: cur['de'],
            en: cur['en'],
            erasmus: cur['erasmus'],
            }
        mentArr.push(cur['ID'], obj)
    });
    sessionStorage.setItem('country', JSON.stringify(mentArr));
}



function countryButtonFunctionality() {

    $('#add_country_btn').on('click', function (){

        $('.modal_form_country').trigger("reset");
        $('#modal_add_country').toggle();

    });
   $('.close_modal_edit_country').on('click', function (){
        $('#modal_edit_country').toggle();
        sessionStorage.removeItem('changedCountry');

    });
   
   //set functionality for all abbrechen/X Buttons
    $('.close_modal_add_country').on('click', event => {
       let parent = event['currentTarget']['parentElement']['parentElement']['parentElement']['parentElement'];
       parent.style.display = "none";

    });
}


function trackCountryChange() {
    $('#country_edit_form').on('change', (e) => {
        //extract name of input field and value that's now in there
        const field = e.target.id;
        const value = e.target.value;
        let trackProgress = {};
        if ('changedCountry' in sessionStorage) {
            trackProgress = JSON.parse(sessionStorage.getItem('changedCountry'));
            trackProgress[field] = value;
        }
        else {
            trackProgress[field] = value;
        }
        sessionStorage.setItem('changedCountry', JSON.stringify(trackProgress));
    });
}

