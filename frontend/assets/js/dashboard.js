const authToken =
    localStorage.getItem(
        "token"
    );

fetch(
    `${API_BASE}/dashboard`,
    {
        headers: {
            Authorization:
                `Bearer ${authToken}`
        }
    }
)
.then(
    response => response.json()
)
.then(
    data => {

        document.getElementById(
            "doctorCount"
        ).innerText =
            data.total_doctors;

        document.getElementById(
            "patientCount"
        ).innerText =
            data.total_patients;

        document.getElementById(
            "appointmentCount"
        ).innerText =
            data.total_appointments;

        document.getElementById(
            "invoiceCount"
        ).innerText =
            data.total_invoices;

        document.getElementById(
            "paidInvoiceCount"
        ).innerText =
            data.paid_invoices;

        document.getElementById(
            "revenueCount"
        ).innerText =
            Number(
                data.total_revenue
            ).toLocaleString(
                "vi-VN"
            ) + " VNĐ";
    }
);