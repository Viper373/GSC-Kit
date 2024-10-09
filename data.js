// data.js

document.addEventListener('DOMContentLoaded', () => {
    loadAndDisplayData();
});

// 加载并显示数据
function loadAndDisplayData() {
    chrome.storage.local.get("gscData", (result) => {
        const dataContainer = document.getElementById('dataContainer');
        const noData = document.getElementById('noData');
        console.log("获取到的存储数据：", result.gscData);
        if (result && result.gscData && result.gscData.length > 0) {
            const data = result.gscData;
            // 清空容器
            dataContainer.innerHTML = '';
            // 创建表格
            const table = document.createElement('table');
            const thead = document.createElement('thead');
            const tbody = document.createElement('tbody');

            // 创建表头
            const headers = Object.keys(data[0]); // 获取表头
            console.log("表头顺序：", headers);
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
                headers.forEach(header => { // 使用相同的表头顺序
                    const td = document.createElement('td');
                    td.textContent = rowData[header];
                    row.appendChild(td);
                });
                tbody.appendChild(row);
            });

            table.appendChild(thead);
            table.appendChild(tbody);
            dataContainer.appendChild(table);
        } else {
            dataContainer.innerHTML = '<p id="noData">没有可显示的数据。请点击“提取数据”按钮获取数据。</p>';
        }
    });
}
