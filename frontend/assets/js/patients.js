const authToken =
    localStorage.getItem(
        "token"
    );

const modalElement =
    document.getElementById(
        "patientModal"
    );

let modal = null;
let editingPatientId = null;
let patientCurrentPage = 1;
const pageSize = 10;
if (modalElement) {

    modal =
        new bootstrap.Modal(
            modalElement
        );
}

const addBtn =
    document.getElementById(
        "addPatientBtn"
    );
if (addBtn) {

    addBtn.addEventListener(
        "click",
        () => {

            editingPatientId = null;

            document
            .querySelector(
                ".modal-title"
            )
            .innerText =
                "Thêm bệnh nhân";

            document
            .getElementById(
                "patientForm"
            )
            .reset();

            modal.show();
        }
    );
}

document
.getElementById(
    "savePatientBtn"
)
.addEventListener(
    "click",
    createPatient
);

loadPatients();

async function loadPatients() {

    const skip =
        (patientCurrentPage  - 1)
        * pageSize;

    const response =
        await fetch(
            `${API_BASE}/patients?skip=${skip}&limit=${pageSize}`,
            {
                headers: {
                    Authorization:
                        `Bearer ${authToken}`
                }
            }
        );

    const patients =
        await response.json();

    renderPatients(
        patients
    );

document
.getElementById(
    "pageInfo"
)
.innerText =
    `Trang ${patientCurrentPage}`;
}

document
.getElementById(
    "searchInput"
)
.addEventListener(
    "input",
    searchPatients
);

function renderPatients(
    patients
) {

    const table =
        document.getElementById(
            "patientTable"
        );

    table.innerHTML = "";

    patients.forEach(
        patient => {

            table.innerHTML += `
            <tr>

                <td>${patient.id}</td>

                <td>${patient.fullname}</td>

                <td>${patient.email}</td>

                <td>${patient.phone ?? ""}</td>

                <td>${patient.gender ?? ""}</td>

                <td>${patient.address ?? ""}</td>

                <td>
                    ${patient.birthday ?? ""}
                </td>

                <td>

                    <button
                        class="btn btn-warning btn-sm me-1"
                        onclick="editPatient(${patient.id})">

                        Sửa

                    </button>

                   <button
                        class="btn btn-danger btn-sm"
                        onclick="deactivatePatient(${patient.id})">

                        Khóa

                    </button>

                </td>

            </tr>
            `;
        }
    );
}


async function searchPatients() {

    const keyword =
        document
        .getElementById(
            "searchInput"
        )
        .value
        .trim();

    if (
        keyword === ""
    ) {

        loadPatients();

        return;
    }

    const response =
        await fetch(
            `${API_BASE}/patients/search?keyword=${keyword}`,
            {
                headers: {
                    Authorization:
                        `Bearer ${authToken}`
                }
            }
        );

    const patients =
        await response.json();

    renderPatients(
        patients
    );
}

async function createPatient() {
    if (
        editingPatientId
    ) {

        return updatePatient();
    }
    const data = {

        fullname:
            document
            .getElementById(
                "fullname"
            ).value,

        email:
            document
            .getElementById(
                "email"
            ).value,

        phone:
            document
            .getElementById(
                "phone"
            ).value,

        password:
            document
            .getElementById(
                "password"
            ).value,

        birthday:
            document
            .getElementById(
                "birthday"
            ).value,

        gender:
            document
            .getElementById(
                "gender"
            ).value,

        address:
            document
            .getElementById(
                "address"
            ).value
    };

    const response =
        await fetch(
            `${API_BASE}/patients/create-with-user`,
            {
                method: "POST",

                headers: {
                    Authorization:
                        `Bearer ${authToken}`,

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

        loadPatients();

        alert(
            "Tạo bệnh nhân thành công"
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

async function deactivatePatient(
    userId
) {

    const confirmed =
        confirm(
            "Khóa tài khoản bệnh nhân này?"
        );

    if (!confirmed) {
        return;
    }

    const response =
        await fetch(
            `${API_BASE}/users/${userId}/status?is_active=false`,
            {
                method: "PUT",

                headers: {
                    Authorization:
                        `Bearer ${authToken}`
                }
            }
        );

    if (
        response.ok
    ) {

        alert(
            "Đã khóa bệnh nhân"
        );

        loadPatients();
    }

    else {

        const error =
            await response.json();

        alert(
            error.detail
        );
    }
}


async function editPatient(
    patientId
) {

    const response =
        await fetch(
            `${API_BASE}/patients/${patientId}`,
            {
                headers: {
                    Authorization:
                        `Bearer ${authToken}`
                }
            }
        );

    const patient =
        await response.json();

    editingPatientId =
        patient.id;

    document
    .querySelector(
        ".modal-title"
    )
    .innerText =
        "Cập nhật bệnh nhân";

    document
    .getElementById(
        "birthday"
    ).value =
        patient.birthday ?? "";

    document
    .getElementById(
        "gender"
    ).value =
        patient.gender ?? "";

    document
    .getElementById(
        "address"
    ).value =
        patient.address ?? "";

    modal.show();
}



async function updatePatient() {

    const data = {

        birthday:
            document
            .getElementById(
                "birthday"
            ).value,

        gender:
            document
            .getElementById(
                "gender"
            ).value,

        address:
            document
            .getElementById(
                "address"
            ).value
    };

    const response =
        await fetch(
            `${API_BASE}/patients/${editingPatientId}`,
            {
                method: "PUT",

                headers: {
                    Authorization:
                        `Bearer ${authToken}`,

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

        editingPatientId =
            null;

        loadPatients();

        alert(
            "Cập nhật thành công"
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


document
.getElementById(
    "prevBtn"
)
.addEventListener(
    "click",
    () => {

        if (
            patientCurrentPage  > 1
        ) {

            patientCurrentPage --;

            loadPatients();
        }
    }
);

document
.getElementById(
    "nextBtn"
)
.addEventListener(
    "click",
    () => {

        patientCurrentPage ++;

        loadPatients();
    }
);