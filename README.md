# EPrepper – Smart AI Study Planner

EPrepper is a web-based study planning application that helps students organize subjects, manage topics, and track exam preparation efficiently. The system analyzes the time available before exams and generates a smart study plan to help students stay on track.

---

## Features

### Subject Management

* Add subjects with exam dates and difficulty levels.

### Topic Tracking

* Add topics under each subject with estimated study hours.

### Progress Tracking

* Mark topics as completed.
* Visual progress indicators.

### Dashboard Analytics

* Overall progress charts.
* Subject-wise progress visualization.

### Smart Study Analysis

The system calculates:

* Days left until exam
* Required study hours
* Available study time

It also shows whether the student is **on track or falling behind**.

### Daily Study Plan Generator

Automatically distributes topics across the remaining days before the exam.

### Theme Mode

* Dark mode
* Light mode

### Account Settings

* Delete subjects
* Delete topics
* Delete account

---

## Tech Stack

### Backend

* Python
* Django

### Frontend

* HTML
* CSS
* Bootstrap

### Visualization

* Chart.js

### Database

* SQLite

---

## Project Structure

```
EPrepper/
│
├── accounts/          # User authentication and dashboard logic
├── subjects/          # Subject and topic management
├── templates/         # HTML templates
├── static/            # CSS, images, and logo
├── studyplanner/      # Main Django project settings
│
├── manage.py
├── requirements.txt
├── Procfile
└── README.md
```

---

## Installation

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/EPrepper.git
cd EPrepper
```

Create a virtual environment:

```
python -m venv venv
```

Activate environment:

Windows

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Run migrations:

```
python manage.py migrate
```

Start the development server:

```
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000
```

---

## Example Workflow

1. Register an account.
2. Add subjects with exam dates.
3. Add topics under each subject.
4. Track progress as topics are completed.
5. View analytics and study schedule.

---

## Deployment

This project can be deployed using platforms such as:

* Render
* Railway
* PythonAnywhere

---

## Future Improvements

* AI-based topic prioritization
* Email reminders for study sessions
* Pomodoro timer integration
* Mobile-friendly PWA version
* Collaborative study groups

---

## Author

Misbha

GitHub:
https://github.com/Misbhaaa

---

## License

This project is created for educational and learning purposes.
