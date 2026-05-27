async function sendOtp() {

    const email =
        document
        .getElementById(
            "email"
        )
        .value;

    console.log("EMAIL =", email);

    const response =
        await fetch(
            `${API_BASE}/auth/forgot-password?email=${email}`,
            {
                method: "POST"
            }
        );

    console.log(
        "STATUS =",
        response.status
    );

    const data =
        await response.json();

    console.log(data);

    document
    .getElementById(
        "message"
    )
    .innerText =
        data.message;
}

async function resetPassword() {

    const email =
        document
        .getElementById(
            "email"
        )
        .value;

    const otp =
        document
        .getElementById(
            "otp"
        )
        .value;

    const newPassword =
        document
        .getElementById(
            "newPassword"
        )
        .value;

    const response =
        await fetch(
            `${API_BASE}/auth/reset-password`
            + `?email=${email}`
            + `&otp=${otp}`
            + `&new_password=${newPassword}`,
            {
                method: "POST"
            }
        );

    const data =
        await response.json();

    if (
        response.ok
    ) {

        alert(
            "Đổi mật khẩu thành công"
        );

        location.href =
            "login.html";
    }

    else {

        alert(
            data.detail
        );
    }
}