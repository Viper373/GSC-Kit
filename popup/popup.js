// popup.js

// 更新数据条数
function updateDataCount() {
    chrome.runtime.sendMessage({action: "getData"}, (response) => {
        const gscData = response.gscData || {};
        let totalCount = 0;

        // 统计所有 URL 的数据条数
        Object.keys(gscData).forEach((url) => {
            const data = gscData[url].data || [];
            totalCount += data.length;
        });

        const dataCountDisplay = document.getElementById('dataCount');
        dataCountDisplay.textContent = `当前数据条数: ${totalCount}`; // 确保正确显示数据条数

        const viewDataBtn = document.getElementById('viewDataBtn');
        const clearDataBtn = document.getElementById('clearDataBtn');

        if (totalCount > 0) {
            viewDataBtn.style.display = 'block';
            clearDataBtn.style.display = 'block';
        } else {
            viewDataBtn.style.display = 'none';
            clearDataBtn.style.display = 'none';
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
                        showNotification("错误", "无法与内容脚本通信。请确保您在正确的页面上，并已重新加载页面。");
                        return;
                    }
                    if (response && response.status === "success") {
                        // 处理成功响应
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
        chrome.runtime.sendMessage({action: "getData"}, (response) => {
            const gscData = response.gscData || {};
            if (Object.keys(gscData).length > 0) {
                exportToExcel(gscData);
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
        iconUrl: 'images/icon-48.png', // 使用48px图标
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

// sheet 名称生成函数
function generateSheetName(url) {
    const urlParams = new URLSearchParams(url.split('?')[1]); // 获取URL中的查询参数
    const resourceId = urlParams.get('resource_id');
    const page = urlParams.get('page');
    const breakdown = urlParams.get('breakdown');

    // 提取域名
    let domain = resourceId.includes('%3A') ? resourceId.split('%3A')[1] : resourceId;

    // 提取页面路径，并替换 `%2F` 为 `/`
    let pagePath = page.replace(/%2F/g, '/');

    // 提取page或query后所有的参数
    let paramsAfterPageOrQuery = '';
    for (const [key, value] of urlParams) {
        if (key !== 'resource_id' && key !== 'page' && key !== 'breakdown') {
            paramsAfterPageOrQuery += `-${key}-${value}`;
        }
    }

    // 生成 sheet 名称
    let sheetName = `${domain}-${pagePath}-${breakdown}${paramsAfterPageOrQuery}`;
    // 替换非法字符：: \ / ? * [ ] 等
    sheetName = sheetName.replace(/[:\\\/\?\*\[\]]/g, '');

    // 处理可能的超长名称，sheet 名不能超过31个字符
    return sheetName.length > 31 ? sheetName.slice(0, 31) : sheetName;
}

// 使用 xlsx.mjs 导出数据为 Excel 文件
async function exportToExcel(gscData) {
    try {
        const xlsxModule = await import('../scripts/xlsx.mjs');
        const {utils, write} = xlsxModule;
        const workbook = utils.book_new();

        // 针对每个 URL 创建一个 sheet
        Object.keys(gscData).forEach((url) => {
            const {headers, data} = gscData[url];
            const worksheetData = [headers];
            data.forEach(row => {
                const rowData = headers.map(header => row[header] || "");
                worksheetData.push(rowData);
            });
            const worksheet = utils.aoa_to_sheet(worksheetData);

            // 使用 generateSheetName 函数生成 sheet 名称
            const sheetName = generateSheetName(url);
            utils.book_append_sheet(workbook, worksheet, sheetName);
        });

        // 导出 Excel 文件
        const excelBuffer = write(workbook, {bookType: 'xlsx', type: 'array'});
        const blob = new Blob([excelBuffer], {type: 'application/octet-stream'});
        const downloadUrl = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = 'gsc_data.xlsx';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(downloadUrl);

        showNotification("成功", "Excel 文件已下载");

        // 导出成功后清空所有数据
        chrome.storage.local.remove(["gscData"], () => {
            console.log("所有数据已清空。");
            const dataCountDisplay = document.getElementById('dataCount');
            dataCountDisplay.textContent = "当前数据条数: 0";
        });
    } catch (error) {
        console.error("导出Excel失败:", error);
        showNotification("错误", "导出Excel失败，请重试。");
    }
}
