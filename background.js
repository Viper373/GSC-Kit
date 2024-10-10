// background.js

// 清除初始数据
chrome.runtime.onInstalled.addListener(() => {
    console.log("gsc_scraper 扩展已安装。");
    // 清除初始存储的数据，包括旧的 headers
    chrome.storage.local.remove(["gscData", "allHeaders", "headers"], () => {
        console.log("初始 GSC 数据已清除。");
    });
});

// 判断是否为目标 GSC 页面
function isGSCUrl(url) {
    const patterns = [
        /^https:\/\/search\.google\.com\/.*\/search-console\/performance\/.*/
    ];
    return patterns.some(pattern => pattern.test(url));
}

// 监听历史状态更新事件（用于 SPA 内部导航）
chrome.webNavigation.onHistoryStateUpdated.addListener(function(details) {
    if (isGSCUrl(details.url)) {
        // 在目标页面上重新注入内容脚本
        chrome.scripting.executeScript({
            target: { tabId: details.tabId },
            files: ['content.js']
        });
    }
});

// 移除注入内容脚本的代码，因为 content_scripts 已经处理了

// 添加消息监听器来处理 'getData' 消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "getData") {
        chrome.storage.local.get(["gscData", "allHeaders"], (result) => {
            sendResponse({gscData: result.gscData || [], allHeaders: result.allHeaders || []});
        });
        return true; // 表示异步响应
    }
});
