// 获取基本资金信息
$(document).ready(function () {
  $.post("/post_total_info/",
    {
      csrfmiddlewaretoken: csrftoken
    },
    function (data, status) {
      console.log(data);
      var total_data = data.total;
      for (var i = 0; i < total_data.length; i++) {
        var rec = total_data[i];
        $("#" + rec.k).text(rec.v);
      }
      update_pie(data.ar, data.an, "assets_part");
      update_pie(data.dr, data.dn, "det_part");
    });
})

// 更新资产和负债的组成
function update_pie(series, labels, pic_id) {
  var options = {
    series: series,
    chart: {
      height: 300,
      type: 'pie',
    },
    labels: labels,
    responsive: [{
      breakpoint: 480,
      options: {
        chart: {
          width: 200
        },
        legend: {
          position: 'bottom'
        }
      }
    }]
  };

  var chart = new ApexCharts(document.querySelector("#"+pic_id), options);
  chart.render();
}

$(document).ready(function(){
  $('#total_change_table').bootstrapTable({
    columns: [
      {
        field: 'occur_date',
        title: '日期'
      }, {
        field: 'prop',
        title: '总资产'
      }, {
        field: 'det',
        title: '负债'
      }, {
          field: 'net',
          title: "净资产"
      }],
      data:[]
  });
})

// 更新资产负债和净值的变动
$(document).ready(function () {
  $.post("/post_month_history/",
    {
      csrfmiddlewaretoken: csrftoken
    },
    function (data, status) {
      console.log(data);
      // update_chart(data.series, data.x_axis, 'total_change', 'line');
      update_ts_chart('total_change', data.series, 'line', '万元')
      $('#total_change_table').bootstrapTable('load', data.table)
    });
})

// 更新预测图
$(document).ready(function () {
  $.post("/post_month_predict/",
    {
      csrfmiddlewaretoken: csrftoken
    },
    function (data, status) {
      // update_chart(data.total_series, data.x_axis, 'total_predict', 'line');
      update_ts_chart('total_predict', data.total_series, 'line', '万元')
      // update_chart(data.cash_series, data.x_axis, 'cash_predict', 'bar');
      update_ts_chart('cash_predict', data.cash_series, 'line', '元')
    });
  
})


// 更新下个月的现金流情况
$(document).ready(function () {
  $.post("/cash_change_next_month/",
    {
      csrfmiddlewaretoken: csrftoken
    },
    function (data, status) {
      console.log(data);
      // update_chart(data.series, data.x_axis, 'total_change', 'line');
      update_next_chart('income_part', data.income, data.income_categories),
      update_next_chart('outcome_part', data.outcome, data.outcome_categories)
    });
})
