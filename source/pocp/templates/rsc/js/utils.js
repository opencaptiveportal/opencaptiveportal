
$(document).ready(function(){
	
	//search btn hover for ie6
	$('#search_btn').hover(
      function () {
        $(this).css('background-image', 'url(images/suche_button_hover.gif)');
      }, 
      function () {
        $(this).removeAttr('style');
      }
    );
	
});