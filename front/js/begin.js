function addNew(evt_name, params){
    var newDiv = $('<div/>', {
	id:'div_' + evt_name,
	//class
    });
    
    var p1 = $("<p><span class = 'evtname spn'>" + evt_name + "</span><span class = 'evtfired spn'>"+params['fired']+"</span><span class = 'evtcompleted spn'>"+params['completed']+"</span></p>");
    p1.appendTo(newDiv);
    return newDiv
}

$.ajax({url:"http://localhost:8888/getlist/", type:'get', dataType:'json'}).done(function(e){
    delete e['meta'];
    $.each(e, function(evt_name, params){
	nDiv = addNew(evt_name, params);
	nDiv.appendTo("#list")
	
    })
})

