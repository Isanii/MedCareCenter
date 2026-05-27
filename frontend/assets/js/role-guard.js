const currentPage =
    window.location.pathname
    .split("/")
    .pop();


// Không kiểm tra ở trang login
if (
    currentPage === "login.html"
) {

    console.log(
        "Skip role guard"
    );

}
else {

    const token =
        localStorage.getItem(
            "token"
        );

    if (!token) {

        location.href =
            "login.html";
    }

    (async () => {

        try {

            const response =
                await fetch(
                    `${API_BASE}/auth/me`,
                    {
                        headers: {
                            Authorization:
                                `Bearer ${token}`
                        }
                    }
                );

            if (!response.ok) {

                localStorage.removeItem(
                    "token"
                );

                location.href =
                    "login.html";

                return;
            }

            const user =
                await response.json();

            const role =
                user.role
                .toLowerCase();

            const path =
                window.location.pathname
                .split("/")
                .pop();

            console.log(
                "ROLE =",
                role
            );

            console.log(
                "PAGE =",
                path
            );

            const adminPages = [

                "dashboard.html",
                "patients.html",
                "doctors.html",
                "appointments.html",
                "invoices.html",
                "medical-records.html"
            ];

            const doctorPages = [

                "doctor-dashboard.html",
                "doctor-appointments.html",
                "doctor-medical-records.html",
                "doctor-medical-record.html",
                "doctor-record-detail.html",
                "doctor-record-edit.html"
            ];

            const patientPages = [

                "patient-dashboard.html",
                "my-appointments.html",
                "my-medical-records.html",
                "my-invoices.html"
            ];


            // ======================
            // ADMIN
            // ======================

            if (
                role === "admin"
            ) {

                return;
            }


            // ======================
            // DOCTOR
            // ======================

            if (
                role === "doctor"
            ) {

                if (

                    adminPages.includes(
                        path
                    )

                    ||

                    patientPages.includes(
                        path
                    )

                ) {

                    location.href =
                        "doctor-dashboard.html";
                }

                return;
            }


            // ======================
            // PATIENT
            // ======================

            if (
                role === "patient"
            ) {

                if (

                    adminPages.includes(
                        path
                    )

                    ||

                    doctorPages.includes(
                        path
                    )

                ) {

                    location.href =
                        "patient-dashboard.html";
                }

                return;
            }

        }

        catch (error) {

            console.error(
                error
            );

            localStorage.removeItem(
                "token"
            );

            location.href =
                "login.html";
        }

    })();
}