let editingDoctorId = null;
let doctorCurrentPage  = 1;

const pageSize = 10;
loadDoctors();

async function loadDoctors(
    page = 1
) {

    doctorCurrentPage = page;

    const skip =
        (page - 1)
        * pageSize;

    const response =
        await fetch(
            `${API_BASE}/doctors?skip=${skip}&limit=${pageSize}`,
            {
                headers: {
                    Authorization:
                        `Bearer ${token}`
                }
            }
        );

    const doctors =
        await response.json();

    renderDoctors(
        doctors
    );

    renderPagination(
        page
    );
}


function renderDoctors(
    doctors
) {

    const table =
        document.getElementById(
            "doctorTable"
        );

    table.innerHTML = "";

    doctors.forEach(
        doctor => {

            table.innerHTML += `
            <tr>

                <td>${doctor.id}</td>

                <td>${doctor.fullname}</td>

                <td>${doctor.email}</td>

                <td>${doctor.specialty}</td>

                <td>${doctor.room_number ?? ""}</td>

                <td>${doctor.years_of_experience}</td>

                <td>
                    ${new Date(
                        doctor.created_at
                    ).toLocaleDateString(
                        "vi-VN"
                    )}
                </td>

                <td>

                    <button
                        class="btn btn-warning btn-sm me-1"
                        onclick="editDoctor(${doctor.id})">

                        Sửa

                    </button>

                    <button
                        class="btn btn-danger btn-sm"
                        onclick="deactivateDoctor(${doctor.id})">

                        Khóa

                    </button>

                </td>

            </tr>
            `;
        }
    );
}


document
.getElementById(
    "searchBtn"
)
.addEventListener(
    "click",
    searchDoctor
);

document
.getElementById(
    "searchInput"
)
.addEventListener(
    "input",
    searchRealtime
);

async function searchDoctor() {

    const keyword =
        document.getElementById(
            "searchInput"
        ).value;

    const response =
        await fetch(
            `${API_BASE}/doctors/search?keyword=${keyword}`,
            {
                headers: {
                    Authorization:
                        `Bearer ${token}`
                }
            }
        );

    const doctors =
        await response.json();

    renderDoctors(
        doctors
    );
}
const modalElement =
    document.getElementById(
        "doctorModal"
    );

console.log(
    "modalElement = ",
    modalElement
);

const modal =
    new bootstrap.Modal(
        modalElement
    );

document
.getElementById(
    "addDoctorBtn"
)
.addEventListener(
    "click",
    () => {

        editingDoctorId =
            null;

        document
        .getElementById(
            "doctorForm"
        )
        .reset();

        document.querySelector(
            ".modal-title"
        ).innerText =
            "Thêm bác sĩ";

        modal.show();
    }
);



document
.getElementById(
    "saveDoctorBtn"
)
.addEventListener(
    "click",
    saveDoctor
);

async function saveDoctor() {

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

        specialty:
            document
            .getElementById(
                "specialty"
            ).value,

        room_number:
            document
            .getElementById(
                "roomNumber"
            ).value,

        years_of_experience:
            Number(
                document
                .getElementById(
                    "experience"
                ).value
            )
    };


    if (editingDoctorId) {

        return updateDoctor(
            data
        );
    }

    const response =
        await fetch(
            `${API_BASE}/doctors/create-with-user`,
            {
                method: "POST",

                headers: {
                    Authorization:
                        `Bearer ${token}`,

                    "Content-Type":
                        "application/json"
                },

                body:
                    JSON.stringify(data)
            }
        );

    if (
        response.ok
    ) {

        modal.hide();
        document
        .getElementById(
            "doctorForm"
        )
        .reset();
        loadDoctors();

        alert(
            "Đã tạo bác sĩ thành công!"
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


async function deactivateDoctor(
    userId
) {

    const confirmed =
        confirm(
            "Khóa tài khoản bác sĩ này?"
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
                        `Bearer ${token}`
                }
            }
        );

    if (
        response.ok
    ) {

        alert(
            "Đã khóa bác sĩ"
        );

        loadDoctors();
    }

    else {

        const error =
            await response.json();

        alert(
            error.detail
        );
    }
}

async function editDoctor(
    doctorId
) {

    const response =
        await fetch(
            `${API_BASE}/doctors/${doctorId}`,
            {
                headers: {
                    Authorization:
                        `Bearer ${token}`
                }
            }
        );

    const doctor =
        await response.json();

    editingDoctorId =
        doctor.id;

    document
    .getElementById(
        "specialty"
    ).value =
        doctor.specialty;

    document
    .getElementById(
        "roomNumber"
    ).value =
        doctor.room_number ?? "";

    document
    .getElementById(
        "experience"
    ).value =
        doctor.years_of_experience;

    document.querySelector(
        ".modal-title"
    ).innerText =
        "Cập nhật bác sĩ";

    modal.show();
}


async function updateDoctor(
    data
) {

    const response =
        await fetch(
            `${API_BASE}/doctors/${editingDoctorId}`,
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
                        {
                            specialty:
                                data.specialty,

                            room_number:
                                data.room_number,

                            years_of_experience:
                                data.years_of_experience
                        }
                    )
            }
        );

    if (
        response.ok
    ) {

        modal.hide();

        editingDoctorId =
            null;

        document
        .getElementById(
            "doctorForm"
        )
        .reset();

        loadDoctors();

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




function renderPagination(
    current
) {

    const pagination =
        document.getElementById(
            "pagination"
        );

    pagination.innerHTML = "";

    for (
        let i = 1;
        i <= current + 1;
        i++
    ) {

        pagination.innerHTML += `
        <li class="page-item
            ${i === current
                ? "active"
                : ""}
        ">

            <a
                class="page-link"
                href="#"
                onclick="loadDoctors(${i})">

                ${i}

            </a>

        </li>
        `;
    }
}


async function searchRealtime() {

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

        loadDoctors();

        return;
    }

    const response =
        await fetch(
            `${API_BASE}/doctors/search?keyword=${keyword}`,
            {
                headers: {
                    Authorization:
                        `Bearer ${token}`
                }
            }
        );

    const doctors =
        await response.json();

    renderDoctors(
        doctors
    );
}