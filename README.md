# Django E-Commerce Website

A fully-featured Django e-commerce website with cart, checkout, payments, product filtering, and authentication features.

## Features

- **Product Catalog**: Browse products with categories, search, and filtering
- **Shopping Cart**: Add, update, and remove items from cart
- **Checkout Process**: Secure checkout with Stripe payment integration
- **User Authentication**: Registration, login, profile management
- **Order Management**: Order history and tracking
- **Wishlist**: Save favorite products
- **Product Reviews**: Customer reviews and ratings
- **Admin Panel**: Full admin interface for product and order management

## Tech Stack

- **Backend**: Django 5.0.7
- **Database**: SQLite (development), PostgreSQL (production)
- **Payments**: Stripe
- **Deployment**: Gunicorn, WhiteNoise
- **Frontend**: Bootstrap 5, Custom CSS

## Installation

### Prerequisites

- Python 3.11.5
- pip
- virtualenv (recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecommerce
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file with your configuration:
   - `SECRET_KEY`: Django secret key
   - `DEBUG`: Set to `False` for production
   - `DATABASE_URL`: PostgreSQL connection string
   - `STRIPE_PUBLISHABLE_KEY`: Stripe publishable key
   - `STRIPE_SECRET_KEY`: Stripe secret key
   - Email configuration settings

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000/` to access the application.

## Project Structure

```
ecommerce/
├── ecommerce_store/          # Django project settings
│   ├── settings.py          # Main settings file
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── shop/                    # Product catalog app
│   ├── models.py            # Product, Category, Review models
│   ├── views.py             # Product catalog views
│   └── urls.py              # Shop app URLs
├── cart/                    # Shopping cart app
│   ├── models.py            # Cart, Order, Payment models
│   ├── views.py             # Cart functionality views
│   └── urls.py              # Cart app URLs
├── accounts/                # User authentication app
│   ├── models.py            # User profile, wishlist models
│   ├── views.py             # Authentication views
│   └── urls.py              # Accounts app URLs
├── checkout/                # Checkout process app
│   ├── views.py             # Checkout and payment views
│   └── urls.py              # Checkout app URLs
├── templates/               # HTML templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploaded files
├── requirements.txt         # Python dependencies
├── runtime.txt              # Python version specification
├── Procfile                 # Heroku deployment configuration
├── gunicorn_config.py       # Gunicorn configuration
└── .env.example            # Environment variables template
```

## Deployment

### Heroku

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create Heroku app**:
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**:
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DATABASE_URL=your-database-url
   heroku config:set STRIPE_PUBLISHABLE_KEY=your-stripe-key
   heroku config:set STRIPE_SECRET_KEY=your-stripe-secret
   ```

4. **Push to Heroku**:
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

5. **Run migrations**:
   ```bash
   heroku run python manage.py migrate
   ```

6. **Create superuser**:
   ```bash
   heroku run python manage.py createsuperuser
   ```

7. **Collect static files**:
   ```bash
   heroku run python manage.py collectstatic
   ```

## Configuration

### Stripe Integration

1. Create a Stripe account at [stripe.com](https://stripe.com)
2. Get your API keys from the Stripe dashboard
3. Add the keys to your environment variables:
   - `STRIPE_PUBLISHABLE_KEY`: Your publishable key
   - `STRIPE_SECRET_KEY`: Your secret key

### Email Configuration

Configure email settings in your `.env` file:
- `EMAIL_HOST`: SMTP server
- `EMAIL_PORT`: SMTP port
- `EMAIL_HOST_USER`: SMTP username
- `EMAIL_HOST_PASSWORD`: SMTP password
- `EMAIL_USE_TLS`: Set to `True` for TLS

## Usage

### Admin Panel

Access the admin panel at `/admin/` to:
- Manage products and categories
- Process orders
- Manage users
- View analytics

### Shopping Flow

1. **Browse Products**: Visit the home page or product catalog
2. **Add to Cart**: Click "Add to Cart" on product pages
3. **View Cart**: Review items in your cart
4. **Checkout**: Enter shipping information and payment details
5. **Payment**: Complete payment via Stripe
6. **Order Confirmation**: Receive order confirmation and tracking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue on GitHub.
