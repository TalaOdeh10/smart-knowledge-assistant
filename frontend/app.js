const API_URL = "http://127.0.0.1:8000";

const fileInput = document.getElementById("fileInput");
const questionInput = document.getElementById("questionInput");
const sendButton = document.getElementById("sendButton");
const chatContainer = document.getElementById("chatContainer");
const documentList = document.getElementById("documentList");
const documentCount = document.getElementById("documentCount");

let documents = [];


// ==========================================
// DOCUMENT MANAGEMENT
// ==========================================

async function loadDocuments() {

    try {

        const response = await fetch(
            `${API_URL}/api/documents`
        );

        if (!response.ok) {
            throw new Error(
                "Failed to load documents."
            );
        }

        documents = await response.json();

        renderDocuments();

    } catch (error) {

        console.error(
            "Failed to load documents:",
            error
        );

    }
}


async function deleteDocument(documentId, filename) {

    const confirmed = confirm(
        `Are you sure you want to delete "${filename}"?`
    );

    if (!confirmed) {
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/api/documents/${documentId}`,
            {
                method: "DELETE"
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Failed to delete document."
            );
        }

        await loadDocuments();

        addSystemMessage(
            `🗑️ ${filename} was deleted successfully.`
        );

    } catch (error) {

        console.error(
            "Delete failed:",
            error
        );

        addSystemMessage(
            `❌ Delete failed: ${error.message}`
        );

    }
}


// ==========================================
// DOCUMENT UPLOAD
// ==========================================

fileInput.addEventListener(
    "change",
    async () => {

        const file = fileInput.files[0];

        if (!file) {
            return;
        }

        await uploadDocument(file);

        fileInput.value = "";
    }
);


async function uploadDocument(file) {

    const formData = new FormData();

    formData.append("file", file);

    try {

        showUploadLoading(file.name);

        const response = await fetch(
            `${API_URL}/api/documents/upload`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail || "Upload failed."
            );

        }

        await loadDocuments();

        addSystemMessage(
            `📄 ${file.name} was successfully uploaded and indexed.`
        );

    } catch (error) {

        addSystemMessage(
            `❌ Upload failed: ${error.message}`
        );

    }
}


// ==========================================
// DOCUMENT LIST
// ==========================================

function renderDocuments() {

    documentCount.textContent =
        documents.length;


    if (documents.length === 0) {

        documentList.innerHTML = `
            <div class="empty-documents">
                No documents uploaded yet.
            </div>
        `;

        return;
    }


    documentList.innerHTML =
        documents.map(document => {

            const statusClass =
                document.status === "indexed"
                    ? "status-indexed"
                    : "status-other";


            return `

                <div class="document-item">

                    <div class="document-icon">
                        📄
                    </div>


                    <div class="document-info">

                        <div class="document-name">
                            ${escapeHtml(document.filename)}
                        </div>

                        <div class="document-status ${statusClass}">
                            ${getStatusIcon(document.status)}
                            ${escapeHtml(document.status)}
                            · ${document.chunk_count} chunks
                        </div>

                    </div>


                    <button
                        class="delete-button"
                        title="Delete document"
                        onclick="deleteDocument(
                            '${escapeHtml(document.id)}',
                            '${escapeHtml(document.filename)}'
                        )"
                    >
                        🗑️
                    </button>

                </div>

            `;

        }).join("");
}


function getStatusIcon(status) {

    if (status === "indexed") {
        return "✓";
    }

    if (status === "processing") {
        return "⏳";
    }

    if (status === "failed") {
        return "✕";
    }

    return "•";
}


// ==========================================
// CHAT
// ==========================================

async function sendQuestion() {

    const question =
        questionInput.value.trim();


    if (!question) {
        return;
    }


    addUserMessage(question);

    questionInput.value = "";

    sendButton.disabled = true;


    const loadingMessage =
        addLoadingMessage();


    try {

        const response = await fetch(
            `${API_URL}/api/chat`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Failed to get answer."
            );

        }


        loadingMessage.remove();


        addAIMessage(
            data.answer,
            data.sources || []
        );


    } catch (error) {

        loadingMessage.remove();


        addAIMessage(
            `Sorry, something went wrong: ${error.message}`,
            []
        );


    } finally {

        sendButton.disabled = false;

        questionInput.focus();

    }
}


// ==========================================
// ENTER KEY
// ==========================================

questionInput.addEventListener(
    "keydown",
    event => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendQuestion();

        }

    }
);


// ==========================================
// USER MESSAGE
// ==========================================

function addUserMessage(text) {

    removeWelcome();


    const message =
        document.createElement("div");

    message.className =
        "message user";


    message.innerHTML = `

        <div class="message-content">
            ${escapeHtml(text)}
        </div>

        <div class="message-avatar">
            You
        </div>

    `;


    chatContainer.appendChild(message);

    scrollToBottom();
}


// ==========================================
// AI MESSAGE
// ==========================================

function addAIMessage(
    answer,
    sources
) {

    removeWelcome();


    const sourceHTML =
        sources.length > 0

            ? `

                <div class="sources">

                    <div class="sources-title">
                        Sources
                    </div>

                    ${sources.map(
                        source => `

                            <div class="source-card">

                                <div class="source-header">

                                    <span>
                                        📄
                                    </span>

                                    <strong>
                                        ${escapeHtml(
                                            source.document
                                        )}
                                    </strong>

                                    <span>
                                        · Page ${source.page}
                                    </span>

                                </div>


                                ${
                                    source.snippet
                                        ? `
                                            <div class="source-snippet">
                                                ${escapeHtml(
                                                    source.snippet
                                                )}
                                            </div>
                                        `
                                        : ""
                                }

                            </div>

                        `
                    ).join("")}

                </div>

            `

            : "";


    const message =
        document.createElement("div");

    message.className =
        "message ai";


    message.innerHTML = `

        <div class="message-avatar">
            🧠
        </div>


        <div class="message-content">

            ${formatAnswer(answer)}

            ${sourceHTML}

        </div>

    `;


    chatContainer.appendChild(message);

    scrollToBottom();
}


// ==========================================
// LOADING MESSAGE
// ==========================================

function addLoadingMessage() {

    removeWelcome();


    const message =
        document.createElement("div");

    message.className =
        "message ai";


    message.innerHTML = `

        <div class="message-avatar">
            🧠
        </div>


        <div class="message-content">

            <div class="typing">

                <span></span>
                <span></span>
                <span></span>

            </div>

        </div>

    `;


    chatContainer.appendChild(message);

    scrollToBottom();


    return message;
}


// ==========================================
// SYSTEM MESSAGE
// ==========================================

function addSystemMessage(text) {

    const message =
        document.createElement("div");

    message.className =
        "message ai";


    message.innerHTML = `

        <div class="message-avatar">
            ℹ️
        </div>


        <div class="message-content">
            ${escapeHtml(text)}
        </div>

    `;


    chatContainer.appendChild(message);

    scrollToBottom();
}


// ==========================================
// SUGGESTIONS
// ==========================================

function useSuggestion(text) {

    questionInput.value = text;

    questionInput.focus();

}


// ==========================================
// HELPERS
// ==========================================

function removeWelcome() {

    const welcome =
        document.querySelector(
            ".welcome"
        );


    if (welcome) {
        welcome.remove();
    }

}


function scrollToBottom() {

    chatContainer.scrollTop =
        chatContainer.scrollHeight;

}


function showUploadLoading(filename) {

    addSystemMessage(
        `⏳ Processing ${filename}...`
    );

}


function formatAnswer(text) {

    return escapeHtml(text)
        .replace(/\n/g, "<br>");
}


function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent =
        String(text);

    return div.innerHTML;

}


// ==========================================
// INITIALIZE APP
// ==========================================

loadDocuments();