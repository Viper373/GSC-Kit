// popup.js

import { exportToExcel, showNotification } from '../scripts/function.js';
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
            if (Object.keys(gscData).length > 0) { // 修改前: response.gscData.length > 0
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

// 加载数据并根据是否有数据显示“查看数据”按钮
function loadDataAndUpdateUI() {
    chrome.runtime.sendMessage({action: "getData"}, (response) => {
        const viewDataBtn = document.getElementById('viewDataBtn');
        if (response && response.gscData && Object.keys(response.gscData).length > 0) { // 修改前: response.gscData.length > 0
            viewDataBtn.style.display = 'block'; // 显示按钮
        } else {
            viewDataBtn.style.display = 'none'; // 隐藏按钮
        }
        updateDataCount(); // 确保更新数据条数
    });
}
