function update_ts_chart(pic_id, data_series, chart_type, ytitle) {
    var options = {
        chart: {
          height: 380,
          width: "100%",
          type: chart_type,
          animations: {
            initialAnimation: {
              enabled: false
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