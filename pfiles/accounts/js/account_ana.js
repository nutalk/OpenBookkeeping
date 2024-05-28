
$(document).ready(function(){
    $("#ana_bnt").click(function(){
        var all_id = "";
        $(":checkbox").each(function(){
            console.log( $(this).attr("id"));

            if($(this).is(":checked")==true){
                all_id = all_id + '|';
                all_id = all_id + $(this).attr("id");
            }
        })
        $.post("/post_account_ana/",
        {
            csrfmiddlewaretoken: csrftoken,
            all_id: all_id
        },
        function (data, status) {
        console.log(data);
        update_ts_chart("long_term_chart", data.long_series, "area", '万元');
        update_ts_chart("short_term_chart", data.short_series, "line", '万元');
        });
    })
})

