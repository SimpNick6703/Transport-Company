# Transport Company Vehicle Rental Management System

A comprehensive web application for managing a transport company's vehicle rental operations based on requirements as provided in [`Instructions.md`](https://github.com/SimpNick6703/Transport-Company/blob/main/Instructions.md). Built with Flask, SQLite, HTML, CSS, and JavaScript.

## Features

- Vehicle Management: Add, update, view, and delete vehicles in the fleet
- Customer Management: Register and manage customer information
- Rental Operations: Create and track vehicle rentals, handle returns and payments
- Dashboard: View key metrics and system status

## Tech Stack

- Backend: Python Flask with SQLAlchemy ORM
- Database: SQLite
- Frontend: HTML, CSS with Bootstrap 5
- Interactive UI: JavaScript

## Setup Instructions

### Prerequisites

- Python 3.8 or higher

### Installation

1. Clone the repository

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python run.py
   ```

4. Access the application at http://localhost:5000

## Project Structure

```
transport_company/
├── app/
│   ├── models/         # Database models
│   ├── routes/         # Route definitions
│   ├── static/         # Static assets (CSS, JS)
│   └── templates/      # HTML templates
├── database/           # SQLite database
├── requirements.txt    # Python dependencies
└── run.py              # Application entry point
```

## Database Schema

- **Vehicles**: Fleet vehicles with details like type, model, capacity
- **Customers**: Customer information including contact and license details
- **Rentals**: Rental records tracking vehicle usage, payments, and status

## License

MIT