

$(document).ready(function(){
	$('.searchCont input').keyup(function(e){
		search(this);
	});
	
	$('body').on('click','.searchCont .tagItem',function(){chooseItem(this);});
});

function search(thisObject){
	var type = $(thisObject).attr('name');
	var s = $(thisObject).val().toLowerCase();
	
	var showList = new Array();
	$(thisObject).parent().children('.completebox').html('');
	
	for (var i = 0; i < data[type].length; i++) {
		console.log(showList);
		if (showList.length > 7){break}
		if (data[type][i].title.toLowerCase().indexOf(s) > -1){
			$(thisObject).parent().children('.completebox').append(searchItem(type,i));
			showList.push(data[type][i].title);
		}
	}
	
	if ($(thisObject).parent().children('.completebox').children('.tagItem').length > 0){
		$(thisObject).parent().children('.completebox').show();
	}
	else {
		$(thisObject).parent().children('.completebox').hide();
	}
}

function searchItem(type, i){
	return "<a class='tagItem'><div style='padding:7px;'>"+ data[type][i].title +"</div></a>"
}

function chooseItem(thisObject){
	$(thisObject).parent().parent().children('input').val($(thisObject).children('div').html());
	
	$(thisObject).parent().hide();
}

