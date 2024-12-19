// 发送预测请求
$(document).ready(function(){
    $("#ana_btn").click(function(){
        const rows = document.querySelectorAll('#dataTable tbody tr');
        const sdata = Array.from(rows).slice(0, -1).map(row => ({
            name: row.cells[0].innerText,
            categoryLarge: row.cells[1].innerText,
            categorySmall: row.cells[2].innerText,
            currentValue: row.cells[3].innerText.replace(/,/g, ''),
            annualRate: row.cells[4].innerText.replace('%', ''),
            cashFlow: row.cells[5].innerText,
            periods: row.cells[6].innerText,
        }));
        $.post("/analyze_debt/",
        {
            ssdata: JSON.stringify(sdata),
            csrfmiddlewaretoken: csrftoken,
        },
        function (data, status) {
            console.log(data);
            // update_ts_chart("long_term_chart", data.long_series, "area", '万元');
            // update_ts_chart("short_term_chart", data.short_series, "line", '万元');
        });
    })
})


// 动态更新小类选项
function updateSubCategory() {
const category = document.getElementById('categoryLarge').value;
const subCategory = document.getElementById('categorySmall');
subCategory.innerHTML = ''; // 清空小类

let options = [];
if (category === '资产') options = ['按月收利', '到期收本息'];
else if (category === '负债') options = ['等额本息', '先息后本', '等额本金', '到期还本付息'];
else if (category === '自由现金流') options = ['月度'];

options.forEach(option => {
    const opt = document.createElement('option');
    opt.value = option;
    opt.textContent = option;
    subCategory.appendChild(opt);
});
}

// 格式化数字为千位分隔符
function formatInput(input) {
input.value = input.value.replace(/,/g, '').replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// 表单验证
function validateForm() {
const name = document.getElementById('name').value.trim();
const categoryLarge = document.getElementById('categoryLarge').value;
const categorySmall = document.getElementById('categorySmall').value;
const currentValue = document.getElementById('currentValue').value.replace(/,/g, '').trim();

if (!name) return alert('请填写名称！');
if (!categoryLarge) return alert('请选择大类！');
if (!categorySmall) return alert('请选择小类！');
if (!currentValue || currentValue === '0') return alert('请填写当前价值！');

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
document.getElementById('categorySmall').innerHTML = '';
document.getElementById('currentValue').value = '0';
document.getElementById('annualRate').value = '0';
document.getElementById('cashFlow').value = '0';
document.getElementById('periods').value = '0';
}

