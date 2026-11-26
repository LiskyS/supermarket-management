// ========================================
// 超市管理系统 - 前端数据管理模块
// 使用localStorage存储数据，替代CSV文件
// 适合大一初学者学习
// ========================================

const DataManager = (function() {
    'use strict';

    const STORE_PREFIX = 'supermarket_';

    // 数据表定义
    const TABLES = {
        products: {
            headers: ['id', 'name', 'price', 'stock', 'category', 'description'],
            defaults: [
                { id: 1, name: '苹果', price: 5.99, stock: 100, category: '水果', description: '新鲜红苹果' },
                { id: 2, name: '香蕉', price: 3.99, stock: 150, category: '水果', description: '进口香蕉' },
                { id: 3, name: '牛奶', price: 6.99, stock: 80, category: '饮品', description: '纯牛奶' },
                { id: 4, name: '面包', price: 4.50, stock: 60, category: '烘焙', description: '全麦面包' },
                { id: 5, name: '鸡蛋', price: 8.99, stock: 120, category: '生鲜', description: '土鸡蛋' }
            ]
        },
        sales: {
            headers: ['id', 'customer_id', 'sale_date', 'total_amount', 'payment_method'],
            defaults: []
        },
        employees: {
            headers: ['id', 'name', 'phone', 'email', 'department', 'position', 'salary', 'hire_date', 'status', 'store_id'],
            defaults: [
                { id: 1, name: '张志华', phone: '1376069****', email: 'zhangzh@store.com', department: '管理部', position: '店长', salary: 8000, hire_date: '2023-01-15', status: '在职', store_id: '08001001' },
                { id: 2, name: '刘思雨', phone: '1376069****', email: 'liusy@store.com', department: '销售部', position: '销售主管', salary: 5500, hire_date: '2023-03-20', status: '在职', store_id: '08001002' }
            ]
        },
        employee_history: {
            headers: ['id', 'employee_id', 'employee_name', 'action', 'old_department', 'new_department', 'old_position', 'new_position', 'old_salary', 'new_salary', 'action_date', 'remark'],
            defaults: []
        },
        members: {
            headers: ['id', 'member_id', 'name', 'phone', 'email', 'birthday', 'join_date', 'points', 'level'],
            defaults: [
                { id: 1, member_id: 'M001', name: '张三', phone: '13800138001', email: 'zhangsan@example.com', birthday: '1990-01-01', join_date: '2024-01-01', points: 100, level: '普通会员' },
                { id: 2, member_id: 'M002', name: '李四', phone: '13800138002', email: 'lisi@example.com', birthday: '1992-02-02', join_date: '2024-02-01', points: 200, level: '银卡会员' }
            ]
        },
        costs: {
            headers: ['id', 'month', 'rent', 'utilities', 'salaries', 'supplies', 'maintenance', 'other', 'total'],
            defaults: [
                { id: 1, month: '2024-01', rent: 15000, utilities: 2500, salaries: 45000, supplies: 3000, maintenance: 1500, other: 2000, total: 69000 },
                { id: 2, month: '2024-02', rent: 15000, utilities: 2200, salaries: 45000, supplies: 2800, maintenance: 1200, other: 1800, total: 68000 }
            ]
        },
        gifts: {
            headers: ['id', 'name', 'points_required', 'description', 'stock'],
            defaults: [
                { id: 1, name: '定制购物袋', points_required: 50, description: '环保可重复使用购物袋', stock: 30 },
                { id: 2, name: '精美马克杯', points_required: 80, description: '定制Logo陶瓷马克杯', stock: 25 },
                { id: 3, name: '雨伞', points_required: 120, description: '防风防雨折叠雨伞', stock: 20 },
                { id: 4, name: '保温饭盒', points_required: 200, description: '304不锈钢保温饭盒', stock: 15 },
                { id: 5, name: '蓝牙耳机', points_required: 500, description: '无线蓝牙耳机', stock: 10 }
            ]
        },
        redemptions: {
            headers: ['id', 'member_id', 'gift_id', 'gift_name', 'points_spent', 'redeem_date'],
            defaults: []
        }
    };

    // ========================================
    // 基础工具函数
    // ========================================

    function getStoreKey(tableName) {
        return STORE_PREFIX + tableName;
    }

    function readTable(tableName) {
        const key = getStoreKey(tableName);
        const data = localStorage.getItem(key);
        if (data) {
            return JSON.parse(data);
        }
        return [];
    }

    function writeTable(tableName, rows) {
        const key = getStoreKey(tableName);
        localStorage.setItem(key, JSON.stringify(rows));
    }

    function getNextId(tableName) {
        const rows = readTable(tableName);
        if (rows.length === 0) return 1;
        const maxId = Math.max(...rows.map(r => Number(r.id)));
        return maxId + 1;
    }

    function now() {
        return new Date();
    }

    function formatDate(date) {
        const d = new Date(date);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        const hours = String(d.getHours()).padStart(2, '0');
        const minutes = String(d.getMinutes()).padStart(2, '0');
        const seconds = String(d.getSeconds()).padStart(2, '0');
        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    }

    function formatDateOnly(date) {
        const d = new Date(date);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    // ========================================
    // 初始化
    // ========================================

    function init() {
        for (const [tableName, tableDef] of Object.entries(TABLES)) {
            const key = getStoreKey(tableName);
            if (!localStorage.getItem(key)) {
                writeTable(tableName, tableDef.defaults);
            }
        }
    }

    // 自动初始化
    init();

    // ========================================
    // 商品管理函数
    // ========================================

    function getProducts() {
        return readTable('products');
    }

    function getProductById(productId) {
        const products = readTable('products');
        return products.find(p => Number(p.id) === Number(productId)) || null;
    }

    function addProduct(name, price, stock, category, description) {
        const newId = getNextId('products');
        const products = readTable('products');
        products.push({
            id: newId,
            name: name,
            price: Number(price),
            stock: Number(stock),
            category: category,
            description: description || ''
        });
        writeTable('products', products);
        return newId;
    }

    function deleteProduct(productId) {
        let products = readTable('products');
        products = products.filter(p => Number(p.id) !== Number(productId));
        writeTable('products', products);
    }

    function updateProduct(productId, name, price, stock, category, description) {
        const products = readTable('products');
        const product = products.find(p => Number(p.id) === Number(productId));
        if (product) {
            product.name = name;
            product.price = Number(price);
            product.stock = Number(stock);
            product.category = category;
            product.description = description || '';
        }
        writeTable('products', products);
    }

    function searchProducts(keyword) {
        const products = readTable('products');
        const kw = keyword.toLowerCase();
        return products.filter(p =>
            p.name.toLowerCase().includes(kw) ||
            p.category.toLowerCase().includes(kw)
        );
    }

    // ========================================
    // 销售管理函数
    // ========================================

    function addSale(customerId, totalAmount, paymentMethod, items) {
        const saleId = getNextId('sales');
        const saleDate = formatDate(now());

        const sales = readTable('sales');
        sales.push({
            id: saleId,
            customer_id: customerId || '',
            sale_date: saleDate,
            total_amount: Number(totalAmount),
            payment_method: paymentMethod
        });
        writeTable('sales', sales);

        // 更新库存
        for (const item of items) {
            updateProductStock(item.product_id, item.quantity);
        }

        // 会员积分
        if (customerId) {
            addMemberPoints(customerId, totalAmount);
        }

        return saleId;
    }

    function updateProductStock(productId, quantity) {
        const products = readTable('products');
        const product = products.find(p => Number(p.id) === Number(productId));
        if (product) {
            product.stock = Number(product.stock) - Number(quantity);
        }
        writeTable('products', products);
    }

    function getSalesCountByDate() {
        const sales = readTable('sales');
        const dateCounts = {};
        for (const sale of sales) {
            const date = sale.sale_date.split(' ')[0];
            dateCounts[date] = (dateCounts[date] || 0) + 1;
        }
        return dateCounts;
    }

    function getSalesAmountByDate() {
        const sales = readTable('sales');
        const dateData = {};
        for (const sale of sales) {
            const date = sale.sale_date.split(' ')[0];
            if (!dateData[date]) {
                dateData[date] = { total: 0, count: 0 };
            }
            dateData[date].total += Number(sale.total_amount);
            dateData[date].count += 1;
        }
        return dateData;
    }

    // ========================================
    // 员工管理函数
    // ========================================

    function getEmployees() {
        return readTable('employees');
    }

    function getEmployeeById(employeeId) {
        const employees = readTable('employees');
        return employees.find(e => Number(e.id) === Number(employeeId)) || null;
    }

    function addEmployee(name, phone, email, department, position, salary, hireDate, storeId) {
        const newId = getNextId('employees');
        const employees = readTable('employees');
        employees.push({
            id: newId,
            name: name,
            phone: phone,
            email: email || '',
            department: department,
            position: position,
            salary: Number(salary),
            hire_date: hireDate,
            status: '在职',
            store_id: storeId
        });
        writeTable('employees', employees);
        return newId;
    }

    function updateEmployee(employeeId, name, phone, email, department, position, salary, storeId) {
        const employees = readTable('employees');
        const emp = employees.find(e => Number(e.id) === Number(employeeId));
        if (!emp) return false;
        emp.name = name;
        emp.phone = phone;
        emp.email = email || '';
        emp.department = department;
        emp.position = position;
        emp.salary = Number(salary);
        emp.store_id = storeId;
        writeTable('employees', employees);
        return true;
    }

    function employeeResign(employeeId, remark) {
        const employees = readTable('employees');
        const emp = employees.find(e => Number(e.id) === Number(employeeId));
        if (!emp) return false;
        emp.status = '离职';
        writeTable('employees', employees);
        addEmployeeHistory(employeeId, '辞职', emp.department, '', emp.position, '', emp.salary, '', remark || '');
        return true;
    }

    function employeePromote(employeeId, newPosition, newSalary, remark) {
        const employees = readTable('employees');
        const emp = employees.find(e => Number(e.id) === Number(employeeId));
        if (!emp) return false;
        const oldPosition = emp.position;
        const oldSalary = emp.salary;
        emp.position = newPosition;
        emp.salary = Number(newSalary);
        writeTable('employees', employees);
        addEmployeeHistory(employeeId, '升职', emp.department, emp.department, oldPosition, newPosition, oldSalary, newSalary, remark || '');
        return true;
    }

    function employeeTransfer(employeeId, newDepartment, newPosition, remark) {
        const employees = readTable('employees');
        const emp = employees.find(e => Number(e.id) === Number(employeeId));
        if (!emp) return false;
        const oldDepartment = emp.department;
        const oldPosition = emp.position;
        emp.department = newDepartment;
        emp.position = newPosition;
        writeTable('employees', employees);
        addEmployeeHistory(employeeId, '调岗', oldDepartment, newDepartment, oldPosition, newPosition, emp.salary, emp.salary, remark || '');
        return true;
    }

    function searchEmployees(keyword) {
        const employees = readTable('employees');
        const kw = keyword.toLowerCase();
        return employees.filter(e =>
            e.name.toLowerCase().includes(kw) ||
            e.department.toLowerCase().includes(kw) ||
            e.position.toLowerCase().includes(kw) ||
            e.store_id.toLowerCase().includes(kw)
        );
    }

    function addEmployeeHistory(employeeId, action, oldDepartment, newDepartment, oldPosition, newPosition, oldSalary, newSalary, remark) {
        const history = readTable('employee_history');
        const newId = history.length + 1;
        const actionDate = formatDate(now());
        const emp = getEmployeeById(employeeId);
        const employeeName = emp ? emp.name : '';
        history.push({
            id: newId,
            employee_id: Number(employeeId),
            employee_name: employeeName,
            action: action,
            old_department: oldDepartment,
            new_department: newDepartment,
            old_position: oldPosition,
            new_position: newPosition,
            old_salary: String(oldSalary),
            new_salary: String(newSalary),
            action_date: actionDate,
            remark: remark || ''
        });
        writeTable('employee_history', history);
    }

    function getEmployeeHistory(employeeId) {
        const history = readTable('employee_history');
        return history.filter(h => Number(h.employee_id) === Number(employeeId));
    }

    // ========================================
    // 会员管理函数
    // ========================================

    function getMembers() {
        return readTable('members');
    }

    function getMemberById(memberId) {
        const members = readTable('members');
        return members.find(m => m.member_id === memberId) || null;
    }

    function addMember(memberId, name, phone, email, birthday, joinDate) {
        const members = readTable('members');
        const newId = members.length + 1;
        const newMember = {
            id: newId,
            member_id: memberId,
            name: name,
            phone: phone,
            email: email || '',
            birthday: birthday,
            join_date: joinDate || formatDateOnly(now()),
            points: 0,
            level: '普通会员'
        };
        members.push(newMember);
        writeTable('members', members);
        return newMember;
    }

    function updateMember(memberId, name, phone, email, birthday, level) {
        const members = readTable('members');
        const member = members.find(m => m.member_id === memberId);
        if (!member) return false;
        member.name = name;
        member.phone = phone;
        member.email = email || '';
        member.birthday = birthday;
        member.level = level;
        writeTable('members', members);
        return true;
    }

    function addMemberPoints(memberId, amount) {
        const members = readTable('members');
        const member = members.find(m => m.member_id === memberId);
        if (!member) return;
        let points = Number(member.points) + Number(amount);
        member.points = points;

        // 自动升级会员等级
        if (points >= 1000 && member.level !== '钻石会员') {
            member.level = '钻石会员';
        } else if (points >= 500 && member.level !== '金卡会员' && member.level !== '钻石会员') {
            member.level = '金卡会员';
        } else if (points >= 200 && member.level === '普通会员') {
            member.level = '银卡会员';
        }
        writeTable('members', members);
    }

    function getMemberPoints(memberId) {
        const member = getMemberById(memberId);
        return member ? Number(member.points) : 0;
    }

    // ========================================
    // 成本分析函数
    // ========================================

    function getCostsByMonth() {
        const costs = readTable('costs');
        const months = [];
        const totals = [];
        for (const cost of costs) {
            months.push(cost.month);
            totals.push(Number(cost.total));
        }
        return { months, totals };
    }

    function getCostBreakdown() {
        const costs = readTable('costs');
        if (costs.length === 0) return {};
        const latestCost = costs[costs.length - 1];
        return {
            '房租': Number(latestCost.rent),
            '水电费': Number(latestCost.utilities),
            '工资': Number(latestCost.salaries),
            '办公用品': Number(latestCost.supplies),
            '维修费': Number(latestCost.maintenance),
            '其他': Number(latestCost.other)
        };
    }

    // ========================================
    // 礼品兑换函数
    // ========================================

    function getGifts() {
        return readTable('gifts');
    }

    function getGiftById(giftId) {
        const gifts = readTable('gifts');
        return gifts.find(g => Number(g.id) === Number(giftId)) || null;
    }

    function redeemGift(memberId, giftId) {
        const member = getMemberById(memberId);
        const gift = getGiftById(giftId);

        if (!member || !gift) {
            return { success: false, message: '会员或礼品不存在' };
        }

        const points = Number(member.points);
        const pointsRequired = Number(gift.points_required);
        const stock = Number(gift.stock);

        if (stock <= 0) {
            return { success: false, message: '礼品库存不足' };
        }
        if (points < pointsRequired) {
            return { success: false, message: '积分不够' };
        }

        // 扣除会员积分
        const members = readTable('members');
        const m = members.find(m => m.member_id === memberId);
        if (m) {
            m.points = points - pointsRequired;
        }
        writeTable('members', members);

        // 减少礼品库存
        const gifts = readTable('gifts');
        const g = gifts.find(g => Number(g.id) === Number(giftId));
        if (g) {
            g.stock = stock - 1;
        }
        writeTable('gifts', gifts);

        // 记录兑换记录
        const redemptions = readTable('redemptions');
        const newId = redemptions.length + 1;
        const redeemDate = formatDate(now());
        redemptions.push({
            id: newId,
            member_id: memberId,
            gift_id: Number(giftId),
            gift_name: gift.name,
            points_spent: pointsRequired,
            redeem_date: redeemDate
        });
        writeTable('redemptions', redemptions);

        return { success: true, message: `兑换成功！已扣除 ${pointsRequired} 积分` };
    }

    // ========================================
    // 数据分析辅助函数
    // ========================================

    function getDailyCustomersData(days) {
        days = days || 7;
        const dateCounts = getSalesCountByDate();
        const dates = [];
        const counts = [];

        for (let i = days - 1; i >= 0; i--) {
            const d = new Date(now());
            d.setDate(d.getDate() - i);
            const dateStr = formatDateOnly(d);
            dates.push(dateStr);
            counts.push(dateCounts[dateStr] || 0);
        }

        return { dates, counts };
    }

    function getAverageTransactionData(days) {
        days = days || 7;
        const dateData = getSalesAmountByDate();
        const dates = [];
        const averagePrices = [];

        for (let i = days - 1; i >= 0; i--) {
            const d = new Date(now());
            d.setDate(d.getDate() - i);
            const dateStr = formatDateOnly(d);
            dates.push(dateStr);
            const data = dateData[dateStr] || { total: 0, count: 0 };
            const avg = data.count > 0 ? Math.round((data.total / data.count) * 100) / 100 : 0;
            averagePrices.push(avg);
        }

        return { dates, average_prices: averagePrices };
    }

    // ========================================
    // 公开API
    // ========================================

    return {
        // 工具函数
        init: init,
        resetData: function() {
            for (const tableName of Object.keys(TABLES)) {
                localStorage.removeItem(getStoreKey(tableName));
            }
            init();
        },

        // 商品管理
        getProducts: getProducts,
        getProductById: getProductById,
        addProduct: addProduct,
        deleteProduct: deleteProduct,
        updateProduct: updateProduct,
        searchProducts: searchProducts,

        // 销售管理
        addSale: addSale,
        getSalesCountByDate: getSalesCountByDate,
        getSalesAmountByDate: getSalesAmountByDate,

        // 员工管理
        getEmployees: getEmployees,
        getEmployeeById: getEmployeeById,
        addEmployee: addEmployee,
        updateEmployee: updateEmployee,
        employeeResign: employeeResign,
        employeePromote: employeePromote,
        employeeTransfer: employeeTransfer,
        searchEmployees: searchEmployees,
        getEmployeeHistory: getEmployeeHistory,

        // 会员管理
        getMembers: getMembers,
        getMemberById: getMemberById,
        addMember: addMember,
        updateMember: updateMember,
        getMemberPoints: getMemberPoints,

        // 成本分析
        getCostsByMonth: getCostsByMonth,
        getCostBreakdown: getCostBreakdown,

        // 礼品兑换
        getGifts: getGifts,
        getGiftById: getGiftById,
        redeemGift: redeemGift,

        // 数据分析
        getDailyCustomersData: getDailyCustomersData,
        getAverageTransactionData: getAverageTransactionData
    };
})();
