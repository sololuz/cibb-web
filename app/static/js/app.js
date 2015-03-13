$(document).ready(function(){
    var $regForm = $("#reForm");
    $regForm.name = $regForm.find("[name=name]");
    $regForm.surname = $regForm.find("[name=surname]");
    $regForm.email = $regForm.find("[name=email]");
    $regForm.address = $regForm.find("[name=address]");
    $regForm.depot = $regForm.find("[name=depot]");
    $regForm.city = $regForm.find("[name=city]");
    $regForm.package = $regForm.find("#package");
    $regForm.submit = $regForm.find("[name=submit]");

    $regForm.submit.click(function(e){
        e.preventDefault();
        e.stopPropagation();


    });







});