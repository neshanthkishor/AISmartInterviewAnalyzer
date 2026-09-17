const API_BASE = "http://127.0.0.1:8000";

const loginForm = document.getElementById("loginForm");

const errorMessage = document.getElementById("errorMessage");
const successMessage = document.getElementById("successMessage");

const loginButton = document.getElementById("loginButton");
const buttonText = document.getElementById("buttonText");
const buttonLoader = document.getElementById("buttonLoader");


function showError(message) {
    if (!errorMessage) return;

    errorMessage.textContent = message;
    errorMessage.style.display = "block";

    if (successMessage) {
        successMessage.style.display = "none";
    }
}


function showSuccess(message) {
    if (!successMessage) return;

    successMessage.textContent = message;
    successMessage.style.display = "block";

    if (errorMessage) {
        errorMessage.style.display = "none";
    }
}


function clearMessages() {
    if (errorMessage) {
        errorMessage.style.display = "none";
    }

    if (successMessage) {
        successMessage.style.display = "none";
    }
}


function setLoading(isLoading) {

    if (!loginButton) return;

    loginButton.disabled = isLoading;

    if (isLoading) {

        if (buttonText) {
            buttonText.textContent = "Signing in...";
        }

        if (buttonLoader) {
            buttonLoader.style.display = "inline-block";
        }

    } else {

        if (buttonText) {
            buttonText.textContent = "Sign In";
        }

        if (buttonLoader) {
            buttonLoader.style.display = "none";
        }
    }
}


if (loginForm) {

    loginForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        clearMessages();

        const email =
            document.getElementById("email").value.trim();

        const password =
            document.getElementById("password").value;


        if (!email || !password) {

            showError(
                "Please enter your email and password."
            );

            return;
        }


        setLoading(true);


        try {

            const response = await fetch(
                `${API_BASE}/api/auth/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                }
            );


            let data;

            try {
                data = await response.json();
            } catch {
                data = {};
            }


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Invalid email or password."
                );
            }


            /*
             * Store authentication information
             */

            localStorage.setItem(
                "access_token",
                data.access_token
            );


            localStorage.setItem(
                "user",
                JSON.stringify(data.user)
            );


            showSuccess(
                "Login successful. Redirecting..."
            );


            setTimeout(() => {

                window.location.href =
                    "dashboard.html";

            }, 800);


        } catch (error) {

            console.error(
                "Login Error:",
                error
            );


            if (
                error.message.includes(
                    "Failed to fetch"
                )
            ) {

                showError(
                    "Backend connection failed. Please make sure FastAPI is running."
                );

            } else {

                showError(
                    error.message
                );
            }

        } finally {

            setLoading(false);
        }

    });
}


/*
 * Show / Hide Password
 */

function togglePassword() {

    const passwordInput =
        document.getElementById("password");

    if (!passwordInput) {
        return;
    }


    if (
        passwordInput.type === "password"
    ) {

        passwordInput.type = "text";

    } else {

        passwordInput.type = "password";
    }
}


/*
 * Forgot Password
 */

function showForgotMessage(event) {

    event.preventDefault();

    showError(
        "Password recovery will be added in the next authentication update."
    );
}