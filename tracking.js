(function($){
	"use strict";

	var QueryString = function () {
  		// This function is anonymous, is executed immediately and 
  		// the return value is assigned to QueryString!
  		var query_string = {};
  		var query = window.location.search.substring(1);
  		var vars = query.split("&");
  		for (var i=0;i<vars.length;i++) {
    		var pair = vars[i].split("=");
        		// If first entry with this name
    		if (typeof query_string[pair[0]] === "undefined") {
      			query_string[pair[0]] = decodeURIComponent(pair[1]);
        		// If second entry with this name
    		} else if (typeof query_string[pair[0]] === "string") {
      			var arr = [ query_string[pair[0]],decodeURIComponent(pair[1]) ];
      			query_string[pair[0]] = arr;
        	// If third or later entry with this name
    		} else {
      			query_string[pair[0]].push(decodeURIComponent(pair[1]));
    		}
  		} 
    	return query_string;
	};
	
	function assign_id(){
		var referrer = document.referrer;
		if(!localStorage.assigned_id && referrer.indexOf(window.location.host) != -1){
			$.ajax({
				'url':'http://192.152.28.101:8000/track/assign_id/',
				'dataType': 'jsonp',
				'data': {'email': QueryString().email},
				'success': function(data){
					localStorage.assigned_id = data.id
				},
				'async': false
			});
		}
	}
	
	function push_event_timer() {
		$.ajax({
			'url': 'http://192.152.28.101:8000/track/save_data/',
			'dataType': 'jsonp',
			'async': false,
			'data':{'page': window.location.href, 'time': TimeMe.getTimeOnCurrentPageInSeconds(), 
			"id": localStorage.assigned_id} 
		});
	}

	function initialize(){
		assign_id();
		TimeMe.setIdleDurationInSeconds(-1);
		TimeMe.setCurrentPageName(window.location.href);
		TimeMe.initialize();
		$(window).on('beforeunload', function(){
			push_event_timer();
		});
		$(window).hashchange(function(){
			push_event_timer();
			change_page();
		});


	}

	function initialize2(){
		TimeMe.setCurrentPageName(window.location.href);
		TimeMe.startTimer();


	}
	function stop(){
		TimeMe.stopTimer();
	}

	function change_page(){
		stop();
		initialize2();
	}

	initialize();


})(jQuery);