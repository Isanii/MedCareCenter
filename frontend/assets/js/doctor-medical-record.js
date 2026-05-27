const token =
    localStorage.getItem(
        "token"
    );

const appointmentId =
    localStorage.getItem(
        "appointment_id"
    );

if (!appointmentId) {

    alert(
        "Không tìm thấy lịch khám"
    );

    location.href =
        "doctor-appointments.html";
}

document
.getElementById(
    "recordForm"
)
.addEventListener(
    "submit",
    saveRecord
);

async function saveRecord(
    e
) {

    e.preventDefault();

    const data = {

        appointment_id:
            Number(
                appointmentId
            ),

        symptoms:
            document
            .getElementById(
                "symptoms"
            ).value,

        diagnosis:
            document
            .getElementById(
                "diagnosis"
            ).value,

        prescription:
            document
            .getElementById(
                "prescription"
            ).value,

        doctor_note:
            document
            .getElementById(
                "doctor_note"
            ).value
    };

    const response =
        await fetch(
            `${API_BASE}/medical-records`,
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

    if (!response.ok) {

        const error =
            await response.json();

        alert(
            error.detail
        );

        return;
    }

    alert(
        "Tạo bệnh án thành công"
    );

    location.href =
        "doctor-medical-records.html";
}