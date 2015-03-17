$(document).ready(function(){

    // var SERVER = "http://cib-bolivia.com"
    var SERVER = "http://localhost:5000"

    var REG_ENDPOINT = SERVER+"/api/registro";
    var SUS_ENDPOINT = SERVER+"/api/suscriptors";

    var REG_EXP = {
        name : /^[A-Za-z0-9 ]{3,20}$/,
        email : /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i,
        username : /^[A-Za-z0-9_]{1,20}$/,
        password :  /^[A-Za-z0-9!@#$%^&*()_]{6,20}$/,
        filled :  /.+/,
    }

    function register(obj){
        console.log("registrando");
    }

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

            $.ajax({
                url: REG_ENDPOINT,
                data: person,
                method: "POST",
                success: function(data){
                    console.log(data);
                },
                error: function(a,b,c){
                    console.log(a,b,c);
                }
            })
        }
    });

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

            $.ajax({
                url: SUS_ENDPOINT,
                data: suscriptor,
                method: "POST",
                success: function(data){
                    console.log(data);
                },
                error: function(a,b,c){

                    console.log(a,b,c);
                }
            })
        }
    });



});