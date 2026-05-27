loadDashboard();

async function loadDashboard() {

    const headers = {
        Authorization:
            `Bearer ${token}`
    };

    const [
        appointmentsRes,
        recordsRes,
        invoicesRes
    ] = await Promise.all([

        fetch(
            `${API_BASE}/appointments/my`,
            { headers }
        ),

        fetch(
            `${API_BASE}/medical-records/my`,
            { headers }
        ),

        fetch(
            `${API_BASE}/invoices/my`,
            { headers }
        )

    ]);

    const appointments =
        await appointmentsRes.json();

    const records =
        await recordsRes.json();

    const invoices =
        await invoicesRes.json();

    document
    .getElementById(
        "totalAppointments"
    )
    .innerText =
        appointments.length;

    document
    .getElementById(
        "pendingAppointments"
    )
    .innerText =
        appointments.filter(
            x =>
                x.status ===
                "pending"
        ).length;

    document
    .getElementById(
        "completedAppointments"
    )
    .innerText =
        appointments.filter(
            x =>
                x.status ===
                "completed"
        ).length;

    document
    .getElementById(
        "recordCount"
    )
    .innerText =
        records.length;

    document
    .getElementById(
        "invoiceCount"
    )
    .innerText =
        invoices.length;

    document
    .getElementById(
        "paidInvoiceCount"
    )
    .innerText =
        invoices.filter(
            x =>
                String(
                    x.payment_status
                )
                .toLowerCase()
                .includes(
                    "paid"
                )
        ).length;
}