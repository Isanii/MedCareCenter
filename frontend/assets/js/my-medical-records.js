
loadRecords();

async function loadRecords() {

    const response =
        await fetch(
            `${API_BASE}/medical-records/my`,
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

            </tr>
            `;
        }
    );
}