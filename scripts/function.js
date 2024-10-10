// function.js

// sheet 名称生成函数
export function generateSheetName(url, index) {
    return `Pages${index}`; // 生成 Pages1, Pages2, 等名称
}

// 使用 xlsx.mjs 导出数据为 Excel 文件
export async function exportToExcel(gscData) {
    try {
        const xlsxModuleUrl = chrome.runtime.getURL('scripts/xlsx.mjs');
        const xlsxModule = await import(xlsxModuleUrl);
        const {utils, write} = xlsxModule;

        // 获取第一个 URL 以提取文件名所需的信息
        const firstUrl = Object.keys(gscData)[0];
        const decodedFirstUrl = decodeURIComponent(firstUrl);
        const urlParams = new URLSearchParams(decodedFirstUrl.split('?')[1]);
        const resourceId = urlParams.get('resource_id');
        const domain = resourceId.includes('sc-domain:') ? resourceId.split(':')[1] : resourceId;

        // 获取当前日期，格式为 YYYY-MM-DD
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        const formattedDate = `${yyyy}-${mm}-${dd}`;

        // 生成文件名
        const fileName = `${domain}-Performance-${formattedDate}.xlsx`;

        const workbook = utils.book_new();
        let sheetIndex = 1;

        Object.keys(gscData).forEach((url) => {
            const {headers, data} = gscData[url];
            const currentUrlParams = new URLSearchParams(url.split('?')[1]);
            const page = currentUrlParams.get('page') || "/blog";
            const breakdown = currentUrlParams.get('breakdown') || "Pages";
            const num_of_days = currentUrlParams.get('num_of_days') || "";
            const num_of_months = currentUrlParams.get('num_of_months') || "";
            const start_date = currentUrlParams.get('start_date') || "";
            const end_date = currentUrlParams.get('end_date') || "";

            // Pages sheet
            const pagesSheetName = `${(breakdown.charAt(0).toUpperCase() + breakdown.slice(1))}s${sheetIndex}`;
            const pagesWorksheetData = [headers];
            data.forEach(row => {
                const rowData = headers.map(header => row[header] || "");
                pagesWorksheetData.push(rowData);
            });
            const pagesWorksheet = utils.aoa_to_sheet(pagesWorksheetData);
            utils.book_append_sheet(workbook, pagesWorksheet, pagesSheetName);

            // 动态生成 Date filter 值
            let dateFilterValue = "";
            if (num_of_days) {
                if (parseInt(num_of_days) === 1) {
                    dateFilterValue = "Most recent date";
                } else {
                    dateFilterValue = `Last ${num_of_days} days`;
                }
            } else if (num_of_months) {
                dateFilterValue = `Last ${num_of_months} months`;
            } else if (start_date && end_date) {
                const startDateObj = new Date(start_date);
                const endDateObj = new Date(end_date);
                const options = {year: 'numeric', month: 'short', day: 'numeric'};
                const startDateStr = startDateObj.toLocaleDateString('en-US', options);
                const endDateStr = endDateObj.toLocaleDateString('en-US', options);
                dateFilterValue = `${startDateStr}-${endDateStr}`;
            } else {
                dateFilterValue = "Date range not specified";
            }

            // Filters sheet
            const filtersSheetName = `Filters${sheetIndex}`;
            const filtersWorksheetData = [
                ["Filter", "Value"],
                ["Date", dateFilterValue],
                ["Page", `+${decodeURIComponent(page)}`]
            ];
            const filtersWorksheet = utils.aoa_to_sheet(filtersWorksheetData);
            utils.book_append_sheet(workbook, filtersWorksheet, filtersSheetName);

            sheetIndex++;
        });

        // 导出 Excel 文件
        const excelBuffer = write(workbook, {bookType: 'xlsx', type: 'array'});
        const blob = new Blob([excelBuffer], {type: 'application/octet-stream'});
        const downloadUrl = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(downloadUrl);

        showNotification("成功", "Excel 文件已下载");

        // 导出成功后清空所有数据
        chrome.storage.local.remove(["gscData"], () => {
            console.log("所有数据已清空。");
            // 如果需要在 data.html 中更新 UI，可以在这里发送消息或进行其他处理
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
        iconUrl: chrome.runtime.getURL('images/icon-48.png'), // 使用绝对路径
        title: title,
        message: message
    }, (notificationId) => {
        // 可选：在一定时间后自动关闭通知
        setTimeout(() => {
            chrome.notifications.clear(notificationId);
        }, 5000);
    });
}

