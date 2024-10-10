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
        const gscData = response.gscData || {};

        let totalRowCount = 0;
        dataContainer.innerHTML = ''; // 清空容器

        Object.keys(gscData).forEach((url, index) => {
            const { headers, data } = gscData[url];
            totalRowCount += data.length;

            if (data.length > 0 && headers.length > 0) {
                // 创建URL标题
                const urlTitle = document.createElement('h2');
                urlTitle.textContent = `数据源自：${url}`;
                dataContainer.appendChild(urlTitle);

                // 创建表格
                const table = document.createElement('table');
                const thead = document.createElement('thead');
                const tbody = document.createElement('tbody');

                // 创建表头
                const headerRow = document.createElement('tr');
                headers.forEach(header => {
                    const th = document.createElement('th');
                    th.textContent = header;
                    headerRow.appendChild(th);
                });
                thead.appendChild(headerRow);

                // 创建表体
                data.forEach(rowData => {
                    const row = document.createElement('tr');
                    headers.forEach(header => {
                        const td = document.createElement('td');
                        td.textContent = rowData[header] || '';
                        row.appendChild(td);
                    });
                    tbody.appendChild(row);
                });

                table.appendChild(thead);
                table.appendChild(tbody);
                dataContainer.appendChild(table);
            }
        });

        // 显示总数据行数
        dataCountDisplay.textContent = `当前数据条数: ${totalRowCount}`;
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

// sheet 名称生成函数
function generateSheetName(url) {
    const urlParams = new URLSearchParams(url.split('?')[1]); // 获取URL中的查询参数
    const resourceId = urlParams.get('resource_id');
    const page = urlParams.get('page');
    const breakdown = urlParams.get('breakdown');

    // 提取域名，去掉前缀 'sc-domain%3A'
    let domain = resourceId.includes('sc-domain%3A') ? resourceId.split('%3A')[1] : resourceId;

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
