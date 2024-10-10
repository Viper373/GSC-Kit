// content.js

// 提取 GSC 数据的函数
function extractGSCData() {
    let data = [];
    let headers = [];
    const table = document.querySelector('table'); // 确保选择正确的表格

    if (table) {
        headers = Array.from(table.querySelectorAll('thead th')).map(th => th.innerText.trim());
        const rows = table.querySelectorAll('tbody tr');

        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            let rowData = {};
            cells.forEach((cell, index) => {
                rowData[headers[index] || `Column${index + 1}`] = cell.innerText.trim();
            });
            data.push(rowData);
        });
    } else {
        console.error("未找到数据表格"); // 输出错误信息
    }

    return {headers, data};
}

// 监听来自弹出页面的消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "extractData") {
        const extracted = extractGSCData();
        const data = extracted.data;
        const headers = extracted.headers;

        // 检查是否成功提取数据
        if (data.length > 0 && headers.length > 0) {
            chrome.storage.local.get(["gscData", "allHeaders"], (result) => {
                let gscData = result.gscData || [];
                let allHeadersSet;

                // 确保 allHeaders 是一个数组
                if (Array.isArray(result.allHeaders)) {
                    allHeadersSet = new Set(result.allHeaders);
                } else {
                    // 如果不是数组，初始化为空的 Set
                    allHeadersSet = new Set();
                }

                // 更新所有表头
                headers.forEach(header => allHeadersSet.add(header));

                // 更新 gscData
                gscData.push(...data);

                // 更新存储
                chrome.storage.local.set({
                    gscData: gscData,
                    allHeaders: Array.from(allHeadersSet)
                }, () => {
                    sendResponse({status: "success"});
                });
            });
        } else {
            console.error("未能提取到数据或表头");
            sendResponse({status: "failure"});
        }
        return true; // 表示异步响应
    }
});

// 定义一个函数，当表格加载完成后执行
function onTableLoaded() {
    console.log('数据表格已加载，可以进行操作');
    // 您可以在这里进行一些初始化操作，或者在需要时自动提取数据
}
// 使用 MutationObserver 监听特定的 DOM 变化
const observer = new MutationObserver((mutationsList, observer) => {
    for (const mutation of mutationsList) {
        if (mutation.type === 'childList') {
            // 检查是否有我们需要的表格
            const table = document.querySelector('table');
            if (table) {
                console.log('检测到数据表格的加载');
                onTableLoaded();
                // 一旦找到表格，停止观察
                observer.disconnect();
                break;
            }
        }
    }
});

// 开始观察文档的根节点
observer.observe(document.body, { childList: true, subtree: true });