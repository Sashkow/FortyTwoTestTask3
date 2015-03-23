$(document).ready(function() { 
	function create_post() {
		var options = { 
	        type:      'post',     
	        enctype:   'multipart/form-data',
	        dataType:  'json',
	        beforeSubmit: function(formData, jqForm, options) {
			 	$('#id_button').val('Saving...');
				$("input, textarea").prop( "disabled", true );
	        },
	        
	        success : function(json) {
	        		if (json.success== true){

	        			$("#id_img").attr('src', json.img_url)
				    	$('#id_button').val('Saved:)');	
				    	$("#results").html("");
	        		}
	        		else{
	        			
	        			var resultsHtml = ""
	        			for(var key in json.errors){
						    if (json.errors.hasOwnProperty(key)){
						        var value=json.errors[key];
								resultsHtml+="<div>" + String(key) + " : " + String(value) + "</div>";
						    }
						}
	        			$("#results").html(resultsHtml);
	        			$('#id_button').val('Failed:(');
	        		}

	        		
				    $('input, textarea').prop( "disabled", false );
				},

	        error : function(data) {
	        	// console.log(data)
	        	// for (var i = 0; i < data.length; i++) {
	        	// 	console.log(data[i])
	        	// };

	      //   	var errors = jQuery.parseJSON(data)
    			// console.log("errors")
    			// console.log(errors)
	            $('#results').html(data);
	            
            	$('#id_button').val('Failed:(');
			    $('input, textarea').prop( "disabl	ed", false );
	        } 
    	};     
	    $('#post-form').ajaxSubmit(options); 
	};	

	$('#post-form').on('submit', function(event){	
		if ($('#ava-clear_id').is(":checked")) {
			$("#id_ava").val("") 
		};
	    create_post();
	    return false;
	});

	
}); 




// 










// This function gets cookie with a given name
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

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});