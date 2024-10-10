// function.js
// sheet 名称生成函数
export function generateSheetName(url) {
    const urlParams = new URLSearchParams(url.split('?')[1]); // 获取URL中的查询参数
    const resourceId = urlParams.get('resource_id');
    const page = urlParams.get('page');
    const breakdown = urlParams.get('breakdown');

    // 提取域名
    let domain = resourceId.includes('%3A') ? resourceId.split('%3A')[1] : resourceId;

    // 提取页面路径，并替换 `%2F` 为 `/`
    let pagePath = page.replace(/%2F/g, '/');

    // 提取page或query后所有的参数
    let paramsAfterPageOrQuery = '';
    for (const [key, value] of urlParams) {
        if (key !== 'resource_id' && key !== 'page' && key !== 'breakdown') {
            paramsAfterPageOrQuery += `-${key}-${value}`;
        }
    }

    // 生成 sheet 名称
    let sheetName = `${domain}-${pagePath}-${breakdown}${paramsAfterPageOrQuery}`;
    // 替换非法字符：: \ / ? * [ ] 等
    sheetName = sheetName.replace(/[:\\\/\?\*\[\]]/g, '');

    // 处理可能的超长名称，sheet 名不能超过31个字符
    return sheetName.length > 31 ? sheetName.slice(0, 31) : sheetName;
}

// 使用 xlsx.mjs 导出数据为 Excel 文件
export async function exportToExcel(gscData) {
    try {
        const xlsxModule = await import('./xlsx.mjs');
        const {utils, write} = xlsxModule;
        const workbook = utils.book_new();

        // 针对每个 URL 创建一个 sheet
        Object.keys(gscData).forEach((url) => {
            const {headers, data} = gscData[url];
            const worksheetData = [headers];
            data.forEach(row => {
                const rowData = headers.map(header => row[header] || "");
                worksheetData.push(rowData);
            });
            const worksheet = utils.aoa_to_sheet(worksheetData);

            // 使用 generateSheetName 函数生成 sheet 名称
            const sheetName = generateSheetName(url);
            utils.book_append_sheet(workbook, worksheet, sheetName);
        });

        // 导出 Excel 文件
        const excelBuffer = write(workbook, {bookType: 'xlsx', type: 'array'});
        const blob = new Blob([excelBuffer], {type: 'application/octet-stream'});
        const downloadUrl = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = 'gsc_data.xlsx';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(downloadUrl);

        showNotification("成功", "Excel 文件已下载");

        // 导出成功后清空所有数据
        chrome.storage.local.remove(["gscData"], () => {
            console.log("所有数据已清空。");
            const dataCountDisplay = document.getElementById('dataCount');
            dataCountDisplay.textContent = "当前数据条数: 0";
        });
    } catch (error) {
        console.error("导出Excel失败:", error);
        showNotification("错误", "导出Excel失败，请重试。");
    }
}

// 使用系统通知代替 alert
export function showNotification(title, message) {
    chrome.notifications.create({
        type: 'basic',
        iconUrl: 'images/icon-48.png', // 使用48px图标
        title: title,
        message: message
    }, (notificationId) => {
        // 可选：在一定时间后自动关闭通知
        setTimeout(() => {
            chrome.notifications.clear(notificationId);
        }, 5000);
    });
}