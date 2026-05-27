loadInvoices();

async function loadInvoices() {

    const response =
        await fetch(
            `${API_BASE}/invoices/my`,
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
                    ${Number(
                        invoice.amount
                    ).toLocaleString(
                        "vi-VN"
                    )}
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

            </tr>
            `;
        }
    );
}