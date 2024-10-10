// content.js

(function () {

    // 提取 GSC 数据的函数
    function extractGSCData() {
        let data = [];
        let headers = [];
        const table = document.querySelector('table');

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
            console.error("未找到数据表格");
        }

        return {headers, data};
    }

    // 获取当前页面的URL
    function getCurrentURL() {
        return window.location.href;
    }

    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        if (request.action === "extractData") {
            const extracted = extractGSCData();
            const data = extracted.data;
            const headers = extracted.headers;
            const url = getCurrentURL(); // 获取当前的URL

            if (data.length > 0 && headers.length > 0) {
                chrome.storage.local.get(["gscData"], (result) => {
                    let gscData = result.gscData || {};
                    if (!gscData[url]) {
                        gscData[url] = {headers: headers, data: []};
                    }

                    gscData[url].data.push(...data); // 将数据存储在该 URL 下

                    chrome.storage.local.set({gscData: gscData}, () => {
                        sendResponse({status: "success"});
                    });
                });
            } else {
                console.error("未能提取到数据或表头");
                sendResponse({status: "failure"});
            }
            return true;
        }
    });
})();
