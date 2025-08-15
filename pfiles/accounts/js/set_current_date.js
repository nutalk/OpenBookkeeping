// 设置日期输入字段为当前日期
document.addEventListener('DOMContentLoaded', function() {
    // 获取当前日期并格式化为YYYY-MM-DD格式
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const todayString = `${year}-${month}-${day}`;
    
    // 找到所有日期输入字段并设置当前日期
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(function(input) {
        // 只有当输入框为空时才设置当前日期
        if (!input.value) {
            input.value = todayString;
        }
    });
});
