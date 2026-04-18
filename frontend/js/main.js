// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    checkAuthentication();
    setupEventListeners();
    loadDashboard();
});

// Check if user is authenticated
async function checkAuthentication() {
    const token = getToken();
    if (!token) {
        showLoginModal();
        return;
    }

    const result = await verifyToken();
    if (result.error) {
        localStorage.removeItem('token');
        showLoginModal();
    }
}

// Setup all event listeners
function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', handleNavigation);
    });

    // Page navigation
    const pages = document.querySelectorAll('.page');
    document.querySelectorAll('[data-page]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const pageName = this.dataset.page;
            
            // Update active link
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Update active page
            pages.forEach(p => p.classList.remove('active'));
            document.getElementById(pageName).classList.add('active');
            
            // Update page title
            const titles = {
                dashboard: 'Dashboard',
                products: 'Product Management',
                sales: 'Sales Management',
                purchases: 'Purchase Management',
                reports: 'Reports & Analytics'
            };
            document.getElementById('pageTitle').textContent = titles[pageName] || 'Dashboard';
            
            // Load page data
            if (pageName === 'products') loadProducts();
            else if (pageName === 'sales') loadSales();
            else if (pageName === 'purchases') loadPurchases();
        });
    });

    // Product Management
    document.getElementById('addProductBtn')?.addEventListener('click', () => openProductModal());
    document.getElementById('productForm')?.addEventListener('submit', saveProduct);
    document.getElementById('productSearch')?.addEventListener('input', filterProducts);
    document.getElementById('categoryFilter')?.addEventListener('change', filterProducts);

    // Sales Management
    document.getElementById('recordSaleBtn')?.addEventListener('click', () => openSaleModal());
    document.getElementById('saleForm')?.addEventListener('submit', recordSale);
    document.getElementById('filterSalesBtn')?.addEventListener('click', filterSalesByDate);

    // Purchase Management
    document.getElementById('recordPurchaseBtn')?.addEventListener('click', () => openPurchaseModal());
    document.getElementById('purchaseForm')?.addEventListener('submit', recordPurchase);
    document.getElementById('filterPurchasesBtn')?.addEventListener('click', filterPurchasesByDate);

    // Modals
    setupModals();

    // Logout
    document.getElementById('logoutBtn')?.addEventListener('click', logout);

    // Menu toggle for mobile
    document.getElementById('toggleSidebar')?.addEventListener('click', toggleSidebar);

    // Login form
    document.getElementById('loginForm')?.addEventListener('submit', handleLogin);
}

// ==================== AUTHENTICATION ====================

function showLoginModal() {
    const modal = document.getElementById('loginModal');
    modal.classList.add('active');
    modal.style.display = 'flex';
}

async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    const result = await loginUser(username, password);
    
    if (result.error) {
        alert('Login failed: ' + result.error);
        return;
    }
    
    setToken(result.token);
    document.getElementById('loginModal').classList.remove('active');
    document.getElementById('loginForm').reset();
    location.reload();
}

function logout() {
    localStorage.removeItem('token');
    location.reload();
}

// ==================== DASHBOARD ====================

async function loadDashboard() {
    const result = await getDashboardMetrics();
    
    if (result.error) {
        console.error('Error loading dashboard:', result.error);
        return;
    }
    
    // Update stats
    document.getElementById('totalProducts').textContent = result.total_products || 0;
    document.getElementById('lowStockAlerts').textContent = result.low_stock_alerts || 0;
    document.getElementById('totalSales').textContent = '₹' + (result.total_sales || 0).toLocaleString();
    
    // Get stock value
    const stockResult = await getStockReport();
    if (!stockResult.error) {
        document.getElementById('stockValue').textContent = '₹' + (stockResult.total_stock_value || 0).toLocaleString();
    }
    
    // Populate low stock table
    const tbody = document.querySelector('#lowStockTable tbody');
    tbody.innerHTML = '';
    
    if (result.low_stock_items && result.low_stock_items.length > 0) {
        result.low_stock_items.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.name}</td>
                <td>${item.sku}</td>
                <td>${item.quantity}</td>
                <td>10</td>
            `;
            tbody.appendChild(row);
        });
    } else {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;">No low stock items</td></tr>';
    }
}

// ==================== PRODUCTS ====================

async function loadProducts() {
    const result = await getProducts();
    
    if (result.error) {
        console.error('Error loading products:', result.error);
        return;
    }
    
    const products = Array.isArray(result) ? result : [];
    displayProducts(products);
    populateProductSelects(products);
    
    // Populate category filter
    const categories = [...new Set(products.map(p => p.category).filter(c => c))];
    const categoryFilter = document.getElementById('categoryFilter');
    categoryFilter.innerHTML = '<option value="">All Categories</option>';
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        categoryFilter.appendChild(option);
    });
}

function displayProducts(products) {
    const tbody = document.querySelector('#productsTable tbody');
    tbody.innerHTML = '';
    
    products.forEach(product => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${product.id}</td>
            <td>${product.name}</td>
            <td>${product.sku}</td>
            <td>${product.category || '-'}</td>
            <td>₹${product.price}</td>
            <td>${product.quantity}</td>
            <td>
                <button class="btn btn-secondary" onclick="editProduct(${product.id})">Edit</button>
                <button class="btn btn-danger" onclick="deleteProductAction(${product.id})">Delete</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function populateProductSelects(products) {
    const saleSelect = document.getElementById('saleProduct');
    const purchaseSelect = document.getElementById('purchaseProduct');
    
    if (saleSelect) {
        saleSelect.innerHTML = '<option value="">Select Product</option>';
        products.forEach(p => {
            const option = document.createElement('option');
            option.value = p.id;
            option.textContent = `${p.name} (SKU: ${p.sku}) - Stock: ${p.quantity}`;
            saleSelect.appendChild(option);
        });
    }
    
    if (purchaseSelect) {
        purchaseSelect.innerHTML = '<option value="">Select Product</option>';
        products.forEach(p => {
            const option = document.createElement('option');
            option.value = p.id;
            option.textContent = `${p.name} (SKU: ${p.sku})`;
            purchaseSelect.appendChild(option);
        });
    }
}

function filterProducts() {
    const searchTerm = document.getElementById('productSearch').value.toLowerCase();
    const categoryFilter = document.getElementById('categoryFilter').value;
    
    const rows = document.querySelectorAll('#productsTable tbody tr');
    rows.forEach(row => {
        const name = row.children[1].textContent.toLowerCase();
        const category = row.children[3].textContent;
        
        const matchesSearch = name.includes(searchTerm);
        const matchesCategory = !categoryFilter || category === categoryFilter;
        
        row.style.display = (matchesSearch && matchesCategory) ? '' : 'none';
    });
}

function openProductModal(productId = null) {
    const modal = document.getElementById('productModal');
    modal.classList.add('active');
    
    if (productId) {
        document.getElementById('modalTitle').textContent = 'Edit Product';
        // Load product data
        getProduct(productId).then(product => {
            document.getElementById('productId').value = product.id;
            document.getElementById('productName').value = product.name;
            document.getElementById('productDescription').value = product.description || '';
            document.getElementById('productSku').value = product.sku;
            document.getElementById('productPrice').value = product.price;
            document.getElementById('productQuantity').value = product.quantity;
            document.getElementById('productCategory').value = product.category || '';
        });
    } else {
        document.getElementById('modalTitle').textContent = 'Add Product';
        document.getElementById('productForm').reset();
        document.getElementById('productId').value = '';
    }
}

async function saveProduct(e) {
    e.preventDefault();
    
    const productId = document.getElementById('productId').value;
    const data = {
        name: document.getElementById('productName').value,
        description: document.getElementById('productDescription').value,
        sku: document.getElementById('productSku').value,
        price: parseFloat(document.getElementById('productPrice').value),
        quantity: parseInt(document.getElementById('productQuantity').value),
        category: document.getElementById('productCategory').value
    };
    
    let result;
    if (productId) {
        result = await updateProduct(productId, data);
    } else {
        result = await createProduct(data);
    }
    
    if (result.error) {
        alert('Error: ' + result.error);
    } else {
        alert('Product saved successfully');
        closeModal('productModal');
        loadProducts();
    }
}

function editProduct(productId) {
    openProductModal(productId);
}

async function deleteProductAction(productId) {
    if (confirm('Are you sure you want to delete this product?')) {
        const result = await deleteProduct(productId);
        if (result.error) {
            alert('Error: ' + result.error);
        } else {
            alert('Product deleted successfully');
            loadProducts();
        }
    }
}

// ==================== SALES ====================

async function loadSales() {
    const result = await getSales();
    
    if (result.error) {
        console.error('Error loading sales:', result.error);
        return;
    }
    
    const sales = Array.isArray(result) ? result : [];
    displaySales(sales);
}

function displaySales(sales) {
    const tbody = document.querySelector('#salesTable tbody');
    tbody.innerHTML = '';
    
    sales.forEach(sale => {
        const row = document.createElement('tr');
        const date = new Date(sale.created_at).toLocaleDateString();
        row.innerHTML = `
            <td>${sale.id}</td>
            <td>${sale.name}</td>
            <td>${sale.customer_name}</td>
            <td>${sale.quantity}</td>
            <td>₹${sale.total_price}</td>
            <td>${sale.payment_method}</td>
            <td>${date}</td>
        `;
        tbody.appendChild(row);
    });
}

function openSaleModal() {
    const modal = document.getElementById('saleModal');
    modal.classList.add('active');
    document.getElementById('saleForm').reset();
}

async function recordSale(e) {
    e.preventDefault();
    
    const data = {
        product_id: parseInt(document.getElementById('saleProduct').value),
        quantity: parseInt(document.getElementById('saleQuantity').value),
        customer_name: document.getElementById('customerName').value,
        payment_method: document.getElementById('paymentMethod').value
    };
    
    const result = await createSale(data);
    
    if (result.error) {
        alert('Error: ' + result.error);
    } else {
        alert('Sale recorded successfully');
        closeModal('saleModal');
        loadSales();
        loadDashboard();
        loadProducts();
    }
}

async function filterSalesByDate() {
    const startDate = document.getElementById('saleStartDate').value;
    const endDate = document.getElementById('saleEndDate').value;
    
    if (!startDate || !endDate) {
        alert('Please select both start and end dates');
        return;
    }
    
    const result = await getSalesByDateRange(startDate, endDate);
    if (result.error) {
        alert('Error: ' + result.error);
    } else {
        displaySales(Array.isArray(result) ? result : []);
    }
}

// ==================== PURCHASES ====================

async function loadPurchases() {
    const result = await getPurchases();
    
    if (result.error) {
        console.error('Error loading purchases:', result.error);
        return;
    }
    
    const purchases = Array.isArray(result) ? result : [];
    displayPurchases(purchases);
}

function displayPurchases(purchases) {
    const tbody = document.querySelector('#purchasesTable tbody');
    tbody.innerHTML = '';
    
    purchases.forEach(purchase => {
        const row = document.createElement('tr');
        const date = new Date(purchase.created_at).toLocaleDateString();
        row.innerHTML = `
            <td>${purchase.id}</td>
            <td>${purchase.name}</td>
            <td>${purchase.supplier_name}</td>
            <td>${purchase.quantity}</td>
            <td>₹${purchase.purchase_price}</td>
            <td>${date}</td>
        `;
        tbody.appendChild(row);
    });
}

function openPurchaseModal() {
    const modal = document.getElementById('purchaseModal');
    modal.classList.add('active');
    document.getElementById('purchaseForm').reset();
}

async function recordPurchase(e) {
    e.preventDefault();
    
    const data = {
        product_id: parseInt(document.getElementById('purchaseProduct').value),
        quantity: parseInt(document.getElementById('purchaseQuantity').value),
        purchase_price: parseFloat(document.getElementById('purchasePrice').value),
        supplier_name: document.getElementById('supplierName').value,
        notes: document.getElementById('purchaseNotes').value
    };
    
    const result = await createPurchase(data);
    
    if (result.error) {
        alert('Error: ' + result.error);
    } else {
        alert('Purchase recorded successfully');
        closeModal('purchaseModal');
        loadPurchases();
        loadDashboard();
        loadProducts();
    }
}

async function filterPurchasesByDate() {
    const startDate = document.getElementById('purchaseStartDate').value;
    const endDate = document.getElementById('purchaseEndDate').value;
    
    if (!startDate || !endDate) {
        alert('Please select both start and end dates');
        return;
    }
    
    const result = await getPurchasesByDateRange(startDate, endDate);
    if (result.error) {
        alert('Error: ' + result.error);
    } else {
        displayPurchases(Array.isArray(result) ? result : []);
    }
}

// ==================== REPORTS ====================

async function generateSalesReport() {
    const startDate = document.getElementById('salesReportStart').value;
    const endDate = document.getElementById('salesReportEnd').value;
    
    if (!startDate || !endDate) {
        alert('Please select both dates');
        return;
    }
    
    const result = await getSalesReport(startDate, endDate);
    
    if (result.error) {
        alert('Error: ' + result.error);
        return;
    }
    
    const html = `
        <div style="padding: 15px; background: #f9f9f9; border-radius: 5px; margin-top: 15px;">
            <p><strong>Total Sales:</strong> ₹${result.total_sales || 0}</p>
            <p><strong>Transactions:</strong> ${result.transaction_count || 0}</p>
        </div>
    `;
    document.getElementById('salesReportContent').innerHTML = html;
}

async function generateProfitReport() {
    const startDate = document.getElementById('profitReportStart').value;
    const endDate = document.getElementById('profitReportEnd').value;
    
    if (!startDate || !endDate) {
        alert('Please select both dates');
        return;
    }
    
    const result = await getProfitAnalysis(startDate, endDate);
    
    if (result.error) {
        alert('Error: ' + result.error);
        return;
    }
    
    const html = `
        <div style="padding: 15px; background: #f9f9f9; border-radius: 5px; margin-top: 15px;">
            <p><strong>Total Sales:</strong> ₹${result.total_sales || 0}</p>
            <p><strong>Total Purchases:</strong> ₹${result.total_purchases || 0}</p>
            <p><strong>Profit:</strong> ₹${result.profit || 0}</p>
            <p><strong>Profit Margin:</strong> ${result.profit_margin || '0%'}</p>
        </div>
    `;
    document.getElementById('profitReportContent').innerHTML = html;
}

// ==================== MODAL UTILITIES ====================

function setupModals() {
    const modals = document.querySelectorAll('.modal');
    
    modals.forEach(modal => {
        const closeBtn = modal.querySelector('.close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                modal.classList.remove('active');
            });
        }
        
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    });
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.remove('active');
}

// ==================== UTILITY FUNCTIONS ====================

function handleNavigation(e) {
    e.preventDefault();
}

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('active');
}
