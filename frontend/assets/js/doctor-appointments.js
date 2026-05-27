
loadAppointments();

async function loadAppointments() {

    const response =
        await fetch(
            `${API_BASE}/appointments/my-doctor`,
            {
                headers: {
                    Authorization:
                        `Bearer ${token}`
                }
            }
        );

    if (!response.ok) {

        alert(
            "Không tải được lịch khám"
        );

        return;
    }

    const appointments =
        await response.json();

    renderAppointments(
        appointments
    );
}

function renderAppointments(
    appointments
) {

    const table =
        document.getElementById(
            "appointmentTable"
        );

    table.innerHTML = "";

    appointments.forEach(
        appointment => {

            table.innerHTML += `
            <tr>

                <td>
                    ${appointment.id}
                </td>

                <td>
                    ${appointment.patient_name}
                </td>

                <td>
                    ${new Date(
                        appointment.appointment_time
                    ).toLocaleString(
                        "vi-VN"
                    )}
                </td>

                <td>
                    ${appointment.status}
                </td>

                <td>
                    ${appointment.note ?? ""}
                </td>

                <td>

                    <button
                        class="btn btn-primary btn-sm"
                        onclick="
                            openMedicalRecord(
                                ${appointment.id}
                            )
                        ">

                        Bệnh án

                    </button>

                </td>

            </tr>
            `;
        }
    );
}

function openMedicalRecord(
    appointmentId
) {

    localStorage.setItem(
        "appointment_id",
        appointmentId
    );

    location.href =
        "doctor-medical-record.html";
}