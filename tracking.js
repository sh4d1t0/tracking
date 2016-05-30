(function($){
	"use strict";


	var QueryString = function () {
  		// This function is anonymous, is executed immediately and 
  		// the return value is assigned to QueryString!
  		var query_string = {};
  		var query = window.location.search.substring(1);
  		if(query.length > 0){
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
  		}
    	return query_string;
	};
	
	
	function _assign_id(email, c){
		$.ajax({
			'url':'http://192.152.28.101:8000/track/assign_id/',
			'data': {'email': email, 'c': c, 'host': window.location.hostname},
			'success': function(data){
				console.log(data);
				localStorage.assigned_id = data.id;
				localStorage.c = data.c;
				localStorage.c_key = data.c_key;
				localStorage.ends = data.ends //Jetzt plus einen Tag
			},
		});
	}

	function assign_id(){
		var referrer = document.referrer;
		var query_string = QueryString();
		
		if(Object.keys(query_string).length){
			if(query_string.email && query_string.c){
				if(localStorage.assigned_id != query_string.email || localStorage.c_key != query_string.c){
					_assign_id(query_string.email, query_string.c);
				}
			}
			if(localStorage.ends){
				if(Date.now() > localStorage.ends){
					_assign_id(query_string.email, query_string.c);
				}
		    }
		}else{
			if(!localStorage.assigned_id){
				_assign_id(query_string.email, query_string.c);
			}
			if(localStorage.ends){
				if(Date.now() > localStorage.ends){
					_assign_id(query_string.email, query_string.c);
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
				"id": localStorage.assigned_id, 'c': localStorage.c, 'c_key': localStorage.c_key}
			});
		}
	}

	function match_organic_lead(){
		var $form = $("form[data-matching-lead='true']");
		if($form.length == 1){
			$form.on('submit', function(e){
				var $nodes = $('[data-track-field]');
				var $values = new Object();
				$nodes.each(function(index){
					$values[$($nodes[index]).data('track-field')]  = $($nodes[index]).val()
				});
				if(localStorage.assigned_id){
					$.ajax({
						'url': 'http://192.152.28.101:8000/track/match_organic_lead/',
						'async': false,
						'data':{'organic_lead': localStorage.assigned_id, "data": $values }
					});
				}
				return true;
			});
		}
		return true;
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
		if(localStorage.c == ""){
			match_organic_lead();
		}
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