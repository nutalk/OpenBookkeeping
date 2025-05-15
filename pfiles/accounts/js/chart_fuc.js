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
        },
        tooltip: {
    enabled: true,
    style: {
        background: 'transparent', // Remove default background
        border: '0' // Remove default border
    },
    custom: function({ series, seriesIndex, dataPointIndex, w }) {
        const timestamp = w.globals.seriesX[seriesIndex][dataPointIndex];
        const date = new Date(timestamp);
        const colors = w.globals.colors; // Get series colors
        
        return `
            <div class="apexcharts-tooltip-box">
                <!-- Header -->
                <div style="
                    background: #6c757d;
                    color: white;
                    padding: 8px 12px;
                    font-weight: 500;
                    border-radius: 3px 3px 0 0;
                ">
                    ${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}
                </div>
                
                <!-- Body -->
                <div style="
                    padding: 8px 12px;
                    background: white;
                    border-radius: 0 0 3px 3px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                ">
                    ${series.map((s, i) => `
                        <div style="
                            display: flex;
                            align-items: center;
                            gap: 8px;
                            margin: 4px 0;
                        ">
                            <span style="
                                display: inline-block;
                                width: 10px;
                                height: 10px;
                                border-radius: 50%;
                                background: ${colors[i]};
                            "></span>
                            <div style="
                                display: flex;
                                justify-content: space-between;
                                flex-grow: 1;
                            ">
                                <span style="color: #666">${w.globals.seriesNames[i]}:</span>
                                <span style="font-weight: 500">${s[dataPointIndex].toFixed(2)}</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
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