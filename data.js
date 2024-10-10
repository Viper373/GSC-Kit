// data.js

document.addEventListener('DOMContentLoaded', () => {
    loadAndDisplayData();
    setupExportButton(); // 初始化导出按钮的事件监听
    setupBackToTopButton(); // 初始化回到顶部按钮的事件监听
    setupClearDataButton(); // 初始化清空数据按钮的事件监听
});

// 添加新的函数
function setupClearDataButton() {
    const clearDataBtn = document.getElementById('clearDataBtn');
    clearDataBtn.addEventListener('click', () => {
        chrome.storage.local.remove(["gscData", "allHeaders"], () => {
            console.log("所有数据已清空。");
            loadAndDisplayData(); // 重新加载并更新界面
            showNotification("提示", "数据已清空。");
        });
    });
}

// 加载并显示数据
function loadAndDisplayData() {
    chrome.runtime.sendMessage({action: "getData"}, (response) => {
        const dataContainer = document.getElementById('dataContainer');
        const dataCountDisplay = document.getElementById('dataCount');
        const gscData = response.gscData || [];
        const allHeaders = response.allHeaders || [];

        if (gscData.length > 0 && allHeaders.length > 0) {
            // 更新数据条数
            dataCountDisplay.textContent = `当前数据条数: ${gscData.length}`;

            // 清空容器
            dataContainer.innerHTML = '';
            // 创建表格
            const table = document.createElement('table');
            const thead = document.createElement('thead');
            const tbody = document.createElement('tbody');

            // 创建表头
            const headerRow = document.createElement('tr');
            allHeaders.forEach(header => {
                const th = document.createElement('th');
                th.textContent = header;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);

            // 创建表体
            gscData.forEach(rowData => {
                const row = document.createElement('tr');
                allHeaders.forEach(header => {
                    const td = document.createElement('td');
                    td.textContent = rowData[header] || '';
                    row.appendChild(td);
                });
                tbody.appendChild(row);
            });

            table.appendChild(thead);
            table.appendChild(tbody);
            dataContainer.appendChild(table);
        } else {
            dataContainer.innerHTML = '<p id="noData">没有可显示的数据。请点击“提取数据”按钮获取数据。</p>';
            dataCountDisplay.textContent = "当前数据条数: 0";
        }
    });
}

// 设置导出按钮的事件监听
function setupExportButton() {
    const exportDataBtn = document.getElementById('exportDataBtn');
    exportDataBtn.addEventListener('click', () => {
        chrome.runtime.sendMessage({action: "getData"}, (response) => {
            if (response && response.gscData && response.gscData.length > 0 && response.headers && response.headers.length > 0) {
                exportToExcel(response.headers, response.gscData);
            } else {
                showNotification("提示", "没有可导出的数据，请先提取数据。");
            }
        });
    });
}

// 使用 xlsx.mjs 导出数据为 Excel 文件
async function exportToExcel(allHeaders, data) {
    try {
        const xlsxModule = await import('./libs/xlsx.mjs');
        const {utils, write} = xlsxModule;
        // 构建一个二维数组，第一行是表头，后续行是数据
        const worksheetData = [allHeaders];
        data.forEach(row => {
            const rowData = allHeaders.map(header => row[header] || "");
            worksheetData.push(rowData);
        });
        const worksheet = utils.aoa_to_sheet(worksheetData);
        const workbook = utils.book_new();
        utils.book_append_sheet(workbook, worksheet, "GSC Data");
        const excelBuffer = write(workbook, {bookType: 'xlsx', type: 'array'});
        const blob = new Blob([excelBuffer], {type: 'application/octet-stream'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'gsc_data.xlsx';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        showNotification("成功", "Excel 文件已下载");

        // 导出成功后清空所有数据
        chrome.storage.local.remove(["gscData", "allHeaders"], () => {
            console.log("所有数据已清空。");
            const dataCountDisplay = document.getElementById('dataCount');
            dataCountDisplay.textContent = "当前数据条数: 0";
        });
    } catch (error) {
        console.error("导出Excel失败:", error);
        showNotification("错误", "导出Excel失败，请重试。");
    }
}

// 设置回到顶部按钮的事件监听
function setupBackToTopButton() {
    const backToTopBtn = document.getElementById('backToTopBtn');

    // 点击按钮时回到顶部
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({top: 0, behavior: 'smooth'});
    });
}

// 控制回到顶部按钮的显示与隐藏
function scrollFunction() {
    const backToTopBtn = document.getElementById('backToTopBtn');
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
        backToTopBtn.style.display = "block";
    } else {
        backToTopBtn.style.display = "none";
    }
}

// 使用系统通知代替 alert
function showNotification(title, message) {
    chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon48.png', // 使用48px图标
        title: title,
        message: message
    }, (notificationId) => {
        // 可选：在一定时间后自动关闭通知
        setTimeout(() => {
            chrome.notifications.clear(notificationId);
        }, 5000);
    });
}
