// API Base URL
const API_BASE_URL = 'http://localhost:5001/api';

// Get authorization token
function getToken() {
    return localStorage.getItem('token');
}

// Set authorization token
function setToken(token) {
    localStorage.setItem('token', token);
}

// Make API call
async function apiCall(endpoint, method = 'GET', data = null) {
    const headers = {
        'Content-Type': 'application/json',
    };

    const token = getToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const options = {
        method: method,
        headers: headers,
    };

    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        const result = await response.json();

        if (!response.ok) {
            console.error('API Error:', result);
            return { error: result.error || 'An error occurred' };
        }

        return result;
    } catch (error) {
        console.error('Network Error:', error);
        return { error: 'Network error occurred' };
    }
}

// Authentication APIs
async function loginUser(username, password) {
    return apiCall('/auth/login', 'POST', { username, password });
}

async function verifyToken() {
    return apiCall('/auth/verify-token', 'GET');
}

// Product APIs
async function getProducts() {
    return apiCall('/products', 'GET');
}

async function getProduct(id) {
    return apiCall(`/products/${id}`, 'GET');
}

async function createProduct(data) {
    return apiCall('/products', 'POST', data);
}

async function updateProduct(id, data) {
    return apiCall(`/products/${id}`, 'PUT', data);
}

async function deleteProduct(id) {
    return apiCall(`/products/${id}`, 'DELETE');
}

async function getLowStockProducts(threshold = 10) {
    return apiCall(`/products/low-stock?threshold=${threshold}`, 'GET');
}

// Sales APIs
async function getSales() {
    return apiCall('/sales', 'GET');
}

async function getSale(id) {
    return apiCall(`/sales/${id}`, 'GET');
}

async function createSale(data) {
    return apiCall('/sales', 'POST', data);
}

async function getSalesByDateRange(startDate, endDate) {
    return apiCall(`/sales/date-range?start_date=${startDate}&end_date=${endDate}`, 'GET');
}

async function getTotalSales(startDate = null, endDate = null) {
    let url = '/sales/total';
    if (startDate && endDate) {
        url += `?start_date=${startDate}&end_date=${endDate}`;
    }
    return apiCall(url, 'GET');
}

// Purchase APIs
async function getPurchases() {
    return apiCall('/purchases', 'GET');
}

async function getPurchase(id) {
    return apiCall(`/purchases/${id}`, 'GET');
}

async function createPurchase(data) {
    return apiCall('/purchases', 'POST', data);
}

async function getPurchasesByDateRange(startDate, endDate) {
    return apiCall(`/purchases/date-range?start_date=${startDate}&end_date=${endDate}`, 'GET');
}

async function getTotalPurchases(startDate = null, endDate = null) {
    let url = '/purchases/total';
    if (startDate && endDate) {
        url += `?start_date=${startDate}&end_date=${endDate}`;
    }
    return apiCall(url, 'GET');
}

// Report APIs
async function getSalesReport(startDate, endDate) {
    return apiCall(`/reports/sales-report?start_date=${startDate}&end_date=${endDate}`, 'GET');
}

async function getPurchaseReport(startDate, endDate) {
    return apiCall(`/reports/purchase-report?start_date=${startDate}&end_date=${endDate}`, 'GET');
}

async function getProfitAnalysis(startDate, endDate) {
    return apiCall(`/reports/profit-analysis?start_date=${startDate}&end_date=${endDate}`, 'GET');
}

async function getStockReport() {
    return apiCall('/reports/stock-report', 'GET');
}

async function getDashboardMetrics() {
    return apiCall('/reports/dashboard', 'GET');
}
