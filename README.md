# Health and Fitness Tracker

**Health and Fitness Tracker** is a simple yet effective web application that allows users to track their daily health activities, monitor trends, and achieve their fitness goals. This application enables users to log their daily activities such as steps taken, calories burned, water intake, and hours of sleep. It helps users visualize their progress, set fitness goals, and assess their journey towards a healthier lifestyle.

---

## Features

- **User Registration & Login**: Secure authentication system to track personal health data.
- **Activity Tracking**: Log daily health activities like steps, calories, water intake, and sleep.
- **Daily Activity Analysis**: Calculate and display weekly and monthly averages.
- **Visualization**: View plots for weekly and monthly activity trends.
- **Edit and Delete Activities**: Update or remove activity logs as needed.
- **Data Insights**: Retrieve specific activity logs by date.

---

## Tech Stack

- **FastAPI**: Framework for backend development and exposing RESTful APIs.
- **PostgreSQL**: Relational database for storing user data and activity logs.
- **Pandas**: Library for data analysis (calculating averages for weekly/monthly analysis).
- **Matplotlib**: Data visualization library for plotting activity trends.

---

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL
- Virtual Environment (optional but recommended)

### Steps to Run Locally

1. Clone this repository:
    ```bash
    git clone https://github.com/SolomiaChunys/Health-and-Fitness-Tracker.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Health-and-Fitness-Tracker
    ```

3. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv env
    ```

4. Activate the virtual environment:
    - On Windows:
      ```bash
      env\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source env/bin/activate
      ```

5. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Set up the database:
    - Make sure PostgreSQL is installed and running.
    - Create a new database.
    - Edit the `DATABASE_URL` in `database.py` to match your PostgreSQL setup.

7. Run the application:
    ```bash
    uvicorn main:app --reload
    ```
---

## API Endpoints

### User Authentication

- **POST /register**: Register a new user (Provide `username` and `password`).
- **POST /login**: Login and get an access token (Provide `username` and `password`).

### Activity Tracking

- **POST /create/activity**: Create a new daily activity log (steps, calories, water intake, sleep).
- **GET /get/activity**: Get all activities of the logged-in user.
- **GET /get/activity/detail/{activity_date}**: Get activity for a specific date.
- **PATCH /update/activity/{activity_date}**: Update an activity log for a given date.
- **DELETE /delete/activity/{activity_date}**: Delete an activity log for a specific date.

### Analysis and Visualization

- **GET /get/analysis/weekly**: Get weekly activity analysis (averages for the current and last week).
- **GET /get/analysis/monthly**: Get monthly activity analysis (averages for the current month and last month).
- **GET /get/analysis/weekly/plot**: View a plot of activity data for the last 7 days.
- **GET /get/analysis/monthly/plot**: View a plot of activity data for the last 30 days.
