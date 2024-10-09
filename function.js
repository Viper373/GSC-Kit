// function.js

// 检查当前 URL 是否为目标页面
function isTargetPage() {
    const url = window.location.href;
    const patterns = [
        /^https:\/\/search\.google\.com\/u\/2\/search-console\/performance\/.*/,
        /^https:\/\/search\.google\.com\/u\/2\/search-console\/index\/.*/
    ];
    return patterns.some(pattern => pattern.test(url));
}
