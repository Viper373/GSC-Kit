// content.js

// 提取 GSC 数据的函数
function extractGSCData() {
    let data = [];
    // 示例：假设数据位于页面的第一个表格中
    const table = document.querySelector('table'); // 根据实际情况调整选择器
    if (table) {
        const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.innerText.trim());
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            let rowData = {};
            cells.forEach((cell, index) => {
                rowData[headers[index] || `Column${index + 1}`] = cell.innerText.trim();
            });
            data.push(rowData);
        });
    }
    return data;
}

// 监听来自弹出页面的消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "extractData") {
        const data = extractGSCData();
        if (data.length > 0) {
            // 保存数据到 storage
            chrome.storage.local.set({gscData: data}, () => {
                console.log("GSC 数据已保存。");
                sendResponse({status: "success"});
            });
        } else {
            sendResponse({status: "failure"});
        }
        return true; // 表示异步响应
    }
});
