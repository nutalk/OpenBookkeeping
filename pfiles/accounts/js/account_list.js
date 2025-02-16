$(document).ready(function () {
    $(".list-group-item").click(function () {
        var current_id = $(this).attr("id");
        var current_name = $(this).text()
        $(".list-group-item").removeClass("active");
        $(this).addClass("active");
        $("#account_id_p").text(current_id);
        $('#account_name_p').text(current_name);
        $('#prop_edit_btn').prop('disabled', false);
        $('#prop_del_btn').prop('disabled', false);
        $('#detail_add_btn').prop('disabled', false);
        $('#detail_edit_btn').prop('disabled', true);
        $('#detail_del_btn').prop('disabled', true);
        $("#id_target_id").val(current_id);
    });
});

$(document).ready(function(){
    var translations = {
        "en": {
            "ID": "ID",
            "Occur Date": "Occur Date",
            "Amount": "Amount",
            "Balance": "Balance",
            "Comment": "Comment"
        },
        "zh-hans": {
            "ID": "ID",
            "Occur Date": "日期",
            "Amount": "金额",
            "Balance": "余额",
            "Comment": "备注"
        }
        // 添加更多语言的翻译
    };
    var currentLanguage = $('#current_lan').text();

    $('#detail_table').bootstrapTable({
        columns: [
        {
            radio: true
        },{
          field: 'id',
          title: translations[currentLanguage]["ID"]
        },{
            field: 'occur_date',
            title: translations[currentLanguage]["Occur Date"]
        }, {
          field: 'amount',
          title: translations[currentLanguage]["Amount"]
        }, {
          field: 'rem_amount',
          title: translations[currentLanguage]["Balance"]
        }, {
            field: 'comment',
            title: translations[currentLanguage]["Comment"]
        }],
        data:[]
    });
})

// get info for a prop
$(document).ready(function () {
    $(".list-group-item").click(function () {
        $.post("/prop_detail_post/",
            {
                prop_id: $(this).attr("id"),
                csrfmiddlewaretoken: csrftoken
            },
            
            function (data, status) {
                // console.log(data);

                for (var i=0; i<data.length; i++){
                    var rec = data[i];
                    $("#"+rec.k).text(rec.v);
                    var objs = $(".prop_edit_form").find("#id_"+rec.k)
                    if (objs.is('select')){
                        objs.children().filter(function() {
                            return $(this).text() == rec.v;
                          }).prop('selected', true);
                    }
                    else {
                        objs.val(rec.v);
                    }
                }
            });
        })
});

function update_detail_table(prop_id) {
    $.post("/prop_detail_table/",
            {
                prop_id: prop_id,
                csrfmiddlewaretoken: csrftoken
            },
            function (data, status) {
                $('#detail_table').bootstrapTable('load', data)
        })
}

// get detail table for a prop
$(document).ready(function () {
    $(".list-group-item").click(function () {
        update_detail_table($(this).attr("id"));
    })
});

$(function(){
    var current_id = $("#account_id_p").text();
    if (current_id == ''){
        $('#prop_edit_btn').prop('disabled', true);
        $('#prop_del_btn').prop('disabled', true);
        $('#detail_add_btn').prop('disabled', true);
        $('#detail_edit_btn').prop('disabled', true);
        $('#detail_del_btn').prop('disabled', true);
        // console.log('btn disabled')
    }
});

// delete prop
$(function(){
    $("#prop_del_btn").click(function(){
        var current_id = $("#account_id_p").text();
        var current_name = $('#account_name_p').text();
        var translations = {
            "en": "Are you sure you want to delete " +current_name +"?",
            "zh-hans": "确认删除 "+current_name+" 吗？"
            // 添加更多语言的翻译
        };
        var currentLanguage = $('#current_lan').text();
        var r = confirm(translations[currentLanguage]);
        if (r ==true){
            $.post("/prop_del/",
            {
                prop_id: current_id,
                csrfmiddlewaretoken: csrftoken
            }).done(function(){
                location.reload();
            })
        }
        
    })
});


$(function(){
    $("#detail_del_btn").click(function(){
        var did = $('#detail_id_p').text();
        var translations = {
            "en": "Are you sure you want to delete ID:" +did +"?",
            "zh-hans": "确认删除 ID:"+did+" 吗？"
            // 添加更多语言的翻译
        };
        var currentLanguage = $('#current_lan').text();
        var r = confirm(translations[currentLanguage]);
        if (r ==true){
            $.post("/detail_del/",
            {
                detail_id: did,
                csrfmiddlewaretoken: csrftoken
            })
        }
        var current_id = $("#account_id_p").text();
        update_detail_table(current_id);
    })
})

$(function(){
    $("#detail_table").on("change", 'input', function(event){
        $('#detail_edit_btn').prop('disabled', false);
        $('#detail_del_btn').prop('disabled', false);
        $("#detail_id_p").text($(this).attr("value"));
        var objs = $(".detail_edit_form").find("#id_id");
        objs.val($(this).attr("value"));
    })
})

$(function(){
    $("#detail_new_modal").on("hidden.bs.modal", function(){
        var current_id = $("#account_id_p").text();
        update_detail_table(current_id);
    })
})

$(function(){
    $("#detail_edit_modal").on("hidden.bs.modal", function(){
        var current_id = $("#account_id_p").text();
        update_detail_table(current_id);
    })
})

$(function(){
    $("#detail_edit_btn").click(function(){
        var did = $('#detail_id_p').text();
        $.post("/detail_get_post/",{
            id: did,
            csrfmiddlewaretoken: csrftoken
        },
        function (data, status) {
            for (var i=0; i<data.length; i++){
                var rec = data[i];
                console.log(rec);
                var objs = $(".detail_edit_form").find("#id_"+rec.k)
                if (objs.is('select')){
                    objs.children().filter(function() {
                        return $(this).text() == rec.v;
                        }).prop('selected', true);
                }
                else {
                    objs.val(rec.v);
                }
            }
        })
    })
})