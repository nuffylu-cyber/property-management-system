/**
 * 小区管理页面脚本
 * 注意：所有CRUD操作已由 community-crud.js 处理
 * 此文件保留用于其他可能的功能扩展
 */

// 移除了所有按钮事件监听器，避免与 community-crud.js 冲突
// 新增、编辑、删除功能全部由模板中的 onclick="CommunityCRUD.xxx()" 调用

// 显示小区表单
async function showCommunityForm(id = null) {
    const url = id ? `/admin/forms/community/${id}/` : '/admin/forms/community/new/';
    const title = id ? '编辑小区' : '新增小区';

    showLoading('加载表单...');

    try {
        const response = await API.get(url);
        hideLoading();

        const modal = new Modal({
            title: title,
            content: response.html,
            size: 'md',
            onConfirm: async function() {
                const form = modal.querySelector('.ajax-form');
                if (!form) return false;

                // 创建FormData对象
                const formData = new FormData(form);
                showLoading('保存中...');

                try {
                    const result = await API.postForm(url, formData);
                    hideLoading();
                    Toast.success(result.message || '保存成功');
                    modal.close();

                    // 刷新页面
                    setTimeout(() => window.location.reload(), 1000);
                    return true;
                } catch (error) {
                    hideLoading();
                    if (error.errors) {
                        FormHelper.showErrors(form, error.errors);
                    }
                    return false;
                }
            }
        });

        modal.show();
    } catch (error) {
        hideLoading();
        Toast.error('加载表单失败');
    }
}

// 显示楼栋表单
async function showBuildingForm(id = null) {
    const url = id ? `/admin/forms/building/${id}/` : '/admin/forms/building/new/';
    const title = id ? '编辑楼栋' : '新增楼栋';

    showLoading('加载表单...');

    try {
        const response = await API.get(url);
        hideLoading();

        const modal = new Modal({
            title: title,
            content: response.html,
            size: 'md',
            onConfirm: async function() {
                const form = modal.querySelector('.ajax-form');
                if (!form) return false;

                // 创建FormData对象
                const formData = new FormData(form);
                showLoading('保存中...');

                try {
                    const result = await API.postForm(url, formData);
                    hideLoading();
                    Toast.success(result.message || '保存成功');
                    modal.close();

                    // 刷新页面
                    setTimeout(() => window.location.reload(), 1000);
                    return true;
                } catch (error) {
                    hideLoading();
                    if (error.errors) {
                        FormHelper.showErrors(form, error.errors);
                    }
                    return false;
                }
            }
        });

        modal.show();
    } catch (error) {
        hideLoading();
        Toast.error('加载表单失败');
    }
}

// 删除小区
async function deleteCommunity(id, name) {
    const confirmed = await confirmDelete(`确定要删除小区"${name}"吗？`);
    if (!confirmed) return;

    showLoading('删除中...');

    try {
        await API.delete(`/api/community/communities/${id}/`);  // 修复API路径
        hideLoading();
        Toast.success('删除成功');

        setTimeout(() => window.location.reload(), 1000);
    } catch (error) {
        hideLoading();
        console.error('删除失败:', error);
        Toast.error('删除失败: ' + (error.message || '未知错误'));
    }
}

// 删除楼栋
async function deleteBuilding(id, name) {
    const confirmed = await confirmDelete(`确定要删除楼栋"${name}"吗？`);
    if (!confirmed) return;

    showLoading('删除中...');

    try {
        await API.delete(`/api/community/buildings/${id}/`);
        hideLoading();
        Toast.success('删除成功');

        setTimeout(() => window.location.reload(), 1000);
    } catch (error) {
        hideLoading();
        Toast.error('删除失败');
    }
}
