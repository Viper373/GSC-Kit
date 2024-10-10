// data.js

import {exportToExcel, showNotification} from '../scripts/function.js';

document.addEventListener('DOMContentLoaded', () => {
    loadAndDisplayData();
    setupExportButton(); // 初始化导出按钮的事件监听
    setupBackToTopButton(); // 初始化回到顶部按钮的事件监听
    setupClearDataButton(); // 初始化清空数据按钮的事件监听
});

// 设置清空数据按钮的事件监听
function setupClearDataButton() {
    const clearDataBtn = document.getElementById('clearDataBtn');
    if (clearDataBtn) { // 检查元素是否存在
        clearDataBtn.addEventListener('click', () => {
            chrome.storage.local.remove(["gscData", "allHeaders"], () => {
                console.log("所有数据已清空。");
                loadAndDisplayData(); // 重新加载并更新界面
                showNotification("提示", "数据已清空。");
            });
        });
    } else {
        console.error("未找到清空数据按钮（clearDataBtn）。请确保 data.html 中存在该元素。");
    }
}

// 设置导出按钮的事件监听
function setupExportButton() {
    const exportDataBtn = document.getElementById('exportDataBtn');
    exportDataBtn.addEventListener('click', () => {
        chrome.runtime.sendMessage({action: "getData"}, (response) => {
            const gscData = response.gscData || {};
            let hasData = false;

            Object.keys(gscData).forEach((url) => {
                if (gscData[url].data && gscData[url].data.length > 0 && gscData[url].headers && gscData[url].headers.length > 0) {
                    hasData = true;
                }
            });

            if (hasData) {
                exportToExcel(gscData);
            } else {
                showNotification("提示", "没有可导出的数据，请先提取数据。");
            }
        });
    });
}

// 加载并显示数据
function loadAndDisplayData() {
    chrome.runtime.sendMessage({action: "getData"}, (response) => {
        const dataContainer = document.getElementById('dataContainer');
        const dataCountDisplay = document.getElementById('dataCount');
        const exportDataCountDisplay = document.getElementById('exportDataCount');
        const gscData = response.gscData || {};

        let totalRowCount = 0;
        dataContainer.innerHTML = ''; // 清空容器

        Object.keys(gscData).forEach((url, index) => {
            const {headers, data} = gscData[url];
            totalRowCount += data.length;

            if (data.length > 0 && headers.length > 0) {
                // 创建URL标题
                const urlTitle = document.createElement('h2');
                urlTitle.textContent = `数据源自：${decodeURIComponent(url)}`;
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
        exportDataCountDisplay.textContent = `导出数据条数: ${totalRowCount}`;
    });
}

// 设置回到顶部按钮的事件监听
function setupBackToTopButton() {
    const backToTopBtn = document.getElementById('backToTopBtn');

    // 点击按钮时回到顶部
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({top: 0, behavior: 'smooth'});
    });

    // 控制回到顶部按钮的显示与隐藏
    window.addEventListener('scroll', () => {
        if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
            backToTopBtn.style.display = "block";
        } else {
            backToTopBtn.style.display = "none";
        }
    });
}
