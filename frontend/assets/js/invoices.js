

const modal =
    new bootstrap.Modal(
        document.getElementById(
            "invoiceModal"
        )
    );

document
.getElementById(
    "addInvoiceBtn"
)
.addEventListener(
    "click",
    async () => {

        await loadAppointments();

        modal.show();
    }
);

document
.getElementById(
    "saveInvoiceBtn"
)
.addEventListener(
    "click",
    createInvoice
);

loadInvoices();

async function loadInvoices() {

    const response =
        await fetch(
            `${API_BASE}/invoices`,
            {
                headers: {
                    Authorization:
                        `Bearer ${token}`
                }
            }
        );

    const invoices =
        await response.json();

    renderInvoices(
        invoices
    );
}

function renderInvoices(
    invoices
) {

    const table =
        document.getElementById(
            "invoiceTable"
        );

    table.innerHTML = "";

    invoices.forEach(
        invoice => {

            table.innerHTML += `
            <tr>

                <td>
                    ${invoice.id}
                </td>

                <td>
                    ${invoice.appointment_id}
                </td>

                <td>
                    ${invoice.amount.toLocaleString()}
                    VNĐ
                </td>

                <td>

                    <span
                        class="
                        badge
                        ${
                            invoice.payment_status === "paid"
                            ?
                            "bg-success"
                            :
                            "bg-warning"
                        }">

                        ${invoice.payment_status}

                    </span>

                </td>

                <td>
                    ${new Date(
                        invoice.created_at
                    ).toLocaleString(
                        "vi-VN"
                    )}
                </td>

                <td>

                    ${
                        invoice.payment_status ===
                        "unpaid"
                        ?
                        `
                        <button
                            class="btn btn-success btn-sm"
                            onclick="
                                markPaid(
                                    ${invoice.id}
                                )
                            ">
                            Thanh toán
                        </button>
                        `
                        :
                        ""
                    }

                    <button
                        class="btn btn-danger btn-sm"
                        onclick="
                            deleteInvoice(
                                ${invoice.id}
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
            </option>
            `;
        }
    );
}

async function createInvoice() {

    const data = {

        appointment_id:
            Number(
                document
                .getElementById(
                    "appointmentId"
                )
                .value
            ),

        amount:
            Number(
                document
                .getElementById(
                    "amount"
                )
                .value
            )
    };

    const response =
        await fetch(
            `${API_BASE}/invoices`,
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

        loadInvoices();

        alert(
            "Tạo hóa đơn thành công"
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

async function markPaid(
    invoiceId
) {

    const response =
        await fetch(
            `${API_BASE}/invoices/${invoiceId}/status`,
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
                        payment_status:
                            "paid"
                    })
            }
        );

    if (
        response.ok
    ) {

        loadInvoices();
    }
}

async function deleteInvoice(
    invoiceId
) {

    if (
        !confirm(
            "Xóa hóa đơn?"
        )
    ) {
        return;
    }

    const response =
        await fetch(
            `${API_BASE}/invoices/${invoiceId}`,
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

        loadInvoices();
    }
}