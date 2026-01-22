/**
 * 通用 CRUD 管理器
 * 适用于所有模块：房产、缴费、报事等
 * 采用页面刷新方式确保数据同步
 */

const UniversalCRUD = (function() {
    const API_BASE_URL = window.location.origin;

    /**
     * API 请求封装
     */
    async function apiRequest(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        };

        const response = await fetch(url, { ...defaultOptions, ...options });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || error.message || '请求失败');
        }

        return response.json();
    }

    /**
     * 加载表单
     * @param {string} formUrl - 表单URL
     */
    async function loadForm(formUrl) {
        try {
            const data = await apiRequest(formUrl);

            if (data.html) {
                return data.html;
            } else {
                throw new Error('表单数据格式错误');
            }
        } catch (error) {
            console.error('加载表单失败:', error);
            showNotification('加载表单失败: ' + error.message, 'error');
            return null;
        }
    }

    /**
     * 提交表单
     * @param {string} formUrl - 表单提交URL
     * @param {FormData} formData - 表单数据
     */
    async function submitForm(formUrl, formData) {
        try {
            const response = await fetch(formUrl, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.errors ? JSON.stringify(data.errors) : '提交失败');
            }

            return data;
        } catch (error) {
            console.error('提交表单失败:', error);
            throw error;
        }
    }

    /**
     * 删除项目
     * @param {string} deleteUrl - 删除URL
     */
    async function deleteItem(deleteUrl) {
        try {
            // 获取CSRF token
            const cookies = document.cookie.split(';');
            let csrfToken = null;
            for (let cookie of cookies) {
                const [name, value] = cookie.trim().split('=');
                if (name === 'csrftoken') {
                    csrfToken = decodeURIComponent(value);
                    break;
                }
            }

            const headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json'
            };

            if (csrfToken) {
                headers['X-CSRFToken'] = csrfToken;
            }

            const response = await fetch(deleteUrl, {
                method: 'DELETE',
                headers: headers,
                credentials: 'same-origin'
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || errorData.message || '删除失败');
            }

            return true;
        } catch (error) {
            console.error('删除失败:', error);
            showNotification('删除失败: ' + error.message, 'error');
            return false;
        }
    }

    /**
     * 显示模态框
     */
    function showModal(title, content, onConfirm = null) {
        const existingModal = document.querySelector('.custom-modal');
        if (existingModal) {
            existingModal.remove();
        }

        const modal = document.createElement('div');
        modal.className = 'custom-modal';
        modal.innerHTML = `
            <div class="modal-overlay" onclick="UniversalCRUD.closeModal()"></div>
            <div class="modal-container">
                <div class="modal-header">
                    <h3 class="modal-title">${title}</h3>
                    <button class="modal-close" onclick="UniversalCRUD.closeModal()">
                        <i class="ri-close-line"></i>
                    </button>
                </div>
                <div class="modal-body">
                    ${content}
                </div>
                ${onConfirm ? `
                    <div class="modal-footer">
                        <button class="btn btn-secondary" onclick="UniversalCRUD.closeModal()">取消</button>
                        <button class="btn btn-primary" id="modal-confirm-btn">确定</button>
                    </div>
                ` : ''}
            </div>
        `;

        document.body.appendChild(modal);

        if (onConfirm) {
            document.getElementById('modal-confirm-btn').addEventListener('click', onConfirm);
        }

        // 初始化房产表单的多业主管理
        if (typeof PropertyForm !== 'undefined' && PropertyForm.initOwnerRows) {
            setTimeout(function() {
                PropertyForm.initOwnerRows();
            }, 50);
        }

        // 添加模态框样式
        if (!document.querySelector('#modal-styles')) {
            const style = document.createElement('style');
            style.id = 'modal-styles';
            style.textContent = `
                .custom-modal {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    z-index: 9999;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .modal-overlay {
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(0, 0, 0, 0.5);
                    backdrop-filter: blur(4px);
                }
                .modal-container {
                    position: relative;
                    background: white;
                    border-radius: 12px;
                    width: 90%;
                    max-width: 600px;
                    max-height: 90vh;
                    overflow: auto;
                    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                }
                .modal-header {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 20px 24px;
                    border-bottom: 1px solid #e5e7eb;
                }
                .modal-title {
                    font-size: 18px;
                    font-weight: 600;
                    color: #1f2937;
                    margin: 0;
                }
                .modal-close {
                    background: none;
                    border: none;
                    font-size: 24px;
                    color: #6b7280;
                    cursor: pointer;
                    padding: 0;
                    width: 32px;
                    height: 32px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 6px;
                    transition: all 0.2s;
                }
                .modal-close:hover {
                    background: #f3f4f6;
                    color: #1f2937;
                }
                .modal-body {
                    padding: 24px;
                }
                .modal-footer {
                    display: flex;
                    gap: 12px;
                    justify-content: flex-end;
                    padding: 16px 24px;
                    border-top: 1px solid #e5e7eb;
                }
            `;
            document.head.appendChild(style);
        }
    }

    /**
     * 关闭模态框
     */
    function closeModal() {
        const modal = document.querySelector('.custom-modal');
        if (modal) {
            modal.remove();
        }
    }

    /**
     * 新增项目（通用）
     */
    async function addItem(config) {
        // 保存当前标签页
        if (typeof TabUtils !== 'undefined' && TabUtils.saveCurrentTab) {
            TabUtils.saveCurrentTab();
        }

        const {
            formUrl,
            title,
            itemName,
            onLoad
        } = config;

        showNotification(`正在加载${itemName}表单...`, 'info');

        const formHtml = await loadForm(formUrl);
        if (!formHtml) {
            showNotification('表单加载失败', 'error');
            return;
        }

        showModal(title, formHtml, async () => {
            const form = document.querySelector('.custom-modal form');
            if (!form) return;

            const formData = new FormData(form);
            const submitBtn = document.getElementById('modal-confirm-btn');
            submitBtn.disabled = true;
            submitBtn.textContent = '保存中...';

            try {
                const result = await submitForm(formUrl, formData);

                if (result.success) {
                    showNotification('保存成功，正在刷新页面...', 'success');
                    closeModal();

                    // 使用TabUtils刷新页面并保持标签页
                    setTimeout(() => {
                        if (typeof TabUtils !== 'undefined' && TabUtils.reloadKeepingTab) {
                            TabUtils.reloadKeepingTab();
                        } else {
                            window.location.reload();
                        }
                    }, 500);
                } else {
                    showNotification('保存失败: ' + JSON.stringify(result.errors), 'error');
                    submitBtn.disabled = false;
                    submitBtn.textContent = '确定';
                }
            } catch (error) {
                showNotification('保存失败: ' + error.message, 'error');
                submitBtn.disabled = false;
                submitBtn.textContent = '确定';
            }
        });

        // 调用onLoad回调（如果提供）
        if (onLoad && typeof onLoad === 'function') {
            setTimeout(() => {
                onLoad();
            }, 100);
        }
    }

    /**
     * 编辑项目（通用）
     */
    async function editItem(config) {
        // 保存当前标签页
        console.log('[UniversalCRUD] editItem called, TabUtils available:', typeof TabUtils !== 'undefined');
        if (typeof TabUtils !== 'undefined' && TabUtils.saveCurrentTab) {
            TabUtils.saveCurrentTab();
            console.log('[UniversalCRUD] Tab saved successfully');
        } else {
            console.warn('[UniversalCRUD] TabUtils.saveCurrentTab not available');
        }

        const {
            formUrl,
            title,
            itemName,
            id,
            onLoad
        } = config;

        showNotification(`正在加载${itemName}表单...`, 'info');

        const formHtml = await loadForm(formUrl);
        if (!formHtml) {
            showNotification('表单加载失败', 'error');
            return;
        }

        showModal(title, formHtml, async () => {
            const form = document.querySelector('.custom-modal form');
            if (!form) return;

            const formData = new FormData(form);
            const submitBtn = document.getElementById('modal-confirm-btn');
            submitBtn.disabled = true;
            submitBtn.textContent = '保存中...';

            try {
                const result = await submitForm(formUrl, formData);

                if (result.success) {
                    showNotification('保存成功，正在刷新页面...', 'success');
                    closeModal();

                    // 使用TabUtils刷新页面并保持标签页
                    setTimeout(() => {
                        if (typeof TabUtils !== 'undefined' && TabUtils.reloadKeepingTab) {
                            TabUtils.reloadKeepingTab();
                        } else {
                            window.location.reload();
                        }
                    }, 500);
                } else {
                    showNotification('保存失败: ' + JSON.stringify(result.errors), 'error');
                    submitBtn.disabled = false;
                    submitBtn.textContent = '确定';
                }
            } catch (error) {
                showNotification('保存失败: ' + error.message, 'error');
                submitBtn.disabled = false;
                submitBtn.textContent = '确定';
            }
        });

        // 调用onLoad回调（如果提供）
        if (onLoad && typeof onLoad === 'function') {
            setTimeout(() => {
                onLoad();
            }, 100);
        }
    }

    /**
     * 确认删除（通用）
     */
    function confirmDelete(config) {
        // 保存当前标签页
        if (typeof TabUtils !== 'undefined' && TabUtils.saveCurrentTab) {
            TabUtils.saveCurrentTab();
        }

        const {
            deleteUrl,
            itemName,
            id,
            name
        } = config;

        showModal('确认删除', `
            <div style="text-align: center; padding: 20px;">
                <i class="ri-error-warning-line" style="font-size: 48px; color: #ef4444; display: block; margin-bottom: 16px;"></i>
                <p style="font-size: 16px; color: #1f2937; margin-bottom: 8px;">
                    确定要删除 ${itemName} <strong>${escapeHtml(name)}</strong> 吗？
                </p>
                <p style="font-size: 14px; color: #6b7280;">此操作无法恢复。</p>
            </div>
        `, async () => {
            const success = await deleteItem(deleteUrl);
            if (success) {
                showNotification('删除成功，正在刷新页面...', 'success');
                closeModal();

                // 使用TabUtils刷新页面并保持标签页
                setTimeout(() => {
                    if (typeof TabUtils !== 'undefined' && TabUtils.reloadKeepingTab) {
                        TabUtils.reloadKeepingTab();
                    } else {
                        window.location.reload();
                    }
                }, 500);
            }
        });
    }

    /**
     * 显示通知
     */
    function showNotification(message, type = 'info') {
        const existingNotification = document.querySelector('.notification-toast');
        if (existingNotification) {
            existingNotification.remove();
        }

        const colors = {
            success: '#10b981',
            error: '#ef4444',
            info: '#3b82f6',
            warning: '#f59e0b'
        };

        const icons = {
            success: 'ri-checkbox-circle-line',
            error: 'ri-close-circle-line',
            info: 'ri-information-line',
            warning: 'ri-error-warning-line'
        };

        const notification = document.createElement('div');
        notification.className = 'notification-toast';
        notification.innerHTML = `
            <i class="${icons[type]}" style="color: ${colors[type]}; font-size: 20px;"></i>
            <span>${message}</span>
        `;

        if (!document.querySelector('#notification-styles')) {
            const style = document.createElement('style');
            style.id = 'notification-styles';
            style.textContent = `
                .notification-toast {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: white;
                    padding: 16px 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    z-index: 10000;
                    animation: slideIn 0.3s ease-out;
                    min-width: 300px;
                }
                @keyframes slideIn {
                    from {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
                @keyframes slideOut {
                    from {
                        transform: translateX(0);
                        opacity: 1;
                    }
                    to {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    /**
     * HTML转义
     */
    function escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // 导出公共API
    return {
        addItem,
        editItem,
        confirmDelete,
        closeModal,
        showNotification
    };
})();

// 导出全局函数供HTML使用
window.UniversalCRUD = UniversalCRUD;
window.closeModal = UniversalCRUD.closeModal;
