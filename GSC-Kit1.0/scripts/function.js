// function.js

// 使用 xlsx.mjs 导出数据为 Excel 文件
export async function exportToExcel(gscData, urlsToExport = null) {
    return new Promise(async (resolve, reject) => {
        try {
            const xlsxModuleUrl = chrome.runtime.getURL('scripts/xlsx.mjs');
            const xlsxModule = await import(xlsxModuleUrl);
            const { utils, write } = xlsxModule;

            // 如果传入 urlsToExport，导出指定的 URLs，否则导出全部
            let urls = urlsToExport || Object.keys(gscData);

            if (urls.length === 0) {
                throw new Error("没有可导出的 URL");
            }

            // 获取第一个 URL 以提取文件名所需的信息
            const firstUrl = decodeURIComponent(urls[0]);
            const urlPath = new URL(firstUrl).pathname;
            const gscType = urlPath.split('/').filter(part => part !== '')[2];
            const urlParams = new URLSearchParams(firstUrl.split('?')[1]);
            const resourceId = urlParams.get('resource_id');
            const domain = resourceId.includes('sc-domain:') ? resourceId.split(':')[1] : resourceId;

            // 获取当前日期，格式为 YYYY-MM-DD
            const today = new Date();
            const yyyy = today.getFullYear();
            const mm = String(today.getMonth() + 1).padStart(2, '0');
            const dd = String(today.getDate()).padStart(2, '0');
            const formattedDate = `${yyyy}-${mm}-${dd}`;

            // 生成文件名
            const fileName = `${gscType.charAt(0).toUpperCase() + gscType.slice(1)}-${formattedDate}.xlsx`;

            const workbook = utils.book_new();
            let sheetIndex = 1;

            urls.forEach((url) => {
                if (!gscData[url]) return; // 跳过没有数据的 URL

                const { headers, data } = gscData[url];
                const decodedUrl = decodeURIComponent(url);
                const currentUrlParams = new URLSearchParams(decodedUrl.split('?')[1]);
                const page = currentUrlParams.get('page').replace("*", "") || "/blog";
                const breakdown = currentUrlParams.get('breakdown') || "page";
                const num_of_days = currentUrlParams.get('num_of_days') || "";
                const num_of_months = currentUrlParams.get('num_of_months') || "";
                const start_date = currentUrlParams.get('start_date') || "";
                const end_date = currentUrlParams.get('end_date') || "";

                // Pages sheet
                const pagesSheetName = `${domain}丨${(breakdown.charAt(0).toUpperCase() + breakdown.slice(1))}s${sheetIndex}`;
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
                    // 转换 'YYYYMMDD' 为 'YYYY-MM-DD'
                    const formatDate = (dateStr) => {
                        if (dateStr.length === 8) {
                            return `${dateStr.slice(0,4)}-${dateStr.slice(4,6)}-${dateStr.slice(6,8)}`;
                        }
                        return dateStr; // 如果格式不对，直接返回原字符串
                    };
                    const formattedStartDate = formatDate(start_date);
                    const formattedEndDate = formatDate(end_date);

                    const startDateObj = new Date(formattedStartDate);
                    const endDateObj = new Date(formattedEndDate);

                    // 检查日期是否有效
                    const isValidDate = (d) => d instanceof Date && !isNaN(d);

                    const options = { year: 'numeric', month: 'short', day: 'numeric' };
                    const startDateStr = isValidDate(startDateObj) ? startDateObj.toLocaleDateString('en-US', options) : start_date;
                    const endDateStr = isValidDate(endDateObj) ? endDateObj.toLocaleDateString('en-US', options) : end_date;
                    dateFilterValue = `${startDateStr}-${endDateStr}`;
                } else {
                    dateFilterValue = "Date range not specified";
                }

                // Filters sheet
                const filtersSheetName = `Filters${sheetIndex}`;
                const filtersWorksheetData = [
                    ["Filter", "Value"],
                    ["Date", dateFilterValue],
                    ["Page", `+${page}`]
                ];
                const filtersWorksheet = utils.aoa_to_sheet(filtersWorksheetData);
                utils.book_append_sheet(workbook, filtersWorksheet, filtersSheetName);

                sheetIndex++;
            });

            // 导出 Excel 文件
            const excelBuffer = write(workbook, { bookType: 'xlsx', type: 'array' });
            const blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
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
            await chrome.storage.local.remove(["gscData"]); // 使用 await 确保移除完成
            console.log("所有数据已清空。");

            // 发送消息通知 UI 更新
            chrome.runtime.sendMessage({ action: "dataCleared" });

            resolve(); // 解析 Promise
        }
        catch (error) {
            console.error(error);
            showNotification("错误", "导出 Excel 文件时出错。请查看控制台以获取更多信息。");
            reject(error); // 拒绝 Promise
        }
    });
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