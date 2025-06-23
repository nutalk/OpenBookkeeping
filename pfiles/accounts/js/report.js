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
var chartCache = {};

function update_pie(series, labels, pic_id) {
  let visible = Array(series.length).fill(true);
  let originalColors = [];

  var options = {
    series: series,
    chart: {
      height: 300,
      type: 'pie',
      id: pic_id,
      events: {
        mounted: function(chartContext, config) {
          // 缓存原始颜色
          originalColors = chartContext.w.globals.colors.slice();
        },
        legendClick: function(chartContext, seriesIndex, config) {
          visible[seriesIndex] = !visible[seriesIndex];
          const newSeries = series.map((s, i) => visible[i] ? s : 0);

          // 设置图例颜色：不可见项目改为灰色
          const fillColors = originalColors.map((color, i) =>
            visible[i] ? color : "#ccc"
          );
          const labelColors = originalColors.map((color, i) =>
            visible[i] ? "#000" : "#999"
          );

          chartCache[pic_id].updateOptions({
            series: newSeries,
            chart: {
              height: 300
            },
            legend: {
              markers: {
                fillColors: fillColors
              },
              labels: {
                colors: labelColors
              }
            }
          }, true, true);

          return false;
        }
      }
    },
    labels: labels,
    legend: {
      show: true,
      position: 'right',
      offsetY: 0,
      height: 'auto',
      onItemClick: {
        toggleDataSeries: false
      },
      markers: {
        fillColors: [] // 动态填充
      },
      labels: {
        colors: []
      }
    },
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

  if (chartCache[pic_id]) {
    chartCache[pic_id].destroy();
  }

  const chart = new ApexCharts(document.querySelector("#" + pic_id), options);
  chart.render();
  chartCache[pic_id] = chart;
}



$(document).ready(function(){
  var translations = {
    "en": {
        "Occur Date": "Occur Date",
        "prop": "Total Assets",
        "det": "Total Liabilities",
        "net": "Net asset"
    },
    "zh-hans": {
      "Occur Date": "日期",
      "prop": "总资产",
      "det": "负债",
      "net": "净资产"
  }
    // 添加更多语言的翻译
};
var currentLanguage = $('#current_lan').text();

  $('#total_change_table').bootstrapTable({
    columns: [
      {
        field: 'occur_date',
        title: translations[currentLanguage]["Occur Date"]
      }, {
        field: 'prop',
        title: translations[currentLanguage]["prop"]
      }, {
        field: 'det',
        title: translations[currentLanguage]["det"]
      }, {
          field: 'net',
          title: translations[currentLanguage]["net"]
      }],
      data:[]
  });
})


$(document).ready(function(){
  var translations = {
    "en": {
        "type": "Type",
        "name": "Name",
        "amount": "Amount",
    },
    "zh-hans": {
      "type": "类别",
      "name": "名称",
      "amount": "金额",
  }
    // 添加更多语言的翻译
};
var currentLanguage = $('#current_lan').text();
  $('#total_month_detail').bootstrapTable({
    columns: [
      {
        field: 'type',
        title: translations[currentLanguage]["type"]
      }, {
        field: 'name',
        title: translations[currentLanguage]["name"]
      }, {
        field: 'amount',
        title: translations[currentLanguage]["amount"]
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
      var translations = {
        "en": "K$",
        "zh-hans": "千元"
        // 添加更多语言的翻译
    };
    var currentLanguage = $('#current_lan').text();
      // update_chart(data.series, data.x_axis, 'total_change', 'line');
      update_ts_chart('total_change', data.series, 'line', translations[currentLanguage], data.detail)
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
      var trans1 = {
        "en": "K$",
        "zh-hans": "千元"
        // 添加更多语言的翻译
    };
    var trans2 = {
      "en": "$",
      "zh-hans": "元"
      // 添加更多语言的翻译
  };
    var currentLanguage = $('#current_lan').text();
      update_ts_chart('total_predict', data.total_series, 'line', trans1[currentLanguage])
      update_ts_chart('cash_predict', data.cash_series, 'bar', trans2[currentLanguage])
    });
  
})


// 更新下个月的现金流情况
$(document).ready(function () {
  $.post("/cash_change_next_month/",
    {
      csrfmiddlewaretoken: csrftoken
    },
    function (data, status) {
      // console.log(data);
      // update_chart(data.series, data.x_axis, 'total_change', 'line');
      update_next_chart('income_part', data.income, data.income_categories);
      update_next_chart('outcome_part', data.outcome, data.outcome_categories);
      $("#income_total").text(data.income_total);
      $("#outcome_total").text(data.outcome_total);
      $("#netcome_total").text(data.netcome_total);
      $("#interest_expense").text(data.interest_expense);

    });
})
