const authToken =
    localStorage.getItem(
        "token"
    );

loadUser();
loadStats();

async function loadUser() {

    const response =
        await fetch(
            `${API_BASE}/auth/me`,
            {
                headers: {
                    Authorization:
                        `Bearer ${authToken}`
                }
            }
        );

    const user =
        await response.json();

    document
    .getElementById(
        "userInfo"
    )
    .innerHTML = `

        <h5>
            ${user.fullname}
        </h5>

        <p>
            Email:
            ${user.email}
        </p>

        <p>
            Vai trò:
            ${user.role}
        </p>

    `;
}

async function loadStats() {

    try {

        const response =
            await fetch(
                `${API_BASE}/dashboard`,
                {
                    headers: {
                        Authorization:
                            `Bearer ${authToken}`
                    }
                }
            );

        if (!response.ok) {
            return;
        }

        const data =
            await response.json();

        document
        .getElementById(
            "patientCount"
        )
        .innerText =
            data.total_patients || 0;

        document
        .getElementById(
            "todayAppointmentCount"
        )
        .innerText =
            data.total_appointments || 0;

        document
        .getElementById(
            "pendingAppointmentCount"
        )
        .innerText =
            data.pending_appointments || 0;

        document
        .getElementById(
            "invoiceCount"
        )
        .innerText =
            data.total_invoices || 0;

    }

    catch (error) {

        console.error(
            error
        );
    }
}

document
.getElementById(
    "logoutBtn"
)
.addEventListener(
    "click",
    () => {

        localStorage.removeItem(
            "token"
        );

        location.href =
            "login.html";
    }
);