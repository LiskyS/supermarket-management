# Supermarket Management System

A multi-edition supermarket management teaching project: a zero-dependency CLI, two Flask + CSV web editions, a stdlib `http.server` edition, and a pure frontend localStorage edition.

> 中文名：超市管理系统。围绕商品、结算、会员、员工、成本分析、礼品兑换与顾客评价，提供五种可直接运行的教学实现。

## 项目简介

本仓库是同一套超市管理业务的多种实现，适合对照学习 Python 基础、CSV 数据持久化、Flask Web 开发、Python 标准库 HTTP 服务以及纯前端 localStorage：

- **商品与库存**：商品增删改查、搜索、库存维护。
- **结算与销售**：购物车、现金/微信/支付宝、会员折扣、生日优惠、销售记录。
- **会员**：会员等级、积分累计与自动升级、积分兑换礼品。
- **员工**：入职、编辑、升职、调岗、辞职、履历记录。
- **经营分析**：每日顾客数、客单价、月度成本、成本构成、周转率等。
- **扩展功能**：`gui-advanced` 增加顾客数据与会员评价；`gui` 与标准库版包含礼品兑换。

> **关于目录名**：`gui/`、`gui-advanced/` 中的 “gui” 是历史命名，实际实现均为 **Flask + HTML 模板的浏览器界面**，不是 PyQt/Tkinter 桌面程序；仓库中没有 Qt/Tkinter 代码，也不需要安装桌面 GUI 库。

## 各版本对照表

| 版本 | 目录 | 形态 | 技术栈 | 启动入口 | 数据存储 |
|------|------|------|--------|----------|----------|
| **cli** | `cli/` | 命令行 | Python 标准库；图表可选 matplotlib | `cli.py` | `data/*.csv`（8 张表） |
| **gui** | `gui/chaoshiguanli/` | 浏览器 Web | Flask 2.3.2 + matplotlib 3.7.1 + 原生 HTML/CSS/JS | `backend_code/app.py` | `data_files/*.csv`（10 张表） |
| **gui-advanced** | `gui-advanced/chaoshiguanli/` | 浏览器 Web（增强） | Flask 2.3.3 + matplotlib 3.7.2 + numpy 1.25.2 | `backend_code/app.py` | `data_files/*.csv`（10 张表） |
| **versions / 标准库版** | `versions/chaoshiguanli标准库版本/chaoshiguanli/` | 零依赖 Web | Python `http.server` + 原生前端 + CSS 图表 | `server.py` | `data/*.csv`（8 张表） |
| **versions / 纯前端版** | `versions/chaoshiguanli纯前端/` | 纯前端 | HTML/CSS/JS + localStorage + Chart.js（CDN） | `frontend_templates/page_index.html` | 浏览器 localStorage（8 类） |

### 差异速览

- **cli**：启动最快，纯命令行菜单，完整覆盖商品、结算、分析、员工、会员、礼品兑换；按 `V` 可调用 matplotlib 弹窗图表（可选）。
- **gui**：功能最完整的 Flask 参考实现，含 8 个页面（含礼品兑换 `/redeem`），数据分析使用 matplotlib 在服务端生成 PNG。
- **gui-advanced**：在 gui 基础上增加顾客数据与会员评价，页面为 7 个（无礼品兑换页）；员工模块只保留列表、新增、编辑、辞职接口。
- **标准库版**：不安装 Flask/matplotlib，只用 `http.server` 提供页面和 JSON API，图表用 CSS 绘制。
- **纯前端版**：不用 Python、不用服务器，数据在浏览器 localStorage，Chart.js 由 CDN 加载；适合课堂演示和快速改造。

## 目录结构

```text
supermarket-management/
├── cli/
│   ├── cli.py                       # 命令行主入口（菜单、输入校验、可视化入口）
│   ├── handler/
│   │   ├── data_handler.py          # CSV 读写 + 业务逻辑 + 统计分析
│   │   └── chart_renderer.py        # matplotlib 图表（可选）
│   ├── data/                        # 8 张 CSV 数据表
│   └── 教程.md
├── gui/chaoshiguanli/
│   ├── backend_code/
│   │   ├── app.py                   # Flask 主入口
│   │   ├── data_handler.py          # CSV 数据层
│   │   └── check_data.py            # 旧 SQLite 版遗留脚本（当前流程不需要）
│   ├── frontend_templates/          # 8 个 HTML 页面
│   ├── data_files/                  # 10 张 CSV 数据表
│   ├── requirements.txt
│   └── 教程.md
├── gui-advanced/chaoshiguanli/
│   ├── backend_code/                # app.py / data_handler.py / check_data.py
│   ├── frontend_templates/          # 7 个 HTML 页面
│   ├── data_files/                  # 10 张 CSV 数据表（含顾客、评价）
│   ├── requirements.txt
│   └── 教程.md
├── versions/
│   ├── chaoshiguanli标准库版本/chaoshiguanli/
│   │   ├── server.py                # http.server 主入口
│   │   ├── handler/data_handler.py
│   │   ├── template/                # 8 个 HTML 页面
│   │   ├── data/                    # 8 张 CSV 数据表
│   │   ├── requirements.txt         # 零依赖说明
│   │   └── 教程.md
│   └── chaoshiguanli纯前端/
│       ├── frontend_templates/
│       │   ├── page_index.html      # 入口页
│       │   ├── page_*.html          # 其余 7 个页面
│       │   └── js/data_manager.js   # localStorage 数据层
│       ├── requirements.txt         # 无 Python 依赖说明
│       └── 教程.md
└── resources/
    ├── 原始数据表/                  # 9 个 xlsx + 店铺负责人信息.txt + 原始数据表.rar
    └── 课后技能训练1-素材/ ... 课后技能训练7-素材/   # 共 11 个 xlsx 练习素材
```

> 本地生成的 `.venv/`、`.idea/`、`__pycache__/`、讲解视频/压缩包等不参与版本管理；仓库只保留源码、教程、演示数据和练习素材。

## 环境与安装

### 环境要求

- Python 3.8 或更高版本（CLI、gui、gui-advanced、标准库版需要）
- 现代浏览器（Chrome / Edge / Firefox 等）
- 不需要 Node.js，也不需要数据库服务；所有数据都在 CSV 或 localStorage 中
- 纯前端版的 Chart.js 通过 CDN 加载，离线时数据分析图表可能无法显示

| 版本 | 安装依赖 |
|------|----------|
| cli | 无必需依赖；如需弹窗图表，执行 `pip install matplotlib` |
| gui | `pip install -r requirements.txt`（Flask 2.3.2、matplotlib 3.7.1） |
| gui-advanced | `pip install -r requirements.txt`（Flask 2.3.3、matplotlib 3.7.2、numpy 1.25.2） |
| 标准库版 | 无，直接使用 Python 标准库 |
| 纯前端版 | 无 |

Flask 版本各自独立，请在对应目录创建虚拟环境，不要把一个版本的依赖混用到另一个版本：

```powershell
cd gui\chaoshiguanli
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

`gui-advanced` 同理，进入 `gui-advanced\chaoshiguanli` 后执行相同命令。cmd 中的激活命令为 `.venv\Scripts\activate.bat`。

## 运行方式

### cli：命令行版

```powershell
cd cli
python cli.py
```

首次运行会初始化 `cli/data/` 下的 CSV（商品、销售、员工、会员、成本、礼品、兑换；员工履历在首次人事操作时生成），仓库中也已附带一套演示数据。主菜单输入 `0` 退出；在数据分析页面按 `V` 可打开 matplotlib 图表窗口（需要已安装 matplotlib，并且系统有图形桌面环境）。

### gui：Flask 基础版

```powershell
cd gui\chaoshiguanli\backend_code
python app.py
```

浏览器访问 <http://127.0.0.1:5000/>。页面包括：首页 `/`、商品 `/products`、结算 `/checkout`、结算确认 `/checkout/confirm`、数据分析 `/analytics`、员工 `/employees`、会员 `/members`、礼品兑换 `/redeem`。

### gui-advanced：Flask 增强版

```powershell
cd gui-advanced\chaoshiguanli\backend_code
python app.py
```

浏览器访问 <http://127.0.0.1:5000/>。页面包括：首页、商品、结算、结算确认、数据分析、员工、会员（会员页内含“会员评价”标签）；没有独立的礼品兑换页。

### versions / 标准库版

```powershell
cd versions\chaoshiguanli标准库版本\chaoshiguanli
python server.py
```

浏览器访问 <http://127.0.0.1:5000/>。该版本不依赖 Flask，页面模板在 `template/`，数据在 `data/`。

### versions / 纯前端版

推荐用本地静态服务器打开，保证多页面共享同一个 localStorage origin：

```powershell
cd versions\chaoshiguanli纯前端\frontend_templates
python -m http.server 8000
```

浏览器访问 <http://127.0.0.1:8000/page_index.html>。也可以直接双击 `page_index.html`；若浏览器对 `file://` 的 localStorage 做了隔离，页面之间的数据可能不互通。

> 三个 Web 服务默认都占用 `5000` 端口，**同一时间只能启动一个**（CLI 版不占端口）。如需并行运行，请修改对应 `app.py` 中的 `port=5000`，或 `server.py` 中的 `port = 5000`。Flask 版本均以 `debug=True` 运行，仅适合本地教学。

## 数据文件说明

### 各版本数据位置

| 版本 | 数据目录 | 数量 | 初始化方式 |
|------|----------|------|------------|
| cli | `cli/data/` | 8 张 CSV | 首次运行自动创建主数据表；履历表在首次人事操作时创建 |
| gui | `gui/chaoshiguanli/data_files/` | 10 张 CSV | 仓库已附带；`init_files()` 补建主数据表（扩展表不自动创建） |
| gui-advanced | `gui-advanced/chaoshiguanli/data_files/` | 10 张 CSV | 仓库已附带；`init_files()` 补建主数据表（扩展表不自动创建） |
| 标准库版 | `versions/chaoshiguanli标准库版本/chaoshiguanli/data/` | 8 张 CSV | 仓库已附带；启动时补建主数据表 |
| 纯前端版 | 浏览器 localStorage | 8 类集合 | 首次加载由 `data_manager.js` 写入种子数据 |

### CSV 数据表

所有 CSV 均为 UTF-8、首行表头。各版本的文件集合略有差异：

| 数据表 | 用途 | 主要字段 | 含该表的 CSV 版本 |
|--------|------|----------|-------------------|
| `data_products.csv` | 商品与库存 | `id`、`name`、`price`、`stock`、`category`、`description` | cli / gui / gui-advanced / 标准库 |
| `data_sales.csv` | 销售主记录 | `id`、`customer_id`、`sale_date`、`total_amount`、`payment_method` | cli / gui / gui-advanced / 标准库 |
| `data_sales_items.csv` | 销售明细（扩展） | `id`、`sale_id`、`product_id`、`quantity`、`price` | gui / gui-advanced |
| `data_employees.csv` | 员工档案 | `id`、`name`、`phone`、`email`、`department`、`position`、`salary`、`hire_date`、`status`、`store_id` | cli / gui / gui-advanced / 标准库 |
| `data_employee_history.csv` | 员工履历 | `id`、`employee_id`、`employee_name`、`action`、`old_department`、`new_department`、`old_position`、`new_position`、`old_salary`、`new_salary`、`action_date`、`remark` | cli / gui / gui-advanced / 标准库 |
| `data_members.csv` | 会员与积分 | `id`、`member_id`、`name`、`phone`、`email`、`birthday`、`join_date`、`points`、`level` | cli / gui / gui-advanced / 标准库 |
| `data_costs.csv` | 月度固定成本 | `id`、`month`、`rent`、`utilities`、`salaries`、`supplies`、`maintenance`、`other`、`total` | cli / gui / gui-advanced / 标准库 |
| `data_gifts.csv` | 礼品目录 | `id`、`name`、`points_required`、`description`、`stock` | cli / gui / 标准库 |
| `data_redemptions.csv` | 礼品兑换记录 | `id`、`member_id`、`gift_id`、`gift_name`、`points_spent`、`redeem_date` | cli / gui / 标准库 |
| `data_turnover.csv` | 周周转率（扩展） | `id`、`week`、`department`、`turnover_rate`、`average_days` | gui / gui-advanced |
| `data_customers.csv` | 顾客信息（扩展） | `id`、`name`、`phone`、`email` | gui-advanced |
| `data_reviews.csv` | 会员评价 | `id`、`member_id`、`member_name`、`sale_id`、`rating`、`comment`、`review_date` | gui-advanced |

> `data_sales_items.csv`、`data_turnover.csv`、`data_customers.csv` 属于附带/预留数据，当前主流程未必全部读取，适合作为扩展练习的数据源；以对应版本的 `data_handler.py`、`app.py` 实际引用为准。

纯前端版把同样的 8 类业务数据存放在 localStorage，键名统一以 `supermarket_` 开头（`supermarket_products`、`supermarket_sales`、`supermarket_employees`、`supermarket_employee_history`、`supermarket_members`、`supermarket_costs`、`supermarket_gifts`、`supermarket_redemptions`）。在浏览器控制台执行 `DataManager.resetData()` 可恢复初始数据。

## 资源目录（实践素材）

`resources/` 是配套的 Excel 练习素材，**不参与程序运行**：

- `原始数据表/`：9 个 xlsx，涵盖销售流水、库存、店铺信息、顾客评价、会员生日、固定成本、周转率等；另有 `店铺负责人信息.txt`（GBK 编码）和 `原始数据表.rar`。
- `课后技能训练1-素材/` 至 `课后技能训练7-素材/`：共 11 个 xlsx，用于排序、筛选、分类汇总、数据透视表、图表等课后训练。
- 部分素材含姓名、手机号等字段，其中手机号已打码；它们只用于教学练习，请勿据此联系任何个人或用于真实经营决策。

## 已知说明与限制

- **gui 不是桌面程序**：`gui/`、`gui-advanced/` 都是 Flask Web 应用，通过浏览器访问；不需要安装 PyQt、PySide 或 Tkinter。
- **端口冲突**：gui、gui-advanced 与标准库版默认端口均为 `5000`，同时启动会失败；请改端口或逐个运行。
- **gui-advanced 的员工模块**：前端页面沿用了 gui 的升职、调岗、搜索、履历界面，但 `gui-advanced` 的 `app.py` 只注册了员工列表、新增、编辑、辞职等接口；点击升职/调岗/搜索/履历时可能返回 404。需要完整人事流程请使用 `gui/` 版本，或自行补齐 API。
- **check_data.py 是旧版遗留**：两个 `backend_code/check_data.py` 读取 `../data/supermarket.db`（SQLite），当前 CSV 版不会生成该数据库，正常运行无需执行它。
- **依赖说明**：`gui-advanced` 的 `requirements.txt` 仍列出 matplotlib、numpy，但当前 `app.py` 主要使用 Flask；按文件安装不影响运行，图表扩展可自行接入。
- **无鉴权**：所有版本都没有登录、权限或支付对接，仅用于教学演示，请勿直接部署到公网或用于真实收银。
- **数据一致性**：纯前端版的数据只存在当前浏览器，换浏览器或清除站点数据后会重置；CSV 版本直接改写文件，操作前建议备份 `data/` 或 `data_files/`。

## 教程索引

每个版本都带有独立教程，包含界面说明、代码修改练习和常见问题：

- `cli/教程.md`
- `gui/chaoshiguanli/教程.md`
- `gui-advanced/chaoshiguanli/教程.md`
- `versions/chaoshiguanli标准库版本/chaoshiguanli/教程.md`
- `versions/chaoshiguanli纯前端/教程.md`

## 示例数据声明

**程序内置的示例数据均为虚构。** 仓库内 CSV 与 localStorage 种子数据中的人名、手机号、邮箱、会员号、门店号、销售与工资记录，均为教学演示或占位数据，姓名均为虚构，不对应任何真实顾客、员工、店铺或机构；示例联系方式只用于演示字段和表单校验，不应视为真实联系方式，请勿用于联系任何人。

`resources/` 中的原始数据表可能来自教学案例，含已打码的姓名/电话字段；本 README 不复述任何具体姓名或联系方式，使用这些素材前请确认其授权范围。本 README 本身不包含真实姓名、学校、班级、学号或联系方式等个人信息。
