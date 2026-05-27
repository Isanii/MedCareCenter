let modal = null;

document.addEventListener(
    "DOMContentLoaded",
    () => {

        modal =
            new bootstrap.Modal(
                document.getElementById(
                    "appointmentModal"
                )
            );
    }
);

document
.getElementById(
    "addAppointmentBtn"
)
.addEventListener(
    "click",
    async () => {

        await loadDoctors();

        modal.show();
    }
);
loadAppointments();

async function loadAppointments() {

    const response =
        await fetch(
            `${API_BASE}/appointments/my`,
            {
                headers: {
                    Authorization:
                        `Bearer ${token}`
                }
            }
        );

    const appointments =
        await response.json();

    renderAppointments(
        appointments
    );
}

async function loadDoctors() {

    const response =
        await fetch(
            `${API_BASE}/doctors?skip=0&limit=100`,
            {
                headers: {
                    Authorization:
                        `Bearer ${token}`
                }
            }
        );

    const doctors =
        await response.json();

    const select =
        document.getElementById(
            "doctorId"
        );

    select.innerHTML =
        "";

    doctors.forEach(
        doctor => {

            select.innerHTML += `
                <option
                    value="${doctor.id}">
                    ${doctor.fullname}
                    (${doctor.specialty})
                </option>
            `;
        }
    );
}
document
.getElementById(
    "saveAppointmentBtn"
)
.addEventListener(
    "click",
    createAppointment
);

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
                    ${appointment.doctor_name}
                </td>

                <td>
                    ${new Date(
                        appointment.appointment_time
                    ).toLocaleString(
                        "vi-VN"
                    )}
                </td>

                <td>

                    <span
                        class="
                        badge
                        ${
                            appointment.status ===
                            "completed"
                            ?
                            "bg-success"
                            :
                            appointment.status ===
                            "cancelled"
                            ?
                            "bg-danger"
                            :
                            appointment.status ===
                            "confirmed"
                            ?
                            "bg-info"
                            :
                            "bg-warning"
                        }">

                        ${appointment.status}

                    </span>

                </td>

                <td>
                    ${appointment.note ?? ""}
                </td>

            </tr>
            `;
        }
    );
}
async function createAppointment() {

    const data = {

        doctor_id:
            Number(
                document
                .getElementById(
                    "doctorId"
                )
                .value
            ),

        appointment_time:
            document
            .getElementById(
                "appointmentTime"
            )
            .value,

        note:
            document
            .getElementById(
                "note"
            )
            .value
    };

    const response =
        await fetch(
            `${API_BASE}/appointments/my`,
            {
                method: "POST",

                headers: {
                    Authorization:
                        `Bearer ${token}`,

                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(
                        data
                    )
            }
        );

    if (
        response.ok
    ) {

        modal.hide();

        loadAppointments();

        alert(
            "Đặt lịch thành công"
        );
    }

    else {

        const error =
            await response.json();

        alert(
            error.detail
        );
    }
}