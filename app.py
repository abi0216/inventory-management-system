"""
Inventory Management System
A Flask-based inventory management application for shops, pharmacies, and warehouses.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps
import os
from datetime import timedelta

# Initialize Flask app

# Use environment variable for Flask secret key (required in production)
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
if not app.secret_key:
    raise RuntimeError('FLASK_SECRET_KEY environment variable is required for production.')
app.permanent_session_lifetime = timedelta(hours=2)  # Session timeout

# Database configuration
DATABASE = os.environ.get('DATABASE', 'database.db')

# Low stock threshold
LOW_STOCK_THRESHOLD = 10



def init_db():
    """
    Initialize the SQLite database and create tables if they don't exist.
    Also ensures a default admin user exists (username: admin, password: admin123).
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Insert default admin user if not exists (INSERT OR IGNORE)
    hashed_password = generate_password_hash('admin123')
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', hashed_password))
    conn.commit()
    conn.close()
    print("Database initialized and admin user ensured.")


# Initialize database when app starts
init_db()


def get_db_connection():
    """Create and return a database connection."""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    except Exception as e:
        print(f"Error connecting to SQLite: {e}")
        return None


def login_required(f):
    """Decorator to protect routes that require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Redirect to dashboard if logged in, otherwise to login."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Please enter both username and password.', 'danger')
            return render_template('login.html')
        
        conn = get_db_connection()
        if not conn:
            flash('Database connection error. Please try again later.', 'danger')
            return render_template('login.html')
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password'], password):
                session.permanent = True
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash(f'Welcome back, {username}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'danger')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        finally:
            conn.close()
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Display the main dashboard with all products."""
    conn = get_db_connection()
    if not conn:
        flash('Database connection error.', 'danger')
        return render_template('dashboard.html', products=[], stats={})
    
    try:
        cursor = conn.cursor()
        
        # Get all products
        cursor.execute("SELECT * FROM products ORDER BY created_at DESC")
        products = [dict(row) for row in cursor.fetchall()]
        
        # Calculate statistics
        cursor.execute("SELECT COUNT(*) as total_products, COALESCE(SUM(quantity), 0) as total_stock FROM products")
        stats = dict(cursor.fetchone())
        
        # Count low stock items
        cursor.execute("SELECT COUNT(*) as low_stock_count FROM products WHERE quantity < ?", (LOW_STOCK_THRESHOLD,))
        low_stock = cursor.fetchone()
        stats['low_stock_count'] = low_stock['low_stock_count']
        
        # Mark low stock products
        for product in products:
            product['is_low_stock'] = product['quantity'] < LOW_STOCK_THRESHOLD
        
        return render_template('dashboard.html', products=products, stats=stats, threshold=LOW_STOCK_THRESHOLD)
    
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        return render_template('dashboard.html', products=[], stats={})
    finally:
        conn.close()


@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    """Add a new product to inventory."""
    if request.method == 'POST':
        product_name = request.form.get('product_name', '').strip()
        category = request.form.get('category', '').strip()
        price = request.form.get('price', '')
        quantity = request.form.get('quantity', '')
        
        # Validation
        errors = []
        if not product_name:
            errors.append('Product name is required.')
        if not category:
            errors.append('Category is required.')
        
        try:
            price = float(price)
            if price < 0:
                errors.append('Price cannot be negative.')
        except (ValueError, TypeError):
            errors.append('Please enter a valid price.')
        
        try:
            quantity = int(quantity)
            if quantity < 0:
                errors.append('Quantity cannot be negative.')
        except (ValueError, TypeError):
            errors.append('Please enter a valid quantity.')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('add_product.html')
        
        conn = get_db_connection()
        if not conn:
            flash('Database connection error.', 'danger')
            return render_template('add_product.html')
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (product_name, category, price, quantity) VALUES (?, ?, ?, ?)",
                (product_name, category, price, quantity)
            )
            conn.commit()
            flash(f'Product "{product_name}" added successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        finally:
            conn.close()
    
    return render_template('add_product.html')


@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    """Edit an existing product."""
    conn = get_db_connection()
    if not conn:
        flash('Database connection error.', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        cursor = conn.cursor()
        
        if request.method == 'POST':
            product_name = request.form.get('product_name', '').strip()
            category = request.form.get('category', '').strip()
            price = request.form.get('price', '')
            quantity = request.form.get('quantity', '')
            
            # Validation
            errors = []
            if not product_name:
                errors.append('Product name is required.')
            if not category:
                errors.append('Category is required.')
            
            try:
                price = float(price)
                if price < 0:
                    errors.append('Price cannot be negative.')
            except (ValueError, TypeError):
                errors.append('Please enter a valid price.')
            
            try:
                quantity = int(quantity)
                if quantity < 0:
                    errors.append('Quantity cannot be negative.')
            except (ValueError, TypeError):
                errors.append('Please enter a valid quantity.')
            
            if errors:
                for error in errors:
                    flash(error, 'danger')
                cursor.execute("SELECT * FROM products WHERE id = ?", (id,))
                product = dict(cursor.fetchone())
                return render_template('edit_product.html', product=product)
            
            cursor.execute(
                "UPDATE products SET product_name = ?, category = ?, price = ?, quantity = ? WHERE id = ?",
                (product_name, category, price, quantity, id)
            )
            conn.commit()
            flash(f'Product "{product_name}" updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        # GET request - fetch product details
        cursor.execute("SELECT * FROM products WHERE id = ?", (id,))
        row = cursor.fetchone()
        
        if not row:
            flash('Product not found.', 'danger')
            return redirect(url_for('dashboard'))
        
        product = dict(row)
        return render_template('edit_product.html', product=product)
    
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
        return redirect(url_for('dashboard'))
    finally:
        conn.close()


@app.route('/delete_product/<int:id>')
@login_required
def delete_product(id):
    """Delete a product from inventory."""
    conn = get_db_connection()
    if not conn:
        flash('Database connection error.', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        cursor = conn.cursor()
        
        # Get product name for confirmation message
        cursor.execute("SELECT product_name FROM products WHERE id = ?", (id,))
        product = cursor.fetchone()
        
        if not product:
            flash('Product not found.', 'danger')
            return redirect(url_for('dashboard'))
        
        cursor.execute("DELETE FROM products WHERE id = ?", (id,))
        conn.commit()
        flash(f'Product "{product["product_name"]}" deleted successfully!', 'success')
    
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
    finally:
        conn.close()
    
    return redirect(url_for('dashboard'))


@app.route('/create_admin')
def create_admin():
    """Utility route to create the default admin user."""
    conn = get_db_connection()
    if not conn:
        return "Database connection error."
    
    try:
        cursor = conn.cursor()
        
        # Check if admin exists
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if cursor.fetchone():
            return "Admin user already exists. Login with username: admin, password: admin123"
        
        # Create admin user with hashed password
        hashed_password = generate_password_hash('admin123')
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ('admin', hashed_password)
        )
        conn.commit()
        return "Admin user created successfully! Username: admin, Password: admin123"
    
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()


# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    flash('Page not found.', 'warning')
    return redirect(url_for('dashboard'))


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    flash('An internal error occurred. Please try again.', 'danger')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    # Run the application
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
