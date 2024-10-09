// background.js

// 检查 URL 是否匹配目标模式
function isTargetUrl(url) {
    const patterns = [
        /^https:\/\/search\.google\.com\/u\/2\/search-console\/performance\/.*/,
        /^https:\/\/search\.google\.com\/u\/2\/search-console\/index\/.*/
    ];
    return patterns.some(pattern => pattern.test(url));
}

// 监听标签页更新以检测 URL 变化
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.url) {
        // 如果新 URL 匹配目标 URL，则清除数据
        if (isTargetUrl(changeInfo.url)) {
            chrome.storage.local.remove("gscData", () => {
                console.log("由于 URL 变化，GSC 数据已清除。");
            });
        }
    }
});

// 监听标签页激活事件，确保当前活动标签页的 URL 是否匹配
chrome.tabs.onActivated.addListener(activeInfo => {
    chrome.tabs.get(activeInfo.tabId, (tab) => {
        if (tab && isTargetUrl(tab.url)) {
            chrome.storage.local.remove("gscData", () => {
                console.log("由于标签页激活，GSC 数据已清除。");
            });
        }
    });
});

// 可选：监听窗口焦点变化，确保在切换窗口时清除数据
chrome.windows.onFocusChanged.addListener(windowId => {
    if (windowId !== chrome.windows.WINDOW_ID_NONE) {
        chrome.tabs.query({active: true, windowId: windowId}, (tabs) => {
            if (tabs[0] && isTargetUrl(tabs[0].url)) {
                chrome.storage.local.remove("gscData", () => {
                    console.log("由于窗口焦点变化，GSC 数据已清除。");
                });
            }
        });
    }
});

// 清除初始数据
chrome.runtime.onInstalled.addListener(() => {
    console.log("gsc_scraper 扩展已安装。");
    // 清除初始存储的数据
    chrome.storage.local.remove("gscData", () => {
        console.log("初始 GSC 数据已清除。");
    });
});
