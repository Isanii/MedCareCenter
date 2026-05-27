const token =
    localStorage.getItem(
        "token"
    );

const recordId =
    localStorage.getItem(
        "record_id"
    );

loadRecord();

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

    if (!response.ok) {

        alert(
            "Không tải được bệnh án"
        );

        return;
    }

    const record =
        await response.json();

    document
    .getElementById(
        "recordDetail"
    )
    .innerHTML = `

    <div class="card">

        <div class="card-body">

            <h5>
                ${record.patient_name}
            </h5>

            <hr>

            <p>

                <strong>
                Triệu chứng:
                </strong>

                ${record.symptoms}

            </p>

            <p>

                <strong>
                Chẩn đoán:
                </strong>

                ${record.diagnosis}

            </p>

            <p>

                <strong>
                Đơn thuốc:
                </strong>

                ${record.prescription}

            </p>

            <p>

                <strong>
                Ghi chú:
                </strong>

                ${record.doctor_note ?? ""}

            </p>

        </div>

    </div>
    `;
}