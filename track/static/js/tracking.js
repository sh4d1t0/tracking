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
	
	function _assign_id(email, c){
		$.ajax({
			'url':'http://192.152.28.101:8000/track/assign_id/',
			'data': {'email': email, 'c': c},
			'success': function(data){
				console.log(data);
				localStorage.assigned_id = data.id;
				localStorage.c = data.c
			},
			'async': false
		});
	}

	function assign_id(){
		var referrer = document.referrer;
		var query_string = QueryString();
		if(!localStorage.assigned_id){
			_assign_id(query_string.email, query_string.c);
		}else{
			if(query_string.length){
				if(query_string.email && query_string.c){
					if(localStorage.assigned_id != query_string.email || localStorage.c != query_string.c){
						_assign_id(query_string.email, query_string.c);
					}
				}
			}
		}
	}
	
	function push_event_timer() {
		if(localStorage.assigned_id){
			$.ajax({
				'url': 'http://192.152.28.101:8000/track/save_data/',
				'async': false,
				'data':{'page': window.location.origin + window.location.pathname, 'time': TimeMe.getTimeOnCurrentPageInSeconds(), 
				"id": localStorage.assigned_id, 'c': localStorage.c}
			});
		}
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