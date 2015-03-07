$(document).ready(function() {
"use strict";

// Contact Form
var request;
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


$('.contact-form form').submit(function(event) {

  var $name = $(this).find('input[name="name"]');
  var $email = $(this).find('input[name="email"]');
  var $message = $(this).find('textarea');

  $('.contact-form p.error').show();
  $('input[name="name"], input[name="email"], textarea').removeClass('error');

  if ($name.val() == '') {
    event.stopPropagation();
    event.preventDefault();

    $('.contact-form p.error').addClass('active').html('<i class="fa fa-exclamation-triangle"></i> Please enter your name.');
    $name.addClass('error').focus();
    return false;
  }

  function IsEmail(email) {
    event.stopPropagation();
    event.preventDefault();

    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
  }

  if ($email.val() == '') {
    event.stopPropagation();
    event.preventDefault();

    $('p.error').addClass('active').html('<i class="fa fa-exclamation-triangle"></i> Please enter your email.');
    $email.addClass('error').focus();
    return false;
  }

  if(!IsEmail($email.val())) {
    event.stopPropagation();
    event.preventDefault();

    $('.contact-form p.error').addClass('active').html('<i class="fa fa-exclamation-triangle"></i> Looks like that email address is not correct. Try again.');
    $email.addClass('error').focus();
    return false;
  }

  if ($message.val() == "") {
    event.stopPropagation();
    event.preventDefault();
    $('.contact-form p.error').addClass('active').html('<i class="fa fa-exclamation-triangle"></i> Please enter your message.');
    $message.addClass('error').focus();
    return false;
  }

  if (request) {
    request.abort();
  }

  var $form = $(this);
  var $inputs = $form.find('input, button, textarea');
  var serializedData = $form.serialize();

  $inputs.prop('disabled', true);


// Setup AJAX
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


  request = $.ajax({
    url: '/api/registro',
    type: 'post',
    data: serializedData
  });

  request.done(function (response, textStatus, jqXHR){
    $('.contact-form p.error').hide();
    $('.contact-form p.message').html('Contact Form Submitted! We will be in touch soon.').fadeOut(2000);
  });

  request.fail(function (jqXHR, textStatus, errorThrown){
    console.error(
      'The following error occured: '+
      textStatus, errorThrown
    );
  });

  request.always(function () {
    $inputs.prop('disabled', false);
  });

  event.preventDefault();

});

});