import json
import urllib.request
import urllib.error


API_URL = "http://127.0.0.1:8000/api/auth/register"

DEMO_FULL_NAME = "Demo User"
DEMO_EMAIL = "demo@interviewiq.com"
DEMO_PASSWORD = "Demo@12345"


data = {
    "full_name": DEMO_FULL_NAME,
    "email": DEMO_EMAIL,
    "password": DEMO_PASSWORD
}


print()
print("========================================")
print("       INTERVIEWIQ DEMO ACCOUNT")
print("========================================")
print()
print("Creating demo account...")
print()


try:

    payload = json.dumps(data).encode("utf-8")

    request = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(request) as response:

        result = response.read().decode("utf-8")

        print("Demo account created successfully!")
        print()

        try:

            print(
                json.dumps(
                    json.loads(result),
                    indent=2
                )
            )

        except:

            print(result)


except urllib.error.HTTPError as error:

    response_text = error.read().decode("utf-8")

    print("Server response:")
    print()

    try:

        result = json.loads(response_text)

        print(
            json.dumps(
                result,
                indent=2
            )
        )

    except:

        print(response_text)


    print()

    if error.code == 400 or error.code == 409:

        print(
            "The demo account may already exist."
        )

    elif error.code == 422:

        print(
            "The registration data was rejected."
        )

    else:

        print(
            "HTTP Error:",
            error.code
        )


except urllib.error.URLError:

    print("Could not connect to the backend.")
    print()
    print(
        "Make sure Uvicorn is running:"
    )
    print()
    print(
        "python -m uvicorn backend.main:app --reload"
    )


except Exception as error:

    print("Unexpected error:")
    print(error)


print()
print("----------------------------------------")
print(" DEMO LOGIN DETAILS")
print("----------------------------------------")
print()
print("Name     :", DEMO_FULL_NAME)
print("Email    :", DEMO_EMAIL)
print("Password :", DEMO_PASSWORD)
print()
print("Login URL:")
print("http://127.0.0.1:8000/login.html")
print()
print("========================================")