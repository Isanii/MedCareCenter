const token =
    localStorage.getItem(
        "token"
    );

if (!token) {

    window.location.href =
        "login.html";
}

fetch(
    `${API_BASE}/auth/me`,
    {
        headers: {
            Authorization:
                `Bearer ${token}`
        }
    }
)
.then(
    response => response.json()
)
.then(
    user => {

        const userInfo =
        document.getElementById(
                "userInfo"
            );

        if (userInfo) {

            userInfo.innerHTML = `
            <div class="card">
                <div class="card-body">

                    <h4>${user.fullname}</h4>

                    <p>Email:
                    ${user.email}</p>

                    <p>Role:
                    ${user.role}</p>

                </div>
            </div>
        `;
        }

        
        const currentUser =
            document.getElementById(
                "currentUser"
            );

        if (currentUser) {

            currentUser.innerHTML = `
                <strong>
                    ${user.fullname}
                </strong>
            `;
        }
    }
);

document
.getElementById(
    "logoutBtn"
)
.addEventListener(
    "click",
    () => {

        localStorage.removeItem(
            "token"
        );

        location.href =
            "login.html";
    }
);