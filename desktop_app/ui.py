import tkinter as tk
from tkinter import messagebox
import requests


# =========================================================
# API
# =========================================================

BASE_URL = "http://127.0.0.1:8000/api/v1/accounts"

RESET_PASSWORD_URL = f"{BASE_URL}/reset-password/"

RESET_CONFIRM_URL = (
    "http://127.0.0.1:8000/api/v1/accounts/reset-confirm/"
)
PROFILE_URL = f"{BASE_URL}/profile/"
LOGIN_URL = f"{BASE_URL}/login/"
REGISTER_URL = f"{BASE_URL}/signup/"



# =========================================================
# Global
# =========================================================

token = None
current_user = None


# =========================================================
# Main Window
# =========================================================

root = tk.Tk()

root.title("Authentication System")
root.geometry("1100x950")
root.configure(bg="#111111")
root.resizable(False, False)


# =========================================================
# Colors
# =========================================================

BG = "#111111"
CARD = "#181818"
WHITE = "#FFFFFF"
GRAY = "#AAAAAA"
BORDER = "#EEEEEE"
BUTTON = "#222222"


# =========================================================
# Helper Functions
# =========================================================

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def title_label(parent, text, size=22):
    return tk.Label(
        parent,
        text=text,
        bg=CARD,
        fg=WHITE,
        font=("Arial", size, "bold")
    )


def label(parent, text):
    return tk.Label(
        parent,
        text=text,
        bg=CARD,
        fg=WHITE,
        font=("Arial", 11)
    )


def entry(parent, show=None):
    return tk.Entry(
        parent,
        bg="#222222",
        fg=WHITE,
        insertbackground=WHITE,
        relief="solid",
        bd=1,
        font=("Arial", 12),
        show=show
    )


def button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=BUTTON,
        fg=WHITE,
        activebackground="#333333",
        activeforeground=WHITE,
        relief="solid",
        bd=1,
        font=("Arial", 11, "bold"),
        padx=20,
        pady=8,
        cursor="hand2"
    )


# =========================================================
# API Error Helper
# =========================================================

def get_api_error(response):
    """
    تبدیل خطاهای DRF به متن قابل نمایش
    """

    try:
        data = response.json()

    except Exception:
        return f"Server error: {response.status_code}"

    if isinstance(data, dict):

        errors = []

        for field, messages in data.items():

            if isinstance(messages, list):
                messages = ", ".join(
                    str(x) for x in messages
                )

            errors.append(
                f"{field}: {messages}"
            )

        return "\n".join(errors)

    if isinstance(data, list):

        return "\n".join(
            str(x) for x in data
        )

    return str(data)


# =========================================================
# AUTH CARD
# =========================================================

auth_card = tk.Frame(
    root,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=2,
    width=400,
    height=550,
)

auth_card.pack_propagate(False)
auth_card.place(x=350, y=40)


# =========================================================
# RESET PASSWORD
# =========================================================

def reset_password():

    reset_window = tk.Toplevel(root)

    reset_window.title("Reset Password")
    reset_window.geometry("450x350")
    reset_window.configure(bg=BG)
    reset_window.resizable(False, False)


    reset_card = tk.Frame(
        reset_window,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=2,
        width=400,
        height=300
    )

    reset_card.pack(
        padx=25,
        pady=25
    )

    reset_card.pack_propagate(False)



    title_label(
        reset_card,
        "RESET PASSWORD",
        18
    ).pack(
        pady=(25,30)
    )


    label(
        reset_card,
        "Email"
    ).pack(
        anchor="w",
        padx=30
    )


    email = entry(reset_card)

    email.pack(
        fill="x",
        padx=30,
        pady=10
    )



    def send_reset_request():

        email_value = email.get().strip()


        if not email_value:

            messagebox.showwarning(
                "Reset Password",
                "Enter your email."
            )

            return



        try:

            response = requests.post(
                RESET_PASSWORD_URL,
                json={
                    "email": email_value
                },
                timeout=10
            )


        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

            return



        if response.status_code == 200:


            data = response.json()


            link = data.get("link")


            if link:


                parts = link.rstrip("/").split("/")


                uid = parts[-2]

                token = parts[-1]


                reset_window.destroy()


                show_new_password_window(
                    uid,
                    token
                )


            else:

                messagebox.showerror(
                    "Error",
                    "Reset link not found."
                )



        else:

            messagebox.showerror(
                "Error",
                get_api_error(response)
            )



    button(
        reset_card,
        "NEXT",
        send_reset_request
    ).pack(
        pady=30
    )
# =========================================================
# GET PROFILE
# =========================================================

def get_profile():

    if not token:

        messagebox.showerror(
            "Authentication Error",
            "You are not logged in."
        )

        return None

    headers = {
        "Authorization": f"Token {token}"
    }

    try:

        response = requests.get(
            PROFILE_URL,
            headers=headers,
            timeout=10
        )

    except requests.exceptions.ConnectionError:

        messagebox.showerror(
            "Connection Error",
            "Cannot connect to Django server."
        )

        return None

    except requests.exceptions.Timeout:

        messagebox.showerror(
            "Connection Error",
            "Server request timed out."
        )

        return None

    except requests.exceptions.RequestException as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

        return None

    if response.status_code == 200:

        return response.json()

    messagebox.showerror(
        "Profile Error",
        get_api_error(response)
    )

    return None


# =========================================================
# LOGIN
# =========================================================
def show_new_password_window(uid, token):


    window = tk.Toplevel(root)

    window.title("New Password")
    window.geometry("450x350")
    window.configure(bg=BG)


    card = tk.Frame(
        window,
        bg=CARD,
        width=400,
        height=300,
        highlightbackground=BORDER,
        highlightthickness=2
    )

    card.pack(
        padx=25,
        pady=25
    )

    card.pack_propagate(False)



    title_label(
        card,
        "NEW PASSWORD",
        18
    ).pack(
        pady=25
    )



    label(
        card,
        "New password"
    ).pack(
        anchor="w",
        padx=30
    )


    password = entry(
        card,
        show="*"
    )

    password.pack(
        fill="x",
        padx=30,
        pady=5
    )



    label(
        card,
        "Confirm password"
    ).pack(
        anchor="w",
        padx=30
    )


    confirm = entry(
        card,
        show="*"
    )

    confirm.pack(
        fill="x",
        padx=30,
        pady=5
    )




    def change_password():


        p1 = password.get()

        p2 = confirm.get()



        if p1 != p2:

            messagebox.showerror(
                "Password",
                "Passwords don't match."
            )

            return



        try:

            response = requests.post(

                f"{RESET_CONFIRM_URL}{uid}/{token}/",

                json={
                    "password":p1
                },

                timeout=10
            )



        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

            return




        if response.status_code == 200:

            messagebox.showinfo(
                "Success",
                "Password changed successfully."
            )

            window.destroy()


        else:

            messagebox.showerror(
                "Failed",
                get_api_error(response)
            )




    button(
        card,
        "CHANGE PASSWORD",
        change_password
    ).pack(
        pady=20
    )
def show_login():

    clear_frame(auth_card)

    # -----------------------------------------------------
    # Tabs
    # -----------------------------------------------------

    tabs = tk.Frame(
        auth_card,
        bg=CARD
    )

    tabs.pack(
        fill="x",
        pady=(15, 25)
    )

    login_tab = tk.Button(
        tabs,
        text="LOGIN",
        bg=BUTTON,
        fg=WHITE,
        relief="solid",
        bd=1,
        font=("Arial", 10, "bold"),
        command=show_login,
    )

    login_tab.pack(
        side="left",
        expand=True,
        fill="x",
        padx=(10, 2)
    )

    register_tab = tk.Button(
        tabs,
        text="REGISTER",
        bg=CARD,
        fg=GRAY,
        relief="solid",
        bd=1,
        font=("Arial", 10, "bold"),
        command=show_register,
    )

    register_tab.pack(
        side="left",
        expand=True,
        fill="x",
        padx=(2, 10)
    )

    # -----------------------------------------------------
    # Title
    # -----------------------------------------------------

    title_label(
        auth_card,
        "LOGIN",
        20
    ).pack(
        pady=(5, 25)
    )

    # -----------------------------------------------------
    # Username
    # -----------------------------------------------------

    label(
        auth_card,
        "Username"
    ).pack(
        anchor="w",
        padx=25
    )

    username = entry(auth_card)

    username.pack(
        fill="x",
        padx=25,
        pady=(5, 20)
    )

    # -----------------------------------------------------
    # Password
    # -----------------------------------------------------

    label(
        auth_card,
        "Password"
    ).pack(
        anchor="w",
        padx=25
    )

    password = entry(
        auth_card,
        show="*"
    )

    password.pack(
        fill="x",
        padx=25,
        pady=(5, 30)
    )

    # =====================================================
    # LOGIN FUNCTION
    # =====================================================

    def login():

        global token
        global current_user

        username_value = username.get().strip()

        password_value = password.get()

        if not username_value or not password_value:

            messagebox.showwarning(
                "Login",
                "Please fill all fields."
            )

            return

        payload = {
            "username": username_value,
            "password": password_value
        }

        try:

            response = requests.post(
                LOGIN_URL,
                json=payload,
                timeout=10
            )

        except requests.exceptions.ConnectionError:

            messagebox.showerror(
                "Connection Error",
                "Cannot connect to Django server.\n\n"
                "Make sure Django is running."
            )

            return

        except requests.exceptions.Timeout:

            messagebox.showerror(
                "Connection Error",
                "Server request timed out."
            )

            return

        except requests.exceptions.RequestException as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

            return

        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        if response.status_code in [200, 202]:

            try:

                data = response.json()

            except Exception:

                data = {}

            token = data.get("token")

            current_user = {
                "username": username_value
            }

            messagebox.showinfo(
                "Login",
                f"Welcome {username_value}!"
            )

            root.withdraw()

            show_profile_window()

        else:

            error = get_api_error(response)

            messagebox.showerror(
                "Login Failed",
                error
            )

    # =====================================================
    # BUTTONS
    # =====================================================

    buttons_frame = tk.Frame(
        auth_card,
        bg=CARD
    )

    buttons_frame.pack(
        pady=10
    )

    button(
        buttons_frame,
        "LOGIN",
        login
    ).pack(
        side="left",
        padx=5
    )

    button(
        buttons_frame,
        "RESET PASSWORD",
        reset_password
    ).pack(
        side="left",
        padx=5
    )

    # -----------------------------------------------------
    # Enter
    # -----------------------------------------------------

    auth_card.bind_all(
        "<Return>",
        lambda event: login()
    )


# =========================================================
# REGISTER
# =========================================================

def show_register():

    clear_frame(auth_card)

    # -----------------------------------------------------
    # Tabs
    # -----------------------------------------------------

    tabs = tk.Frame(
        auth_card,
        bg=CARD
    )

    tabs.pack(
        fill="x",
        pady=(15, 15)
    )

    login_tab = tk.Button(
        tabs,
        text="LOGIN",
        bg=CARD,
        fg=GRAY,
        relief="solid",
        bd=1,
        font=("Arial", 10, "bold"),
        command=show_login,
    )

    login_tab.pack(
        side="left",
        expand=True,
        fill="x",
        padx=(10, 2)
    )

    register_tab = tk.Button(
        tabs,
        text="REGISTER",
        bg=BUTTON,
        fg=WHITE,
        relief="solid",
        bd=1,
        font=("Arial", 10, "bold"),
        command=show_register,
    )

    register_tab.pack(
        side="left",
        expand=True,
        fill="x",
        padx=(2, 10)
    )

    # -----------------------------------------------------
    # Title
    # -----------------------------------------------------

    title_label(
        auth_card,
        "REGISTER",
        20
    ).pack(
        pady=(5, 12)
    )

    # -----------------------------------------------------
    # Username
    # -----------------------------------------------------

    label(
        auth_card,
        "Username"
    ).pack(
        anchor="w",
        padx=25
    )

    username = entry(auth_card)

    username.pack(
        fill="x",
        padx=25,
        pady=(3, 8)
    )

    # -----------------------------------------------------
    # Password
    # -----------------------------------------------------

    label(
        auth_card,
        "Password"
    ).pack(
        anchor="w",
        padx=25
    )

    password = entry(
        auth_card,
        show="*"
    )

    password.pack(
        fill="x",
        padx=25,
        pady=(3, 8)
    )

    # -----------------------------------------------------
    # Confirm Password
    # -----------------------------------------------------

    label(
        auth_card,
        "Confirm password"
    ).pack(
        anchor="w",
        padx=25
    )

    confirm_password = entry(
        auth_card,
        show="*"
    )

    confirm_password.pack(
        fill="x",
        padx=25,
        pady=(3, 8)
    )

    # -----------------------------------------------------
    # Email
    # -----------------------------------------------------

    label(
        auth_card,
        "Email"
    ).pack(
        anchor="w",
        padx=25
    )

    email = entry(auth_card)

    email.pack(
        fill="x",
        padx=25,
        pady=(3, 8)
    )

    # -----------------------------------------------------
    # First Name
    # -----------------------------------------------------

    label(
        auth_card,
        "First name"
    ).pack(
        anchor="w",
        padx=25
    )

    first_name = entry(auth_card)

    first_name.pack(
        fill="x",
        padx=25,
        pady=(3, 8)
    )

    # -----------------------------------------------------
    # Last Name
    # -----------------------------------------------------

    label(
        auth_card,
        "Last name"
    ).pack(
        anchor="w",
        padx=25
    )

    last_name = entry(auth_card)

    last_name.pack(
        fill="x",
        padx=25,
        pady=(3, 8)
    )

    # -----------------------------------------------------
    # Phone
    # -----------------------------------------------------

    label(
        auth_card,
        "Phone"
    ).pack(
        anchor="w",
        padx=25
    )

    phone = entry(auth_card)

    phone.pack(
        fill="x",
        padx=25,
        pady=(3, 10)
    )

    # =====================================================
    # REGISTER FUNCTION
    # =====================================================

    def register():

        username_value = username.get().strip()

        password_value = password.get()

        confirm_value = confirm_password.get()

        email_value = email.get().strip()

        first_name_value = first_name.get().strip()

        last_name_value = last_name.get().strip()

        phone_value = phone.get().strip()

        # -------------------------------------------------
        # Validation
        # -------------------------------------------------

        if not username_value:

            messagebox.showwarning(
                "Register",
                "Username is required."
            )

            return

        if not email_value:

            messagebox.showwarning(
                "Register",
                "Email is required."
            )

            return

        if not password_value:

            messagebox.showwarning(
                "Register",
                "Password is required."
            )

            return

        if password_value != confirm_value:

            messagebox.showerror(
                "Register",
                "Passwords do not match."
            )

            return

        # -------------------------------------------------
        # Payload
        # -------------------------------------------------

        payload = {
            "username": username_value,
            "email": email_value,
            "password": password_value,
            "password1": confirm_value,
            "first_name": first_name_value,
            "last_name": last_name_value,
            "phone": phone_value,
        }

        # -------------------------------------------------
        # Request
        # -------------------------------------------------

        try:

            response = requests.post(
                REGISTER_URL,
                json=payload,
                timeout=10
            )

        except requests.exceptions.ConnectionError:

            messagebox.showerror(
                "Connection Error",
                "Cannot connect to Django server.\n\n"
                "Make sure Django is running."
            )

            return

        except requests.exceptions.Timeout:

            messagebox.showerror(
                "Connection Error",
                "Server request timed out."
            )

            return

        except requests.exceptions.RequestException as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

            return

        # -------------------------------------------------
        # Success
        # -------------------------------------------------

        if response.status_code in [200, 201]:

            messagebox.showinfo(
                "Register",
                "Registration successful!\n\n"
                "You can now login."
            )

            show_login()

        else:

            error = get_api_error(response)

            messagebox.showerror(
                "Registration Failed",
                error
            )

    # -----------------------------------------------------
    # Button
    # -----------------------------------------------------

    button(
        auth_card,
        "REGISTER",
        register
    ).pack(
        pady=5
    )

    auth_card.bind_all(
        "<Return>",
        lambda event: register()
    )


# =========================================================
# PROFILE WINDOW
# =========================================================
def show_new_password_window(uid, token):


    window = tk.Toplevel(root)

    window.title("New Password")

    window.geometry("450x350")

    window.configure(bg=BG)



    card = tk.Frame(
        window,
        bg=CARD,
        width=400,
        height=300,
        highlightbackground=BORDER,
        highlightthickness=2
    )

    card.pack(
        padx=25,
        pady=25
    )

    card.pack_propagate(False)



    title_label(
        card,
        "SET NEW PASSWORD",
        18
    ).pack(
        pady=25
    )



    label(
        card,
        "New password"
    ).pack(
        anchor="w",
        padx=30
    )


    password = entry(
        card,
        show="*"
    )

    password.pack(
        fill="x",
        padx=30,
        pady=5
    )



    label(
        card,
        "Confirm password"
    ).pack(
        anchor="w",
        padx=30
    )


    confirm = entry(
        card,
        show="*"
    )

    confirm.pack(
        fill="x",
        padx=30,
        pady=5
    )




    def change_password():


        if password.get() != confirm.get():

            messagebox.showerror(
                "Error",
                "Passwords do not match."
            )

            return



        url = (
            RESET_CONFIRM_URL
            + f"{uid}/{token}/"
        )



        try:

            response = requests.post(
                url,
                json={
                    "password": password.get(),
                    "confirm_password": confirm.get()
                },
                timeout=10
            )


        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

            return




        if response.status_code == 200:


            messagebox.showinfo(
                "Success",
                "Password changed successfully."
            )


            window.destroy()



        else:

            messagebox.showerror(
                "Failed",
                get_api_error(response)
            )



    button(
        card,
        "CHANGE PASSWORD",
        change_password
    ).pack(
        pady=20
    )
def show_profile_window():

    profile_window = tk.Toplevel(root)

    profile_window.title("User Profile")
    profile_window.geometry("750x800")
    profile_window.configure(bg=BG)
    profile_window.resizable(False, False)

    # =====================================================
    # API URLs
    # =====================================================

    PROFILE_URL = (
        "http://127.0.0.1:8000/api/v1/accounts/profile/"
    )

    CHANGE_PASSWORD_URL = (
        "http://127.0.0.1:8000/api/v1/accounts/change-password/"
    )

    SERVICES_URL = (
        "http://127.0.0.1:8000/api/v1/services/"
    )

    # =====================================================
    # Main Card
    # =====================================================

    profile_card = tk.Frame(
        profile_window,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=2,
        width=650,
        height=700
    )

    profile_card.pack(
        padx=50,
        pady=50
    )

    profile_card.pack_propagate(False)

    # =====================================================
    # GET PROFILE
    # =====================================================

    def get_profile():

        if not token:

            messagebox.showerror(
                "Authentication Error",
                "You are not logged in."
            )

            return None

        headers = {
            "Authorization": f"Token {token}"
        }

        try:

            response = requests.get(
                PROFILE_URL,
                headers=headers,
                timeout=10
            )

        except requests.exceptions.ConnectionError:

            messagebox.showerror(
                "Connection Error",
                "Cannot connect to Django server."
            )

            return None

        except requests.exceptions.Timeout:

            messagebox.showerror(
                "Connection Error",
                "Server request timed out."
            )

            return None

        except requests.exceptions.RequestException as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

            return None

        if response.status_code == 200:

            return response.json()

        messagebox.showerror(
            "Profile Error",
            get_api_error(response)
        )

        return None

    # =====================================================
    # PROFILE TAB
    # =====================================================

    def show_profile():

        clear_frame(profile_card)

        # -------------------------------------------------
        # Tabs
        # -------------------------------------------------

        tabs = tk.Frame(
            profile_card,
            bg=CARD
        )

        tabs.pack(
            fill="x",
            pady=(15, 20)
        )

        profile_tab = tk.Button(
            tabs,
            text="PROFILE",
            bg=BUTTON,
            fg=WHITE,
            relief="solid",
            bd=1,
            font=("Arial", 10, "bold"),
            command=show_profile
        )

        profile_tab.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(10, 2)
        )

        data_tab = tk.Button(
            tabs,
            text="DATA",
            bg=CARD,
            fg=GRAY,
            relief="solid",
            bd=1,
            font=("Arial", 10, "bold"),
            command=show_data
        )

        data_tab.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(2, 10)
        )

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title_label(
            profile_card,
            "PROFILE",
            22
        ).pack(
            pady=(5, 20)
        )

        # -------------------------------------------------
        # Profile
        # -------------------------------------------------

        profile = get_profile()

        if profile is None:
            return

        username_value = profile.get("username") or "-"
        email_value = profile.get("email") or "-"
        first_name_value = profile.get("first_name") or "-"
        last_name_value = profile.get("last_name") or "-"
        phone_value = profile.get("phone") or "-"

        # -------------------------------------------------
        # User Information
        # -------------------------------------------------

        info_frame = tk.Frame(
            profile_card,
            bg=CARD
        )

        info_frame.pack(
            fill="x",
            padx=35
        )

        label(
            info_frame,
            f"Username: {username_value}"
        ).pack(
            anchor="w",
            pady=3
        )

        label(
            info_frame,
            f"Email: {email_value}"
        ).pack(
            anchor="w",
            pady=3
        )

        label(
            info_frame,
            f"First name: {first_name_value}"
        ).pack(
            anchor="w",
            pady=3
        )

        label(
            info_frame,
            f"Last name: {last_name_value}"
        ).pack(
            anchor="w",
            pady=3
        )

        label(
            info_frame,
            f"Phone: {phone_value}"
        ).pack(
            anchor="w",
            pady=3
        )

        # =================================================
        # CHANGE PASSWORD
        # =================================================

        tk.Label(
            profile_card,
            text="CHANGE PASSWORD",
            bg=CARD,
            fg=WHITE,
            font=("Arial", 14, "bold")
        ).pack(
            pady=(15, 10)
        )

        label(
            profile_card,
            "Old password"
        ).pack(
            anchor="w",
            padx=35
        )

        old_password = entry(
            profile_card,
            show="*"
        )

        old_password.pack(
            fill="x",
            padx=35,
            pady=(3, 7)
        )

        label(
            profile_card,
            "New password"
        ).pack(
            anchor="w",
            padx=35
        )

        new_password = entry(
            profile_card,
            show="*"
        )

        new_password.pack(
            fill="x",
            padx=35,
            pady=(3, 7)
        )

        label(
            profile_card,
            "Confirm new password"
        ).pack(
            anchor="w",
            padx=35
        )

        confirm_password = entry(
            profile_card,
            show="*"
        )

        confirm_password.pack(
            fill="x",
            padx=35,
            pady=(3, 10)
        )

        # =================================================
        # CHANGE PASSWORD FUNCTION
        # =================================================

        def change_password():

            old_password_value = old_password.get()

            new_password_value = new_password.get()

            confirm_password_value = confirm_password.get()

            if not old_password_value:

                messagebox.showwarning(
                    "Password",
                    "Please enter your old password."
                )

                return

            if not new_password_value:

                messagebox.showwarning(
                    "Password",
                    "Please enter your new password."
                )

                return

            if new_password_value != confirm_password_value:

                messagebox.showerror(
                    "Password",
                    "Passwords do not match."
                )

                return

            payload = {
                "old_password": old_password_value,
                "new_password": new_password_value,
                "conf_password": confirm_password_value
            }

            headers = {
                "Authorization": f"Token {token}"
            }

            try:

                response = requests.post(
                    CHANGE_PASSWORD_URL,
                    json=payload,
                    headers=headers,
                    timeout=10
                )

            except requests.exceptions.RequestException as e:

                messagebox.showerror(
                    "Error",
                    str(e)
                )

                return

            if response.status_code in [200, 201, 204]:

                messagebox.showinfo(
                    "Success",
                    "Password changed successfully."
                )

                old_password.delete(0, tk.END)
                new_password.delete(0, tk.END)
                confirm_password.delete(0, tk.END)

            else:

                messagebox.showerror(
                    "Password Change Failed",
                    get_api_error(response)
                )

        button(
            profile_card,
            "CHANGE PASSWORD",
            change_password
        ).pack(
            pady=5
        )

    # =====================================================
    # DATA TAB
    # =====================================================

    def show_data():

        clear_frame(profile_card)

        # -------------------------------------------------
        # Tabs
        # -------------------------------------------------

        tabs = tk.Frame(
            profile_card,
            bg=CARD
        )

        tabs.pack(
            fill="x",
            pady=(15, 20)
        )

        profile_tab = tk.Button(
            tabs,
            text="PROFILE",
            bg=CARD,
            fg=GRAY,
            relief="solid",
            bd=1,
            font=("Arial", 10, "bold"),
            command=show_profile
        )

        profile_tab.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(10, 2)
        )

        data_tab = tk.Button(
            tabs,
            text="DATA",
            bg=BUTTON,
            fg=WHITE,
            relief="solid",
            bd=1,
            font=("Arial", 10, "bold"),
            command=show_data
        )

        data_tab.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(2, 10)
        )

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        title_label(
            profile_card,
            "SERVICES",
            22
        ).pack(
            pady=(5, 15)
        )

        # -------------------------------------------------
        # Services Panel
        # -------------------------------------------------

        data_frame = tk.Frame(
            profile_card,
            bg="#222222"
        )

        data_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(5, 20)
        )

        scrollbar = tk.Scrollbar(
            data_frame
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        data_text = tk.Text(
            data_frame,
            bg="#222222",
            fg=WHITE,
            insertbackground=WHITE,
            font=("Arial", 10),
            relief="flat",
            yscrollcommand=scrollbar.set,
            wrap="word"
        )

        data_text.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        scrollbar.config(
            command=data_text.yview
        )

        data_text.insert(
            tk.END,
            "Loading services..."
        )

        # =================================================
        # GET SERVICES
        # =================================================

        def load_services():

            headers = {}

            if token:

                headers["Authorization"] = (
                    f"Token {token}"
                )

            try:

                response = requests.get(
                    SERVICES_URL,
                    headers=headers,
                    timeout=10
                )

            except requests.exceptions.RequestException as e:

                data_text.delete(
                    "1.0",
                    tk.END
                )

                data_text.insert(
                    tk.END,
                    str(e)
                )

                return

            if response.status_code == 200:

                try:

                    data = response.json()

                except Exception:

                    data = response.text

                data_text.delete(
                    "1.0",
                    tk.END
                )

                if isinstance(data, list):

                    for index, service in enumerate(
                        data,
                        start=1
                    ):

                        data_text.insert(
                            tk.END,
                            f"Service {index}\n"
                        )

                        if isinstance(service, dict):

                            for key, value in service.items():

                                data_text.insert(
                                    tk.END,
                                    f"{key}: {value}\n"
                                )

                        else:

                            data_text.insert(
                                tk.END,
                                str(service)
                            )

                        data_text.insert(
                            tk.END,
                            "\n" + "-" * 45 + "\n\n"
                        )

                elif isinstance(data, dict):

                    for key, value in data.items():

                        data_text.insert(
                            tk.END,
                            f"{key}: {value}\n\n"
                        )

                else:

                    data_text.insert(
                        tk.END,
                        str(data)
                    )

            else:

                data_text.delete(
                    "1.0",
                    tk.END
                )

                data_text.insert(
                    tk.END,
                    f"Error {response.status_code}\n\n"
                    f"{get_api_error(response)}"
                )

        load_services()

    # =====================================================
    # Start Profile
    # =====================================================

    show_profile()

    # =====================================================
    # Close Window
    # =====================================================

    def on_close():

        global token
        global current_user

        token = None
        current_user = None

        profile_window.destroy()

        root.deiconify()

        show_login()

    profile_window.protocol(
        "WM_DELETE_WINDOW",
        on_close
    )


# =========================================================
# START
# =========================================================

show_login()

root.mainloop()