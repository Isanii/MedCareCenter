const token =
    localStorage.getItem(
        "token"
    );

const recordId =
    localStorage.getItem(
        "record_id"
    );

loadRecord();

document
.getElementById(
    "editForm"
)
.addEventListener(
    "submit",
    updateRecord
);

async function loadRecord() {

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

    document
    .getElementById(
        "symptoms"
    ).value =
        record.symptoms;

    document
    .getElementById(
        "diagnosis"
    ).value =
        record.diagnosis;

    document
    .getElementById(
        "prescription"
    ).value =
        record.prescription;

    document
    .getElementById(
        "doctor_note"
    ).value =
        record.doctor_note ?? "";
}

async function updateRecord(
    e
) {

    e.preventDefault();

    const data = {

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
            `${API_BASE}/medical-records/${recordId}`,
            {
                method: "PUT",

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
        "Cập nhật bệnh án thành công"
    );

    location.href =
        "doctor-medical-records.html";
}