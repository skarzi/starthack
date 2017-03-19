var source = [];
$.getJSON('/static/airport_id_city.json', function(data) {
  console.log(data[0], data.length);
  source = data;
});

$("#id-city-1, #id-city-2" ).autocomplete({
    minLength: 3,
    source: function(request, response){
        console.log('Completing!');
        var search_term = request.term.toLowerCase();
        var ret = [];
        $.each(source, function(i, airport_item){
            if (airport_item.id.toLowerCase().indexOf(search_term) !== -1 ||
                  airport_item.city.toLowerCase().indexOf(search_term) === 0)
                ret.push(airport_item.city + '(' + airport_item.id + ')');
        });
      response(ret);
    }});


