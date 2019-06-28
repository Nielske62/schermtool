setInterval(function() {
	
	req = jQuery.get('http://127.0.0.1:9999/index/daemon/');
	
	req.done(function(data) {
		
		$('#statistiek').html(data);
		
	});

}, 30000);

