$( "#openNav" ).click(function() {
    $('#mySidenav').addClass('open');
    $('body').addClass('open-bg');
  });
  $( "#closeNav" ).click(function() {
    $('#mySidenav').removeClass('open');
    $('body').removeClass('open-bg');
  });