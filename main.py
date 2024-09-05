import flet as ft
import pyrebase
#  pip install pyrebase then pycryptodome then pyrebase4
#  pip install pycryptodome
#  pip install pyrebase4
import re

# Firebase configuration :
firebaseConfig = {
    'apiKey': "", # add this information please to connect firebase with this python script 
    'authDomain': "",
    'databaseURL': "",
    'projectId': "",
    'storageBucket': "",
    'messagingSenderId': "",
    'appId': ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

def main(page: ft.Page):
    page.title = "Flet Authentication App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ALWAYS

    def is_valid_moroccan_phone_number(phone):
        return re.match(r"(\+212|0)[5-7]\d{8}$", phone)

    def register_user(e):
        email = email_field.value
        password = password_field.value
        first_name = first_name_field.value
        last_name = last_name_field.value
        phone = phone_field.value
        address = address_field.value
        id_number = id_number_field.value
        roles = roles_dropdown.value

        if not is_valid_moroccan_phone_number(phone):
            status_label.value = "Invalid phone number. Please enter a valid Moroccan phone number."
            status_label.color = ft.colors.RED
            status_label.update()
            return

        user_data = {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "address": address,
            "id_number": id_number,
            "roles": roles
        }

        try:
            user = auth.create_user_with_email_and_password(user_data["email"], user_data["password"])
            auth.send_email_verification(user['idToken'])

            user_id = user['localId']
            db.child("users").child(user_id).set({
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "phone": user_data["phone"],
                "address": user_data["address"],
                "id_number": user_data["id_number"],
                "roles": user_data["roles"]
            })

            status_label.value = "User registered successfully! A verification email has been sent."
            status_label.color = ft.colors.GREEN

        except Exception as ex:
            error_message = str(ex)
            if "EMAIL_EXISTS" in error_message:
                status_label.value = "The email address is already in use by another account."
            elif "INVALID_EMAIL" in error_message:
                status_label.value = "The email address is not valid."
            elif "WEAK_PASSWORD" in error_message:
                status_label.value = "The password is too weak. It should be at least 6 characters."
            else:
                status_label.value = f"An error occurred: {error_message}"
            status_label.color = ft.colors.RED

        status_label.update()

    def login_user(e):
        email = login_email_field.value
        password = login_password_field.value

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            page.client_storage.set("idToken", user["idToken"])
            page.client_storage.set("localId", user["localId"])
            show_dashboard()
        except Exception as ex:
            login_status_label.value = "Login failed. Please check your email and password."
            login_status_label.color = ft.colors.RED
            login_status_label.update()

    def logout(e):
        page.client_storage.clear()
        show_login()

    def show_register():
        page.views.clear()
        page.views.append(register_view)
        page.update()

    def show_login():
        page.views.clear()
        page.views.append(login_view)
        page.update()

    def show_dashboard():
        user_id = page.client_storage.get("localId")
        user_roles = db.child("users").child(user_id).child("roles").get().val()
        last_name = db.child("users").child(user_id).child("last_name").get().val()

        page.views.clear()

        if "Employer" in user_roles:
            dashboard_view = ft.View(
                "/dashboard",
                [
                    ft.Text(value=f"Welcome, {last_name}!", size=30),
                    ft.Text(value="Employer Dashboard"),
                    ft.ElevatedButton(text="View Job Postings", on_click=lambda e: show_job_postings()),
                    ft.ElevatedButton(text="Logout", on_click=logout)
                ],
                scroll=ft.ScrollMode.ALWAYS
            )
        elif "Employeur" in user_roles:
            dashboard_view = ft.View(
                "/dashboard",
                [
                    ft.Text(value=f"Welcome, {last_name}!", size=30),
                    ft.Text(value="Employeur Dashboard"),
                    ft.ElevatedButton(text="Create Job Posting", on_click=lambda e: show_create_job()),
                    ft.ElevatedButton(text="View My Job Postings", on_click=lambda e: show_my_job_postings()),
                    ft.ElevatedButton(text="Logout", on_click=logout)
                ],
                scroll=ft.ScrollMode.ALWAYS
            )
        elif "Etudiant" in user_roles:
            dashboard_view = ft.View(
                "/dashboard",
                [
                    ft.Text(value=f"Welcome, {last_name}!", size=30),
                    ft.Text(value="Etudiant Dashboard"),
                    ft.ElevatedButton(text="View Job Postings", on_click=lambda e: show_job_postings()),
                    ft.ElevatedButton(text="Logout", on_click=logout)
                ],
                scroll=ft.ScrollMode.ALWAYS
            )
        else:  # Admin
            dashboard_view = ft.View(
                "/dashboard",
                [
                    ft.Text(value=f"Welcome, {last_name}! You're an admin.", size=30),
                    ft.Text(value="Admin Dashboard"),
                    ft.ElevatedButton(text="View All Job Postings", on_click=lambda e: show_all_job_postings()),
                    ft.ElevatedButton(text="Logout", on_click=logout)
                ],
                scroll=ft.ScrollMode.ALWAYS
            )

        page.views.append(dashboard_view)
        page.update()

    def show_create_job():
        page.views.clear()
        page.views.append(create_job_view)
        page.update()

    def show_my_job_postings():
        user_id = page.client_storage.get("localId")
        job_postings = db.child("job_postings").order_by_child("created_by").equal_to(user_id).get()
        jobs = [
            ft.Column(
                [
                    ft.Text(f"Job: {job.val()['title']} - {job.val()['status']}"),
                    ft.ElevatedButton(text="View Applications", on_click=lambda e, job_id=job.key(): show_applications(job_id))
                ]
            ) for job in job_postings.each()
        ]
        jobs.append(ft.ElevatedButton(text="Back to Dashboard", on_click=lambda e: show_dashboard()))
        page.views.clear()
        page.views.append(ft.View("/my_job_postings", jobs, scroll=ft.ScrollMode.ALWAYS))
        page.update()

    def show_applications(job_id):
        applications = db.child("job_postings").child(job_id).child("applications").get()
        apps = []
        for app in applications.each():
            app_data = app.val()
            app_view = ft.Column(
                [
                    ft.Text(f"Name: {app_data['user_name']}"),
                    ft.Text(f"Address: {app_data['user_address']}"),
                    ft.ElevatedButton(text="Accept", on_click=lambda e, app_id=app.key(): accept_application(job_id, app_id, app_data['user_id'])),
                    ft.ElevatedButton(text="Reject", on_click=lambda e, app_id=app.key(): reject_application(job_id, app_id, app_data['user_id']))
                ]
            )
            apps.append(app_view)
        apps.append(ft.ElevatedButton(text="Back to Job Postings", on_click=lambda e: show_my_job_postings()))
        page.views.clear()
        page.views.append(ft.View("/applications", apps, scroll=ft.ScrollMode.ALWAYS))
        page.update()

    def accept_application(job_id, app_id, user_id):
        db.child("job_postings").child(job_id).child("applications").child(app_id).update({"status": "Accepted"})
        db.child("users").child(user_id).child("notifications").push({"message": "Your application has been accepted. Please proceed to the job."})
        show_applications(job_id)

    def reject_application(job_id, app_id, user_id):
        db.child("job_postings").child(job_id).child("applications").child(app_id).update({"status": "Rejected"})
        db.child("users").child(user_id).update({"status": "Deactivated"})
        show_applications(job_id)

    def show_job_postings():
        job_postings = db.child("job_postings").get()
        jobs = []
        for job in job_postings.each():
            job_data = job.val()
            job_view = ft.Column(
                [
                    ft.Text(f"Title: {job_data['title']}"),
                    ft.Text(f"Description: {job_data['description']}"),
                    ft.Text(f"Salary: {job_data['salary']}"),
                    ft.Text(f"Type: {job_data['type']}"),
                    ft.Text(f"Address: {job_data['address']}"),
                    ft.Text(f"Number of Positions: {job_data['num_positions']}"),
                    ft.ElevatedButton(text="Apply", on_click=lambda e, job_id=job.key(): apply_for_job(job_id))
                ]
            )
            jobs.append(job_view)
        jobs.append(ft.ElevatedButton(text="Back to Dashboard", on_click=lambda e: show_dashboard()))
        page.views.clear()
        page.views.append(ft.View("/job_postings", jobs, scroll=ft.ScrollMode.ALWAYS))
        page.update()

    def apply_for_job(job_id):
        user_id = page.client_storage.get("localId")
        user_data = db.child("users").child(user_id).get().val()
        application_data = {
            "user_id": user_id,
            "user_name": user_data["first_name"] + " " + user_data["last_name"],
            "user_address": user_data["address"],
            "status": "Pending"
        }
        db.child("job_postings").child(job_id).child("applications").push(application_data)
        show_job_postings()

    def show_all_job_postings():
        job_postings = db.child("job_postings").get()
        jobs = [ft.Text(f"Job: {job.val()['title']} - {job.val()['status']}") for job in job_postings.each()]
        jobs.append(ft.ElevatedButton(text="Back to Dashboard", on_click=lambda e: show_dashboard()))
        page.views.clear()
        page.views.append(ft.View("/all_job_postings", jobs, scroll=ft.ScrollMode.ALWAYS))
        page.update()

    def create_job_posting(e):
        job_data = {
            "title": job_title_field.value,
            "description": job_description_field.value,
            "salary": job_salary_field.value,
            "type": job_type_dropdown.value,
            "address": job_address_field.value,
            "num_positions": int(job_positions_field.value),
            "created_by": page.client_storage.get("localId"),
            "status": "Open"
        }
        db.child("job_postings").push(job_data)
        status_label_create_job.value = "Job posted successfully!"
        status_label_create_job.color = ft.colors.GREEN
        status_label_create_job.update()

    job_title_field = ft.TextField(label="Job Title", expand=1)
    job_description_field = ft.TextField(label="Job Description", expand=1)
    job_salary_field = ft.TextField(label="Salary", expand=1)
    job_address_field = ft.TextField(label="Job Address", expand=1)
    job_positions_field = ft.TextField(label="Number of Positions", expand=1)
    job_type_dropdown = ft.Dropdown(
        label="Select Job Type",
        options=[
            ft.dropdown.Option("Hourly"),
            ft.dropdown.Option("Weekly"),
            ft.dropdown.Option("Monthly"),
        ],
        width=370
    )
    create_job_button = ft.ElevatedButton(text="Create Job", on_click=create_job_posting)
    status_label_create_job = ft.Text()

    create_job_view = ft.View(
        "/create_job",
        [
            ft.Image(src="logo.png", width=100, height=100),
            ft.Row(controls=[job_title_field, job_salary_field]),
            ft.Row(controls=[job_description_field, job_address_field]),
            ft.Row(controls=[job_positions_field, job_type_dropdown]),
            create_job_button,
            status_label_create_job,
            ft.ElevatedButton(text="Back to Dashboard", on_click=lambda e: show_dashboard())
        ],
        scroll=ft.ScrollMode.ALWAYS
    )

    email_field = ft.TextField(label="Email", expand=1)
    password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, expand=1)
    first_name_field = ft.TextField(label="First Name", expand=1)
    last_name_field = ft.TextField(label="Last Name", expand=1)
    phone_field = ft.TextField(label="Phone Number", expand=1)
    id_number_field = ft.TextField(label="ID Number", expand=1)
    address_field = ft.TextField(label="Address")

    roles_dropdown = ft.Dropdown(
        label="Select Your Role in Bricollage",
        options=[
            ft.dropdown.Option("Employer"),
            ft.dropdown.Option("Employeur"),
            ft.dropdown.Option("Etudiant"),
        ],
        width=370
    )

    register_button = ft.ElevatedButton(text="Register", on_click=register_user)
    status_label = ft.Text()

    name_row = ft.Row(controls=[first_name_field, last_name_field])
    email_password_row = ft.Row(controls=[email_field, password_field])
    phone_id_row = ft.Row(controls=[phone_field, id_number_field])

    register_view = ft.View(
        "/register",
        [
            ft.Image(src="logo.png", width=100, height=100),
            email_password_row,
            name_row,
            phone_id_row,
            address_field,
            roles_dropdown,
            register_button,
            status_label,
            ft.ElevatedButton(text="Go to Login", on_click=lambda e: show_login())
        ],
        scroll=ft.ScrollMode.ALWAYS
    )

    login_email_field = ft.TextField(label="Email")
    login_password_field = ft.TextField(label="Password", password=True, can_reveal_password=True)
    login_button = ft.ElevatedButton(text="Login", on_click=login_user)
    login_status_label = ft.Text()

    login_view = ft.View(
        "/login",
        [
            ft.Image(src="logo.png", width=100, height=100),
            login_email_field,
            login_password_field,
            login_button,
            login_status_label,
            ft.ElevatedButton(text="Go to Register", on_click=lambda e: show_register())
        ],
        scroll=ft.ScrollMode.ALWAYS
    )

    show_login()

ft.app(target=main)
