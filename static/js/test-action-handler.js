/**
 * Action参数处理器 - 用于调试
 * 在页面加载后立即执行
 */

console.log('[Action Handler] Script loaded');

// 立即检查URL参数
const urlParams = new URLSearchParams(window.location.search);
const action = urlParams.get('action');
const tab = urlParams.get('tab');

console.log('[Action Handler] Current URL:', window.location.href);
console.log('[Action Handler] Tab parameter:', tab);
console.log('[Action Handler] Action parameter:', action);

// 在DOMContentLoaded后处理
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        console.log('[Action Handler] DOMContentLoaded fired');
        handleAction();
    });
} else {
    console.log('[Action Handler] DOM already loaded');
    setTimeout(handleAction, 100);
}

function handleAction() {
    const currentPath = window.location.pathname;

    console.log('[Action Handler] Current path:', currentPath);
    console.log('[Action Handler] typeof BillCRUD:', typeof BillCRUD);
    console.log('[Action Handler] typeof OwnerCRUD:', typeof OwnerCRUD);
    console.log('[Action Handler] typeof UniversalCRUD:', typeof UniversalCRUD);

    if (currentPath === '/admin/payment/') {
        console.log('[Action Handler] Processing payment page action:', action);

        if (action === 'add') {
            console.log('[Action Handler] Action is "add", checking BillCRUD...');

            if (typeof BillCRUD !== 'undefined') {
                console.log('[Action Handler] BillCRUD is defined');
                console.log('[Action Handler] typeof BillCRUD.addBill:', typeof BillCRUD.addBill);

                if (typeof BillCRUD.addBill === 'function') {
                    console.log('[Action Handler] ✓ Calling BillCRUD.addBill()');

                    // 先切换标签页
                    if (tab === 'bills') {
                        const tabElement = document.querySelector(`.tab[onclick*="switchTab(this, 'bills')"]`);
                        if (tabElement) {
                            console.log('[Action Handler] Switching to bills tab');
                            tabElement.click();
                        }
                    }

                    // 延迟执行新增操作
                    setTimeout(function() {
                        console.log('[Action Handler] Executing addBill now...');
                        try {
                            BillCRUD.addBill();
                            console.log('[Action Handler] ✓ BillCRUD.addBill() called successfully');
                        } catch (e) {
                            console.error('[Action Handler] ✗ Error calling addBill:', e);
                        }
                    }, 500);
                } else {
                    console.error('[Action Handler] ✗ BillCRUD.addBill is not a function');
                }
            } else {
                console.error('[Action Handler] ✗ BillCRUD is undefined');
            }
        }
    } else if (currentPath === '/admin/property/') {
        console.log('[Action Handler] Processing property page action:', action);

        if (action === 'add') {
            console.log('[Action Handler] Action is "add", checking OwnerCRUD...');

            if (typeof OwnerCRUD !== 'undefined') {
                console.log('[Action Handler] OwnerCRUD is defined');
                console.log('[Action Handler] typeof OwnerCRUD.addOwner:', typeof OwnerCRUD.addOwner);

                if (typeof OwnerCRUD.addOwner === 'function') {
                    console.log('[Action Handler] ✓ Calling OwnerCRUD.addOwner()');

                    // 先切换标签页
                    if (tab === 'owners') {
                        const tabElement = document.querySelector(`.tab[onclick*="switchTab(this, 'owners')"]`);
                        if (tabElement) {
                            console.log('[Action Handler] Switching to owners tab');
                            tabElement.click();
                        }
                    }

                    // 延迟执行新增操作
                    setTimeout(function() {
                        console.log('[Action Handler] Executing addOwner now...');
                        try {
                            OwnerCRUD.addOwner();
                            console.log('[Action Handler] ✓ OwnerCRUD.addOwner() called successfully');
                        } catch (e) {
                            console.error('[Action Handler] ✗ Error calling addOwner:', e);
                        }
                    }, 500);
                } else {
                    console.error('[Action Handler] ✗ OwnerCRUD.addOwner is not a function');
                }
            } else {
                console.error('[Action Handler] ✗ OwnerCRUD is undefined');
            }
        }
    } else if (currentPath === '/admin/maintenance/') {
        console.log('[Action Handler] Processing maintenance page action:', action);

        if (action === 'dispatch') {
            console.log('[Action Handler] Action is "dispatch"');

            // 先切换标签页
            if (tab === 'requests-list') {
                const tabElement = document.querySelector(`.tab[onclick*="switchTab(this, 'requests-list')"]`);
                if (tabElement) {
                    console.log('[Action Handler] Switching to requests-list tab');
                    tabElement.click();
                }
            }

            // 延迟执行筛选
            setTimeout(function() {
                console.log('[Action Handler] Applying dispatch filter...');
                const statusFilter = document.getElementById('request-filter-status');
                if (statusFilter) {
                    statusFilter.value = 'pending';
                    console.log('[Action Handler] ✓ Status filter set to pending');
                } else {
                    console.error('[Action Handler] ✗ Status filter not found');
                }
            }, 500);
        }
    }
}

// 导出处理函数供其他脚本使用
window.ActionHandler = {
    handleAction: handleAction
};

console.log('[Action Handler] Handler initialized');
