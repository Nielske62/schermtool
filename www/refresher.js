setInterval(function() {
	
	req = jQuery.get('daemon');
	
	req.done(function(data) {
		
		$('#statistiek').html(data);
		
	});

}, 3000);

