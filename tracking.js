(function($){
	"use strict";

//Version 2.0

	var TrackDash = function(){
		this.QueryString = function () {
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


		this.setId = function(id){
			localStorage.assigned_id = id
		};

		this.setCampaign = function(campaign){
			localStorage.c = campaign
		};

		this.setCampaignKey = function(campaignKey){
			localStorage.c_key = campaignKey
		};

		this.setEnds = function(ends){
			localStorage.ends = ends
		};
			
		this.getEnds = function(){
			return localStorage.ends && localStorage.ends || null
		};
			
		this.getId = function(){
			return localStorage.assigned_id && localStorage.assigned_id || null
		};

		this.getCampaign = function(){
			return localStorage.c && localStorage.c || null
		};

		this.getCampaignKey = function(){
			return localStorage.c_key && localStorage.c_key || null	
		};

		this.getPage = function(){
			return window.location.origin + window.location.pathname
		};

		this.getTime = function(){
			return  TimeMe.getTimeOnCurrentPageInSeconds()
		};
		this.stop = function(){
			TimeMe.stopTimer();
		};

		this.change_page = function(){
			this.stop();
			this.initialize2();

		};
	};
	
	TrackDash.prototype._assign_id = function(email, c){
		var that = this;
		$.ajax({
			'url':'http://192.152.282.101:8000/track/assign_id/',
			'data': {'email': email, 'c': c, 'host': window.location.hostname},
			'success': function(data){
				that.setId (data.id);
				that.setCampaign(data.c);
				that.setCampaignKey(data.c_key);
				that.setEnds(data.ends);
			},
		});
	};

	TrackDash.prototype.event = function(info){
		var td = new TrackDash();
		info['lead'] = td.getId();
		info['domain'] = window.location.origin;
		info['url'] = window.location.href;
		$.ajax({
			'url': 'http://192.152.282.101:8000/track/event/',
			'data':{"data": JSON.stringify(info)}
		});

	};


	TrackDash.prototype.initialize2 = function(){
		TimeMe.setCurrentPageName(window.location.href);
		TimeMe.startTimer();

	};


	TrackDash.prototype.assign_id = function(){
		var query_string = this.QueryString();
	
		if(Object.keys(query_string).length){
			if(query_string.email && query_string.c){
				if(this.getId() != query_string.email || this.getCampaignKey() != query_string.c){
					this._assign_id(query_string.email, query_string.c);
				}
			}
			if(this.getEnds()){
				if(Date.now() > this.getEnds()){
					this._assign_id(query_string.email, query_string.c);
				}
	    	}
		}else{
			if(!this.getId()){
				this._assign_id(query_string.email, query_string.c);
			}
			if(this.getEnds()){
				if(Date.now() > this.getEnds()){
					this._assign_id(query_string.email, query_string.c);
				}
	    	}
		}
	};

	TrackDash.prototype.push_event_timer = function(){
		var that = this;
		if(this.getId()){
			$.ajax({
				'url': 'http://192.152.282.101:8000/track/save_data/',
				'async': false,
				'data':{'page': that.getPage(), 'time': that.getTime(),
						"id": that.getId(), 'c': that.getCampaign(), 'c_key': that.getCampaignKey()}
			});
		}
	};
	TrackDash.prototype.match_organic_lead = function(){
		var $form = $("form[data-matching-lead='true']");
		var that = this;
		if($form.length == 1){
			$form.on('submit', function(e){
				var $nodes = $('[data-track-field]');
				var $values = new Object();
				$nodes.each(function(index){
					$values[$($nodes[index]).data('track-field')]  = $($nodes[index]).val()
				});
				if(that.getId()){
					$.ajax({
						'url': 'http://192.152.282.101:8000/track/match_organic_lead/',
						'async': false,
						'data':{'organic_lead': that.getId(), "data": JSON.stringify($values) }
					});
				}
				return true;
			});
		}
	};
	TrackDash.prototype.initialize = function(){
		var that = this;
		this.assign_id();
		TimeMe.setIdleDurationInSeconds(-1);
		TimeMe.setCurrentPageName(window.location.href);
		TimeMe.initialize();
		/*$(window).hashchange(function(){
			push_event_timer();
			change_page();
		});*/
		$(window).on('beforeunload', function(){
			that.push_event_timer();
		});
		if(!this.getCampaign()){
			this.match_organic_lead();
		}
	};


	$(document).ready(function(){var trackdash = new TrackDash();trackdash.initialize();window.dataEvent = trackdash.event});
})(jQuery);