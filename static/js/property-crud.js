/**
 * 房产管理 CRUD 模块
 */

// 房产管理
window.PropertyCRUD = {
    // 新增房产
    addProperty: function() {
        UniversalCRUD.addItem({
            formUrl: '/admin/forms/property/new/',
            title: '新增房产',
            itemName: '房产'
        });
    },

    // 编辑房产
    editProperty: function(id) {
        UniversalCRUD.editItem({
            formUrl: `/admin/forms/property/${id}/`,
            title: '编辑房产',
            itemName: '房产',
            id: id
        });
    },

    // 删除房产
    deleteProperty: function(id, roomNumber) {
        UniversalCRUD.confirmDelete({
            deleteUrl: `/api/property/properties/${id}/`,
            itemName: '房产',
            id: id,
            name: roomNumber
        });
    }
};

// 业主管理
window.OwnerCRUD = {
    // 新增业主
    addOwner: function() {
        UniversalCRUD.addItem({
            formUrl: '/admin/forms/owner/new/',
            title: '新增业主',
            itemName: '业主'
        });
    },

    // 编辑业主
    editOwner: function(id) {
        UniversalCRUD.editItem({
            formUrl: `/admin/forms/owner/${id}/`,
            title: '编辑业主',
            itemName: '业主',
            id: id
        });
    },

    // 删除业主
    deleteOwner: function(id, name) {
        UniversalCRUD.confirmDelete({
            deleteUrl: `/api/property/owners/${id}/`,
            itemName: '业主',
            id: id,
            name: name
        });
    }
};

// 租户管理
window.TenantCRUD = {
    // 新增租户
    addTenant: function() {
        UniversalCRUD.addItem({
            formUrl: '/admin/forms/tenant/new/',
            title: '新增租户',
            itemName: '租户'
        });
    },

    // 编辑租户
    editTenant: function(id) {
        UniversalCRUD.editItem({
            formUrl: `/admin/forms/tenant/${id}/`,
            title: '编辑租户',
            itemName: '租户',
            id: id
        });
    },

    // 删除租户
    deleteTenant: function(id, name) {
        UniversalCRUD.confirmDelete({
            deleteUrl: `/api/property/tenants/${id}/`,
            itemName: '租户',
            id: id,
            name: name
        });
    }
};

// 房产表单多业主管理
window.PropertyForm = {
    ownerRowIndex: 0,

    // 初始化业主行索引
    initOwnerRows: function() {
        const ownersList = document.getElementById('owners-list');
        if (!ownersList) return;

        const rows = ownersList.querySelectorAll('.owner-row');
        this.ownerRowIndex = rows.length;
        console.log('PropertyForm initialized with', this.ownerRowIndex, 'owner(s)');
    },

    // 添加业主行
    addOwnerRow: function() {
        console.log('Adding owner row...');
        const ownersList = document.getElementById('owners-list');
        if (!ownersList) {
            console.error('owners-list not found!');
            return;
        }

        const newRow = document.createElement('div');
        newRow.className = 'owner-row';
        newRow.style = 'background: var(--gray-50); padding: 15px; border-radius: 8px; margin-bottom: 10px; border: 1px solid var(--gray-200);';

        newRow.innerHTML = `
            <input type="hidden" name="owner_id_${this.ownerRowIndex}" value="">
            <div class="row">
                <div class="col-md-4">
                    <div class="form-group">
                        <label class="form-label">业主姓名</label>
                        <input type="text" name="owner_name_${this.ownerRowIndex}" class="form-control"
                               placeholder="请输入业主姓名" required>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-group">
                        <label class="form-label">联系电话</label>
                        <input type="text" name="owner_phone_${this.ownerRowIndex}" class="form-control"
                               placeholder="请输入手机号码">
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label class="form-label">所有权比例(%)</label>
                        <input type="number" name="owner_ratio_${this.ownerRowIndex}" class="form-control"
                               value="100" min="0" max="100" step="1">
                    </div>
                </div>
                <div class="col-md-1">
                    <div class="form-group">
                        <label class="form-label">&nbsp;</label>
                        <button type="button" class="btn btn-error btn-sm"
                                onclick="PropertyForm.removeOwnerRow(this)" style="width: 100%; padding: 8px;">
                            <i class="ri-delete-bin-line"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;

        ownersList.appendChild(newRow);
        this.ownerRowIndex++;
        document.getElementById('owners-count').value = this.ownerRowIndex;
        console.log('Owner row added. Total:', this.ownerRowIndex);
    },

    // 删除业主行
    removeOwnerRow: function(button) {
        console.log('Removing owner row...');
        const row = button.closest('.owner-row');
        const ownersList = document.getElementById('owners-list');

        if (!ownersList) {
            console.error('owners-list not found!');
            return;
        }

        // 至少保留一个业主
        if (ownersList.children.length <= 1) {
            alert('至少需要一个业主！');
            return;
        }

        row.remove();
        this.updateOwnerIndices();
        console.log('Owner row removed.');
    },

    // 更新业主索引
    updateOwnerIndices: function() {
        console.log('Updating owner indices...');
        const ownersList = document.getElementById('owners-list');
        if (!ownersList) {
            console.error('owners-list not found!');
            return;
        }

        const rows = ownersList.querySelectorAll('.owner-row');
        console.log('Total rows:', rows.length);

        rows.forEach((row, index) => {
            // 获取或创建owner_id隐藏字段
            let idInput = row.querySelector('input[type="hidden"][name^="owner_id_"]');
            if (!idInput) {
                idInput = document.createElement('input');
                idInput.type = 'hidden';
                idInput.name = `owner_id_${index}`;
                idInput.value = '';
                row.insertBefore(idInput, row.firstChild);
            } else {
                idInput.name = `owner_id_${index}`;
            }

            // 更新所有输入框的name属性
            const nameInput = row.querySelector('input[name^="owner_name_"]');
            const phoneInput = row.querySelector('input[name^="owner_phone_"]');
            const ratioInput = row.querySelector('input[name^="owner_ratio_"]');

            if (nameInput) {
                nameInput.name = `owner_name_${index}`;
            }
            if (phoneInput) {
                phoneInput.name = `owner_phone_${index}`;
            }
            if (ratioInput) {
                ratioInput.name = `owner_ratio_${index}`;
            }
        });

        document.getElementById('owners-count').value = rows.length;
        this.ownerRowIndex = rows.length;
        console.log('Indices updated. New count:', rows.length);
    }
};

// 业主表单多房产管理
window.OwnerForm = {
    propertyRowIndex: 0,

    // 初始化房产行索引
    initPropertyRows: function() {
        const propertiesList = document.getElementById('properties-list');
        if (!propertiesList) return;

        const rows = propertiesList.querySelectorAll('.property-row');
        this.propertyRowIndex = rows.length;
        console.log('OwnerForm initialized with', this.propertyRowIndex, 'propertie(s)');

        // 保存每一行的初始房产选择
        rows.forEach((row, index) => {
            const propertySelect = row.querySelector(`select[name="property_id_${index}"]`);
            const communitySelect = row.querySelector(`select[name="property_community_${index}"]`);

            if (propertySelect && communitySelect) {
                // 保存初始选中的房产ID和对应的小区ID
                const initialPropertyId = propertySelect.value;
                const initialCommunityId = communitySelect.value;

                if (initialPropertyId) {
                    // 将初始值存储在dataset中
                    propertySelect.dataset.initialPropertyId = initialPropertyId;
                    propertySelect.dataset.initialCommunityId = initialCommunityId;
                    console.log(`Row ${index}: initial property=${initialPropertyId}, community=${initialCommunityId}`);
                }
            }
        });

        // 绑定小区选择事件
        this.bindCommunityEvents();
    },

    // 绑定小区选择变化事件
    bindCommunityEvents: function() {
        const communitySelects = document.querySelectorAll('.property-community-select');
        console.log('Binding events to', communitySelects.length, 'community selects');

        communitySelects.forEach(select => {
            // 检查是否已经绑定过事件
            if (!select.dataset.eventBound) {
                console.log('Binding change event to:', select.name, 'value:', select.value);
                select.addEventListener('change', this.handleCommunityChange.bind(this));
                select.dataset.eventBound = 'true';
            } else {
                console.log('Event already bound to:', select.name);
            }
        });
    },

    // 处理小区选择变化
    handleCommunityChange: function(event) {
        console.log('=== handleCommunityChange called ===');
        const communitySelect = event.target;
        const communityId = communitySelect.value;
        const rowIndex = communitySelect.dataset.rowIndex;

        console.log('Row index:', rowIndex, 'Community ID:', communityId);

        // 使用更精确的选择器：先找到当前行，再在行内查找房产选择框
        const currentRow = communitySelect.closest('.property-row');
        if (!currentRow) {
            console.error('Cannot find parent row!');
            return;
        }

        const propertySelect = currentRow.querySelector('select[name^="property_id_"]');
        if (!propertySelect) {
            console.error('Cannot find property select in row!');
            return;
        }

        console.log('Found property select:', propertySelect.name, 'Current value:', propertySelect.value);

        // 保存当前选中的房产ID
        const currentPropertyId = propertySelect.value;
        const initialCommunityId = propertySelect.dataset.initialCommunity;

        console.log('Current property:', currentPropertyId, 'Initial community:', initialCommunityId);

        // 如果小区ID为空，清空房产选择
        if (!communityId) {
            propertySelect.innerHTML = '<option value="">请先选择小区</option>';
            return;
        }

        // 检查是否是初始化阶段的小区（即当前房产对应的小区）
        // 如果是，且当前房产属于这个小区，则不做任何处理
        if (initialCommunityId && initialCommunityId === communityId && currentPropertyId) {
            console.log('Skipping - already on initial community with selected property');
            return;
        }

        // 显示加载状态
        propertySelect.innerHTML = '<option value="">加载中...</option>';
        propertySelect.disabled = true;

        console.log('Fetching properties for community:', communityId);

        // 使用与管理后台相同的API（不需要认证）
        fetch(`/admin/api/properties-by-community/?community_id=${communityId}`)
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('API returned:', data);

                propertySelect.innerHTML = '<option value="">请选择房产</option>';
                propertySelect.disabled = false;

                // API返回的数据在properties字段中
                const properties = data.properties || [];

                if (properties.length > 0) {
                    console.log('Loaded', properties.length, 'properties');

                    properties.forEach(prop => {
                        const option = document.createElement('option');
                        option.value = prop.id;
                        // 使用full_address作为显示文本
                        const address = prop.full_address || prop.name || `房产${prop.id}`;
                        option.textContent = address;
                        option.dataset.communityId = communityId;

                        // 检查是否是之前选中的房产
                        if (prop.id === currentPropertyId) {
                            option.selected = true;
                            console.log('Keeping selected property:', address);
                        }

                        propertySelect.appendChild(option);
                    });

                    console.log('Property select updated. New value:', propertySelect.value);
                } else {
                    console.log('No properties found');
                    const option = document.createElement('option');
                    option.value = '';
                    option.textContent = '该小区暂无房产';
                    propertySelect.appendChild(option);
                }
            })
            .catch(error => {
                console.error('加载房产列表失败:', error);
                propertySelect.innerHTML = '<option value="">加载失败</option>';
                propertySelect.disabled = false;
            });
    },

    // 添加房产行
    addPropertyRow: function() {
        console.log('Adding property row...');
        const propertiesList = document.getElementById('properties-list');
        if (!propertiesList) {
            console.error('properties-list not found!');
            return;
        }

        // 获取所有小区选项(从第一行复制)
        const firstRowCommunity = document.querySelector('.property-community-select');
        if (!firstRowCommunity) {
            console.error('Cannot find community select template!');
            return;
        }

        const communityOptions = firstRowCommunity.innerHTML;

        const newRow = document.createElement('div');
        newRow.className = 'property-row';
        newRow.dataset.rowIndex = this.propertyRowIndex;
        newRow.style = 'background: var(--gray-50); padding: 15px; border-radius: 8px; margin-bottom: 10px; border: 1px solid var(--gray-200)';

        newRow.innerHTML = `
            <input type="hidden" name="property_op_id_${this.propertyRowIndex}" value="">
            <div class="row">
                <div class="col-md-3">
                    <div class="form-group">
                        <label class="form-label">小区</label>
                        <select name="property_community_${this.propertyRowIndex}"
                                class="form-control property-community-select"
                                data-row-index="${this.propertyRowIndex}"
                                required>
                            ${communityOptions}
                        </select>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-group">
                        <label class="form-label">房产</label>
                        <select name="property_id_${this.propertyRowIndex}"
                                class="form-control property-select"
                                data-row-index="${this.propertyRowIndex}"
                                required>
                            <option value="">请先选择小区</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="form-group">
                        <label class="form-label">所有权比例(%)</label>
                        <input type="number" name="property_ratio_${this.propertyRowIndex}"
                               class="form-control" value="100"
                               min="0" max="100" step="1">
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="form-group">
                        <label class="form-label">&nbsp;</label>
                        <button type="button" class="btn btn-error btn-sm"
                                onclick="OwnerForm.removePropertyRow(this)"
                                style="width: 100%; padding: 8px;">
                            <i class="ri-delete-bin-line"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;

        propertiesList.appendChild(newRow);
        this.propertyRowIndex++;
        document.getElementById('properties-count').value = this.propertyRowIndex;

        // 绑定新行的小区选择事件（只绑定新添加的行）
        const newCommunitySelect = newRow.querySelector('.property-community-select');
        if (newCommunitySelect) {
            newCommunitySelect.addEventListener('change', this.handleCommunityChange.bind(this));
            newCommunitySelect.dataset.eventBound = 'true';
        }

        console.log('Property row added. Total:', this.propertyRowIndex);
    },

    // 删除房产行
    removePropertyRow: function(button) {
        console.log('Removing property row...');
        const row = button.closest('.property-row');
        const propertiesList = document.getElementById('properties-list');

        if (!propertiesList) {
            console.error('properties-list not found!');
            return;
        }

        // 至少保留一套房产
        if (propertiesList.children.length <= 1) {
            alert('至少需要保留一套房产!');
            return;
        }

        row.remove();
        this.updatePropertyIndices();
        console.log('Property row removed.');
    },

    // 更新房产索引
    updatePropertyIndices: function() {
        console.log('Updating property indices...');
        const propertiesList = document.getElementById('properties-list');
        if (!propertiesList) {
            console.error('properties-list not found!');
            return;
        }

        const rows = propertiesList.querySelectorAll('.property-row');
        console.log('Total rows:', rows.length);

        rows.forEach((row, index) => {
            // 更新行的 data-row-index 属性
            row.dataset.rowIndex = index;

            // 更新隐藏字段(name=property_op_id_X)
            let opIdInput = row.querySelector('input[type="hidden"][name^="property_op_id_"]');
            if (opIdInput) {
                opIdInput.name = `property_op_id_${index}`;
            }

            // 更新小区选择(name=property_community_X)
            const communitySelect = row.querySelector('select[name^="property_community_"]');
            if (communitySelect) {
                communitySelect.name = `property_community_${index}`;
                communitySelect.dataset.rowIndex = index;
            }

            // 更新房产选择(name=property_id_X)
            const propertySelect = row.querySelector('select[name^="property_id_"]');
            if (propertySelect) {
                propertySelect.name = `property_id_${index}`;
                propertySelect.dataset.rowIndex = index;
            }

            // 更新所有权比例(name=property_ratio_X)
            const ratioInput = row.querySelector('input[name^="property_ratio_"]');
            if (ratioInput) {
                ratioInput.name = `property_ratio_${index}`;
            }
        });

        // 重新绑定事件（使用标志位避免重复）
        this.bindCommunityEvents();

        document.getElementById('properties-count').value = rows.length;
        this.propertyRowIndex = rows.length;
        console.log('Indices updated. New count:', rows.length);
    },

    // 编辑模式:加载已有房产(模板已完成,此方法保留备用)
    loadProperties: function(properties) {
        // 由Django模板直接渲染,无需JS加载
        console.log('Properties loaded from template');
    }
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 延迟初始化，确保表单已加载
    setTimeout(function() {
        PropertyForm.initOwnerRows();
        OwnerForm.initPropertyRows();
    }, 100);
});

// 监听模态框打开事件
document.addEventListener('shown.bs.modal', function() {
    PropertyForm.initOwnerRows();
    OwnerForm.initPropertyRows();
});
