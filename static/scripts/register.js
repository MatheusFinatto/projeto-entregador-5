$(document).ready(function(){

    var errors = 4;

    $('#password').focus(function() {
        $('.password-constraints').css('display', 'inline');
        // $('.password-constraints').css('visibility', 'visible');
    });

    $('#password').focusout(function() {
        var str = $("#password").val();
        if (!(str.length > 0) || errors == 0) {
            $('.password-constraints').css('display', 'none');
        }
    });

    $('#password').change(function() {
        var str = $("#password").val();
        errors = validatePassword(str);
        if (errors == 0) {
            $('.password-constraints').css('display', 'none');
        }
    });

});

function validatePassword(str) {
    // Validates password and return errors
    var errors = 4;

    if (str.length < 8) {
        $('#length').css('color', 'red')
    } else {
        $('#length').css('color', 'rgb(118, 184, 63)')
        errors--
    }

    if (str.toUpperCase() == str) {
        $('#lowercase').css('color', 'red')
    } else {
        $('#lowercase').css('color', 'rgb(118, 184, 63)')
        errors--
    }

    if (str.toLowerCase() == str) {
        $('#uppercase').css('color', 'red')
    } else {
        $('#uppercase').css('color', 'rgb(118, 184, 63)')
        errors--
    }

    var numberPattern = /\d+/g;

    if (str.match(numberPattern) == null) {
        $('#numbers').css('color', 'red')
    } else {
        $('#numbers').css('color', 'rgb(118, 184, 63)')
        errors--
    }

    return errors;
}

