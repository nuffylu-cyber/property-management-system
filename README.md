<img width="1915" height="906" alt="image" src="https://github.com/user-attachments/assets/c21ad8d2-87ee-4647-b7c2-fb3751b3772e" />

# 智慧物业管理系统

> **基于Django的现代化物业管理SaaS平台**
>
> **开发阶段**: 第一阶段已完成 ✅
> **版本**: v1.0
> **更新日期**: 2026-01-12

---

## 🎯 项目简介

智慧物业管理系统是一个功能完整的物业管理SaaS平台，提供社区、房产、缴费、报事等全方位管理功能，支持微信支付集成，具备完善的RBAC权限系统。

### 核心特性

- ✅ **多角色权限管理** - 支持7种用户角色，细粒度权限控制
- ✅ **完整的业务模块** - 社区房产、缴费管理、报事管理
- ✅ **微信支付集成** - 支持个人账号和企业对公账户
- ✅ **操作审计日志** - 完整记录所有用户操作
- ✅ **现代化界面** - 响应式设计，实时CRUD交互
- ✅ **RESTful API** - 前后端分离架构，支持多端接入
- ✅ **Docker部署** - 容器化部署，支持一键启动

---

## 🚀 快速开始

### 环境要求

- Python 3.11+
- PostgreSQL 13+ (生产环境)
- Redis 6+
- Nginx 1.18+

### 一键启动（Docker）

```bash
# 克隆项目
git clone <repository-url>
cd 物业管理系统

# 启动所有服务
docker-compose up -d

# 执行数据库迁移
docker-compose exec web python manage.py migrate

# 创建超级用户
docker-compose exec web python manage.py createsuperuser

# 访问系统
open http://localhost:8000/admin/
```

### 开发环境启动

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements/development.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件

# 数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 初始化权限数据
python manage.py init_permissions

# 启动开发服务器
python manage.py runserver
```

### 访问地址

- **管理后台**: http://localhost:8000/admin/
- **API文档**: http://localhost:8000/swagger/
- **ReDoc文档**: http://localhost:8000/redoc/

---

## 📚 文档导航

### ⭐ 必读文档（第一阶段完成）

| 文档 | 说明 | 适用对象 |
|------|------|---------|
| **[DOCS_INDEX.md](DOCS_INDEX.md)** | 📖 完整文档索引 | 所有人员 |
| **[PHASE1_SUMMARY.md](PHASE1_SUMMARY.md)** | 第一阶段完整总结 | 项目经理、开发人员 |
| **[PHASE2_START_GUIDE.md](PHASE2_START_GUIDE.md)** | 第二阶段快速指南 | 开发人员 |
| **[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md)** | 技术架构详解 | 架构师、后端开发 |
| **[CLEANUP_LOG.md](CLEANUP_LOG.md)** | 代码清理日志 | 项目维护 |

### 快速链接

- 🎯 **新加入成员**: 先读 [PHASE2_START_GUIDE.md](PHASE2_START_GUIDE.md)
- 📊 **了解项目**: 查看 [PHASE1_SUMMARY.md](PHASE1_SUMMARY.md)
- 🏗️ **技术架构**: 阅读 [PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md)
- 🔧 **开发调试**: 参考 [PHASE2_START_GUIDE.md - 调试技巧](PHASE2_START_GUIDE.md#调试技巧)

---

## 📖 项目概览

### 技术栈

```
后端:  Django 4.2.7 + Django REST Framework 3.14
数据库: SQLite (开发) / PostgreSQL (生产)
缓存:  Redis
任务队列: Celery 5.3
前端: HTML5 + CSS3 + JavaScript
认证: JWT + Session
部署: Docker + Docker Compose + Nginx
```

### 功能模块

| 模块 | 功能点 | 状态 |
|------|--------|------|
| 用户管理 | 7种角色、权限控制、操作日志 | ✅ 100% |
| 社区管理 | 社区信息、楼栋管理 | ✅ 100% |
| 房产管理 | 房产、业主、租户管理 | ✅ 100% |
| 缴费管理 | 费用标准、账单、缴费记录 | ✅ 100% |
| 报事管理 | 报事申请、工单处理 | ✅ 100% |
| 微信集成 | 公众号对接、消息处理 | ✅ 100% |
| 权限系统 | RBAC权限控制 | ✅ 100% |
| 支付配置 | 微信支付配置 | ✅ 100% |

### 项目统计

```
Django应用: 6个
数据模型: 18个
API接口: 50+ 个
代码行数: 6,894 行
HTML模板: 23 个
JavaScript: 9 个文件
开发时间: 2个月
```

---

## 🗂️ 项目结构

```
物业管理系统/
├── apps/                      # Django应用
│   ├── core/                  # 核心模块（用户、权限、日志）
│   ├── community/             # 社区管理
│   ├── property/              # 房产管理
│   ├── payment/               # 缴费管理
│   ├── maintenance/           # 报事管理
│   └── wechat/                # 微信集成
├── config/                    # 配置文件
├── templates/                 # HTML模板
├── static/                    # 静态文件（CSS、JS）
├── docs/                      # 文档目录
├── logs/                      # 日志文件
├── requirements/              # Python依赖
├── venv/                      # 虚拟环境
├── .env                       # 环境变量
├── Dockerfile                 # Docker配置
├── docker-compose.yml         # Docker Compose配置
└── manage.py                  # Django管理脚本
```

---

## 🎯 第一阶段成果

### 已完成功能

✅ **完整的用户权限系统**
- 7种用户角色（超级管理员、管理员、财务、前台、工程部、业主、租户）
- 基于角色的访问控制(RBAC)
- 操作日志审计
- 权限可视化配置

✅ **社区房产管理**
- 社区信息管理
- 楼栋管理
- 房产管理（支持多种类型）
- 业主管理（支持多房产）
- 租户管理

✅ **缴费管理**
- 费用标准配置
- 账单管理
- 缴费记录
- 多种支付方式

✅ **报事管理**
- 报事申请
- 工单处理流程
- 看板视图
- 统计分析

✅ **PC管理后台**
- 现代化UI设计
- 实时CRUD交互
- 搜索筛选功能
- 数据导出功能

✅ **微信集成**
- 公众号对接
- 消息处理
- 用户同步

✅ **技术架构**
- RESTful API
- Swagger文档
- Docker部署
- 日志系统

### 代码质量

- ✅ 遵循Django最佳实践
- ✅ 完整的API文档
- ✅ 代码结构清晰
- ✅ 注释详细
- ✅ 已清理临时文件
- ✅ 已优化代码结构

---

## 📋 第二阶段规划

### 业务流程对接

1. **缴费流程优化**
   - 自动生成月度账单
   - 微信支付对接
   - 缴费提醒功能
   - 逾期催缴流程

2. **报事流程优化**
   - 自动派单规则
   - 工程师评价系统
   - 报事统计分析
   - 满意度调查

3. **用户端功能**
   - 小程序端开发
   - 业主自助服务
   - 在线缴费
   - 报事进度查询

### 技术优化

- 性能优化（分页、缓存）
- 功能增强（批量操作、高级搜索）
- 系统集成（财务软件、门禁系统）

**详细规划**: 查看 [PHASE1_SUMMARY.md - 第二阶段规划](PHASE1_SUMMARY.md#第二阶段规划)

---

## 🛠️ 常用命令

```bash
# Django管理
python manage.py runserver              # 启动开发服务器
python manage.py migrate                 # 数据库迁移
python manage.py createsuperuser         # 创建超级用户
python manage.py collectstatic           # 收集静态文件
python manage.py shell                   # Django Shell

# 自定义命令
python manage.py init_permissions        # 初始化权限数据

# Docker
docker-compose up -d                     # 启动所有服务
docker-compose down                      # 停止服务
docker-compose logs -f web               # 查看日志

# Celery
celery -A config worker -l info          # 启动Worker
celery -A config beat -l info            # 启动Beat
```

---

## 📞 获取帮助

### 文档资源

- 📖 [完整文档索引](DOCS_INDEX.md)
- 🎯 [第二阶段快速指南](PHASE2_START_GUIDE.md)
- 📊 [第一阶段总结](PHASE1_SUMMARY.md)
- 🏗️ [项目架构文档](PROJECT_ARCHITECTURE.md)

### 常见问题

**Q: 项目无法启动？**
A: 检查环境变量配置，确保数据库迁移已完成

**Q: 权限错误？**
A: 运行 `python manage.py init_permissions` 初始化权限

**Q: 找不到某个文件？**
A: 参考 [DOCS_INDEX.md](DOCS_INDEX.md) 或 [PHASE2_START_GUIDE.md](PHASE2_START_GUIDE.md)

**Q: 如何添加新功能？**
A: 参考 [PHASE2_START_GUIDE.md - 开发工作流](PHASE2_START_GUIDE.md#开发工作流)

---

## 📄 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

---

## 👥 团队

- **项目负责人**: [您的名字]
- **技术架构**: Django + DRF
- **开发时间**: 2025年Q4 - 2026年1月

---

## 🎉 致谢

感谢所有为项目做出贡献的开发者！

---

**第一阶段开发完成** ✅
**准备好进入第二阶段开发** 🚀

> **提示**: 建议将 [DOCS_INDEX.md](DOCS_INDEX.md) 加入浏览器书签，方便快速查找文档！

- 📖 项目概述和开发历史
- 🏗️ 系统架构详细说明
- 🗄️ 完整的数据模型文档
- 🔌 所有API接口说明
- 💻 代码结构和规范
- 🔐 权限系统详解
- 🎯 下一步开发计划
- ⚡ 已知问题和优化建议

**适合**: 全面了解项目、新开发者入职、技术交接

#### 2. QUICK_REFERENCE.md
**快速参考指南**
- 🎯 项目当前状态
- 📂 关键文件位置
- 🗄️ 数据库模型速查
- 🔌 API端点速查表
- 🎨 前端组件速查
- 🔧 常用命令
- 📝 开发模板

**适合**: 日常开发、快速查阅、Claude Code参考

#### 3. PROJECT_CHECKLIST.md
**项目配置清单**
- ✅ 环境配置检查
- ⚙️ 系统配置说明
- 🗄️ 数据库配置
- 🔐 权限配置
- 🔌 API配置
- 🎨 前端配置
- 📋 功能模块状态
- 🚀 部署前检查清单

**适合**: 环境搭建、部署准备、项目检查

#### 4. OPTIMIZATION_SUMMARY.md
**优化总结文档**
- ✅ 已完成的优化内容
- 🔧 新增API接口说明
- 🔐 权限验证工具使用
- 📊 初始化数据说明
- 💡 使用指南
- 🎯 后续建议

**适合**: 了解最近的优化工作、使用新功能

---

## 🎯 按场景查找文档

### 场景1: 第一次接触项目
1. 阅读 `PROJECT_DEVELOPMENT_GUIDE.md` 的"项目概述"部分
2. 查看 `QUICK_REFERENCE.md` 的"项目当前状态"
3. 运行 `PROJECT_CHECKLIST.md` 中的"快速开始"命令

### 场景2: 开始新功能开发
1. 查看 `QUICK_REFERENCE.md` 的"开发模板"部分
2. 参考 `PROJECT_DEVELOPMENT_GUIDE.md` 的"代码结构"
3. 遵循 `PROJECT_DEVELOPMENT_GUIDE.md` 的"开发规范"

### 场景3: 修改权限系统
1. 阅读 `PROJECT_DEVELOPMENT_GUIDE.md` 的"权限系统"
2. 查看 `OPTIMIZATION_SUMMARY.md` 的权限初始化说明
3. 使用 `QUICK_REFERENCE.md` 的权限管理命令

### 场景4: 添加新的API
1. 参考 `QUICK_REFERENCE.md` 的"API端点速查"
2. 使用 `PROJECT_DEVELOPMENT_GUIDE.md` 的"添加新API端点"指南
3. 遵循 `PROJECT_DEVELOPMENT_GUIDE.md` 的"API文档规范"

### 场景5: 准备部署
1. 检查 `PROJECT_CHECKLIST.md` 的所有项目
2. 配置生产环境（参考"生产环境配置"）
3. 完成部署前检查清单

### 场景6: Claude AI继续开发
1. **首先阅读** `QUICK_REFERENCE.md`（快速了解项目）
2. **需要详情时** 查看 `PROJECT_DEVELOPMENT_GUIDE.md`
3. **检查配置** 使用 `PROJECT_CHECKLIST.md`

---

## 📂 项目文件结构

```
物业管理系统/
├── 📄 README.md                        # 本文档（文档索引）
├── 📄 PROJECT_DEVELOPMENT_GUIDE.md    # 完整开发文档（主文档）
├── 📄 QUICK_REFERENCE.md               # 快速参考指南
├── 📄 PROJECT_CHECKLIST.md             # 项目配置清单
├── 📄 OPTIMIZATION_SUMMARY.md          # 优化总结文档
│
├── 📁 apps/                             # 应用模块
├── 📁 config/                           # 项目配置
├── 📁 templates/                        # 模板文件
├── 📁 static/                           # 静态文件
├── 📁 media/                            # 媒体文件
├── 📁 logs/                             # 日志文件
├── 📁 venv/                             # 虚拟环境
│
├── 📄 manage.py                         # Django管理脚本
├── 📄 db.sqlite3                        # SQLite数据库
└── 📄 requirements.txt                  # 依赖包清单
```

---

## 🚀 快速开始

### 1. 环境准备
```bash
# 激活虚拟环境
venv\Scripts\activate  # Windows
# 或
source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库初始化
```bash
# 应用迁移
python manage.py migrate

# 初始化权限
python manage.py init_permissions

# 创建超级管理员
python manage.py createsuperuser
```

### 3. 启动服务器
```bash
python manage.py runserver
```

### 4. 访问系统
- 管理后台: http://127.0.0.1:8000/admin/
- API文档: http://127.0.0.1:8000/swagger/

---

## 📖 文档使用建议

### 给开发者
1. **开发前**: 阅读完整的 `PROJECT_DEVELOPMENT_GUIDE.md`
2. **开发中**: 使用 `QUICK_REFERENCE.md` 快速查阅
3. **提交前**: 检查 `PROJECT_DEVELOPMENT_GUIDE.md` 的"开发规范"

### 给Claude AI
1. **首次接手**: 先读 `QUICK_REFERENCE.md` 了解项目概况
2. **开发任务**: 参考 `QUICK_REFERENCE.md` 的"开发模板"和"常用命令"
3. **深入理解**: 查看 `PROJECT_DEVELOPMENT_GUIDE.md` 获取详细信息

---

## 🎯 开发工作流

```
┌─────────────────────────────────────────┐
│         1. 阅读文档                     │
│    - QUICK_REFERENCE.md (快速)         │
│    - PROJECT_DEVELOPMENT_GUIDE.md (详细)│
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         2. 理解需求                     │
│    - 功能模块                           │
│    - API接口                            │
│    - 权限要求                           │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         3. 开发实现                     │
│    - 使用开发模板                        │
│    - 遵循代码规范                        │
│    - 编写API文档                         │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         4. 测试验证                     │
│    - 运行开发服务器                      │
│    - 测试API接口                         │
│    - 验证权限                            │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         5. 提交代码                     │
│    - 遵循Git提交规范                     │
│    - 更新文档（如有必要）                │
└─────────────────────────────────────────┘
```

---

## 🔍 关键概念速查

### 权限系统
- **36个权限**: 覆盖7大模块
- **7种角色**: super_admin, admin, finance, receptionist, engineering, owner, tenant
- **5种操作**: view, create, edit, delete, export
- **初始化命令**: `python manage.py init_permissions`

### API架构
- **认证方式**: JWT (Simple JWT)
- **文档**: Swagger UI (`/swagger/`)
- **权限**: 默认需要认证
- **格式**: JSON

### 数据库
- **开发**: SQLite
- **生产推荐**: PostgreSQL
- **ORM**: Django ORM
- **优化**: 使用 select_related()

---

## 📞 获取帮助

### 文档内搜索
```bash
# 在文档中搜索关键字
grep "关键字" *.md
```

### 查看特定主题
- API文档 → `QUICK_REFERENCE.md` 或 `/swagger/`
- 权限系统 → `PROJECT_DEVELOPMENT_GUIDE.md` 的"权限系统"
- 开发规范 → `PROJECT_DEVELOPMENT_GUIDE.md` 的"开发规范"
- 优化建议 → `PROJECT_DEVELOPMENT_GUIDE.md` 的"已知问题与优化建议"

---

## ✨ 文档更新日志

### v1.0 (2026-01-12)
- ✅ 创建完整项目开发文档
- ✅ 创建快速参考指南
- ✅ 创建项目配置清单
- ✅ 创建优化总结文档
- ✅ 创建文档索引（本文档）

---

## 🎓 推荐阅读顺序

### 新手入门
1. README.md（本文档）
2. QUICK_REFERENCE.md
3. PROJECT_CHECKLIST.md（快速开始部分）

### 开发深入
1. PROJECT_DEVELOPMENT_GUIDE.md（完整阅读）
2. OPTIMIZATION_SUMMARY.md
3. 各模块源代码

### 维护部署
1. PROJECT_CHECKLIST.md（完整阅读）
2. PROJECT_DEVELOPMENT_GUIDE.md（部署相关部分）

---

**提示**: 将此文档设为书签，随时可以快速找到所需信息！ 📑

---

**项目版本**: v1.0
**最后更新**: 2026-01-12
**维护者**: Claude Code AI Assistant
