/**
 * 缴费管理 CRUD 模块
 */

// ============================================
// 账单管理器
// ============================================
window.BillManager = {
    selectedItems: new Set(),

    // 全选/反选
    toggleSelectAll: function(checkbox) {
        const checkboxes = document.querySelectorAll('.bill-checkbox');
        checkboxes.forEach(cb => {
            cb.checked = checkbox.checked;
            const billId = cb.value;
            if (checkbox.checked) {
                this.selectedItems.add(billId);
            } else {
                this.selectedItems.delete(billId);
            }
        });
        this.updateBatchDeleteButton();
    },

    // 单个选择
    toggleSelect: function(checkbox) {
        const billId = checkbox.value;
        if (checkbox.checked) {
            this.selectedItems.add(billId);
        } else {
            this.selectedItems.delete(billId);
        }
        this.updateBatchDeleteButton();
    },

    // 更新批量删除按钮状态
    updateBatchDeleteButton: function() {
        const btn = document.getElementById('batch-delete-bills-btn');
        if (btn) {
            btn.disabled = this.selectedItems.size === 0;
            btn.style.opacity = this.selectedItems.size === 0 ? '0.5' : '1';
        }
    },

    // 应用筛选
    applyFilters: function() {
        const community = document.getElementById('bill-filter-community')?.value || '';
        const feeType = document.getElementById('bill-filter-fee-type')?.value || '';
        const status = document.getElementById('bill-filter-status')?.value || '';
        const searchInput = document.getElementById('bill-search-input');
        const searchValue = searchInput ? searchInput.value.trim() : '';

        const url = new URL(window.location);
        url.searchParams.set('page', '1');
        url.searchParams.set('tab', 'bills');

        if (community) url.searchParams.set('community', community);
        else url.searchParams.delete('community');

        if (feeType) url.searchParams.set('fee_type', feeType);
        else url.searchParams.delete('fee_type');

        if (status) url.searchParams.set('status', status);
        else url.searchParams.delete('status');

        if (searchValue) url.searchParams.set('search', searchValue);
        else url.searchParams.delete('search');

        window.location.href = url.toString();
    },

    // 批量删除账单
    batchDeleteBills: async function() {
        const checkboxes = document.querySelectorAll('.bill-checkbox:checked');

        if (checkboxes.length === 0) {
            alert('请先选择要删除的账单');
            return;
        }

        const billIds = Array.from(checkboxes).map(cb => cb.value);

        const confirmed = confirm(`确定要删除选中的 ${billIds.length} 个账单吗？\n\n此操作无法恢复！`);
        if (!confirmed) return;

        try {
            // 获取CSRF token
            const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]')?.content ||
                              document.querySelector('meta[name="csrf-token"]')?.content ||
                              document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

            // 发送批量删除请求
            const response = await fetch('/api/payment/bills/batch_delete/', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin',
                body: JSON.stringify({
                    bill_ids: billIds
                })
            });

            const result = await response.json();

            if (result.success) {
                alert(result.message);
                // 刷新页面以显示更新后的数据
                window.location.reload();
            } else {
                alert('删除失败：' + (result.error || '未知错误'));
            }
        } catch (error) {
            console.error('批量删除错误:', error);
            alert('删除失败：网络错误或服务器异常');
        }
    }
};

// ============================================
// 费用标准管理器
// ============================================
window.FeeManager = {
    selectedItems: new Set(),

    toggleSelectAll: function(checkbox) {
        const checkboxes = document.querySelectorAll('.fee-checkbox');
        checkboxes.forEach(cb => {
            cb.checked = checkbox.checked;
            const feeId = cb.value;
            if (checkbox.checked) {
                this.selectedItems.add(feeId);
            } else {
                this.selectedItems.delete(feeId);
            }
        });
        this.updateBatchDeleteButton();
    },

    toggleSelect: function(checkbox) {
        const feeId = checkbox.value;
        if (checkbox.checked) {
            this.selectedItems.add(feeId);
        } else {
            this.selectedItems.delete(feeId);
        }
        this.updateBatchDeleteButton();
    },

    updateBatchDeleteButton: function() {
        const btn = document.getElementById('batch-delete-fees-btn');
        if (btn) {
            btn.disabled = this.selectedItems.size === 0;
            btn.style.opacity = this.selectedItems.size === 0 ? '0.5' : '1';
        }
    },

    applyFilters: function() {
        const community = document.getElementById('fee-filter-community')?.value || '';
        const feeType = document.getElementById('fee-filter-type')?.value || '';

        const url = new URL(window.location);
        url.searchParams.set('page', '1');
        url.searchParams.set('tab', 'standards');

        if (community) url.searchParams.set('community', community);
        else url.searchParams.delete('community');

        if (feeType) url.searchParams.set('fee_type', feeType);
        else url.searchParams.delete('fee_type');

        window.location.href = url.toString();
    },

    batchDeleteFeeStandards: function() {
        if (this.selectedItems.size === 0) {
            alert('请先选择要删除的费用标准');
            return;
        }

        if (!confirm(`确定要删除选中的 ${this.selectedItems.size} 个费用标准吗？`)) {
            return;
        }

        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
        const deletePromises = Array.from(this.selectedItems).map(feeId => {
            return fetch(`/api/payment/fee-standards/${feeId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            });
        });

        Promise.all(deletePromises)
            .then(() => {
                alert('批量删除成功');
                window.location.reload();
            })
            .catch(error => {
                alert('批量删除失败: ' + error.message);
            });
    }
};

// ============================================
// 缴费记录管理器
// ============================================
window.RecordManager = {
    selectedItems: new Set(),

    toggleSelectAll: function(checkbox) {
        const checkboxes = document.querySelectorAll('.record-checkbox');
        checkboxes.forEach(cb => {
            cb.checked = checkbox.checked;
            const recordId = cb.value;
            if (checkbox.checked) {
                this.selectedItems.add(recordId);
            } else {
                this.selectedItems.delete(recordId);
            }
        });
        this.updateBatchDeleteButton();
    },

    toggleSelect: function(checkbox) {
        const recordId = checkbox.value;
        if (checkbox.checked) {
            this.selectedItems.add(recordId);
        } else {
            this.selectedItems.delete(recordId);
        }
        this.updateBatchDeleteButton();
    },

    updateBatchDeleteButton: function() {
        const btn = document.getElementById('batch-delete-records-btn');
        if (btn) {
            btn.disabled = this.selectedItems.size === 0;
            btn.style.opacity = this.selectedItems.size === 0 ? '0.5' : '1';
        }
    },

    applyFilters: function() {
        const community = document.getElementById('record-filter-community')?.value || '';
        const paymentMethod = document.getElementById('record-filter-method')?.value || '';
        const searchInput = document.getElementById('record-search-input');
        const searchValue = searchInput ? searchInput.value.trim() : '';

        const url = new URL(window.location);
        url.searchParams.set('page', '1');
        url.searchParams.set('tab', 'records');

        if (community) url.searchParams.set('community', community);
        else url.searchParams.delete('community');

        if (paymentMethod) url.searchParams.set('payment_method', paymentMethod);
        else url.searchParams.delete('payment_method');

        if (searchValue) url.searchParams.set('search', searchValue);
        else url.searchParams.delete('search');

        window.location.href = url.toString();
    },

    batchDeleteRecords: function() {
        if (this.selectedItems.size === 0) {
            alert('请先选择要删除的缴费记录');
            return;
        }

        if (!confirm(`确定要删除选中的 ${this.selectedItems.size} 条缴费记录吗？`)) {
            return;
        }

        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
        const deletePromises = Array.from(this.selectedItems).map(recordId => {
            return fetch(`/api/payment/records/${recordId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            });
        });

        Promise.all(deletePromises)
            .then(() => {
                alert('批量删除成功');
                window.location.reload();
            })
            .catch(error => {
                alert('批量删除失败: ' + error.message);
            });
    }
};

// ============================================
// CRUD 操作
// ============================================

// 缴费记录管理
window.RecordCRUD = {
    // 查看缴费记录详情
    viewRecord: function(recordId) {
        console.log('Viewing record:', recordId);

        // 获取CSRF token
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        // 获取缴费记录详情
        fetch(`/api/payment/records/${recordId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('获取缴费记录详情失败');
                }
                return response.json();
            })
            .then(data => {
                console.log('Record data:', data);
                this.showRecordDetail(data);
            })
            .catch(error => {
                console.error('Error:', error);
                // 如果API不存在，从表格行获取数据
                this.showRecordDetailFromRow(recordId);
            });
    },

    // 从表格行获取数据并显示详情
    showRecordDetailFromRow: function(recordId) {
        const row = document.querySelector(`input[value="${recordId}"]`).closest('tr');
        if (!row) {
            alert('未找到缴费记录');
            return;
        }

        const cells = row.querySelectorAll('td');
        const record = {
            transaction_id: cells[1].textContent.trim(),
            property_unit: cells[2].querySelector('div')?.textContent.trim() || '',
            floor_room: cells[2].querySelectorAll('div')[1]?.textContent.trim() || '',
            owner: cells[3].textContent.trim(),
            amount: cells[4].textContent.trim(),
            payment_method: cells[5].textContent.trim(),
            payment_time: cells[6].textContent.trim(),
            operator: cells[7].textContent.trim()
        };

        this.showRecordDetail(record);
    },

    // 显示缴费记录详情
    showRecordDetail: function(record) {
        const modalHtml = `
            <div id="record-detail-modal" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 9999;">
                <div style="background: white; border-radius: 12px; padding: 32px; width: 600px; max-width: 90%; max-height: 80vh; overflow-y: auto; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
                        <h2 style="font-size: 20px; font-weight: 600; margin: 0;">缴费记录详情</h2>
                        <button onclick="document.getElementById('record-detail-modal').remove()" style="background: none; border: none; font-size: 24px; cursor: pointer; color: #64748B;">&times;</button>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div>
                            <label style="display: block; font-size: 12px; font-weight: 500; margin-bottom: 4px; color: #64748B;">交易号</label>
                            <div style="font-size: 14px; color: #1F2937; font-family: monospace;">${record.transaction_id || '-'}</div>
                        </div>
                        <div>
                            <label style="display: block; font-size: 12px; font-weight: 500; margin-bottom: 4px; color: #64748B;">商户订单号</label>
                            <div style="font-size: 14px; color: #1F2937; font-family: monospace;">${record.out_trade_no || '-'}</div>
                        </div>
                        <div>
                            <label style="display: block; font-size: 12px; font-weight: 500; margin-bottom: 4px; color: #64748B;">房产</label>
                            <div style="font-size: 14px; color: #1F2937; font-weight: 600;">${record.property_unit || record.bill?.property_unit || '-'}</div>
                            ${record.floor_room || record.bill?.property_unit?.floor_room_display ? `<div style="font-size: 12px; color: #94A3B8;">${record.floor_room || record.bill?.property_unit?.floor_room_display}</div>` : ''}
                        </div>
                        <div>
                            <label style="display: block; font-size: 12px; font-weight: 500; margin-bottom: 4px; color: #64748B;">业主</label>
                            <div style="font-size: 14px; color: #1F2937;">${record.payer || record.owner || '-'}</div>
                        </div>
                        <div>
                            <label style="display: block; font-size: 12px; font-weight: 500; margin-bottom: 4px; color: #64748B;">缴费金额</label>
                            <div style="font-size: 18px; color: #10B981; font-weight: 700;">${record.amount ? '¥' + record.amount : '-'}</div>
                        </div>
                        <div>
                            <label style="display: block; font-size: 12px; font-weight: 500; margin-bottom: 4px; color: #64748B;">支付方式</label>
                            <div style="font-size: 14px; color: #1F2937;">${this.getPaymentMethodDisplay(record.payment_method)}</div>
                        </div>
                        <div>
                            <label style="display: block; font-size: 12px; font-weight: 500; margin-bottom: 4px; color: #64748B;">缴费时间</label>
                            <div style="font-size: 14px; color: #1F2937;">${record.payment_time || '-'}</div>
                        </div>
                        <div>
                            <label style="display: block; font-size: 12px; font-weight: 500; margin-bottom: 4px; color: #64748B;">操作人</label>
                            <div style="font-size: 14px; color: #1F2937;">${record.operator || '-'}</div>
                        </div>
                        ${record.status ? `
                        <div>
                            <label style="display: block; font-size: 12px; font-weight: 500; margin-bottom: 4px; color: #64748B;">状态</label>
                            <div style="font-size: 14px; color: #1F2937;">${this.getStatusDisplay(record.status)}</div>
                        </div>
                        ` : ''}
                    </div>

                    <div style="margin-top: 24px; text-align: right;">
                        <button onclick="document.getElementById('record-detail-modal').remove()" style="padding: 10px 20px; border: 1px solid #CBD5E1; background: white; border-radius: 6px; font-size: 14px; cursor: pointer; color: #64748B;">关闭</button>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);
    },

    // 获取支付方式显示文本
    getPaymentMethodDisplay: function(method) {
        const methodMap = {
            'wechat': '微信支付',
            'alipay': '支付宝',
            'cash': '现金',
            'bank_transfer': '银行转账'
        };
        return methodMap[method] || method || '-';
    },

    // 获取状态显示文本
    getStatusDisplay: function(status) {
        const statusMap = {
            'success': '成功',
            'refund': '退款',
            'failed': '失败'
        };
        return statusMap[status] || status || '-';
    }
};

// 费用标准管理
window.FeeCRUD = {
    // 新增费用标准
    addFeeStandard: function() {
        UniversalCRUD.addItem({
            formUrl: '/admin/forms/fee-standard/new/',
            title: '新增费用标准',
            itemName: '费用标准'
        });
    },

    // 编辑费用标准
    editFeeStandard: function(id) {
        UniversalCRUD.editItem({
            formUrl: `/admin/forms/fee-standard/${id}/`,
            title: '编辑费用标准',
            itemName: '费用标准',
            id: id
        });
    },

    // 删除费用标准
    deleteFeeStandard: function(id, name) {
        UniversalCRUD.confirmDelete({
            deleteUrl: `/api/payment/fee-standards/${id}/`,
            itemName: '费用标准',
            id: id,
            name: name
        });
    }
};

// 账单管理
window.BillCRUD = {
    // 新增账单
    addBill: function() {
        UniversalCRUD.addItem({
            formUrl: '/admin/forms/payment-bill/new/',
            title: '新增账单',
            itemName: '账单',
            onLoad: function() {
                BillForm.initCommunityCascade();
            }
        });
    },

    // 编辑账单
    editBill: function(id) {
        UniversalCRUD.editItem({
            formUrl: `/admin/forms/payment-bill/${id}/`,
            title: '编辑账单',
            itemName: '账单',
            id: id,
            onLoad: function() {
                BillForm.initCommunityCascade();
                BillForm.initPaymentFields();
            }
        });
    },

    // 删除账单
    deleteBill: function(id, owner) {
        UniversalCRUD.confirmDelete({
            deleteUrl: `/api/payment/bills/${id}/`,
            itemName: '账单',
            id: id,
            name: owner
        });
    },

    // 导入Excel账单
    importExcel: function() {
        // 创建导入对话框
        const dialogHtml = `
            <div id="import-dialog" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 9999;">
                <div style="background: white; border-radius: 12px; padding: 32px; width: 500px; max-width: 90%; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
                        <h2 style="font-size: 20px; font-weight: 600; margin: 0;">导入应缴费用Excel</h2>
                        <button onclick="document.getElementById('import-dialog').remove()" style="background: none; border: none; font-size: 24px; cursor: pointer; color: #64748B;">&times;</button>
                    </div>

                    <div style="margin-bottom: 20px;">
                        <label style="display: block; font-size: 13px; font-weight: 500; margin-bottom: 8px; color: #334155;">选择小区 *</label>
                        <select id="import-community" class="form-control" style="width: 100%; padding: 10px; border: 1px solid #CBD5E1; border-radius: 6px; font-size: 14px;">
                            <option value="">请选择小区</option>
                        </select>
                    </div>

                    <div style="margin-bottom: 20px;">
                        <label style="display: block; font-size: 13px; font-weight: 500; margin-bottom: 8px; color: #334155;">费用类型</label>
                        <select id="import-fee-type" class="form-control" style="width: 100%; padding: 10px; border: 1px solid #CBD5E1; border-radius: 6px; font-size: 14px;">
                            <option value="property">物业费</option>
                            <option value="public_electric">公摊电费</option>
                            <option value="water">水费</option>
                            <option value="parking">停车费</option>
                            <option value="payable" selected>应缴费用</option>
                            <option value="other">其他</option>
                        </select>
                    </div>

                    <div style="margin-bottom: 20px;">
                        <label style="display: block; font-size: 13px; font-weight: 500; margin-bottom: 8px; color: #334155;">账期</label>
                        <input type="text" id="import-billing-period" class="form-control" value="2026-01" style="width: 100%; padding: 10px; border: 1px solid #CBD5E1; border-radius: 6px; font-size: 14px;" placeholder="如：2026-01">
                    </div>

                    <div style="margin-bottom: 20px;">
                        <label style="display: block; font-size: 13px; font-weight: 500; margin-bottom: 8px; color: #334155;">上传Excel文件 *</label>
                        <div style="border: 2px dashed #CBD5E1; border-radius: 8px; padding: 24px; text-align: center; cursor: pointer; transition: all 0.2s;" onclick="document.getElementById('import-file').click()" onmouseover="this.style.borderColor='#3B82F6'; this.style.background='#F8FAFC'" onmouseout="this.style.borderColor='#CBD5E1'; this.style.background='white'">
                            <input type="file" id="import-file" accept=".xlsx,.xls" style="display: none;" onchange="BillCRUD.handleFileSelect(this)">
                            <div id="file-preview" style="display: none;">
                                <i class="ri-file-excel-2-line" style="font-size: 32px; color: #10B981;"></i>
                                <p id="file-name" style="margin: 8px 0 0 0; font-size: 14px; color: #334155;"></p>
                            </div>
                            <div id="upload-hint">
                                <i class="ri-upload-cloud-2-line" style="font-size: 32px; color: #64748B;"></i>
                                <p style="margin: 8px 0 0 0; font-size: 14px; color: #64748B;">点击或拖拽文件到此处上传</p>
                                <p style="margin: 4px 0 0 0; font-size: 12px; color: #94A3B8;">支持 .xlsx 或 .xls 格式</p>
                            </div>
                        </div>
                    </div>

                    <div style="background: #FEF3C7; border-left: 4px solid #F59E0B; padding: 12px; margin-bottom: 20px; border-radius: 4px;">
                        <p style="margin: 0; font-size: 12px; color: #92400E;">
                            <strong>Excel文件要求：</strong><br>
                            • 必须包含列：房号、业主、应缴金额<br>
                            • 房号格式示例：1号楼-501、2-601、1号楼1单元-201、1-2-201<br>
                            • 业主可以是单个姓名或多个姓名（如：张三（李四））
                        </p>
                    </div>

                    <div style="display: flex; gap: 12px; justify-content: flex-end;">
                        <button onclick="document.getElementById('import-dialog').remove()" style="padding: 10px 20px; border: 1px solid #CBD5E1; background: white; border-radius: 6px; font-size: 14px; cursor: pointer; color: #64748B;">取消</button>
                        <button onclick="BillCRUD.submitImport()" style="padding: 10px 20px; border: none; background: #0F4C81; color: white; border-radius: 6px; font-size: 14px; cursor: pointer;">开始导入</button>
                    </div>

                    <div id="import-result" style="display: none; margin-top: 20px;"></div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', dialogHtml);

        // 加载小区列表
        fetch('/api/community/communities/')
            .then(response => response.json())
            .then(data => {
                const select = document.getElementById('import-community');
                if (data.results) {
                    data.results.forEach(community => {
                        const option = document.createElement('option');
                        option.value = community.id;
                        option.textContent = community.name;
                        select.appendChild(option);
                    });
                } else if (Array.isArray(data)) {
                    data.forEach(community => {
                        const option = document.createElement('option');
                        option.value = community.id;
                        option.textContent = community.name;
                        select.appendChild(option);
                    });
                }
            })
            .catch(error => {
                console.error('加载小区列表失败:', error);
            });
    },

    // 处理文件选择
    handleFileSelect: function(input) {
        const file = input.files[0];
        if (file) {
            document.getElementById('file-preview').style.display = 'block';
            document.getElementById('upload-hint').style.display = 'none';
            document.getElementById('file-name').textContent = file.name;
        }
    },

    // 提交导入
    submitImport: function() {
        const communityId = document.getElementById('import-community').value;
        const feeType = document.getElementById('import-fee-type').value;
        const billingPeriod = document.getElementById('import-billing-period').value;
        const fileInput = document.getElementById('import-file');

        if (!communityId) {
            alert('请选择小区');
            return;
        }

        if (!fileInput.files.length) {
            alert('请选择Excel文件');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('community_id', communityId);
        formData.append('fee_type', feeType);
        formData.append('billing_period', billingPeriod);

        // 显示加载状态
        const resultDiv = document.getElementById('import-result');
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = '<p style="text-align: center; color: #64748B;"><i class="ri-loader-4-line ri-spin"></i> 正在导入...</p>';

        // 获取CSRF token
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

        fetch('/api/payment/bills/import_excel/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultDiv.innerHTML = `<div style="background: #FEE2E2; border-left: 4px solid #EF4444; padding: 12px; border-radius: 4px;"><p style="margin: 0; color: #991B1B; font-size: 14px;">${data.error}</p></div>`;
            } else {
                const stats = data.stats;
                let resultHtml = `
                    <div style="background: ${stats.error_count > 0 ? '#FEF3C7' : '#D1FAE5'}; border-left: 4px solid ${stats.error_count > 0 ? '#F59E0B' : '#10B981'}; padding: 12px; border-radius: 4px; margin-bottom: 12px;">
                        <p style="margin: 0 0 8px 0; color: ${stats.error_count > 0 ? '#92400E' : '#065F46'}; font-size: 14px; font-weight: 600;">${data.message}</p>
                        <p style="margin: 4px 0; color: ${stats.error_count > 0 ? '#92400E' : '#065F46'}; font-size: 13px;">
                            总行数: ${stats.total_rows} | 成功: ${stats.success_count} | 失败: ${stats.error_count}
                        </p>
                        ${stats.success_count > 0 && stats.error_count === 0 ? `
                            <p style="margin: 8px 0 0 0; color: #065F46; font-size: 13px;">
                                <i class="ri-check-line"></i> 导入成功！页面将在2秒后自动刷新...
                            </p>
                        ` : ''}
                    </div>
                `;

                // 如果有失败记录，显示下载按钮
                if (stats.failed_records && stats.failed_records.length > 0) {
                    resultHtml += `
                        <div style="background: #FEE2E2; border-left: 4px solid #EF4444; padding: 12px; border-radius: 4px; margin-bottom: 12px;">
                            <p style="margin: 0 0 8px 0; color: #991B1B; font-size: 14px; font-weight: 600;">
                                有 ${stats.failed_records.length} 条记录导入失败
                            </p>
                            <p style="margin: 4px 0; color: #991B1B; font-size: 13px;">
                                点击下方按钮下载失败记录Excel文件，查看详细错误原因
                            </p>
                            <button onclick="BillCRUD.downloadFailedRecords(${JSON.stringify(stats.failed_records).replace(/"/g, '&quot;')})"
                                    style="margin-top: 8px; margin-right: 8px; padding: 8px 16px; background: #EF4444; color: white; border: none; border-radius: 6px; font-size: 14px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px;">
                                <i class="ri-download-line"></i>
                                下载失败记录Excel
                            </button>
                            <button onclick="location.reload()"
                                    style="margin-top: 8px; padding: 8px 16px; background: #0F4C81; color: white; border: none; border-radius: 6px; font-size: 14px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px;">
                                <i class="ri-refresh-line"></i>
                                关闭并刷新
                            </button>
                        </div>
                    `;
                }

                if (stats.errors.length > 0) {
                    resultHtml += `
                        <div style="background: #FEF3C7; border-left: 4px solid #F59E0B; padding: 12px; border-radius: 4px; max-height: 200px; overflow-y: auto;">
                            <p style="margin: 0 0 8px 0; color: #92400E; font-size: 14px; font-weight: 600;">错误详情（前20条）：</p>
                            <ul style="margin: 0; padding-left: 20px; font-size: 12px; color: #92400E;">
                    `;
                    stats.errors.slice(0, 20).forEach(error => {
                        resultHtml += `<li style="margin: 4px 0;">${error}</li>`;
                    });
                    resultHtml += '</ul></div>';
                }

                resultDiv.innerHTML = resultHtml;

                // 如果导入成功且没有失败记录，2秒后自动刷新
                // 如果有失败记录，不自动刷新，让用户有时间下载失败记录
                if (stats.success_count > 0 && stats.error_count === 0) {
                    setTimeout(() => {
                        location.reload();
                    }, 2000);
                }
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `<div style="background: #FEE2E2; border-left: 4px solid #EF4444; padding: 12px; border-radius: 4px;"><p style="margin: 0; color: #991B1B; font-size: 14px;">导入失败: ${error.message}</p></div>`;
        });
    },

    // 下载失败记录Excel文件
    downloadFailedRecords: function(failedRecords) {
        if (!failedRecords || failedRecords.length === 0) {
            alert('没有失败记录');
            return;
        }

        // 使用SheetJS (xlsx)库生成Excel文件
        // 准备数据，保持与上传文件相同的表头
        const excelData = failedRecords.map(record => ({
            '行号': record.row,
            '房号': record.房号 || '',
            '业主': record.业主 || '',
            '应缴金额': record.应缴金额 || '',
            '失败原因': record.失败原因 || ''
        }));

        // 创建工作表
        const ws = XLSX.utils.json_to_sheet(excelData);

        // 设置列宽
        ws['!cols'] = [
            { wch: 8 },  // 行号
            { wch: 20 }, // 房号
            { wch: 15 }, // 业主
            { wch: 12 }, // 应缴金额
            { wch: 50 }  // 失败原因
        ];

        // 创建工作簿
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, '导入失败记录');

        // 生成文件名（包含时间戳）
        const now = new Date();
        const timestamp = now.toISOString().replace(/[:.]/g, '-').slice(0, -5);
        const fileName = `缴费导入失败记录_${timestamp}.xlsx`;

        // 生成Excel文件并触发下载
        XLSX.writeFile(wb, fileName);
    }
};

// ============================================
// 账单表单管理器
// ============================================
window.BillForm = {
    // 初始化支付方式字段
    initPaymentFields: function() {
        console.log('=== BillForm.initPaymentFields called ===');

        const modal = document.querySelector('.custom-modal');
        if (!modal) {
            console.error('Modal not found!');
            return;
        }

        const statusSelect = modal.querySelector('#id_status');
        const paymentFieldsRow = modal.querySelector('#payment-fields-row');
        const paidAtInput = modal.querySelector('#id_paid_at');
        const paymentMethodRequired = modal.querySelector('#payment-method-required');
        const paymentMethodError = modal.querySelector('#payment-method-error');
        const paymentMethodSelect = modal.querySelector('#id_payment_method');
        const paidAmountGroup = modal.querySelector('#paid-amount-group');
        const paidAmountInput = modal.querySelector('#id_paid_amount_input');
        const paidAmountError = modal.querySelector('#paid-amount-error');
        const amountInput = modal.querySelector('#id_amount');
        const form = modal.querySelector('.ajax-form');

        console.log('Found elements:', {
            statusSelect: !!statusSelect,
            paymentFieldsRow: !!paymentFieldsRow,
            paidAtInput: !!paidAtInput,
            paymentMethodRequired: !!paymentMethodRequired,
            paymentMethodError: !!paymentMethodError,
            paymentMethodSelect: !!paymentMethodSelect,
            paidAmountGroup: !!paidAmountGroup,
            paidAmountInput: !!paidAmountInput,
            amountInput: !!amountInput,
            form: !!form
        });

        if (!statusSelect || !paymentFieldsRow) {
            console.error('Required elements not found!');
            return;
        }

        // 更新支付方式必填状态
        function updatePaymentMethodRequired(isRequired) {
            console.log('updatePaymentMethodRequired:', isRequired);
            if (isRequired) {
                if (paymentMethodRequired) {
                    paymentMethodRequired.style.display = 'inline';
                }
                if (paymentMethodSelect) {
                    paymentMethodSelect.required = true;
                }
            } else {
                if (paymentMethodRequired) {
                    paymentMethodRequired.style.display = 'none';
                }
                if (paymentMethodSelect) {
                    paymentMethodSelect.required = false;
                }
                if (paymentMethodError) {
                    paymentMethodError.style.display = 'none';
                }
            }
        }

        // 状态变化事件处理
        function handleStatusChange() {
            const status = statusSelect.value;
            console.log('Status changed to:', status);

            if (status === 'paid' || status === 'partial') {
                console.log('Showing payment fields');
                paymentFieldsRow.style.display = 'flex';
                updatePaymentMethodRequired(true);

                if (paidAtInput && !paidAtInput.value) {
                    const now = new Date();
                    const year = now.getFullYear();
                    const month = String(now.getMonth() + 1).padStart(2, '0');
                    const day = String(now.getDate()).padStart(2, '0');
                    const hours = String(now.getHours()).padStart(2, '0');
                    const minutes = String(now.getMinutes()).padStart(2, '0');
                    const seconds = String(now.getSeconds()).padStart(2, '0');

                    paidAtInput.value = `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
                }

                // 处理部分缴的已缴金额输入框
                if (status === 'partial') {
                    if (paidAmountGroup) {
                        paidAmountGroup.style.display = 'block';
                    }
                    if (paidAmountInput) {
                        paidAmountInput.required = true;
                    }
                } else {
                    // 已缴状态，隐藏已缴金额输入框
                    if (paidAmountGroup) {
                        paidAmountGroup.style.display = 'none';
                    }
                    if (paidAmountInput) {
                        paidAmountInput.required = false;
                    }
                }
            } else {
                console.log('Hiding payment fields');
                paymentFieldsRow.style.display = 'none';
                if (paymentMethodSelect) {
                    paymentMethodSelect.value = '';
                }
                if (paidAtInput) {
                    paidAtInput.value = '';
                }
                if (paidAmountInput) {
                    paidAmountInput.value = '';
                    paidAmountInput.required = false;
                }
                if (paidAmountGroup) {
                    paidAmountGroup.style.display = 'none';
                }
                updatePaymentMethodRequired(false);
            }
        }

        // 移除旧的事件监听器（如果存在）
        if (statusSelect._statusChangeHandler) {
            statusSelect.removeEventListener('change', statusSelect._statusChangeHandler);
        }

        // 添加状态变化监听器
        statusSelect._statusChangeHandler = handleStatusChange;
        statusSelect.addEventListener('change', handleStatusChange);

        // 初始化当前状态
        console.log('Initial status:', statusSelect.value);
        handleStatusChange();

        // 表单提交验证
        if (form && !form._paymentValidationSetup) {
            form._paymentValidationSetup = true;

            form.addEventListener('submit', function(e) {
                const status = statusSelect.value;

                // 验证支付方式
                if ((status === 'paid' || status === 'partial') && paymentMethodSelect) {
                    if (!paymentMethodSelect.value || paymentMethodSelect.value === '') {
                        e.preventDefault();
                        e.stopPropagation();

                        if (paymentMethodError) {
                            paymentMethodError.style.display = 'block';
                            paymentMethodError.textContent = '请选择支付方式';
                        }

                        paymentMethodSelect.focus();
                        return false;
                    } else {
                        if (paymentMethodError) {
                            paymentMethodError.style.display = 'none';
                        }
                    }
                }

                // 验证部分缴的已缴金额
                if (status === 'partial' && paidAmountInput && amountInput) {
                    const paidAmount = parseFloat(paidAmountInput.value);
                    const totalAmount = parseFloat(amountInput.value);

                    if (!paidAmount || paidAmount <= 0) {
                        e.preventDefault();
                        e.stopPropagation();

                        if (paidAmountError) {
                            paidAmountError.style.display = 'block';
                            paidAmountError.textContent = '请输入已缴金额';
                        }

                        paidAmountInput.focus();
                        return false;
                    }

                    if (paidAmount > totalAmount) {
                        e.preventDefault();
                        e.stopPropagation();

                        if (paidAmountError) {
                            paidAmountError.style.display = 'block';
                            paidAmountError.textContent = '已缴金额不能超过应缴金额';
                        }

                        paidAmountInput.focus();
                        return false;
                    }

                    // 验证通过，隐藏错误提示
                    if (paidAmountError) {
                        paidAmountError.style.display = 'none';
                    }
                }
            });

            // 当用户输入已缴金额时，隐藏错误提示
            if (paidAmountInput) {
                paidAmountInput.addEventListener('input', function() {
                    if (paidAmountError) {
                        paidAmountError.style.display = 'none';
                    }
                });
            }

            // 当用户选择支付方式时，隐藏错误提示
            if (paymentMethodSelect) {
                paymentMethodSelect.addEventListener('change', function() {
                    if (this.value && paymentMethodError) {
                        paymentMethodError.style.display = 'none';
                    }
                });
            }
        }

        console.log('Payment fields initialized successfully');
    },

    // 初始化小区级联选择
    initCommunityCascade: function() {
        console.log('=== BillForm.initCommunityCascade called ===');

        // 等待DOM完全加载
        setTimeout(() => {
            // 查找小区和房产选择框（在模态框内）
            const modal = document.querySelector('.custom-modal');
            if (!modal) {
                console.error('Modal not found!');
                return;
            }

            const communitySelect = modal.querySelector('select[name="community"]');
            const propertySelect = modal.querySelector('select[name="property_unit"]');

            if (!communitySelect) {
                console.error('Community select not found in modal!');
                return;
            }

            if (!propertySelect) {
                console.error('Property select not found in modal!');
                return;
            }

            console.log('Found community select:', communitySelect);
            console.log('Found property select:', propertySelect);
            console.log('Initial community value:', communitySelect.value);
            console.log('Initial property options:', propertySelect.options.length);

            // 检查是否已经绑定过事件
            if (communitySelect.dataset.billEventBound) {
                console.log('Event already bound, skipping...');
                return;
            }

            // 保存初始状态
            const initialCommunityId = communitySelect.value;
            const initialPropertyId = propertySelect.value;

            // 绑定小区选择变化事件
            communitySelect.addEventListener('change', function(event) {
                console.log('Community change event triggered!');
                BillForm.handleCommunityChange(event, propertySelect);
            });

            communitySelect.dataset.billEventBound = 'true';
            console.log('Event bound successfully');

            // 如果有初始选中的小区，加载其房产列表
            if (initialCommunityId) {
                console.log('Loading properties for initial community:', initialCommunityId);
                this.loadPropertiesForCommunity(initialCommunityId, propertySelect, initialPropertyId);
            } else {
                console.log('No initial community selected');
            }
        }, 200);
    },

    // 处理小区选择变化
    handleCommunityChange: function(event, propertySelect) {
        const communityId = event.target.value;
        console.log('=== Community changed to:', communityId, '===');

        if (!communityId) {
            propertySelect.innerHTML = '<option value="">请先选择小区</option>';
            propertySelect.required = false;
            return;
        }

        propertySelect.required = true;
        this.loadPropertiesForCommunity(communityId, propertySelect, null);
    },

    // 加载指定小区的房产列表
    loadPropertiesForCommunity: function(communityId, propertySelect, selectedPropertyId) {
        console.log('=== Loading properties for community:', communityId, '===');

        // 显示加载状态
        propertySelect.innerHTML = '<option value="">加载中...</option>';
        propertySelect.disabled = true;

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
                console.log('API returned:', data.properties ? data.properties.length : 0, 'properties');
                console.log('First property data:', data.properties ? data.properties[0] : 'No results');

                propertySelect.innerHTML = '<option value="">请选择房产</option>';
                propertySelect.disabled = false;
                propertySelect.required = true;

                // API返回的数据在properties字段中
                const properties = data.properties || [];

                if (Array.isArray(properties) && properties.length > 0) {
                    let selectedFound = false;

                    properties.forEach(prop => {
                        const option = document.createElement('option');
                        option.value = prop.id;
                        // 使用full_address作为显示文本
                        const address = prop.full_address || prop.name || `房产${prop.id}`;
                        option.textContent = address;
                        // 保存community_id
                        option.dataset.communityId = communityId;

                        // 如果有指定的房产ID，设置选中
                        if (selectedPropertyId && prop.id === selectedPropertyId) {
                            option.selected = true;
                            selectedFound = true;
                            console.log('Selected property:', address);
                        }

                        propertySelect.appendChild(option);
                    });

                    console.log('Property select updated. Total options:', propertySelect.options.length);
                } else {
                    console.log('No properties found for community:', communityId);
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

    // 处理账单状态变更
    onStatusChange: function(selectElement) {
        const billId = selectElement.dataset.billId;
        const newStatus = selectElement.value;

        console.log('=== Bill Status Change ===');
        console.log('Bill ID:', billId);
        console.log('New Status:', newStatus);

        // 显示/隐藏支付方式下拉框
        const paymentMethodContainer = document.getElementById(`payment-method-container-${billId}`);
        if (newStatus === 'paid' || newStatus === 'partial') {
            paymentMethodContainer.style.display = 'block';
        } else {
            paymentMethodContainer.style.display = 'none';
            // 清空支付方式选择
            const paymentMethodSelect = paymentMethodContainer.querySelector('.bill-payment-method-select');
            if (paymentMethodSelect) {
                paymentMethodSelect.value = '';
            }
        }

        // 更新状态到后端
        this.updateBillStatus(billId, newStatus, selectElement);
    },

    // 更新账单状态到后端
    updateBillStatus: function(billId, status, selectElement) {
        console.log('=== updateBillStatus ===');
        console.log('Bill ID:', billId);
        console.log('New Status:', status);

        // 获取CSRF token（从cookie中获取）
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        const csrfToken = getCookie('csrftoken');
        console.log('CSRF Token:', csrfToken ? 'Found' : 'Not found');

        fetch(`/admin/api/bills/${billId}/update-status/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                status: status
            }),
            credentials: 'same-origin'
        })
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data);
            if (data.success) {
                console.log('Status updated successfully');
                // 更新下拉框背景色
                this.updateStatusSelectColor(selectElement, status);
                // 保存当前状态到dataset，用于错误恢复
                selectElement.dataset.originalStatus = status;
            } else {
                console.error('Update failed:', data.error);
                alert('更新失败：' + (data.error || '未知错误'));
                // 恢复原状态
                const originalStatus = selectElement.dataset.originalStatus || 'unpaid';
                selectElement.value = originalStatus;
            }
        })
        .catch(error => {
            console.error('Error updating status:', error);
            alert('更新失败：网络错误');
            // 恢复原状态
            const originalStatus = selectElement.dataset.originalStatus || 'unpaid';
            selectElement.value = originalStatus;
        });
    },

    // 处理支付方式变更
    onPaymentMethodChange: function(selectElement) {
        const billId = selectElement.dataset.billId;
        const paymentMethod = selectElement.value;

        console.log('=== Payment Method Change ===');
        console.log('Bill ID:', billId);
        console.log('Payment Method:', paymentMethod);

        if (!paymentMethod) {
            return; // 没有选择支付方式，不更新
        }

        // 更新支付方式到后端
        this.updatePaymentMethod(billId, paymentMethod);
    },

    // 更新支付方式到后端
    updatePaymentMethod: function(billId, paymentMethod) {
        console.log('=== updatePaymentMethod ===');
        console.log('Bill ID:', billId);
        console.log('Payment Method:', paymentMethod);

        // 获取CSRF token（从cookie中获取）
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        const csrfToken = getCookie('csrftoken');
        console.log('CSRF Token:', csrfToken ? 'Found' : 'Not found');

        fetch(`/admin/api/bills/${billId}/update-payment-method/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                payment_method: paymentMethod
            }),
            credentials: 'same-origin'
        })
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data);
            if (data.success) {
                console.log('Payment method updated successfully');
            } else {
                console.error('Update failed:', data.error);
                alert('更新支付方式失败：' + (data.error || '未知错误'));
            }
        })
        .catch(error => {
            console.error('Error updating payment method:', error);
            alert('更新支付方式失败：网络错误');
        });
    },

    // 更新状态选择框的颜色
    updateStatusSelectColor: function(selectElement, status) {
        // 根据状态设置背景色
        const colorMap = {
            'paid': { bg: 'var(--success-light)', color: 'var(--success)' },
            'partial': { bg: 'var(--warning-light)', color: 'var(--warning)' },
            'overdue': { bg: 'var(--error-light)', color: 'var(--error)' },
            'unpaid': { bg: 'var(--gray-100)', color: 'var(--gray-600)' }
        };

        const colors = colorMap[status] || colorMap['unpaid'];
        selectElement.style.backgroundColor = colors.bg;
        selectElement.style.color = colors.color;
    }
};
