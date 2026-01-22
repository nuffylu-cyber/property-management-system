/**
 * 小区管理 - 完整 CRUD 功能模块（修复版）
 * 采用页面刷新方式确保数据同步
 */

// API 基础路径
const API_BASE_URL = window.location.origin;
const API_ENDPOINTS = {
    // 小区 API
    communities: '/api/community/communities/',
    communityForm: '/admin/forms/community/',

    // 楼栋 API
    buildings: '/api/community/buildings/',
    buildingForm: '/admin/forms/building/'
};

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
 * 加载小区表单
 * @param {string|null} id - 小区ID，null表示新增
 */
async function loadCommunityForm(id = null) {
    try {
        const url = id
            ? `${API_ENDPOINTS.communityForm}${id}/`
            : `${API_ENDPOINTS.communityForm}new/`;

        const data = await apiRequest(url);

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
 * 加载楼栋表单
 * @param {string|null} id - 楼栋ID，null表示新增
 */
async function loadBuildingForm(id = null) {
    try {
        const url = id
            ? `${API_ENDPOINTS.buildingForm}${id}/`
            : `${API_ENDPOINTS.buildingForm}new/`;

        const data = await apiRequest(url);

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
 * 提交小区表单
 * @param {FormData} formData - 表单数据
 * @param {string|null} id - 小区ID，null表示新增
 */
async function submitCommunityForm(formData, id = null) {
    try {
        const url = id
            ? `${API_ENDPOINTS.communityForm}${id}/`
            : `${API_ENDPOINTS.communityForm}new/`;

        const response = await fetch(url, {
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
 * 提交楼栋表单
 * @param {FormData} formData - 表单数据
 * @param {string|null} id - 楼栋ID，null表示新增
 */
async function submitBuildingForm(formData, id = null) {
    try {
        const url = id
            ? `${API_ENDPOINTS.buildingForm}${id}/`
            : `${API_ENDPOINTS.buildingForm}new/`;

        const response = await fetch(url, {
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
 * 删除小区
 * @param {string} id - 小区ID
 */
async function deleteCommunity(id) {
    try {
        const response = await fetch(`${API_ENDPOINTS.communities}${id}/`, {
            method: 'DELETE',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        });

        if (!response.ok) {
            throw new Error('删除失败');
        }

        return true;
    } catch (error) {
        console.error('删除小区失败:', error);
        showNotification('删除小区失败: ' + error.message, 'error');
        return false;
    }
}

/**
 * 删除楼栋
 * @param {string} id - 楼栋ID
 */
async function deleteBuilding(id) {
    try {
        const response = await fetch(`${API_ENDPOINTS.buildings}${id}/`, {
            method: 'DELETE',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        });

        if (!response.ok) {
            throw new Error('删除失败');
        }

        return true;
    } catch (error) {
        console.error('删除楼栋失败:', error);
        showNotification('删除楼栋失败: ' + error.message, 'error');
        return false;
    }
}

/**
 * 显示模态框
 * @param {string} title - 标题
 * @param {string} content - HTML内容
 * @param {Function} onConfirm - 确认回调
 */
function showModal(title, content, onConfirm = null) {
    // 移除已存在的模态框
    const existingModal = document.querySelector('.custom-modal');
    if (existingModal) {
        existingModal.remove();
    }

    const modal = document.createElement('div');
    modal.className = 'custom-modal';
    modal.innerHTML = `
        <div class="modal-overlay" onclick="closeModal()"></div>
        <div class="modal-container">
            <div class="modal-header">
                <h3 class="modal-title">${title}</h3>
                <button class="modal-close" onclick="closeModal()">
                    <i class="ri-close-line"></i>
                </button>
            </div>
            <div class="modal-body">
                ${content}
            </div>
            ${onConfirm ? `
                <div class="modal-footer">
                    <button class="btn btn-secondary" onclick="closeModal()">取消</button>
                    <button class="btn btn-primary" id="modal-confirm-btn">确定</button>
                </div>
            ` : ''}
        </div>
    `;

    document.body.appendChild(modal);

    if (onConfirm) {
        document.getElementById('modal-confirm-btn').addEventListener('click', onConfirm);
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
 * 新增小区
 */
async function addCommunity() {
    showNotification('正在加载表单...', 'info');

    const formHtml = await loadCommunityForm(null);
    if (!formHtml) {
        showNotification('表单加载失败', 'error');
        return;
    }

    showModal('新增小区', formHtml, async () => {
        const form = document.querySelector('.custom-modal form');
        if (!form) return;

        const formData = new FormData(form);
        const submitBtn = document.getElementById('modal-confirm-btn');
        submitBtn.disabled = true;
        submitBtn.textContent = '保存中...';

        try {
            const result = await submitCommunityForm(formData, null);

            if (result.success) {
                showNotification('保存成功，正在刷新页面...', 'success');
                closeModal();
                // 刷新整个页面以获取最新数据
                setTimeout(() => {
                    window.location.reload();
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
}

/**
 * 编辑小区
 * @param {string} id - 小区ID
 */
async function editCommunity(id) {
    showNotification('正在加载表单...', 'info');

    const formHtml = await loadCommunityForm(id);
    if (!formHtml) {
        showNotification('表单加载失败', 'error');
        return;
    }

    showModal('编辑小区', formHtml, async () => {
        const form = document.querySelector('.custom-modal form');
        if (!form) return;

        const formData = new FormData(form);
        const submitBtn = document.getElementById('modal-confirm-btn');
        submitBtn.disabled = true;
        submitBtn.textContent = '保存中...';

        try {
            const result = await submitCommunityForm(formData, id);

            if (result.success) {
                showNotification('保存成功，正在刷新页面...', 'success');
                closeModal();
                // 刷新整个页面以获取最新数据
                setTimeout(() => {
                    window.location.reload();
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
}

/**
 * 确认删除小区
 * @param {string} id - 小区ID
 * @param {string} name - 小区名称
 */
function confirmDeleteCommunity(id, name) {
    showModal('确认删除', `
        <div style="text-align: center; padding: 20px;">
            <i class="ri-error-warning-line" style="font-size: 48px; color: #ef4444; display: block; margin-bottom: 16px;"></i>
            <p style="font-size: 16px; color: #1f2937; margin-bottom: 8px;">确定要删除小区 <strong>${escapeHtml(name)}</strong> 吗？</p>
            <p style="font-size: 14px; color: #6b7280;">此操作将同时删除该小区的所有楼栋数据，且无法恢复。</p>
        </div>
    `, async () => {
        const success = await deleteCommunity(id);
        if (success) {
            showNotification('删除成功，正在刷新页面...', 'success');
            closeModal();
            // 刷新整个页面以获取最新数据
            setTimeout(() => {
                window.location.reload();
            }, 500);
        }
    });
}

/**
 * 新增楼栋
 */
async function addBuilding() {
    showNotification('正在加载表单...', 'info');

    const formHtml = await loadBuildingForm(null);
    if (!formHtml) {
        showNotification('表单加载失败', 'error');
        return;
    }

    showModal('新增楼栋', formHtml, async () => {
        const form = document.querySelector('.custom-modal form');
        if (!form) return;

        const formData = new FormData(form);
        const submitBtn = document.getElementById('modal-confirm-btn');
        submitBtn.disabled = true;
        submitBtn.textContent = '保存中...';

        try {
            const result = await submitBuildingForm(formData, null);

            if (result.success) {
                showNotification('保存成功，正在刷新页面...', 'success');
                closeModal();
                // 刷新整个页面以获取最新数据
                setTimeout(() => {
                    window.location.reload();
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
}

/**
 * 编辑楼栋
 * @param {string} id - 楼栋ID
 */
async function editBuilding(id) {
    showNotification('正在加载表单...', 'info');

    const formHtml = await loadBuildingForm(id);
    if (!formHtml) {
        showNotification('表单加载失败', 'error');
        return;
    }

    showModal('编辑楼栋', formHtml, async () => {
        const form = document.querySelector('.custom-modal form');
        if (!form) return;

        const formData = new FormData(form);
        const submitBtn = document.getElementById('modal-confirm-btn');
        submitBtn.disabled = true;
        submitBtn.textContent = '保存中...';

        try {
            const result = await submitBuildingForm(formData, id);

            if (result.success) {
                showNotification('保存成功，正在刷新页面...', 'success');
                closeModal();
                // 刷新整个页面以获取最新数据
                setTimeout(() => {
                    window.location.reload();
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
}

/**
 * 确认删除楼栋
 * @param {string} id - 楼栋ID
 * @param {string} name - 楼栋名称
 */
function confirmDeleteBuilding(id, name) {
    showModal('确认删除', `
        <div style="text-align: center; padding: 20px;">
            <i class="ri-error-warning-line" style="font-size: 48px; color: #ef4444; display: block; margin-bottom: 16px;"></i>
            <p style="font-size: 16px; color: #1f2937; margin-bottom: 8px;">确定要删除楼栋 <strong>${escapeHtml(name)}</strong> 吗？</p>
            <p style="font-size: 14px; color: #6b7280;">此操作无法恢复。</p>
        </div>
    `, async () => {
        const success = await deleteBuilding(id);
        if (success) {
            showNotification('删除成功，正在刷新页面...', 'success');
            closeModal();
            // 刷新整个页面以获取最新数据
            setTimeout(() => {
                window.location.reload();
            }, 500);
        }
    });
}

/**
 * 显示通知
 * @param {string} message - 消息内容
 * @param {string} type - 消息类型: success, error, info, warning
 */
function showNotification(message, type = 'info') {
    // 移除已存在的通知
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

    // 添加通知样式
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

    // 3秒后自动消失
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * HTML转义函数
 * @param {string} text - 要转义的文本
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 导出函数供全局使用
window.CommunityCRUD = {
    addCommunity,
    editCommunity,
    confirmDeleteCommunity,
    addBuilding,
    editBuilding,
    confirmDeleteBuilding
};
