$(document).ready(function() {
    "use strict";

    var QUERY_ENDPOINT = "http://cib-bolivia/api/contacts";
    // var QUERY_ENDPOINT = "http://localhost:5000/api/contacts";

    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    var $contacForm = $('.contact-form form');

    $contacForm.find('#sendContact').click(function(e) {

        var $name = $( $contacForm.get(0).name );
        var $email = $( $contacForm.get(0).email );
        var $message = $contacForm.find('textarea');

        console.log($name);
        console.log($email);
        console.log($message);

        $('.contact-form p.error').show();
        $('input[name="name"], input[name="email"], textarea').removeClass('error');

        // e.stopPropagation();
        e.preventDefault();



        var validate = true;
        if ($name.val() == '') {
            $('.contact-form p.error').addClass('active').html('<i class="fa fa-exclamation-triangle"></i> Please enter your name.');
            $name.addClass('error').focus();
            validate = false;
        }

        function IsEmail(email) {
            var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
            return regex.test(email);
        }

        if ($email.val() == '') {
            $('p.error').addClass('active').html('<i class="fa fa-exclamation-triangle"></i> Please enter your email.');
            $email.addClass('error').focus();
            validate = false;
        }

        console.log("IsEmail"+ IsEmail($email.val()) );

        if(!IsEmail($email.val())) {
            $('.contact-form p.error').addClass('active').html('<i class="fa fa-exclamation-triangle"></i> Looks like that email address is not correct. Try again.');
            $email.addClass('error').focus();
            validate = false;
        }

        if ($message.val() == "") {
            $('.contact-form p.error').addClass('active').html('<i class="fa fa-exclamation-triangle"></i> Please enter your message.');
            $message.addClass('error').focus();
            validate = false;
        }


        if(validate){

            console.log("todo valido");


            function csrfSafeMethod(method) {
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            var consulta = {
                name: $name.val(),
                email: $email.val(),
                message: $message.val()
            }

            console.log( "consulta", consulta);


            var request = $.ajax({
                url: QUERY_ENDPOINT,
                method: 'POST',
                data: consulta
            });

            request.done(function (response, textStatus, jqXHR){
                $('.contact-form p.error').hide();
                $('.contact-form p.message').html('Consulta enviado, muchas gracias.').fadeOut(2000);
            });

            request.fail(function (jqXHR, textStatus, errorThrown){
                console.error('The following error occured: '+ textStatus, errorThrown);
            });


        }

    });

});