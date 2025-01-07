// 发送预测请求
$(document).ready(function(){
    $("#ana_btn").click(function(){
        const rows = document.querySelectorAll('#dataTable tbody tr');
        const sdata = Array.from(rows).slice(0, -1).map(row => ({
            name: row.cells[0].innerText,
            type: row.cells[7].innerText,
            ctype: row.cells[8].innerText,
            sum_amount: row.cells[3].innerText.replace(/,/g, ''),
            rate: row.cells[4].innerText.replace('%', ''),
            currency: row.cells[5].innerText,
            term_month: row.cells[6].innerText,
        }));
        $.post("/analyze_debt/",
        {
            ssdata: JSON.stringify(sdata),
            csrfmiddlewaretoken: csrftoken,
        },
        function (data, status) {
            console.log(data);
            var trans1 = {
              "en": "K$",
              "zh-hans": "万元"
              // 添加更多语言的翻译
          };
          var trans2 = {
            "en": "$",
            "zh-hans": "元"
            // 添加更多语言的翻译
        };
          var currentLanguage = $('#current_lan').text();
            update_ts_chart("ana_total_predict", data.total_series, "line", trans1[currentLanguage]);
            update_ts_chart("ana_cash_predict", data.cash_series, "bar", trans2[currentLanguage]);
            $('#ana_cashflow_table').bootstrapTable('load', data.table)
        });
    })
})

// 格式化数字为千位分隔符
function formatInput(input) {
input.value = input.value.replace(/,/g, '').replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// 表单验证
function validateForm() {
  var trans1 = {
    "en": "Please fill account name!",
    "zh-hans": "请填写名称！"
    // 添加更多语言的翻译
};
var currentLanguage = $('#current_lan').text();
  const name = document.getElementById('name').value.trim();
  if (!name) return alert(trans1[currentLanguage]);

  return true;
}

// 添加表格行
function addRow() {
if (!validateForm()) return;

const name = document.getElementById('name').value.trim();
var selLarge = document.getElementById("categoryLarge");
var categoryLarge = selLarge.options[selLarge.selectedIndex].text;
var account_type = selLarge.value;

var selSmall = document.getElementById("categorySmall");
var categorySmall = selSmall.options[selSmall.selectedIndex].text;
var repayment_type = selSmall.value;

const currentValue = document.getElementById('currentValue').value;
const annualRate = document.getElementById('annualRate').value;
const cashFlow = document.getElementById('cashFlow').value;
const periods = document.getElementById('periods').value;

const tbody = document.querySelector('#dataTable tbody');
const row = tbody.insertRow(tbody.rows.length - 1); // 在表单行前插入

row.insertCell(0).innerText = name;
row.insertCell(1).innerText = categoryLarge;
row.insertCell(2).innerText = categorySmall;
row.insertCell(3).innerText = currentValue;
row.insertCell(4).innerText = annualRate + '%';
row.insertCell(5).innerText = cashFlow;
row.insertCell(6).innerText = periods;
row.insertCell(7).innerText = account_type;
row.insertCell(8).innerText = repayment_type; 
 // 隐藏新插入行的最后两列
 row.cells[7].classList.add('hidden-column');
 row.cells[8].classList.add('hidden-column');

var trans1 = {
  "en": "Delet",
  "zh-hans": "删除"
  // 添加更多语言的翻译
};
var currentLanguage = $('#current_lan').text();

const deleteBtn = document.createElement('button');
deleteBtn.className = 'btn btn-danger btn-sm';
deleteBtn.textContent = trans1[currentLanguage];
deleteBtn.onclick = () => tbody.deleteRow(row.rowIndex-1);
row.insertCell(9).appendChild(deleteBtn);

// 清空表单
document.getElementById('name').value = '';
document.getElementById('categoryLarge').value = '';
document.getElementById('categorySmall').value = '';
document.getElementById('currentValue').value = '0';
document.getElementById('annualRate').value = '0';
document.getElementById('cashFlow').value = '0';
document.getElementById('periods').value = '0';
}

// 现金流明细表
$(document).ready(function(){
  var translations = {
    "en": {
        "date": "Data",
        "name": "Name",
        "balance": "Balance",
        "payment": "Repayment",
        "amortization": "Principal",
        "interest": "Interest"
    },
    "zh-hans": {
      "date": "日期",
      "name": "名称",
      "balance": "余额",
      "payment": "现金流",
      "amortization": "本金",
      "interest": "利息"
  }
    // 添加更多语言的翻译
};
var currentLanguage = $('#current_lan').text();
    $('#ana_cashflow_table').bootstrapTable({
      columns: [
        {
          field: 'date',
          title: translations[currentLanguage]['date']
        }, {
          field: 'name',
          title: translations[currentLanguage]['name']
        }, {
          field: 'balance',
          title: translations[currentLanguage]['balance'],
          formatter: function (value, row, index) {
            value = parseInt(value).toString();
            var parts = value.split('.');
            parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
            return parts.join('.');
          }
        }, {
            field: 'payment',
            title: translations[currentLanguage]['payment'],
            formatter: function (value, row, index) {
                value = parseInt(value).toString();
                var parts = value.split('.');
                parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
                return parts.join('.');
              }
        },{
            field: 'amortization',
            title: translations[currentLanguage]['amortization'],
            formatter: function (value, row, index) {
                value = parseInt(value).toString();
                var parts = value.split('.');
                parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
                return parts.join('.');
              }
        },{
            field: 'interest',
            title: translations[currentLanguage]['interest'],
            formatter: function (value, row, index) {
                value = parseInt(value).toString();
                var parts = value.split('.');
                parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
                return parts.join('.');
              }
        }],
        data:[]
    });
  })