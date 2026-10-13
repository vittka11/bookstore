# Bookstore

Bookstore is a Django web application for managing books and online orders.

## Features

- Book catalog with categories
- Create, update, view, and delete books
- User registration and authentication
- Shopping cart
- Order creation
- Stripe Checkout integration
- Email notification after order creation
- English and Ukrainian localization
- Asynchronous Django views
- PostgreSQL database
- Redis
- Docker and Docker Compose
- Automated tests with pytest
- Test coverage with pytest-cov

## Installation and Run

1. Clone the repository:

```bash
git clone https://github.com/vittka11/bookstore.git
cd bookstore
``` 
2. Create the `.env` file from `.env.example` and add the required environment variables.
3. Build and start the Docker containers:

```bash
   docker compose up -d --build
```
4. Apply database migrations:

```bash
   docker compose exec web python manage.py migrate
```
5. Open the application in your browser:

   `http://localhost:8000/`
   ## Testing

Run all tests:

```bash
docker compose exec web pytest -v
```
Check test coverage:

```bash
docker compose exec web pytest --cov=. --cov-report=term-missing
```
## AI Usage

AI tools were used to improve the project. All AI-generated suggestions were reviewed before being applied to the code.
AI was used for:

- Code review of complex Django views
- Generating and improving model tests
- Generating docstrings for Django views
- Improving project documentation