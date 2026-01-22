/**
 * 标签页工具函数
 * 用于在页面刷新后保持当前激活的标签页状态
 */

(function() {
    // 全局变量，保存当前标签页名称
    let _savedTabName = null;

    /**
     * 保存当前激活的标签页名称
     * 应该在打开模态框之前调用
     */
    function saveCurrentTab() {
        const activeTab = document.querySelector('.tab.active');
        if (!activeTab) {
            _savedTabName = null;
            return;
        }

        const onclick = activeTab.getAttribute('onclick');
        if (!onclick) {
            _savedTabName = null;
            return;
        }

        // 从onclick属性中提取标签页名称
        const match = onclick.match(/switchTab\(this,\s*'([^']+)'\)/);
        _savedTabName = match ? match[1] : null;

        console.log('[TabUtils] 已保存当前标签页:', _savedTabName);
    }

    /**
     * 获取保存的标签页名称
     * @returns {string|null} 标签页名称
     */
    function getSavedTab() {
        return _savedTabName;
    }

    /**
     * 获取当前激活的标签页名称
     * @returns {string|null} 标签页名称，如果未找到则返回null
     */
    function getCurrentTabName() {
        // 优先返回保存的标签页
        if (_savedTabName) {
            return _savedTabName;
        }

        const activeTab = document.querySelector('.tab.active');
        if (!activeTab) return null;

        const onclick = activeTab.getAttribute('onclick');
        if (!onclick) return null;

        // 从onclick属性中提取标签页名称
        // 匹配格式: switchTab(this, 'tabname')
        const match = onclick.match(/switchTab\(this,\s*'([^']+)'\)/);
        return match ? match[1] : null;
    }

    /**
     * 获取包含所有查询参数的URL字符串
     * 如果没有查询参数，会自动添加当前激活的标签页
     * @returns {string} 查询字符串（包含"?"）
     */
    function getUrlWithTab() {
        const urlParams = new URLSearchParams(window.location.search);
        let queryString = urlParams.toString();

        // 如果没有查询参数，尝试检测当前激活的标签页
        if (!queryString) {
            const tabName = getCurrentTabName();
            if (tabName) {
                queryString = 'tab=' + tabName;
            }
        }

        return queryString ? ('?' + queryString) : '';
    }

    /**
     * 刷新页面并保持当前标签页状态
     * @param {number} delay - 延迟时间（毫秒），默认500ms
     */
    function reloadKeepingTab(delay = 500) {
        setTimeout(() => {
            const queryString = getUrlWithTab();
            console.log('[TabUtils] 刷新页面，URL参数:', queryString);
            console.log('[TabUtils] 保存的标签页:', _savedTabName);
            console.log('[TabUtils] 当前路径:', window.location.pathname);
            if (queryString) {
                console.log('[TabUtils] 跳转到:', window.location.pathname + queryString);
                window.location.href = window.location.pathname + queryString;
            } else {
                console.log('[TabUtils] 无URL参数，执行reload');
                window.location.reload();
            }
        }, delay);
    }

    /**
     * 刷新页面并保持当前标签页状态（带时间戳，避免缓存）
     * @param {number} delay - 延迟时间（毫秒），默认500ms
     */
    function reloadKeepingTabWithTimestamp(delay = 500) {
        setTimeout(() => {
            const urlParams = new URLSearchParams(window.location.search);
            let queryString = urlParams.toString();

            // 如果没有查询参数，尝试检测当前激活的标签页
            if (!queryString) {
                const tabName = getCurrentTabName();
                if (tabName) {
                    queryString = 'tab=' + tabName;
                }
            }

            const finalUrl = new URL(window.location.pathname, window.location.origin);
            if (queryString) {
                finalUrl.search = queryString + '&_t=' + Date.now();
            } else {
                finalUrl.searchParams.set('_t', Date.now());
            }
            console.log('[TabUtils] 刷新页面（带时间戳），URL:', finalUrl.toString());
            window.location.href = finalUrl.toString();
        }, delay);
    }

    // 导出工具函数
    window.TabUtils = {
        saveCurrentTab,
        getSavedTab,
        getCurrentTabName,
        getUrlWithTab,
        reloadKeepingTab,
        reloadKeepingTabWithTimestamp
    };
})();
