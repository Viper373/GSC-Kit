// content.js

(function () {

    // 提取 GSC 数据的函数，返回一个 Promise
    function extractGSCData() {
        return new Promise((resolve) => {
            const table = document.querySelector('table');
            if (!table) {
                console.error("未找到数据表格");
                resolve({ headers: [], data: [] });
                return;
            }

            const tbody = table.querySelector('tbody');
            if (!tbody) {
                console.error("未找到表格的 tbody");
                resolve({ headers: [], data: [] });
                return;
            }

            const extractData = () => {
                let data = [];
                let headers = Array.from(table.querySelectorAll('thead th')).map(th => th.innerText.trim());
                const rows = tbody.querySelectorAll('tr');

                if (rows.length === 0) {
                    console.warn("表格中没有数据行");
                    return null;
                }

                rows.forEach(row => {
                    const cells = row.querySelectorAll('td');
                    let rowData = {};
                    cells.forEach((cell, index) => {
                        rowData[headers[index] || `Column${index + 1}`] = cell.innerText.trim();
                    });
                    data.push(rowData);
                });

                return { headers, data };
            };

            const observer = new MutationObserver((mutations, obs) => {
                const result = extractData();
                if (result) {
                    obs.disconnect();
                    resolve(result);
                }
            });

            observer.observe(tbody, { childList: true, subtree: true });

            // 如果表格已经加载，立即提取数据
            const result = extractData();
            if (result) {
                observer.disconnect();
                resolve(result);
            }
        });
    }

    // 获取当前页面的 URL 并解码
    function getCurrentURL() {
        const currentURL = window.location.href;
        console.log(`当前页面 URL: ${currentURL}`); // 添加日志
        return decodeURIComponent(currentURL);
    }

    // 函数：处理提取数据
    function handleExtractData(sendResponse) {
        extractGSCData().then(extracted => {
            const data = extracted.data;
            const headers = extracted.headers;
            const url = getCurrentURL(); // 获取并解码当前的 URL

            console.log(`提取数据自 URL: ${url}`); // 添加日志

            if (data.length > 0 && headers.length > 0) {
                chrome.storage.local.get(["gscData"], (result) => {
                    let gscData = result.gscData || {};
                    if (!gscData[url]) {
                        gscData[url] = { headers: headers, data: [] };
                        console.log(`初始化 URL 的数据存储: ${url}`); // 添加日志
                    } else {
                        console.log(`追加数据到现有 URL 的数据存储: ${url}`); // 添加日志
                    }

                    gscData[url].data.push(...data); // 将数据存储在该 URL 下
                    console.log("数据:", gscData); // 添加日志

                    chrome.storage.local.set({ gscData: gscData }, () => {
                        console.log(`数据成功存储到 URL: ${url}`); // 添加日志
                        sendResponse({ status: "success" });
                    });
                });
            } else {
                console.error("未能提取到数据或表头");
                sendResponse({ status: "failure" });
            }
        });

        return true; // 异步响应
    }

    // 监听消息
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        if (request.action === "extractData") {
            handleExtractData(sendResponse);
            return true; // 异步响应
        }
    });

    // 监听 URL 变化（适用于 SPA）
    let lastUrl = location.href;
    const observer = new MutationObserver(() => {
        const currentUrl = location.href;
        if (currentUrl !== lastUrl) {
            lastUrl = currentUrl;
            console.log(`URL 已更改为: ${currentUrl}`); // 添加日志
            // 可在此处执行其他操作，如自动提取数据
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });

})();
