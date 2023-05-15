$(document).on('DOMContentLoaded', () => {
    $('.btn-logout').on('click', () =>{
        $.ajax('/logout', {type: 'GET',
        success: function(data, status, xhr){
            location.replace("/")
        }});
       
    });
});