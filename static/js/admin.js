/**
 * 物业管理系统 - 通用JavaScript库
 * 包含：模态框、消息提示、AJAX请求、表单处理
 */

// ============================================
// 配置
// ============================================
const CONFIG = {
    csrfToken: document.querySelector('[name=csrfmiddlewaretoken]')?.value || '',
    apiBase: '/api',
    modalClass: 'admin-modal',
    toastClass: 'admin-toast'
};

// ============================================
// 模态框组件
// ============================================
class Modal {
    constructor(options = {}) {
        this.options = {
            title: options.title || '标题',
            content: options.content || '',
            size: options.size || 'md', // sm, md, lg, xl
            onConfirm: options.onConfirm || null,
            onCancel: options.onCancel || null,
            confirmText: options.confirmText || '确定',
            cancelText: options.cancelText || '取消',
            showFooter: options.showFooter !== false
        };

        this.modal = null;
        this.overlay = null;
        this.create();
    }

    create() {
        // 创建遮罩层
        this.overlay = document.createElement('div');
        this.overlay.className = 'modal-overlay';

        // 创建模态框
        this.modal = document.createElement('div');
        this.modal.className = `modal modal-${this.options.size}`;

        this.modal.innerHTML = `
            <div class="modal-header">
                <h3 class="modal-title">${this.options.title}</h3>
                <button class="modal-close" onclick="modal.close()">
                    <i class="ri-close-line"></i>
                </button>
            </div>
            <div class="modal-body">
                ${this.options.content}
            </div>
            ${this.options.showFooter ? `
            <div class="modal-footer">
                <button class="btn btn-secondary" onclick="modal.close()">${this.options.cancelText}</button>
                <button class="btn btn-primary modal-confirm">${this.options.confirmText}</button>
            </div>
            ` : ''}
        `;

        // 添加到页面
        this.overlay.appendChild(this.modal);
        document.body.appendChild(this.overlay);

        // 绑定确认按钮事件
        if (this.options.onConfirm) {
            const confirmBtn = this.modal.querySelector('.modal-confirm');
            confirmBtn.addEventListener('click', () => {
                if (this.options.onConfirm()) {
                    this.close();
                }
            });
        }

        // 点击遮罩关闭
        this.overlay.addEventListener('click', (e) => {
            if (e.target === this.overlay) {
                this.close();
            }
        });

        // ESC键关闭
        this.handleEscape = (e) => {
            if (e.key === 'Escape') {
                this.close();
            }
        };
        document.addEventListener('keydown', this.handleEscape);
    }

    show() {
        this.overlay.style.display = 'flex';
        document.body.style.overflow = 'hidden';

        // 动画
        setTimeout(() => {
            this.overlay.classList.add('show');
            this.modal.classList.add('show');
        }, 10);
    }

    close() {
        this.overlay.classList.remove('show');
        this.modal.classList.remove('show');

        setTimeout(() => {
            this.overlay.style.display = 'none';
            document.body.style.overflow = '';

            if (this.options.onCancel) {
                this.options.onCancel();
            }
        }, 300);
    }

    setContent(content) {
        const body = this.modal.querySelector('.modal-body');
        if (body) {
            body.innerHTML = content;
        }
    }

    destroy() {
        document.removeEventListener('keydown', this.handleEscape);
        this.overlay.remove();
    }
}

// ============================================
// Toast消息提示
// ============================================
class Toast {
    static show(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;

        const icon = {
            success: 'ri-checkbox-circle-fill',
            error: 'ri-close-circle-fill',
            warning: 'ri-error-warning-fill',
            info: 'ri-information-fill'
        }[type] || 'ri-information-fill';

        toast.innerHTML = `
            <i class="${icon}"></i>
            <span>${message}</span>
        `;

        document.body.appendChild(toast);

        // 动画
        setTimeout(() => toast.classList.add('show'), 10);

        // 自动关闭
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    static success(message, duration) {
        this.show(message, 'success', duration);
    }

    static error(message, duration) {
        this.show(message, 'error', duration);
    }

    static warning(message, duration) {
        this.show(message, 'warning', duration);
    }

    static info(message, duration) {
        this.show(message, 'info', duration);
    }
}

// ============================================
// AJAX请求封装
// ============================================
class API {
    static async request(url, options = {}) {
        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CONFIG.csrfToken
            }
        };

        const finalOptions = { ...defaultOptions, ...options };

        // 如果是GET请求，添加参数到URL
        if (finalOptions.method === 'GET' && finalOptions.params) {
            const urlObj = new URL(url, window.location.origin);
            Object.keys(finalOptions.params).forEach(key => {
                if (finalOptions.params[key] !== null && finalOptions.params[key] !== undefined) {
                    urlObj.searchParams.set(key, finalOptions.params[key]);
                }
            });
            url = urlObj.toString();
            delete finalOptions.params;
        }

        try {
            const response = await fetch(url, finalOptions);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || data.detail || '请求失败');
            }

            return data;
        } catch (error) {
            Toast.error(error.message);
            throw error;
        }
    }

    static async get(url, params = {}) {
        return this.request(url, { method: 'GET', params });
    }

    static async post(url, data = {}) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    static async postForm(url, formData) {
        // 提交表单数据（使用FormData格式）
        const options = {
            method: 'POST',
            headers: {
                'X-CSRFToken': CONFIG.csrfToken
            },
            body: formData // FormData对象，不需要设置Content-Type
        };

        const defaultOptions = {
            method: 'POST',
            headers: {
                'X-CSRFToken': CONFIG.csrfToken
            }
        };

        const finalOptions = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, finalOptions);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || data.detail || '请求失败');
            }

            return data;
        } catch (error) {
            Toast.error(error.message);
            throw error;
        }
    }

    static async put(url, data = {}) {
        return this.request(url, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    static async delete(url) {
        return this.request(url, { method: 'DELETE' });
    }
}

// ============================================
// 表单工具
// ============================================
class FormHelper {
    static serialize(form) {
        const formData = new FormData(form);
        const data = {};

        formData.forEach((value, key) => {
            if (data[key]) {
                // 处理多选框等重复字段
                if (Array.isArray(data[key])) {
                    data[key].push(value);
                } else {
                    data[key] = [data[key], value];
                }
            } else {
                data[key] = value;
            }
        });

        return data;
    }

    static validate(form) {
        const errors = [];

        // 检查必填字段
        form.querySelectorAll('[required]').forEach(field => {
            if (!field.value.trim()) {
                const label = field.previousElementSibling?.textContent || field.name;
                errors.push(`${label}不能为空`);
            }
        });

        return {
            valid: errors.length === 0,
            errors
        };
    }

    static clear(form) {
        form.reset();
        // 清空自定义错误提示
        form.querySelectorAll('.error-message').forEach(el => el.remove());
        form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
    }

    static showErrors(form, errors) {
        // 清除旧的错误
        this.clear(form);

        // 显示新错误
        Object.keys(errors).forEach(fieldName => {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                field.classList.add('is-invalid');

                const errorDiv = document.createElement('div');
                errorDiv.className = 'error-message';
                errorDiv.textContent = errors[fieldName];
                field.parentNode.appendChild(errorDiv);
            }
        });
    }
}

// ============================================
// 确认对话框
// ============================================
function confirmDelete(message = '确定要删除吗？') {
    return new Promise((resolve) => {
        const modal = new Modal({
            title: '确认删除',
            content: `<p>${message}</p>`,
            size: 'sm',
            confirmText: '删除',
            cancelText: '取消',
            onConfirm: () => {
                resolve(true);
                return true;
            },
            onCancel: () => {
                resolve(false);
                modal.destroy();
            }
        });

        modal.show();
    });
}

// ============================================
// 页面加载提示
// ============================================
function showLoading(message = '加载中...') {
    const loading = document.createElement('div');
    loading.className = 'loading-overlay';
    loading.id = 'globalLoading';
    loading.innerHTML = `
        <div class="loading-spinner">
            <i class="ri-loader-4-line spin"></i>
            <span>${message}</span>
        </div>
    `;
    document.body.appendChild(loading);
}

function hideLoading() {
    const loading = document.getElementById('globalLoading');
    if (loading) {
        loading.remove();
    }
}

// ============================================
// 格式化工具
// ============================================
const Format = {
    // 格式化日期
    date(dateStr) {
        if (!dateStr) return '-';
        const date = new Date(dateStr);
        return date.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
        });
    },

    // 格式化日期时间
    datetime(dateStr) {
        if (!dateStr) return '-';
        const date = new Date(dateStr);
        return date.toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    // 格式化金额
    money(amount) {
        if (amount === null || amount === undefined) return '-';
        return new Intl.NumberFormat('zh-CN', {
            style: 'currency',
            currency: 'CNY'
        }).format(amount);
    },

    // 格式化文件大小
    fileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }
};

// ============================================
// 初始化
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    // 全局点击事件委托
    document.addEventListener('click', async (e) => {
        // 处理删除按钮
        if (e.target.closest('.btn-delete')) {
            const btn = e.target.closest('.btn-delete');
            const url = btn.dataset.url;
            const message = btn.dataset.confirm || '确定要删除吗？';

            if (url) {
                e.preventDefault();
                const confirmed = await confirmDelete(message);
                if (confirmed) {
                    showLoading('删除中...');
                    try {
                        await API.delete(url);
                        Toast.success('删除成功');
                        setTimeout(() => window.location.reload(), 1000);
                    } catch (error) {
                        hideLoading();
                    }
                }
            }
        }

        // 处理编辑按钮
        if (e.target.closest('.btn-edit')) {
            const btn = e.target.closest('.btn-edit');
            const url = btn.dataset.url;

            if (url) {
                e.preventDefault();
                // 触发编辑事件，由具体页面处理
                window.dispatchEvent(new CustomEvent('editItem', {
                    detail: { url, button: btn }
                }));
            }
        }

        // 处理状态切换按钮
        if (e.target.closest('.btn-toggle')) {
            const btn = e.target.closest('.btn-toggle');
            const url = btn.dataset.url;

            if (url) {
                e.preventDefault();
                showLoading('更新中...');
                try {
                    const result = await API.post(url, {
                        status: btn.dataset.status
                    });
                    Toast.success('状态更新成功');
                    setTimeout(() => window.location.reload(), 1000);
                } catch (error) {
                    hideLoading();
                }
            }
        }
    });

    // 表单提交处理
    document.addEventListener('submit', async (e) => {
        const form = e.target;

        // 检查是否是AJAX表单
        if (form.classList.contains('ajax-form')) {
            e.preventDefault();

            // 验证表单
            const validation = FormHelper.validate(form);
            if (!validation.valid) {
                Toast.error('请检查表单填写');
                FormHelper.showErrors(form, {
                    general: validation.errors
                });
                return;
            }

            const url = form.action || form.dataset.url;
            const method = form.method || 'POST';
            const formData = FormHelper.serialize(form);

            showLoading('提交中...');

            try {
                const result = await API.request(url, {
                    method: method.toUpperCase(),
                    body: JSON.stringify(formData)
                });

                Toast.success('操作成功');

                // 如果有回调
                if (form.dataset.successCallback) {
                    window[form.dataset.successCallback](result);
                } else {
                    setTimeout(() => window.location.reload(), 1000);
                }
            } catch (error) {
                hideLoading();
                // 显示服务器返回的错误
                if (error.errors) {
                    FormHelper.showErrors(form, error.errors);
                }
            }
        }
    });
});

// 导出到全局
window.Modal = Modal;
window.Toast = Toast;
window.API = API;
window.FormHelper = FormHelper;
window.confirmDelete = confirmDelete;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.Format = Format;
