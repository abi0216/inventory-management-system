# Inventory Management System

A full-stack inventory management application built with Flask and MySQL, suitable for shops, pharmacies, or warehouses.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)

## Features

- **User Authentication**: Secure session-based login/logout
- **Product Management**: Full CRUD operations (Create, Read, Update, Delete)
- **Inventory Tracking**: Stock-in and stock-out via quantity updates
- **Low Stock Alerts**: Visual alerts for products with quantity below 10
- **Dashboard Analytics**: Total products, total stock, and low stock counts
- **Responsive Design**: Mobile-friendly Bootstrap UI

## Tech Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML5 + Bootstrap 5
- **Authentication**: Session-based with werkzeug security
- **Icons**: Bootstrap Icons

## Project Structure

```
inventory-management-system/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── database.sql           # Database schema and sample data
<br />
# Inventory Management System



![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3.0-blue.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)

---

## 🚀 Live Demo

**[View Deployed App on Render](https://inventory-management-system.onrender.com)**

---

## 🛠️ Tech Stack

- **Backend:** Python Flask
- **Database:** SQLite (file-based, zero setup)
- **Frontend:** HTML5 + Bootstrap 5
- **Authentication:** Session-based (Werkzeug security)
- **Icons:** Bootstrap Icons

---

## ✨ Features

- **User Authentication:** Secure session-based login/logout
- **Product Management:** Add, edit, delete products
- **Stock In/Out:** Update product quantity (stock in/out)
- **Low Stock Alerts:** Red badge for products with quantity ≤ 5
- **Dashboard Analytics:** Total products, total stock, low stock count
- **Responsive UI:** Clean, mobile-friendly Bootstrap design
- **Logout:** One-click logout from dashboard
- **Deployment Ready:** Works on Render, Railway, etc.

---

## 📸 Screenshots

> _Add your screenshots here!_

![Dashboard Screenshot](screenshots/dashboard.png)
![Login Screenshot](screenshots/login.png)

---

## 🗂️ Project Structure

```
inventory-management-system/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
├── templates/
│   ├── login.html         # Login page
│   ├── dashboard.html     # Main dashboard
│   ├── add_product.html   # Add product form
│   └── edit_product.html  # Edit product form
│
└── static/
     └── css/
          └── style.css      # Custom styles
```

---

## 🖥️ Local Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/abi0216/inventory-management-system.git
    cd inventory-management-system
    ```
2. **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Set environment variable for Flask secret key:**
    ```bash
    # Windows
    set FLASK_SECRET_KEY=your-very-secret-key
    # macOS/Linux
    export FLASK_SECRET_KEY=your-very-secret-key
    ```
5. **Run the app:**
    ```bash
    python app.py
    ```
6. **Login:**
    - Username: `admin`
    - Password: `admin123`

---

## ☁️ Deployment (Render)

1. **Push your code to GitHub.**
2. **Create a new Web Service on [Render](https://render.com):**
    - **Build Command:** `pip install -r requirements.txt`
    - **Start Command:** `gunicorn app:app`
3. **Add environment variable:**
    - `FLASK_SECRET_KEY=your-very-secret-key`
4. **Deploy!**

---

## 📋 License

MIT License. Free for personal and commercial use.

---

## 🙋‍♂️ Author & Credits

- [abi0216](https://github.com/abi0216)

---

## 💡 Portfolio Use

This project is clean, beginner-friendly, and ready for your portfolio. Fork, star, and use it as a base for your own inventory or admin systems!
The application will be available at: `http://localhost:5000`

## Usage

### Login
1. Navigate to `http://localhost:5000`
2. Enter username: `admin`
3. Enter password: `admin123`

### Dashboard
- View all products in a table
- See total products, total stock, and low stock counts
- Low stock items (quantity < 10) are highlighted in red

### Add Product
1. Click "Add Product" button
2. Fill in product details:
   - Product Name
   - Category
   - Price
   - Quantity
3. Click "Add Product"

### Edit Product
1. Click the edit (pencil) icon on any product
2. Modify the details
3. Click "Update Product"

### Delete Product
1. Click the delete (trash) icon on any product
2. Confirm the deletion

### Stock Management
- To add stock: Edit product and increase quantity
- To remove stock: Edit product and decrease quantity

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `your-secret-key-change-in-production` |
| `DB_HOST` | MySQL host | `localhost` |
| `DB_USER` | MySQL username | `root` |
| `DB_PASSWORD` | MySQL password | `` |
| `DB_NAME` | Database name | `inventory_db` |
| `FLASK_DEBUG` | Debug mode | `True` |
| `PORT` | Application port | `5000` |

## Deployment

### Railway/Render Deployment

1. Create a MySQL database on your platform
2. Set the environment variables:
   ```
   DB_HOST=your-db-host
   DB_USER=your-db-user
   DB_PASSWORD=your-db-password
   DB_NAME=inventory_db
   SECRET_KEY=your-secure-secret-key
   FLASK_DEBUG=False
   ```
3. Deploy the application

### Docker Deployment (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## Security Features

- Password hashing with werkzeug.security
- Parameterized SQL queries (SQL injection prevention)
- Session-based authentication
- Session timeout (2 hours)
- Login required decorator for protected routes

## API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Redirect to dashboard or login |
| `/login` | GET, POST | User login |
| `/logout` | GET | User logout |
| `/dashboard` | GET | Main dashboard |
| `/add_product` | GET, POST | Add new product |
| `/edit_product/<id>` | GET, POST | Edit product |
| `/delete_product/<id>` | GET | Delete product |
| `/create_admin` | GET | Create default admin user |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please open an issue on the repository.
