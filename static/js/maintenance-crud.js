/**
 * 报事管理 CRUD 模块
 */

// 报修管理
window.MaintenanceCRUD = (function() {
    const API_BASE_URL = window.location.origin;

    /**
     * 获取CSRF token
     */
    function getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return decodeURIComponent(value);
            }
        }
        return null;
    }

    /**
     * 派单
     */
    async function assignMaintenance(id, requestNumber) {
        const modal = document.createElement('div');
        modal.className = 'custom-modal';
        modal.innerHTML = `
            <div class="modal-overlay" onclick="MaintenanceCRUD.closeAssignModal()"></div>
            <div class="modal-container">
                <div class="modal-header">
                    <h3 class="modal-title">派单 - ${requestNumber}</h3>
                    <button class="modal-close" onclick="MaintenanceCRUD.closeAssignModal()">
                        <i class="ri-close-line"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <form id="assign-form">
                        <div class="form-group">
                            <label for="assigned-to">
                                指派给
                                <span class="required">*</span>
                            </label>
                            <input type="text" id="assigned-to" name="assigned_to" required
                                   placeholder="请输入维修人员姓名"
                                   autocomplete="off">
                            <small>请输入负责处理此报事的维修人员姓名</small>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" onclick="MaintenanceCRUD.closeAssignModal()">取消</button>
                    <button type="button" class="btn btn-primary" onclick="MaintenanceCRUD.submitAssign('${id}')">
                        <i class="ri-send-plane-fill" style="margin-right: 4px;"></i>
                        确定派单
                    </button>
                </div>
            </div>
        `;

        // 移除现有模态框
        const existingModal = document.querySelector('.custom-modal');
        if (existingModal) {
            existingModal.remove();
        }

        document.body.appendChild(modal);

        // 聚焦输入框
        setTimeout(() => {
            const input = document.getElementById('assigned-to');
            if (input) {
                input.focus();
                // 支持回车提交
                input.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        MaintenanceCRUD.submitAssign(id);
                    }
                });
            }
        }, 100);
    }

    /**
     * 关闭派单模态框
     */
    function closeAssignModal() {
        const modal = document.querySelector('.custom-modal');
        if (modal) {
            modal.remove();
        }
    }

    /**
     * 提交派单
     */
    async function submitAssign(id) {
        const assignedTo = document.getElementById('assigned-to').value.trim();

        if (!assignedTo) {
            UniversalCRUD.showNotification('请输入维修人员姓名', 'error');
            return;
        }

        const csrfToken = getCSRFToken();
        const submitBtn = document.querySelector('.modal-footer .btn-primary');
        submitBtn.disabled = true;
        submitBtn.textContent = '派单中...';

        try {
            const response = await fetch(`${API_BASE_URL}/api/maintenance/requests/${id}/assign/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin',
                body: JSON.stringify({ assigned_to: assignedTo })
            });

            const data = await response.json();

            if (response.ok) {
                UniversalCRUD.showNotification('派单成功，正在刷新页面...', 'success');
                closeAssignModal();
                setTimeout(() => {
                    // 保留URL中的所有查询参数，包括tab等
                    const urlParams = new URLSearchParams(window.location.search);
                    let queryString = urlParams.toString();

                    // 如果没有查询参数，尝试检测当前激活的标签页
                    if (!queryString) {
                        const activeTab = document.querySelector('.tab.active');
                        if (activeTab && activeTab.getAttribute('onclick')) {
                            const match = activeTab.getAttribute('onclick').match(/switchTab\(this,\s*'([^']+)'\)/);
                            if (match && match[1]) {
                                queryString = 'tab=' + match[1];
                            }
                        }
                    }

                    if (queryString) {
                        window.location.href = window.location.pathname + '?' + queryString;
                    } else {
                        window.location.reload();
                    }
                }, 500);
            } else {
                throw new Error(data.error || data.message || '派单失败');
            }
        } catch (error) {
            UniversalCRUD.showNotification('派单失败: ' + error.message, 'error');
            submitBtn.disabled = false;
            submitBtn.textContent = '确定派单';
        }
    }

    /**
     * 开始处理
     */
    async function startMaintenance(id) {
        if (!confirm('确认开始处理此报事？')) {
            return;
        }

        const csrfToken = getCSRFToken();

        try {
            const response = await fetch(`${API_BASE_URL}/api/maintenance/requests/${id}/start/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            });

            const data = await response.json();

            if (response.ok) {
                UniversalCRUD.showNotification('已开始处理，正在刷新页面...', 'success');
                setTimeout(() => {
                    // 保留URL中的所有查询参数，包括tab等
                    const urlParams = new URLSearchParams(window.location.search);
                    let queryString = urlParams.toString();

                    // 如果没有查询参数，尝试检测当前激活的标签页
                    if (!queryString) {
                        const activeTab = document.querySelector('.tab.active');
                        if (activeTab && activeTab.getAttribute('onclick')) {
                            const match = activeTab.getAttribute('onclick').match(/switchTab\(this,\s*'([^']+)'\)/);
                            if (match && match[1]) {
                                queryString = 'tab=' + match[1];
                            }
                        }
                    }

                    if (queryString) {
                        window.location.href = window.location.pathname + '?' + queryString;
                    } else {
                        window.location.reload();
                    }
                }, 500);
            } else {
                throw new Error(data.error || data.message || '操作失败');
            }
        } catch (error) {
            UniversalCRUD.showNotification('操作失败: ' + error.message, 'error');
        }
    }

    /**
     * 完成报事
     */
    async function completeMaintenance(id) {
        const modal = document.createElement('div');
        modal.className = 'custom-modal';
        modal.innerHTML = `
            <div class="modal-overlay" onclick="MaintenanceCRUD.closeCompleteModal()"></div>
            <div class="modal-container">
                <div class="modal-header">
                    <h3 class="modal-title">完成报事</h3>
                    <button class="modal-close" onclick="MaintenanceCRUD.closeCompleteModal()">
                        <i class="ri-close-line"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <form id="complete-form">
                        <div class="form-group">
                            <label for="result-description">
                                处理结果说明
                                <span class="required">*</span>
                            </label>
                            <textarea id="result-description" name="result_description" required rows="5"
                                      placeholder="请详细描述处理结果、使用材料、花费时间等信息"
                                      autocomplete="off"></textarea>
                            <small>请详细描述报事处理情况，包括采取的措施、使用材料、处理结果等</small>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" onclick="MaintenanceCRUD.closeCompleteModal()">取消</button>
                    <button type="button" class="btn btn-primary" onclick="MaintenanceCRUD.submitComplete('${id}')">
                        <i class="ri-check-fill" style="margin-right: 4px;"></i>
                        确定完成
                    </button>
                </div>
            </div>
        `;

        // 移除现有模态框
        const existingModal = document.querySelector('.custom-modal');
        if (existingModal) {
            existingModal.remove();
        }

        document.body.appendChild(modal);

        // 聚焦输入框
        setTimeout(() => {
            const textarea = document.getElementById('result-description');
            if (textarea) {
                textarea.focus();
                // 支持Ctrl+Enter提交
                textarea.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter' && e.ctrlKey) {
                        e.preventDefault();
                        MaintenanceCRUD.submitComplete(id);
                    }
                });
            }
        }, 100);
    }

    /**
     * 关闭完成模态框
     */
    function closeCompleteModal() {
        const modal = document.querySelector('.custom-modal');
        if (modal) {
            modal.remove();
        }
    }

    /**
     * 提交完成
     */
    async function submitComplete(id) {
        const resultDescription = document.getElementById('result-description').value.trim();

        if (!resultDescription) {
            UniversalCRUD.showNotification('请输入处理结果说明', 'error');
            return;
        }

        const csrfToken = getCSRFToken();
        const submitBtn = document.querySelector('.modal-footer .btn-primary');
        submitBtn.disabled = true;
        submitBtn.textContent = '提交中...';

        try {
            const response = await fetch(`${API_BASE_URL}/api/maintenance/requests/${id}/complete/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin',
                body: JSON.stringify({ result_description: resultDescription })
            });

            const data = await response.json();

            if (response.ok) {
                UniversalCRUD.showNotification('已完成，正在刷新页面...', 'success');
                closeCompleteModal();
                setTimeout(() => {
                    // 保留URL中的所有查询参数，包括tab等
                    const urlParams = new URLSearchParams(window.location.search);
                    let queryString = urlParams.toString();

                    // 如果没有查询参数，尝试检测当前激活的标签页
                    if (!queryString) {
                        const activeTab = document.querySelector('.tab.active');
                        if (activeTab && activeTab.getAttribute('onclick')) {
                            const match = activeTab.getAttribute('onclick').match(/switchTab\(this,\s*'([^']+)'\)/);
                            if (match && match[1]) {
                                queryString = 'tab=' + match[1];
                            }
                        }
                    }

                    if (queryString) {
                        window.location.href = window.location.pathname + '?' + queryString;
                    } else {
                        window.location.reload();
                    }
                }, 500);
            } else {
                throw new Error(data.error || data.message || '操作失败');
            }
        } catch (error) {
            UniversalCRUD.showNotification('操作失败: ' + error.message, 'error');
            submitBtn.disabled = false;
            submitBtn.textContent = '确定完成';
        }
    }

    /**
     * 关闭报事
     */
    async function closeMaintenance(id, requestNumber) {
        if (!confirm(`确认关闭报事 ${requestNumber} 吗？`)) {
            return;
        }

        const csrfToken = getCSRFToken();

        try {
            const response = await fetch(`${API_BASE_URL}/api/maintenance/requests/${id}/close/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            });

            const data = await response.json();

            if (response.ok) {
                UniversalCRUD.showNotification('报事已关闭，正在刷新页面...', 'success');
                setTimeout(() => {
                    const urlParams = new URLSearchParams(window.location.search);
                    let queryString = urlParams.toString();

                    if (!queryString) {
                        const activeTab = document.querySelector('.tab.active');
                        if (activeTab && activeTab.getAttribute('onclick')) {
                            const match = activeTab.getAttribute('onclick').match(/switchTab\(this,\s*'([^']+)'\)/);
                            if (match && match[1]) {
                                queryString = 'tab=' + match[1];
                            }
                        }
                    }

                    if (queryString) {
                        window.location.href = window.location.pathname + '?' + queryString;
                    } else {
                        window.location.reload();
                    }
                }, 500);
            } else {
                throw new Error(data.error || data.message || '操作失败');
            }
        } catch (error) {
            UniversalCRUD.showNotification('操作失败: ' + error.message, 'error');
        }
    }

    /**
     * 重新打开报事（返工）
     */
    async function reopenMaintenance(id, requestNumber) {
        if (!confirm(`确认重新打开报事 ${requestNumber} 吗？\n\n报事将返回"处理中"状态。`)) {
            return;
        }

        const csrfToken = getCSRFToken();

        try {
            const response = await fetch(`${API_BASE_URL}/api/maintenance/requests/${id}/reopen/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            });

            const data = await response.json();

            if (response.ok) {
                UniversalCRUD.showNotification('报事已重新打开，正在刷新页面...', 'success');
                setTimeout(() => {
                    const urlParams = new URLSearchParams(window.location.search);
                    let queryString = urlParams.toString();

                    if (!queryString) {
                        const activeTab = document.querySelector('.tab.active');
                        if (activeTab && activeTab.getAttribute('onclick')) {
                            const match = activeTab.getAttribute('onclick').match(/switchTab\(this,\s*'([^']+)'\)/);
                            if (match && match[1]) {
                                queryString = 'tab=' + match[1];
                            }
                        }
                    }

                    if (queryString) {
                        window.location.href = window.location.pathname + '?' + queryString;
                    } else {
                        window.location.reload();
                    }
                }, 500);
            } else {
                throw new Error(data.error || data.message || '操作失败');
            }
        } catch (error) {
            UniversalCRUD.showNotification('操作失败: ' + error.message, 'error');
        }
    }

    // 导出公共API
    return {
        // 原有的CRUD功能
        addMaintenance: function() {
            UniversalCRUD.addItem({
                formUrl: '/admin/forms/maintenance/new/',
                title: '新增报修',
                itemName: '报修',
                onLoad: function() {
                    MaintenanceForm.initCommunityCascade();
                }
            });
        },

        editMaintenance: function(id) {
            UniversalCRUD.editItem({
                formUrl: `/admin/forms/maintenance/${id}/`,
                title: '编辑报修',
                itemName: '报修',
                id: id,
                onLoad: function() {
                    MaintenanceForm.initCommunityCascade();
                }
            });
        },

        deleteMaintenance: function(id, title) {
            UniversalCRUD.confirmDelete({
                deleteUrl: `/api/maintenance/requests/${id}/`,
                itemName: '报修',
                id: id,
                name: title
            });
        },

        // 新增的派单功能
        assignMaintenance,
        closeAssignModal,
        submitAssign,
        startMaintenance,
        completeMaintenance,
        closeCompleteModal,
        submitComplete,
        // 新增的关闭和重开功能
        closeMaintenance,
        reopenMaintenance
    };
})();

/**
 * 报事表单管理器
 * 处理表单级联选择等逻辑
 */
window.MaintenanceForm = {
    // 初始化小区级联选择
    initCommunityCascade: function() {
        console.log('=== MaintenanceForm.initCommunityCascade called ===');

        // 等待DOM完全加载，增加超时时间
        setTimeout(() => {
            console.log('Looking for modal and select elements...');

            // 查找小区和房产选择框（在模态框内）
            const modal = document.querySelector('.custom-modal');
            console.log('Modal found:', modal);

            if (!modal) {
                console.error('Modal not found!');
                return;
            }

            const communitySelect = modal.querySelector('select[name="community"]');
            const propertySelect = modal.querySelector('select[name="property"]');

            console.log('Community select element:', communitySelect);
            console.log('Property select element:', propertySelect);

            if (!communitySelect) {
                console.error('Community select not found in modal!');
                console.log('Available selects in modal:', modal.querySelectorAll('select'));
                return;
            }

            if (!propertySelect) {
                console.error('Property select not found in modal!');
                console.log('Available selects in modal:', modal.querySelectorAll('select'));
                return;
            }

            console.log('Found community select:', communitySelect);
            console.log('Found property select:', propertySelect);
            console.log('Initial community value:', communitySelect.value);
            console.log('Initial property options:', propertySelect.options.length);

            // 检查是否已经绑定过事件
            if (communitySelect.dataset.maintenanceEventBound) {
                console.log('Event already bound, skipping...');
                return;
            }

            // 保存初始状态
            const initialCommunityId = communitySelect.value;
            const initialPropertyId = propertySelect.value;

            // 绑定小区选择变化事件
            communitySelect.addEventListener('change', function(event) {
                console.log('Community change event triggered!');
                MaintenanceForm.handleCommunityChange(event, propertySelect);
            });

            communitySelect.dataset.maintenanceEventBound = 'true';
            console.log('Event bound successfully');

            // 如果有初始选中的小区，加载其房产列表
            if (initialCommunityId) {
                console.log('Loading properties for initial community:', initialCommunityId);
                this.loadPropertiesForCommunity(initialCommunityId, propertySelect, initialPropertyId);
            } else {
                console.log('No initial community selected');
                propertySelect.disabled = true;
            }
        }, 500);
    },

    // 处理小区选择变化
    handleCommunityChange: function(event, propertySelect) {
        const communityId = event.target.value;
        console.log('=== Community changed to:', communityId, '===');

        if (!communityId) {
            propertySelect.innerHTML = '<option value="">请先选择小区</option>';
            propertySelect.disabled = true;
            propertySelect.required = false;
            return;
        }

        propertySelect.disabled = false;
        propertySelect.required = true;
        this.loadPropertiesForCommunity(communityId, propertySelect, null);
    },

    // 加载指定小区的房产列表
    loadPropertiesForCommunity: function(communityId, propertySelect, selectedPropertyId) {
        console.log('=== Loading properties for community:', communityId, '===');

        // 显示加载状态
        propertySelect.innerHTML = '<option value="">加载中...</option>';
        propertySelect.disabled = true;

        // 使用与管理后台相同的API
        fetch(`/admin/api/properties-by-community/?community_id=${communityId}`)
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('API returned:', data.properties ? data.properties.length : 0, 'properties');
                console.log('Sample property data:', data.properties ? data.properties[0] : 'No data');

                // 清空现有选项
                propertySelect.innerHTML = '<option value="">请选择房产</option>';

                // 添加房产选项
                if (data.properties && data.properties.length > 0) {
                    data.properties.forEach(property => {
                        const option = document.createElement('option');
                        option.value = property.id;
                        // 使用API返回的name字段作为显示文本
                        option.textContent = property.name || property.full_address || '未知房产';
                        // 如果是当前选中的房产，则设置为选中
                        if (selectedPropertyId && property.id === selectedPropertyId) {
                            option.selected = true;
                        }
                        propertySelect.appendChild(option);
                    });
                    propertySelect.disabled = false;
                    console.log('Properties loaded successfully');
                } else {
                    console.log('No properties found for this community');
                    const option = document.createElement('option');
                    option.value = '';
                    option.textContent = '该小区暂无房产';
                    propertySelect.appendChild(option);
                }
            })
            .catch(error => {
                console.error('Failed to load properties:', error);
                propertySelect.innerHTML = '<option value="">加载失败</option>';
            });
    }
};

/**
 * 报事请求管理器
 * 处理筛选、分页等操作
 */
window.RequestManager = (function() {
    return {
        /**
         * 导出Excel
         */
        exportExcel: function() {
            // 获取当前页面的筛选参数
            const urlParams = new URLSearchParams(window.location.search);
            const exportParams = new URLSearchParams();

            // 添加筛选参数
            if (urlParams.get('community')) exportParams.append('community', urlParams.get('community'));
            if (urlParams.get('category')) exportParams.append('category', urlParams.get('category'));
            if (urlParams.get('priority')) exportParams.append('priority', urlParams.get('priority'));
            if (urlParams.get('status')) exportParams.append('status', urlParams.get('status'));
            if (urlParams.get('search')) exportParams.append('search', urlParams.get('search'));

            // 构建导出URL
            const queryString = exportParams.toString();
            const exportUrl = `/api/maintenance/requests/export_excel/${queryString ? '?' + queryString : ''}`;

            // 创建隐藏的iframe来触发下载
            const iframe = document.createElement('iframe');
            iframe.style.display = 'none';
            iframe.src = exportUrl;
            document.body.appendChild(iframe);

            // 显示提示
            UniversalCRUD.showNotification('正在导出报事记录...', 'success');

            // 清理iframe
            setTimeout(() => {
                document.body.removeChild(iframe);
            }, 5000);
        },

        /**
         * 应用筛选
         */
        applyFilters: function() {
            const community = document.getElementById('request-filter-community')?.value || '';
            const category = document.getElementById('request-filter-category')?.value || '';
            const priority = document.getElementById('request-filter-priority')?.value || '';
            const status = document.getElementById('request-filter-status')?.value || '';
            const searchInput = document.getElementById('request-search-input');
            const searchValue = searchInput ? searchInput.value.trim() : '';

            const url = new URL(window.location);
            url.searchParams.set('page', '1');

            if (community) url.searchParams.set('community', community);
            else url.searchParams.delete('community');

            if (category) url.searchParams.set('category', category);
            else url.searchParams.delete('category');

            if (priority) url.searchParams.set('priority', priority);
            else url.searchParams.delete('priority');

            if (status) url.searchParams.set('status', status);
            else url.searchParams.delete('status');

            if (searchValue) url.searchParams.set('search', searchValue);
            else url.searchParams.delete('search');

            window.location.href = url.toString();
        },

        /**
         * 跳转到指定页面
         */
        goToPage: function(pageNum) {
            const url = new URL(window.location);
            url.searchParams.set('page', pageNum);
            window.location.href = url.toString();
        },

        /**
         * 修改每页显示数量
         */
        changePageSize: function(size) {
            const url = new URL(window.location);
            url.searchParams.set('page_size', size);
            url.searchParams.set('page', '1');
            window.location.href = url.toString();
        }
    };
})();
