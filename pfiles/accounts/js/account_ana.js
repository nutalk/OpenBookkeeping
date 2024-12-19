// 发送预测请求
$(document).ready(function(){
    $("#ana_btn").click(function(){
        const rows = document.querySelectorAll('#dataTable tbody tr');
        const sdata = Array.from(rows).slice(0, -1).map(row => ({
            name: row.cells[0].innerText,
            type: row.cells[1].innerText,
            ctype: row.cells[2].innerText,
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
            update_ts_chart("ana_total_predict", data.total_series, "line", '万元');
            update_ts_chart("ana_cash_predict", data.cash_series, "bar", '元');
        });
    })
})

// 格式化数字为千位分隔符
function formatInput(input) {
input.value = input.value.replace(/,/g, '').replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// 表单验证
function validateForm() {
const name = document.getElementById('name').value.trim();
if (!name) return alert('请填写名称！');

return true;
}

// 添加表格行
function addRow() {
if (!validateForm()) return;

const name = document.getElementById('name').value.trim();
const categoryLarge = document.getElementById('categoryLarge').value;
const categorySmall = document.getElementById('categorySmall').value;
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

const deleteBtn = document.createElement('button');
deleteBtn.className = 'btn btn-danger btn-sm';
deleteBtn.textContent = '删除';
deleteBtn.onclick = () => tbody.deleteRow(row.rowIndex-1);
row.insertCell(7).appendChild(deleteBtn);

// 清空表单
document.getElementById('name').value = '';
document.getElementById('categoryLarge').value = '';
document.getElementById('categorySmall').value = '';
document.getElementById('currentValue').value = '0';
document.getElementById('annualRate').value = '0';
document.getElementById('cashFlow').value = '0';
document.getElementById('periods').value = '0';
}

