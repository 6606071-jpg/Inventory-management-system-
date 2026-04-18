# Inventory Management System

A comprehensive inventory management system designed to help small business owners manage their stock levels, sales, purchases, and generate detailed reports.

## 🎯 Features

- **Product Management**: Add, update, delete product details
- **Stock Tracking**: Real-time inventory level monitoring
- **Sales Management**: Record and track daily sales transactions
- **Purchase Management**: Monitor incoming stock from suppliers
- **Billing System**: Generate invoices for customers
- **Stock Alerts**: Notifications for low stock levels
- **Reports**: Sales reports, stock reports, and profit analysis
- **User Authentication**: Secure login system
- **Dashboard**: Quick overview of business metrics

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: MySQL
- **Authentication**: JWT (JSON Web Tokens)

### Frontend
- **HTML5**, **CSS3**, **JavaScript (Vanilla)**
- **Responsive Design**: Works on desktop and mobile
- **REST API Integration**

## 📋 Project Structure

```
project/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── product.py
│   │   │   ├── sale.py
│   │   │   └── purchase.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── products.py
│   │   │   ├── sales.py
│   │   │   ├── purchases.py
│   │   │   └── reports.py
│   │   ├── utils/
│   │   │   ├── db.py
│   │   │   └── auth.py
│   │   ├── config.py
│   │   └── __init__.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── api.js
│   │   └── main.js
│   └── pages/
├── database/
│   ├── schema.sql
│   └── seed_data.sql
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- MySQL 5.7+
- Node.js (optional, for development tools)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd project
   ```

2. **Setup Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your MySQL credentials
   ```

3. **Setup MySQL Database**
   ```bash
   mysql -u root -p < ../database/schema.sql
   mysql -u root -p inventory_system < ../database/seed_data.sql
   ```

4. **Start Flask Server**
   ```bash
   cd backend
   python main.py
   ```
   The server will run at `http://localhost:5000`

5. **Open Frontend**
   - Open `frontend/index.html` in a web browser, or
   - Serve it using a local HTTP server:
   ```bash
   cd frontend
   python -m http.server 8000
   ```
   - Navigate to `http://localhost:8000`

### Default Credentials (for testing)
- **Username**: admin
- **Password**: password

## 📚 API Documentation

### Authentication
- **POST** `/api/auth/login` - Login user
- **GET** `/api/auth/verify-token` - Verify JWT token
- **POST** `/api/auth/logout` - Logout user

### Products
- **GET** `/api/products` - Get all products
- **GET** `/api/products/<id>` - Get product by ID
- **POST** `/api/products` - Create product
- **PUT** `/api/products/<id>` - Update product
- **DELETE** `/api/products/<id>` - Delete product
- **GET** `/api/products/low-stock` - Get low stock products

### Sales
- **GET** `/api/sales` - Get all sales
- **GET** `/api/sales/<id>` - Get sale by ID
- **POST** `/api/sales` - Record sale
- **GET** `/api/sales/date-range` - Get sales by date range
- **GET** `/api/sales/total` - Get total sales

### Purchases
- **GET** `/api/purchases` - Get all purchases
- **GET** `/api/purchases/<id>` - Get purchase by ID
- **POST** `/api/purchases` - Record purchase
- **GET** `/api/purchases/date-range` - Get purchases by date range
- **GET** `/api/purchases/total` - Get total purchases

### Reports
- **GET** `/api/reports/sales-report` - Generate sales report
- **GET** `/api/reports/purchase-report` - Generate purchase report
- **GET** `/api/reports/profit-analysis` - Generate profit analysis
- **GET** `/api/reports/stock-report` - Generate stock report
- **GET** `/api/reports/dashboard` - Get dashboard metrics

## 🔧 Configuration

Edit `.env` file to configure:
- Flask environment and port
- MySQL connection details
- Stock alert threshold
- Secret key for sessions

## 📊 Database Schema

### Tables
- **users** - User accounts and roles
- **products** - Product inventory
- **sales** - Sales transactions
- **purchases** - Purchase transactions
- **stock_alerts** - Low stock notifications
- **audit_logs** - Activity logs

## 🔐 Security Features

- Password hashing with salt
- JWT authentication
- CORS protection
- SQL injection prevention (parameterized queries)
- User roles and permissions

## 🎨 UI Features

- Responsive design for all devices
- Dark-themed sidebar navigation
- Interactive dashboard with metrics
- Data tables with sorting and filtering
- Modal dialogs for forms
- Real-time search functionality
- Stock alert notifications

## 📝 Future Enhancements

- [ ] Supplier management
- [ ] Customer management
- [ ] Advanced analytics
- [ ] PDF invoice generation
- [ ] Email notifications
- [ ] Multi-user support with roles
- [ ] Barcode scanning
- [ ] Mobile app
- [ ] API rate limiting
- [ ] Data backup and restore

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Created for small business inventory management.

## 📞 Support

For support, email support@inventory.local or open an issue on GitHub.

---

**Happy Inventory Management! 📦**
