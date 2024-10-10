// background.js

// 清除初始数据
chrome.runtime.onInstalled.addListener(() => {
    console.log("gsc_scraper 扩展已安装。");
    chrome.storage.local.remove(["gscData", "allHeaders", "headers"], () => {
        console.log("初始 GSC 数据已清除。");
    });
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "getData") {
        chrome.storage.local.get(["gscData"], (result) => {
            sendResponse({gscData: result.gscData || {}});
        });
        return true; // 异步响应
    }
});
