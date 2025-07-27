# E-Filing Mock Server

A Flask-based mock server for e-filing ITR (Income Tax Return) submissions.

## Features

- Mock ITR form submission endpoint
- Health check endpoint
- Docker containerization
- Production-ready configuration

## Quick Start with Docker

### Using Docker Compose (Recommended)

1. Build and run the application:
   ```bash
   docker-compose up --build
   ```

2. The server will be available at `http://localhost:5000`

### Using Docker directly

1. Build the Docker image:
   ```bash
   docker build -t efiling-mock-server .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 efiling-mock-server
   ```

## API Endpoints

### Health Check
- **GET** `/health`
- Returns server health status

### File ITR
- **POST** `/file_itr`
- Request body:
  ```json
  {
    "itr_form_type": "ITR1",
    "user_data": {
      "personalInfo": {
        "pan": "ABCDE1234F"
      },
      "form3CD": {
        "partAPL": {
          "persumptiveInc44AD": {
            "totPersumptiveInc44AD": 0
          },
          "persumptiveInc44ADA": {
            "totPersumptiveInc44ADA": 0
          }
        }
      },
      "insights": {
        "cumulativeSalary": {
          "salary": 500000
        }
      }
    },
    "pan": "ABCDE1234F"
  }
  ```

## Development

To run the application locally without Docker:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python server.py
   ```

## Docker Configuration

The application is configured with:
- Python 3.11 slim base image
- Non-root user for security
- Health checks
- Production environment settings
- Port 5000 exposed

## Environment Variables

- `FLASK_ENV`: Set to `production` in Docker
- `FLASK_APP`: Points to `server.py`
- `PYTHONUNBUFFERED`: Ensures Python output is sent straight to terminal 