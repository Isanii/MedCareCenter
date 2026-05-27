
const modal =
    new bootstrap.Modal(
        document.getElementById(
            "recordModal"
        )
    );

let editingId = null;

document
.getElementById(
    "addRecordBtn"
)
.addEventListener(
    "click",
    async () => {

        editingId = null;

        document
        .getElementById(
            "recordForm"
        )
        .reset();

        await loadAppointments();

        modal.show();
    }
);

document
.getElementById(
    "saveRecordBtn"
)
.addEventListener(
    "click",
    saveRecord
);

loadRecords();

async function loadRecords() {

    const response =
        await fetch(
            `${API_BASE}/medical-records`,
            {
                headers: {
                    Authorization:
                        `Bearer ${token}`
                }
            }
        );

    const records =
        await response.json();

    renderRecords(
        records
    );
}

function renderRecords(
    records
) {

    const table =
        document.getElementById(
            "recordTable"
        );

    table.innerHTML = "";

    records.forEach(
        record => {

            table.innerHTML += `
            <tr>

                <td>
                    ${record.id}
                </td>

                <td>
                    ${record.appointment_id}
                </td>

                <td>
                    ${record.symptoms ?? ""}
                </td>

                <td>
                    ${record.diagnosis ?? ""}
                </td>

                <td>
                    ${record.prescription ?? ""}
                </td>

                <td>
                    ${record.doctor_note ?? ""}
                </td>

                <td>
                    ${new Date(
                        record.created_at
                    ).toLocaleString(
                        "vi-VN"
                    )}
                </td>

                <td>

                    <button
                        class="btn btn-warning btn-sm"
                        onclick="
                            editRecord(
                                ${record.id}
                            )
                        ">
                        Sửa
                    </button>

                    <button
                        class="btn btn-danger btn-sm"
                        onclick="
                            deleteRecord(
                                ${record.id}
                            )
                        ">
                        Xóa
                    </button>

                </td>

            </tr>
            `;
        }
    );
}

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

    const select =
        document.getElementById(
            "appointmentId"
        );

    select.innerHTML = "";

    appointments.forEach(
        appointment => {

            select.innerHTML += `
            <option
                value="${appointment.id}">
                #${appointment.id}
                -
                ${appointment.patient_name}
                -
                ${appointment.doctor_name}
            </option>
            `;
        }
    );
}

async function saveRecord() {

    const data = {

        appointment_id:
            Number(
                document
                .getElementById(
                    "appointmentId"
                )
                .value
            ),

        symptoms:
            document
            .getElementById(
                "symptoms"
            )
            .value,

        diagnosis:
            document
            .getElementById(
                "diagnosis"
            )
            .value,

        prescription:
            document
            .getElementById(
                "prescription"
            )
            .value,

        doctor_note:
            document
            .getElementById(
                "doctorNote"
            )
            .value
    };

    let url =
        `${API_BASE}/medical-records`;

    let method =
        "POST";

    if (
        editingId
    ) {

        url =
            `${API_BASE}/medical-records/${editingId}`;

        method =
            "PUT";
    }

    const response =
        await fetch(
            url,
            {
                method,

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

        loadRecords();

        alert(
            editingId
            ?
            "Cập nhật thành công"
            :
            "Tạo bệnh án thành công"
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

async function editRecord(
    recordId
) {

    const response =
        await fetch(
            `${API_BASE}/medical-records/${recordId}`,
            {
                headers: {
                    Authorization:
                        `Bearer ${token}`
                }
            }
        );

    const record =
        await response.json();

    editingId =
        record.id;

    await loadAppointments();

    document
    .getElementById(
        "appointmentId"
    )
    .value =
        record.appointment_id;

    document
    .getElementById(
        "symptoms"
    )
    .value =
        record.symptoms ?? "";

    document
    .getElementById(
        "diagnosis"
    )
    .value =
        record.diagnosis ?? "";

    document
    .getElementById(
        "prescription"
    )
    .value =
        record.prescription ?? "";

    document
    .getElementById(
        "doctorNote"
    )
    .value =
        record.doctor_note ?? "";

    modal.show();
}

async function deleteRecord(
    recordId
) {

    if (
        !confirm(
            "Xóa bệnh án này?"
        )
    ) {
        return;
    }

    const response =
        await fetch(
            `${API_BASE}/medical-records/${recordId}`,
            {
                method:
                    "DELETE",

                headers: {
                    Authorization:
                        `Bearer ${token}`
                }
            }
        );

    if (
        response.ok
    ) {

        loadRecords();

        alert(
            "Đã xóa bệnh án"
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