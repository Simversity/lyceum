var evtStorage = new SimStorage({ns: 'BouncerEvent', strict: true});

e_obj = Object
//evtStorage.clear()
function storeEvents(f_context){
    //alert("Events")
    if (f_context['real_evt_name'][0] != "_" && f_context['user_id']){
	str_fcontext = JSON.stringify(f_context);
	console.log(str_fcontext);
	if(st = evtStorage.get("events")){
	    //console.log(st)
	    
	    var new_st = st + "|||" + str_fcontext;
	    evtStorage.set("events", new_st);
	}else{
	    evtStorage.set("events", str_fcontext);
	}
    }
}
function pollEvtStorage(){
    if(evtStorage.getAll().length){
	console.log("Polling Event Storage")
	var evtStr = evtStorage.get("events");
	var evts = evtStr.split("|||");
	var evts_obj = []
	$.each(evts, function(index, item) {
	    evts_obj.push(JSON.parse(item));
	});
	//var evts_obj_str = JSON.stringify(evts_obj);
	//console.log(evts_obj);
	e_obj = evts_obj
	//alert("event_polling")
	_jack.ajax_call({
	    'url': 'http://localhost:8888/log/',
	    'relay_urlname': "evt/",
	    'relay_method': "POST",
	    'relay_data': {'events_list': evts_obj},
	    'complete': function() {
	//	alert("completee");
	    },
	    'beforeSend': function(xhr) {
	///	alert("before");
	    },
	    'success': function(ret, textStatus, xhr) {
		alert("success");
	    },
	    
	    /*'success' : function(r){
		alert("ee")
		//evtStorage.clear();
	    },*/
	    'error': function(){
		alert("errr")
	    }
	});
	
    }
}

function testErr(){
    _jack.ajax_call({
	    'url': 'http://localhost:8888/',
	    'relay_urlname': "evt/",
	    'relay_method': "POST",
	    'relay_data': {'events_list': 22},
	    'complete': function() {
	//	alert("completee");
	    },
	    'beforeSend': function(xhr) {
	///	alert("before");
	    },
	    'success': function(ret, textStatus, xhr) {
		alert("success");
	    },
	    
	    /*'success' : function(r){
		alert("ee")
		//evtStorage.clear();
	    },*/
	    'error': function(){
		alert("errr")
	    }
	});
	
}

setInterval(pollEvtStorage, "120000")
