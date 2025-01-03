function update_ts_chart(pic_id, data_series, chart_type, ytitle, detail_data=null) {
    var options = {
        chart: {
          height: 380,
          width: "100%",
          type: chart_type,
          animations: {
            initialAnimation: {
              enabled: false
            }
          },
          events:{
            click(event, chartContext, opts){
              if (detail_data){
                console.log(opts.dataPointIndex);
                $('#total_month_detail').bootstrapTable('load', detail_data[opts.dataPointIndex]);
                // var show_detail = detail_data[opts.dataPointIndex];
              }
              
            }
          }
        },
        dataLabels: {
          enabled: false,
        },
        series: data_series,
        xaxis: {
          type: "datetime",
          labels: {
            datetimeFormatter: {
              year: 'yyyy',
              month: 'yyyy-MM',
              day: 'yyyy-MM-dd',
              hour: 'HH:mm'
            }
          }
        },
        yaxis: {
          labels: {
            formatter: function(val, index) {
              return val.toFixed(2);
            }
          },
          title: {
            text: ytitle
          },
        }
      };
      
      var chart = new ApexCharts(document.querySelector("#"+pic_id), options);
      
      chart.render();
}

function update_next_chart(pic_id, data_series, v_categories){
  var translations = {
    "en": "$",
    "zh-hans": "元"
    // 添加更多语言的翻译
};
var currentLanguage = $('#current_lan').text();
  var options = {
    series: data_series,
    chart: {
    type: 'bar',
    height: 350,
    stacked: true,
  },
  plotOptions: {
    bar: {
      horizontal: true,
      dataLabels: {
        total: {
          enabled: true,
          offsetX: 0,
          style: {
            fontSize: '13px',
            fontWeight: 900
          }
        }
      }
    },
  },
  stroke: {
    width: 1,
    colors: ['#fff']
  },

  xaxis: {
    categories: v_categories,
    labels: {
      formatter: function (val) {
        return val + translations[currentLanguage]
      }
    }
  },
  yaxis: {
    title: {
      text: undefined
    },
  },
  tooltip: {
    y: {
      formatter: function (val) {
        return val + translations[currentLanguage]
      }
    }
  },
  fill: {
    opacity: 1
  },
  legend: {
    position: 'top',
    horizontalAlign: 'left',
    offsetX: 40
  }
  };

  var chart = new ApexCharts(document.querySelector("#"+pic_id), options);
  chart.render();
}