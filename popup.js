// popup.js

// 更新数据条数
function updateDataCount() {
    chrome.runtime.sendMessage({action: "getData"}, (response) => {
        if (response && response.gscData) {
            const dataCount = response.gscData.length;
            const dataCountDisplay = document.getElementById('dataCount');
            dataCountDisplay.textContent = `当前数据条数: ${dataCount}`;

            const viewDataBtn = document.getElementById('viewDataBtn');
            const clearDataBtn = document.getElementById('clearDataBtn'); // 新增

            if (dataCount > 0) {
                viewDataBtn.style.display = 'block';
                clearDataBtn.style.display = 'block'; // 显示清空数据按钮
            } else {
                viewDataBtn.style.display = 'none';
                clearDataBtn.style.display = 'none'; // 隐藏清空数据按钮
            }
        } else {
            const dataCountDisplay = document.getElementById('dataCount');
            dataCountDisplay.textContent = `当前数据条数: 0`;
            const viewDataBtn = document.getElementById('viewDataBtn');
            const clearDataBtn = document.getElementById('clearDataBtn'); // 新增
            viewDataBtn.style.display = 'none';
            clearDataBtn.style.display = 'none'; // 隐藏清空数据按钮
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const extractBtn = document.getElementById('extractBtn');
    const exportBtn = document.getElementById('exportBtn');
    const viewDataBtn = document.getElementById('viewDataBtn');
    const clearDataBtn = document.getElementById('clearDataBtn');

    // 加载并更新UI
    loadDataAndUpdateUI();

    // 提取数据按钮点击事件
    extractBtn.addEventListener('click', () => {
        // 向当前活动标签页的内容脚本发送提取数据的消息
        chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
            if (tabs[0]) {
                chrome.tabs.sendMessage(tabs[0].id, {action: "extractData"}, (response) => {
                    if (chrome.runtime.lastError) {
                        console.error("发送消息时出错:", chrome.runtime.lastError.message);
                        return;
                    }
                    if (response && response.status === "success") {
                        // 更新数据条数和按钮显示
                        updateDataCount();
                    } else {
                        showNotification("失败", "数据提取失败。请确保在正确的页面上运行此扩展。");
                    }
                });
            } else {
                console.error("未找到活动标签页。");
            }
        });
    });

    // 导出为 Excel 按钮点击事件
    exportBtn.addEventListener('click', () => {
        // 从存储中获取数据并导出
        chrome.runtime.sendMessage({action: "getData"}, (response) => {
            if (response && response.gscData && response.gscData.length > 0 && response.allHeaders && response.allHeaders.length > 0) {
                exportToExcel(response.allHeaders, response.gscData);
            } else {
                showNotification("提示", "没有可导出的数据，请先提取数据。");
            }
        });
    });

    // 查看数据按钮点击事件
    viewDataBtn.addEventListener('click', () => {
        const dataUrl = chrome.runtime.getURL('data.html');
        chrome.tabs.create({url: dataUrl});
    });

    // 清空数据按钮点击事件
    clearDataBtn.addEventListener('click', () => {
        chrome.storage.local.remove(["gscData", "allHeaders", "headers"], () => {
            console.log("所有数据已清空。");
            updateDataCount();
            showNotification("提示", "数据已清空。");
        });
    });
});

// 监听提取完成的消息以显示提示（可选）
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "extractionComplete") {
        loadDataAndUpdateUI(); // 加载并更新UI
    }
});

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

// 加载数据并根据是否有数据显示“查看数据”按钮
function loadDataAndUpdateUI() {
    chrome.runtime.sendMessage({action: "getData"}, (response) => {
        const viewDataBtn = document.getElementById('viewDataBtn');
        if (response && response.gscData && response.gscData.length > 0) {
            viewDataBtn.style.display = 'block'; // 显示按钮
        } else {
            viewDataBtn.style.display = 'none'; // 隐藏按钮
        }
        updateDataCount(); // 确保更新数据条数
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

