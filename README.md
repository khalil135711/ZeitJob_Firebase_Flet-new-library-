<img width="1117" alt="Bildschirmfoto 2024-09-05 um 21 21 24" src="https://github.com/user-attachments/assets/37495953-ecde-4f83-bf54-8e5fbf427dd0">

# Flet Authentication App

A Python-based web application built using the [Flet](https://flet.dev/) framework and [Firebase](https://firebase.google.com/) (via Pyrebase). This app provides user authentication with role-based access control, allowing users to register, log in, and access different features based on their roles (Employer, Employeur, Etudiant, Admin).

## Features

- **User Registration and Login**: Users can register using an email and password and log in to access the application.
- **Role-Based Access Control**: Different roles (Employer, Employeur, Etudiant, Admin) are provided with different interfaces and functionalities.
- **Job Posting and Management**: Employers can create, view, and manage job postings.
- **Application Management**: Users can apply for jobs, and admins can manage applications and user roles.
- **Real-Time Database**: Firebase Realtime Database is used for storing user and job data.
<img width="828" alt="Bildschirmfoto 2024-09-05 um 21 31 10" src="https://github.com/user-attachments/assets/372a34eb-5209-48d8-964f-759b1e9f745e">

<img width="800" alt="Bildschirmfoto 2024-09-05 um 21 31 30" src="https://github.com/user-attachments/assets/5074aef3-5805-471b-affe-349939243834">
## Prerequisites

- Python 3.8 or later
- Firebase Project (with Realtime Database and Authentication enabled)
- `flet` and `pyrebase` Python packages

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/khalil135711/ZeitJob_Firebase_Flet-new-library-.git
cd ZeitJob_Firebase_Flet-new-library-
```
### 2. Install Required Python Packages:

Ensure you have the required packages installed:
```bash
pip install pyrebase 
pip install pycryptodome
pip install pyrebase4
```
### 3. Configure Firebase
Create a Firebase project in the Firebase Console. Enable Authentication (Email/Password) and Realtime Database. Obtain your Firebase configuration and update the firebaseConfig dictionary in the code:
```bash
firebaseConfig = {
    'apiKey': "YOUR_API_KEY",
    'authDomain': "YOUR_AUTH_DOMAIN",
    'databaseURL': "YOUR_DATABASE_URL",
    'projectId': "YOUR_PROJECT_ID",
    'storageBucket': "YOUR_STORAGE_BUCKET",
    'messagingSenderId': "YOUR_MESSAGING_SENDER_ID",
    'appId': "YOUR_APP_ID"
}
```

## Usage

# Registration
On the registration page, fill in your details (Email, Password, First Name, Last Name, Phone Number, Address, ID Number, and Role).
Click the "Register" button. A verification email will be sent to the provided email address.

# Login
Go to the login page.
Enter your email and password, then click the "Login" button to access the dashboard.
# Dashboard

Depending on your role, you will see different options in your dashboard:

Employer: View job postings, manage applications.
Employeur: Create job postings, view your postings.
Etudiant: View job postings and apply for jobs.
Admin: Manage all job postings and user roles.
Creating a Job Posting (Employeur Role)
Click on "Create Job Posting".
Fill in the job details (Title, Description, Salary, etc.).
Click "Create Job" to post the job.
Managing Applications (Admin Role)
Admins can view all job postings and manage user applications (accept or reject).

# Contributing

Contributions are welcome! Please fork the repository and create a pull request.





