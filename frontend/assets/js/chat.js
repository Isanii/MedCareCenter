const token =
    localStorage.getItem(
        "token"
    );

let currentReceiver =
    null;

loadMessages();

setInterval(
    loadMessages,
    3000
);



async function sendMessage() {

    const receiverId =
        document
        .getElementById(
            "receiverId"
        )
        .value;

    const content =
        document
        .getElementById(
            "messageInput"
        )
        .value;

    if (!content) {
        return;
    }

    await fetch(

        `${API_BASE}/messages`,

        {
            method: "POST",

            headers: {

                "Content-Type":
                    "application/json",

                Authorization:
                    `Bearer ${token}`
            },

            body: JSON.stringify({

                receiver_id:
                    Number(
                        receiverId
                    ),

                content
            })
        }
    );

    document
    .getElementById(
        "messageInput"
    )
    .value = "";

    loadMessages();
}



async function loadMessages() {

    const receiverId =
        document
        .getElementById(
            "receiverId"
        );

    if (
        !receiverId ||
        !receiverId.value
    ) {
        return;
    }

    currentReceiver =
        receiverId.value;

    const response =
        await fetch(

            `${API_BASE}/messages/conversation/${currentReceiver}`,

            {
                headers: {
                    Authorization:
                        `Bearer ${token}`
                }
            }
        );

    const messages =
        await response.json();

    const chatBox =
        document.getElementById(
            "chatBox"
        );

    chatBox.innerHTML = "";

    messages.forEach(
        msg => {

            chatBox.innerHTML += `

            <div class="message">

                <strong>
                    User ${msg.sender_id}
                </strong>

                <br>

                ${msg.content}

            </div>

            `;
        }
    );

    chatBox.scrollTop =
        chatBox.scrollHeight;
}