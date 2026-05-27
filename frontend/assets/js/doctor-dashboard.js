

loadDashboard();

async function loadDashboard() {

    const response =
        await fetch(
            `${API_BASE}/dashboard/doctor`,
            {
                headers: {
                    Authorization:
                        `Bearer ${token}`
                }
            }
        );

    if (!response.ok) {

        alert(
            "Không tải được Dashboard"
        );

        return;
    }

    const stats =
        await response.json();

    document
    .getElementById(
        "appointmentCount"
    )
    .innerText =
        stats.appointment_count;

    document
    .getElementById(
        "pendingCount"
    )
    .innerText =
        stats.pending_count;

    document
    .getElementById(
        "completedCount"
    )
    .innerText =
        stats.completed_count;

    document
    .getElementById(
        "recordCount"
    )
    .innerText =
        stats.record_count;
}