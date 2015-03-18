$(document).ready(function(){

    var SERVER = "http://cib-bolivia.com"
    // var SERVER = "http://localhost:5000"

    var REG_ENDPOINT = "/api/registro";
    var SUS_ENDPOINT = "/api/suscriptors";
    var QUERY_ENDPOINT = "/api/contacts";


    var MESSAGE = {
        contacto_ok: "Cracias por contactarse con nosotros.",
        contacto_fail: "No se pudo establecer conexion",
        suscripcion_ok: "Gracias por suscribirse a nuestro boletin.",
        suscripcion_fail: "Su suscripcion no se completo.",
        registro_ok: "Gracias por registrarse al evento.",
        registro_fail: "Su registro no pudo concretarse."
    }

    var REG_EXP = {
        name : /^[A-Za-z0-9 ]{3,20}$/,
        email : /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i,
        username : /^[A-Za-z0-9_]{1,20}$/,
        password :  /^[A-Za-z0-9!@#$%^&*()_]{6,20}$/,
        filled :  /.+/,
    }

    toastr.options = {
      "closeButton": false,
      "debug": false,
      "newestOnTop": false,
      "progressBar": false,
      "positionClass": "toast-top-center",
      "preventDuplicates": false,
      "onclick": null,
      "showDuration": "500",
      "hideDuration": "1200",
      "timeOut": "5000",
      "extendedTimeOut": "500",
      "showEasing": "swing",
      "hideEasing": "linear",
      "showMethod": "fadeIn",
      "hideMethod": "fadeOut",
      "preventDuplicates" : true,
      "closeButton" : true
    };

    var Loader = {
        open: function(){
            document.getElementById('modalLoader').style.display = 'block';
            document.getElementById('fade').style.display = 'block';
        },
        close: function(){
            document.getElementById('modalLoader').style.display = 'none';
            document.getElementById('fade').style.display = 'none';
        }
    }

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

    // FORMULARIO DE CONTACTO
    var $contacForm = $('.contact-form form');
    $contacForm.find('#sendContact').click(function(e) {

        e.preventDefault();
        e.stopPropagation();

        console.log("guardando Conta");

        var $name = $( $contacForm.get(0).name );
        var $email = $( $contacForm.get(0).email );
        var $message = $contacForm.find('textarea');

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
            var consulta = {
                name: $name.val(),
                email: $email.val(),
                message: $message.val()
            }
            var request = $.ajax({
                url: QUERY_ENDPOINT,
                method: 'POST',
                data: consulta
            });

            Loader.open();

            request.done(function (response, textStatus, jqXHR){
                $('.contact-form p.error').hide();
                $('.contact-form p.message').html('Consulta enviado, muchas gracias.').fadeOut(2000);
                Loader.close();
                toastr["success"](MESSAGE.contacto_ok);
                $contacForm.get(0).reset();
                $name.focus();
            });
            request.fail(function (jqXHR, textStatus, errorThrown){
                console.error('The following error occured: '+ textStatus, errorThrown);
                Loader.close();
                toastr["error"](MESSAGE.contacto_fail);

            });
        }
    });


    //  FORMULARIO DE REGISTRO
    var $regForm = $("#regForm");
    $regForm.name = $( $regForm.get(0).name );
    $regForm.surname = $( $regForm.get(0).surname );
    $regForm.email = $( $regForm.get(0).email );
    $regForm.address = $( $regForm.get(0).address );
    $regForm.depot = $( $regForm.get(0).depot );
    $regForm.city = $( $regForm.get(0).city );
    $regForm.package = $("#package");
    $regForm.submit = $( $regForm.get(0).submit );

    $regForm.submit.click(function(e){
        e.stopPropagation();
        e.preventDefault()

        var validate = true;
        if( !REG_EXP.name.test($regForm.city.val()) ){
            $regForm.city.addClass("error");
            $regForm.city.focus();
            validate = false;
        } else $regForm.city.removeClass("error");


        if( !REG_EXP.filled.test($regForm.package.val()) ){
            $regForm.package.addClass("error");
            $regForm.package.focus();
            validate = false;
        } else $regForm.package.removeClass("error");

        if( !REG_EXP.filled.test($regForm.depot.val()) ){
            $regForm.depot.addClass("error");
            $regForm.depot.focus();
            validate = false;
        } else $regForm.depot.removeClass("error");

        if( !REG_EXP.filled.test($regForm.address.val()) ){
            $regForm.address.addClass("error");
            $regForm.address.focus();
            validate = false;
        } else $regForm.address.removeClass("error");


        if( !REG_EXP.email.test($regForm.email.val()) ){
            $regForm.email.addClass("error");
            $regForm.email.focus();
            validate = false;
        } else $regForm.email.removeClass("error");

        if( !REG_EXP.name.test($regForm.surname.val()) ){
            $regForm.surname.addClass("error");
            $regForm.surname.focus();
            validate = false;
        } else $regForm.surname.removeClass("error");

        if( !REG_EXP.name.test($regForm.name.val()) ){
            $regForm.name.addClass("error");
            $regForm.name.focus();
            validate = false;
        } else $regForm.name.removeClass("error");


        if(validate) {
            var person = {
                name: $regForm.name.val(),
                surname: $regForm.surname.val(),
                email: $regForm.email.val(),
                address: $regForm.address.val(),
                depot: $regForm.depot.val(),
                city: $regForm.city.val(),
                package: $regForm.package.val()
            }

            Loader.open();

            $.ajax({
                url: REG_ENDPOINT,
                data: person,
                method: "POST",
                success: function(data){
                    console.log(data);
                    Loader.close();
                    toastr["success"](MESSAGE.registro_ok);
                    $regForm.get(0).reset();
                    $regForm.name.focus();
                },
                error: function(a,b,c){
                    console.log(a,b,c);
                    Loader.close();
                    toastr["error"](MESSAGE.registro_fail);
                }
            })
        }
    });

    // FORMULARIO DE SUSCRIPCION
    var $susForm = $("#suscriptorForm");

    $susForm.email = $( $susForm.get(0).email );
    $susForm.submit = $susForm.find("button");

    $susForm.submit.click(function(e){
        e.preventDefault();
        e.stopPropagation();

        var validate = true;
        if( !REG_EXP.email.test($susForm.email.val()) ){
            $susForm.email.addClass("error'");
            $susForm.email.focus();
            validate = false;
        } else $susForm.email.removeClass("error");

        if(validate) {
            var suscriptor = { email: $susForm.email.val() }

            Loader.open();

            $.ajax({
                url: SUS_ENDPOINT,
                data: suscriptor,
                method: "POST",
                success: function(data){
                    console.log(data);
                    Loader.close();
                    toastr["success"](MESSAGE.suscripcion_ok);
                    $susForm.get(0).reset();
                    $susForm.email.focus();
                },
                error: function(a,b,c){
                    console.log(a,b,c);
                    Loader.close();
                    toastr["error"](MESSAGE.suscripcion_fail);
                }
            })
        }
    });



});