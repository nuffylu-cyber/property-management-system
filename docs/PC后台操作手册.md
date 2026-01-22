# 物业管理系统 - PC后台操作手册

## 目录
1. [系统安装和启动](#1-系统安装和启动)
2. [登录系统](#2-登录系统)
3. [小区和楼栋管理](#3-小区和楼栋管理)
4. [房产管理](#4-房产管理)
5. [业主管理](#5-业主管理)
6. [租户管理](#6-租户管理)
7. [费率标准管理](#7-费率标准管理)
8. [账单管理](#8-账单管理)
9. [缴费记录查询](#9-缴费记录查询)
10. [报事管理](#10-报事管理)
11. [用户和权限管理](#11-用户和权限管理)
12. [数据统计](#12-数据统计)

---

## 1. 系统安装和启动

### 1.1 Windows 系统

#### 步骤1：安装 Python
1. 访问 https://www.python.org/downloads/
2. 下载 Python 3.11.x 安装包
3. 运行安装程序，**务必勾选 "Add Python to PATH"**
4. 点击 "Install Now" 完成安装

#### 步骤2：验证安装
打开命令提示符（CMD）或 PowerShell：
```bash
python --version
```
应显示：Python 3.11.x

#### 步骤3：安装 PostgreSQL
1. 访问 https://www.postgresql.org/download/windows/
2. 下载 PostgreSQL 15 安装包
3. 运行安装程序，设置密码（记住这个密码！）
4. 保持默认端口 5432
5. 完成安装

#### 步骤4：安装 Git（可选）
1. 访问 https://git-scm.com/download/win
2. 下载并安装

#### 步骤5：获取项目代码
```bash
# 如果有 Git
git clone <repository-url>
cd 物业管理系统

# 或者直接解压项目压缩包
```

#### 步骤6：创建虚拟环境
```bash
# 在项目目录下
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate
```

#### 步骤7：安装依赖
```bash
pip install --upgrade pip
pip install -r requirements/development.txt
```

#### 步骤8：配置环境变量
```bash
# 复制配置文件
copy .env.example .env

# 编辑 .env 文件（使用记事本或VS Code）
notepad .env
```

编辑 `.env` 文件内容：
```env
# Django 配置
SECRET_KEY=django-insecure-change-this-to-random-string-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=config.settings.development

# 数据库配置
DB_ENGINE=django.db.backends.postgresql
DB_NAME=property_management
DB_USER=postgres
DB_PASSWORD=你安装PostgreSQL时设置的密码
DB_HOST=localhost
DB_PORT=5432

# 其他配置保持默认即可
SITE_URL=http://localhost:8000
```

#### 步骤9：创建数据库
打开 pgAdmin（PostgreSQL 的管理工具）：
1. 点击 pgAdmin 图标启动
2. 输入密码登录
3. 右键 "Databases" -> "Create" -> "Database"
4. 输入数据库名：`property_management`
5. 点击 "Save"

或使用命令行：
```bash
# 打印 SQL Shell (psql)
cd "C:\Program Files\PostgreSQL\15\bin"
psql -U postgres

# 在 psql 中执行
CREATE DATABASE property_management;
\q
```

#### 步骤10：数据库迁移
```bash
# 确保虚拟环境已激活
python manage.py makemigrations
python manage.py migrate
```

#### 步骤11：创建管理员账号
```bash
python manage.py createsuperuser
```
按提示输入：
- 用户名：`admin`
- 邮箱：`admin@example.com`
- 密码：设置一个强密码（至少8位）
- 确认密码

#### 步骤12：启动系统
```bash
python manage.py runserver
```

看到以下输出表示成功：
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### 1.2 快速启动（后续使用）

每次使用时：
```bash
# 1. 打开命令提示符，进入项目目录
cd D:\claude code\物业管理系统

# 2. 激活虚拟环境
venv\Scripts\activate

# 3. 启动服务器
python manage.py runserver
```

---

## 2. 登录系统

### 2.1 访问后台
打开浏览器（推荐 Chrome、Edge），访问：
```
http://localhost:8000/admin
```

### 2.2 登录
输入刚创建的管理员账号：
- 用户名：`admin`
- 密码：（您设置的密码）

点击 **"登录"** 按钮

### 2.3 后台界面概览
登录后看到主界面，包含以下模块：
- **认证和授权**（用户、用户组）
- **核心模块**（用户、操作日志、系统配置）
- **小区管理**（小区、楼栋）
- **房产管理**（房产、业主、租户）
- **缴费管理**（费率标准、账单、缴费记录）
- **报事管理**（报事记录、处理日志）
- **微信用户**（微信用户、消息记录）

---

## 3. 小区和楼栋管理

### 3.1 创建小区

**步骤：**
1. 点击左侧菜单 **"小区管理"** → **"小区s"**
2. 点击右上角 **"+ 增加"** 按钮
3. 填写信息：
   ```
   小区名称：银座小区
   小区地址：XX市XX区XX街道1号
   总户数：413
   开发商：（选填）
   物业公司：（选填）
   小区描述：（选填）
   ```
4. 点击 **"保存"** 按钮

**批量创建小区示例：**
重复以上步骤创建第二个小区：
- 小区名称：锦尚名都小区
- 总户数：812

### 3.2 创建楼栋

**步骤：**
1. 点击 **"小区管理"** → **"楼栋s"**
2. 点击 **"+ 增加"**
3. 填写信息：
   ```
   所属小区：选择"银座小区"
   楼栋号：1栋
   楼栋类型：选择"高层"
   总楼层数：32
   单元数：2
   楼栋描述：（选填）
   ```
4. 点击 **"保存"**

**批量创建楼栋：**
为每个小区创建多个楼栋：
- 1栋、2栋、3栋... 根据实际情况创建

---

## 4. 房产管理

### 4.1 创建房产

**步骤：**
1. 点击 **"房产管理"** → **"房产s"**
2. 点击 **"+ 增加"**
3. 填写信息：
   ```
   所属小区：银座小区
   所属楼栋：1栋
   单元号：1单元
   楼层：1
   房号：101
   面积：89.5
   房产类型：住宅
   状态：空置
   ```
4. 点击 **"保存"**

**批量导入建议：**
由于房产数量较多，建议开发 Excel 导入功能后批量导入。

**房产编号规则：**
- 房号格式：楼层+房号（如：1楼101室 = 101）
- 单元号：如有多单元，填写"1单元"、"2单元"

### 4.2 查看房产列表
1. 在房产列表页面可以：
   - 搜索房号
   - 按小区、楼栋、类型、状态筛选
   - 查看完整地址
   - 查看当前业主

---

## 5. 业主管理

### 5.1 创建业主

**步骤：**
1. 点击 **"房产管理"** → **"业主s"**
2. 点击 **"+ 增加"**
3. 填写信息：
   ```
   业主姓名：张三
   联系电话：13800138000
   身份证号：110101199001011234
   是否已认证：勾选
   ```
4. 点击 **"保存"**

### 5.2 关联房产

业主创建后，需要关联房产：

**方法1：在房产列表中关联**
1. 进入 **"房产s"** 列表
2. 点击要关联的房产（如：银座小区-1栋-1单元-1-101）
3. 在页面中找到业主关联区域
4. 选择业主，设置所有权类型和比例
5. 保存

**方法2：创建业主时直接关联**
需要通过 Python shell 或开发批量关联功能

### 5.3 批量导入业主数据

**使用 Excel 导入（需要先开发此功能）：**

准备 Excel 文件格式：
```
| 姓名      | 电话         | 身份证号               | 小区     | 楼栋 | 单元 | 楼层 | 房号 |
|-----------|-------------|------------------------|----------|------|------|------|------|
| 张三      | 13800138000 | 110101199001011234     | 银座小区 | 1栋  | 1单元 | 1    | 101  |
| 李四      | 13900139000 | 110101199002022345     | 银座小区 | 1栋  | 1单元 | 1    | 102  |
```

**临时方法：使用 Python Shell**
```bash
python manage.py shell
```

```python
from apps.property.models import Owner, Property, OwnerProperty
from apps.community.models import Building

# 创建业主
owner = Owner.objects.create(
    name='张三',
    phone='13800138000',
    id_card='110101199001011234',
    is_verified=True
)

# 查找房产
property = Property.objects.get(
    building__name='1栋',
    unit='1单元',
    floor=1,
    room_number='101'
)

# 关联业主和房产
OwnerProperty.objects.create(
    owner=owner,
    property=property,
    ownership_type='full'
)

print(f"业主 {owner.name} 创建成功并关联房产")
```

### 5.4 查看业主信息
1. 在业主列表页面可以：
   - 搜索业主姓名、电话、身份证
   - 查看业主的所有房产
   - 查看是否已认证
   - 查看微信绑定状态

---

## 6. 租户管理

### 6.1 创建租户

**步骤：**
1. 点击 **"房产管理"** → **"租户s"**
2. 点击 **"+ 增加"**
3. 填写信息：
   ```
   租户姓名：王五
   联系电话：13700137000
   身份证号：110101199003033456
   租赁房产：选择已出租的房产
   租赁开始日期：2024-01-01
   租赁结束日期：2024-12-31
   是否有效：勾选
   ```
4. 点击 **"保存"**

**注意事项：**
- 只有已出租状态的房产才能添加租户
- 租赁到期后需要更新"是否有效"状态

---

## 7. 费率标准管理

### 7.1 创建物业费标准

**步骤：**
1. 点击 **"缴费管理"** → **"物业费标准s"**
2. 点击 **"+ 增加"**
3. 填写信息：
   ```
   所属小区：银座小区
   费用名称：住宅物业费
   费用类型：物业费
   每平米单价：2.5
   计费周期：按月
   费用说明：住宅物业费，每平方米2.5元/月
   是否启用：勾选
   ```
4. 点击 **"保存"**

### 7.2 创建其他费率标准

示例费用类型：
- **公摊电费**：每平米0.5元/月
- **水费**：按吨计算（阶梯计价）
- **停车费**：每月200元/车位
- **装修管理费**：一次性收取

**不同房产类型的费率：**
- 住宅物业费：2.5元/㎡/月
- 商业物业费：5元/㎡/月
- 车库物业费：1元/㎡/月

---

## 8. 账单管理

### 8.1 批量生成账单

**步骤：**
1. 点击 **"缴费管理"** → **"缴费账单s"**
2. 点击右上角 **"批量创建"** 按钮（在API接口中，前端需要调用）
3. 或使用 Python Shell：

```bash
python manage.py shell
```

```python
from apps.payment.models import FeeStandard, PaymentBill
from apps.property.models import Property
from datetime import date
import uuid

# 获取费率标准
fee_standard = FeeStandard.objects.filter(
    community__name='银座小区',
    fee_type='property',
    is_active=True
).first()

# 获取所有房产
properties = Property.objects.filter(community__name='银座小区')

# 批量生成2024年1月账单
billing_period = '2024-01'
due_date = date(2024, 1, 31)

created_count = 0
for prop in properties:
    # 检查是否已有账单
    if PaymentBill.objects.filter(
        property=prop,
        fee_type='property',
        billing_period=billing_period
    ).exists():
        continue

    # 获取业主
    owner_relation = prop.owners.first()
    if not owner_relation:
        continue

    # 计算金额
    amount = prop.area * fee_standard.price_per_square

    # 生成账单
    PaymentBill.objects.create(
        bill_number=f"{billing_period.replace('-', '')}{str(uuid.uuid4().int)[:6]}",
        community=prop.community,
        property=prop,
        owner=owner_relation.owner,
        fee_type='property',
        billing_period=billing_period,
        amount=amount,
        due_date=due_date
    )
    created_count += 1

print(f"成功生成 {created_count} 条账单")
```

### 8.2 查看和筛选账单

1. 在账单列表页面可以：
   - 按小区、房产、业主、费用类型、状态、账期筛选
   - 搜索账单编号、房号、业主姓名
   - 查看应收、已收、未收金额
   - 查看缴费状态

### 8.3 单个创建账单

**步骤：**
1. 点击 **"缴费管理"** → **"缴费账单s"**
2. 点击 **"+ 增加"**
3. 填写信息：
   ```
   账单编号：系统自动生成
   所属小区：银座小区
   房产：选择具体房产
   业主：自动填充
   费用类型：物业费
   账期：2024-01
   应缴金额：223.75
   应缴日期：2024-01-31
   备注：1月份物业费
   ```
4. 点击 **"保存"**

### 8.4 手动修改账单状态

当业主线下缴费后，需要手动更新账单状态：

**步骤：**
1. 在账单列表找到对应账单
2. 点击账单编号进入详情页
3. 修改以下信息：
   ```
   已缴金额：223.75
   状态：已缴
   缴费时间：选择当前时间
   ```
4. 点击 **"保存"**

---

## 9. 缴费记录查询

### 9.1 查看所有缴费记录

**步骤：**
1. 点击 **"缴费管理"** → **"缴费记录s"**
2. 可以筛选：
   - 按账单
   - 按状态（成功/退款/失败）
   - 按支付方式（微信/支付宝/现金）
3. 搜索：
   - 微信交易号
   - 商户订单号
   - 缴费人姓名

### 9.2 导出缴费记录

**方法1：使用 Django Admin 导出功能**
1. 在缴费记录列表页面
2. 勾选要导出的记录
3. 选择操作（Action）：导出为 CSV/Excel

**方法2：使用 Python Shell**
```python
import csv
from apps.payment.models import PaymentRecord

# 查询记录
records = PaymentRecord.objects.filter(
    payment_time__month=1,  # 1月份
    status='success'
)

# 导出CSV
with open('payment_records_jan.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['交易号', '账单号', '缴费人', '金额', '支付方式', '支付时间'])
    for record in records:
        writer.writerow([
            record.transaction_id,
            record.bill.bill_number,
            record.payer,
            record.amount,
            record.get_payment_method_display(),
            record.payment_time
        ])
```

---

## 10. 报事管理

### 10.1 查看报事记录

**步骤：**
1. 点击 **"报事管理"** → **"报事记录s"**
2. 可以看到所有业主提交的报事
3. 筛选条件：
   - 按小区、房产
   - 按类别（电工、水工、土木等）
   - 按状态（待派单、已派单、处理中、已完成）
   - 按优先级（一般、紧急、非常紧急）

### 10.2 派单处理

**步骤：**
1. 找到状态为"待派单"的报事记录
2. 点击进入详情页
3. 修改信息：
   ```
   状态：已派单
   指派给：电工张三
   派单时间：自动填充
   ```
4. 点击 **"保存"**

**或者通过 API 操作：**
```bash
# 使用 curl 或 Postman
curl -X POST http://localhost:8000/api/maintenance/requests/{id}/assign/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"assigned_to": "电工张三"}'
```

### 10.3 更新处理进度

**开始处理：**
1. 找到已派单的报事
2. 修改状态为"处理中"
3. 填写"开始处理时间"
4. 保存

**完成处理：**
1. 修改状态为"已完成"
2. 填写"处理结果说明"
3. 上传"处理结果图片"（如果有）
4. 保存

### 10.4 查看处理日志

1. 进入报事详情页
2. 滚动到"报事处理日志"区域
3. 可以看到所有操作记录：
   - 报事创建时间
   - 派单信息
   - 处理进度
   - 完成时间

### 10.5 查看业主评价

1. 找到已完成的报事
2. 在详情页可以查看：
   - 评分（1-5星）
   - 业主反馈意见

---

## 11. 用户和权限管理

### 11.1 创建管理员账号

**步骤：**
1. 点击左侧 **"核心模块"** → **"用户s"**
2. 点击 **"+ 增加"**
3. 填写信息：
   ```
   用户名：finance01
   邮箱：finance01@example.com
   密码：设置密码
   确认密码：再次输入
   联系电话：13900139000
   角色：财务
   活跃状态：勾选
   ```
4. 点击 **"保存"**

### 11.2 创建前台账号

重复上述步骤，选择角色为"前台"：
- 用户名：reception01
- 角色：前台

### 11.3 权限说明

| 角色 | 权限范围 |
|------|----------|
| 超级管理员 | 全部权限 |
| 财务 | 费率标准、账单管理、缴费记录、数据统计 |
| 前台 | 报事管理、业主信息查询、房产查询 |

### 11.4 修改密码

**方法1：管理员重置**
1. 进入用户列表
2. 点击用户名
3. 滚动到"密码"区域
4. 输入新密码
5. 保存

**方法2：用户自行修改**
需要开发用户自助修改密码功能

---

## 12. 数据统计

### 12.1 查看缴费统计

**通过 API：**
```bash
curl -X GET http://localhost:8000/api/payment/bills/statistics/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**返回数据示例：**
```json
{
  "total_bills": 1225,
  "total_amount": 245000.00,
  "total_paid": 180000.00,
  "total_unpaid": 65000.00,
  "unpaid_count": 325,
  "paid_count": 900
}
```

### 12.2 查看报事统计

**使用 Django Admin：**
1. 进入报事记录列表
2. 右侧有筛选器
3. 可以看到各状态的报事数量

**通过 Python Shell：**
```python
from apps.maintenance.models import MaintenanceRequest

# 按状态统计
from django.db.models import Count
stats = MaintenanceRequest.objects.values('status').annotate(
    count=Count('id')
)

for stat in stats:
    print(f"{stat['status']}: {stat['count']}")

# 按类别统计
category_stats = MaintenanceRequest.objects.values('category').annotate(
    count=Count('id')
)

for stat in category_stats:
    print(f"{stat['category']}: {stat['count']}")
```

---

## 13. 常见操作场景

### 场景1：每月初批量生成账单

**时间：每月7号左右（收到供电局费用单后）**

**操作步骤：**
1. 计算本月公摊电费
2. 创建/更新公摊电费费率标准
3. 使用 Python Shell 批量生成账单
4. 检查生成的账单数量和金额
5. 导出账单列表供核对

### 场景2：业主通过微信缴费

**流程：**
1. 业主关注微信公众号
2. 点击菜单"我的服务"
3. 微信授权登录
4. 绑定业主身份（输入姓名、身份证、房号）
5. 查看账单
6. 选择账单，微信支付
7. 系统自动更新账单状态
8. 业主收到缴费成功通知

**后台操作：**
- 在缴费记录中查看交易
- 核实金额和状态

### 场景3：业主报事处理

**流程：**
1. 业主通过微信公众号提交报事
2. 前台收到通知（或在后台查看）
3. 前台派单给维修人员（通过微信群或电话）
4. 维修人员处理并拍照
5. 前台上传处理结果
6. 业主查看处理结果
7. 业主评价服务

**后台操作：**
- 查看报事记录
- 更新状态和派单信息
- 上传处理结果
- 查看业主评价

### 场景4：新业主入住

**操作步骤：**
1. 创建业主信息
2. 关联房产
3. 更新房产状态为"自住"或"出租"
4. 如为出租，创建租户信息
5. 通知业主绑定微信公众号

### 场景5：房产过户

**操作步骤：**
1. 查找到对应房产
2. 解除原业主关联（或保留作为历史记录）
3. 创建新业主信息
4. 关联房产
5. 更新房产状态

---

## 14. 常见问题解决

### 问题1：无法启动系统

**检查：**
1. PostgreSQL 是否运行
2. 数据库是否创建
3. .env 配置是否正确
4. 虚拟环境是否激活

**解决方法：**
```bash
# 检查 PostgreSQL
# Windows: 打开服务管理器，查看 postgresql-xxx-15 服务

# 重新迁移数据库
python manage.py migrate

# 查看错误日志
python manage.py runserver --verbosity=2
```

### 问题2：忘记管理员密码

**解决方法：**
```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='admin')
user.set_password('新密码')
user.save()
print("密码已重置")
```

### 问题3：账单生成失败

**检查：**
1. 费率标准是否已创建且启用
2. 房产是否已关联业主
3. 该账期是否已存在账单

**解决方法：**
- 先创建费率标准
- 确保房产已关联业主
- 检查日志错误信息

### 问题4：图片上传失败

**检查：**
1. media 目录是否存在且有写权限
2. 文件大小是否超过限制（默认100MB）

**解决方法：**
```bash
# 创建 media 目录
mkdir media
# Windows: mkdir media

# 检查权限
# 右键 media 文件夹 -> 属性 -> 安全
```

---

## 15. 快捷操作技巧

### 15.1 使用书签快速访问

将以下链接添加到浏览器书签：
- 后台首页：`http://localhost:8000/admin`
- 账单管理：`http://localhost:8000/admin/payment/paymentbill/`
- 报事管理：`http://localhost:8000/admin/maintenance/maintenancerequest/`

### 15.2 使用筛选器快速查找

常用筛选组合：
- 查看本月未缴账单：状态=未缴，账期=2024-01
- 查看待处理报事：状态=待派单 或 已派单
- 查看特定小区：所属小区=银座小区

### 15.3 批量操作

在列表页面：
1. 勾选多条记录
2. 选择操作（下拉菜单）
3. 点击执行

---

## 16. 系统维护

### 16.1 数据备份

**备份数据库：**
```bash
# Windows
cd "C:\Program Files\PostgreSQL\15\bin"
pg_dump -U postgres property_management > backup.sql

# 或使用 pgAdmin 右键数据库 -> Backup
```

**恢复数据库：**
```bash
psql -U postgres property_management < backup.sql
```

### 16.2 查看操作日志

1. 点击 **"核心模块"** → **"操作日志s"**
2. 可以看到所有用户的操作记录
3. 用于审计和问题追踪

### 16.3 清理旧数据

**清理过期日志：**
```python
from django.utils import timezone
from datetime import timedelta
from apps.core.models import OperationLog

# 删除6个月前的日志
six_months_ago = timezone.now() - timedelta(days=180)
OperationLog.objects.filter(created_at__lt=six_months_ago).delete()
```

---

## 17. 联系支持

如遇到问题：
1. 查看本文档
2. 查看 `docs/开发指南.md`
3. 查看 API 文档：`http://localhost:8000/swagger/`
4. 联系开发团队

---

## 附录A：键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl + S | 保存当前表单 |
| Esc | 取消并返回 |
| Ctrl + F | 搜索（列表页） |
| Ctrl + Shift + F | 高级搜索 |

## 附录B：常用数据字典

### 费用类型
- property：物业费
- public_electric：公摊电费
- water：水费
- parking：停车费
- other：其他

### 账单状态
- unpaid：未缴
- partial：部分缴
- paid：已缴
- overdue：逾期

### 报事类别
- electric：电工
- plumbing：水工
- civil：土木
- elevator：电梯
- cleaning：清洁
- security：安保
- other：其他

### 报事状态
- pending：待派单
- assigned：已派单
- processing：处理中
- completed：已完成
- closed：已关闭

### 用户角色
- admin：超级管理员
- finance：财务
- receptionist：前台
- owner：业主
- tenant：租户
