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
├── README.md              # This file
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

## Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

## Installation

### 1. Clone or Download the Project

```bash
cd inventory-management-system
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up MySQL Database

#### Option A: Using MySQL Command Line
```bash
mysql -u root -p < database.sql
```

#### Option B: Using MySQL Workbench
1. Open MySQL Workbench
2. Connect to your MySQL server
3. Open `database.sql` file
4. Execute the script

### 5. Configure Database Connection

Edit the database configuration in `app.py` or set environment variables:

```python
# Default configuration in app.py
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Add your MySQL password here
    'database': 'inventory_db'
}
```

Or use environment variables:
```bash
# Windows
set DB_HOST=localhost
set DB_USER=root
set DB_PASSWORD=your_password
set DB_NAME=inventory_db

# macOS/Linux
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=inventory_db
```

### 6. Create Admin User

Visit `http://localhost:5000/create_admin` to create the default admin user, or the user will be created from the SQL script.

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

### 7. Run the Application

```bash
python app.py
```

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
