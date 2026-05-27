const form =
    document.getElementById(
        "loginForm"
    );

form.addEventListener(
    "submit",
    async (e) => {

        e.preventDefault();

        const email =
            document.getElementById(
                "email"
            ).value;

        const password =
            document.getElementById(
                "password"
            ).value;

        try {

            const response =
                await fetch(
                    `${API_BASE}/auth/login`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            email,
                            password
                        })
                    }
                );

            const data =
                await response.json();

            if (!response.ok) {

                throw new Error(
                    data.detail
                );
            }

            localStorage.setItem(
                "token",
                data.access_token
            );

            const meResponse =
                await fetch(
                    `${API_BASE}/auth/me`,
                    {
                        headers: {
                            Authorization:
                                `Bearer ${data.access_token}`
                        }
                    }
                );

            const user =
                await meResponse.json();

            if (
                user.role === "admin"
            ) {

                window.location.href =
                    "dashboard.html";
            }
            else if (
                user.role === "doctor"
            ) {

                window.location.href =
                    "doctor-dashboard.html";
            }
            else if (
                user.role === "patient"
            ) {

                window.location.href =
                    "patient-dashboard.html";
            }
            else if (
                data.role ===
                "receptionist"
            ) {

                window.location.href =
                    "receptionist-dashboard.html";
            }
            else {

                window.location.href =
                    "index.html";
            }

        }

        catch (error) {

            document.getElementById(
                "message"
            ).innerText =
                error.message;
        }
    }
);