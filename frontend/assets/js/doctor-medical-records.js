const token =
    localStorage.getItem(
        "token"
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

    if (!response.ok) {

        alert(
            "Không tải được bệnh án"
        );

        return;
    }

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
                    ${record.patient_name}
                </td>

                <td>
                    ${record.doctor_name}
                </td>

                <td>
                    ${record.diagnosis}
                </td>

                <td>
                    ${record.id}
                </td>

               <td>

               <button
                    class="btn btn-primary btn-sm"
                    onclick="
                        viewRecord(
                            ${record.id}
                        )
                    ">

                    Xem

                </button>

                <button
                    class="btn btn-warning btn-sm ms-1"
                    onclick="
                        editRecord(
                            ${record.id}
                        )
                    ">

                    Sửa

                </button>

            </td>

            </tr>
            `;
        }
    );
}

function viewRecord(
    recordId
) {

    localStorage.setItem(
        "record_id",
        recordId
    );

    location.href =
        "doctor-record-detail.html";
}


function editRecord(
    recordId
) {

    localStorage.setItem(
        "record_id",
        recordId
    );

    location.href =
        "doctor-record-edit.html";
}