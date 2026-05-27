async function register() {

    const fullname =
        document
        .getElementById(
            "fullname"
        )
        .value;

    const email =
        document
        .getElementById(
            "email"
        )
        .value;

    const phone =
        document
        .getElementById(
            "phone"
        )
        .value;

    const password =
        document
        .getElementById(
            "password"
        )
        .value;

    const response =
        await fetch(
            `${API_BASE}/auth/register`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(
                    {
                        fullname,
                        email,
                        phone,
                        password,
                        role: "patient"
                    }
                )
            }
        );

    const data =
        await response.json();

    if (
        response.ok
    ) {

        alert(
            "Đăng ký thành công"
        );

        location.href =
            "login.html";
    }

    else {

        const message =
            document.getElementById(
                "message"
            );

        message.classList.remove(
            "d-none"
        );

        message.innerText =
            data.detail ||
            "Email đã tồn tại";
    }
}