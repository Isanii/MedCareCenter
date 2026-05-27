loadAppointments();
const modal =
    new bootstrap.Modal(
        document.getElementById(
            "appointmentModal"
        )
    );

document
.getElementById(
    "addAppointmentBtn"
)
.addEventListener(
    "click",
    async () => {

        await loadPatientsSelect();

        await loadDoctorsSelect();

        modal.show();
    }
);

document
.getElementById(
    "saveAppointmentBtn"
)
.addEventListener(
    "click",
    createAppointment
);


async function loadAppointments() {

    const response =
        await fetch(
            `${API_BASE}/appointments`,
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
                                appointment.status === "completed"
                                    ? "bg-success"
                                :
                                appointment.status === "confirmed"
                                    ? "bg-info"
                                :
                                appointment.status === "cancelled"
                                    ? "bg-danger"
                                :
                                    "bg-warning"
                            }
                        ">

                        ${appointment.status}

                    </span>

                </td>

                <td>
                    ${appointment.note ?? ""}
                </td>

                <td>

                    ${
                        appointment.status ===
                        "pending"

                        ||

                        appointment.status ===
                        "confirmed"

                        ?

                        `
                        <button
                            class="btn btn-sm btn-danger"
                            onclick="
                                cancelAppointment(
                                    ${appointment.id}
                                )
                            ">
                            Hủy
                        </button>
                        `

                        :

                        ""
                    }

                </td>

                <td>

                    <select
                        class="form-select form-select-sm"

                        onchange="
                            updateStatus(
                                ${appointment.id},
                                this.value
                            )
                        ">

                        <option
                            value="pending"
                            ${
                                appointment.status ===
                                "pending"
                                ?
                                "selected"
                                :
                                ""
                            }>
                            Pending
                        </option>

                        <option
                            value="confirmed"
                            ${
                                appointment.status ===
                                "confirmed"
                                ?
                                "selected"
                                :
                                ""
                            }>
                            Confirmed
                        </option>

                        <option
                            value="completed"
                            ${
                                appointment.status ===
                                "completed"
                                ?
                                "selected"
                                :
                                ""
                            }>
                            Completed
                        </option>

                        <option
                            value="cancelled"
                            ${
                                appointment.status ===
                                "cancelled"
                                ?
                                "selected"
                                :
                                ""
                            }>
                            Cancelled
                        </option>

                    </select>

                </td>

            </tr>
            `;
        }
    );
}



async function updateStatus(
    appointmentId,
    status
) {

    const response =
        await fetch(
            `${API_BASE}/appointments/${appointmentId}/status`,
            {
                method: "PATCH",

                headers: {
                    Authorization:
                        `Bearer ${token}`,

                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(
                        {
                            status
                        }
                    )
            }
        );

    if (
        response.ok
    ) {

        loadAppointments();
    }

    else {

        const error =
            await response.json();

        alert(
            error.detail
        );
    }
}


async function loadPatientsSelect() {

    const response =
        await fetch(
            `${API_BASE}/patients?skip=0&limit=100`,
            {
                headers: {
                    Authorization:
                        `Bearer ${token}`
                }
            }
        );

    const patients =
        await response.json();

    const select =
        document.getElementById(
            "patientId"
        );

    select.innerHTML =
        "";

    patients.forEach(
        patient => {

            select.innerHTML += `
                <option
                    value="${patient.id}">
                    ${patient.fullname}
                </option>
            `;
        }
    );
}



async function loadDoctorsSelect() {

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

async function createAppointment() {

    const data = {

        patient_id:
            Number(
                document
                .getElementById(
                    "patientId"
                )
                .value
            ),

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
            `${API_BASE}/appointments`,
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
            "Tạo lịch hẹn thành công"
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



async function cancelAppointment(
    appointmentId
) {

    if (
        !confirm(
            "Bạn có chắc muốn hủy lịch?"
        )
    ) {
        return;
    }

    const response =
        await fetch(
            `${API_BASE}/appointments/${appointmentId}/status`,
            {
                method: "PATCH",

                headers: {
                    Authorization:
                        `Bearer ${token}`,

                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify({
                        status:
                            "cancelled"
                    })
            }
        );

    if (
        response.ok
    ) {

        loadAppointments();

        alert(
            "Đã hủy lịch hẹn"
        );
    }

    else {

        alert(
            "Không thể hủy lịch"
        );
    }
}