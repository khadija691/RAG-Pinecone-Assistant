// ==========================================
// ELEMENTS
// ==========================================

const pdfInput = document.getElementById("pdfInput");
const uploadButton = document.getElementById("uploadButton");

const uploadBox = document.getElementById("uploadBox");
const fileInfo = document.getElementById("fileInfo");
const fileName = document.getElementById("fileName");
const fileStatus = document.getElementById("fileStatus");
const removeFile = document.getElementById("removeFile");

const questionInput = document.getElementById("questionInput");
const askButton = document.getElementById("askButton");

const loading = document.getElementById("loading");

const answerSection = document.getElementById("answerSection");
const answerContent = document.getElementById("answerContent");
const sourcesContainer = document.getElementById("sourcesContainer");


// ==========================================
// VARIABLES
// ==========================================

let selectedFile = null;
let documentUploaded = false;


// ==========================================
// CHOOSE PDF BUTTON
// ==========================================

uploadButton.addEventListener("click", () => {

    // Open Windows file picker
    pdfInput.click();

});


// ==========================================
// FILE SELECTED
// ==========================================

pdfInput.addEventListener("change", async () => {

    if (!pdfInput.files.length) {
        return;
    }

    selectedFile = pdfInput.files[0];

    // Show file information
    fileName.textContent = selectedFile.name;
    fileStatus.textContent = "Processing document...";

    fileInfo.style.display = "flex";

    // Upload automatically
    await uploadPDF();

});


// ==========================================
// UPLOAD PDF
// ==========================================

async function uploadPDF() {

    if (!selectedFile) {
        return;
    }

    uploadButton.disabled = true;

    try {

        const formData = new FormData();

        formData.append("pdf", selectedFile);


        const response = await fetch(
            "/upload",
            {
                method: "POST",
                body: formData
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.error || "Upload failed"
            );

        }


        // Upload successful

        documentUploaded = true;

        fileStatus.textContent =
            `✓ Document processed — ${data.pages} pages, ${data.chunks} chunks`;

        uploadButton.textContent =
            "Choose Another PDF";


        console.log("Upload successful:", data);

    }

    catch (error) {

        console.error("Upload error:", error);

        documentUploaded = false;

        fileStatus.textContent =
            "✗ Upload failed: " + error.message;

    }

    finally {

        uploadButton.disabled = false;

    }

}


// ==========================================
// REMOVE FILE
// ==========================================

removeFile.addEventListener("click", () => {

    selectedFile = null;
    documentUploaded = false;

    pdfInput.value = "";

    fileInfo.style.display = "none";

    uploadButton.textContent = "Choose PDF";

    answerSection.style.display = "none";

    answerContent.textContent = "";

    sourcesContainer.innerHTML = "";

});


// ==========================================
// ASK AI
// ==========================================

askButton.addEventListener("click", async () => {

    const question = questionInput.value.trim();


    // Check document

    if (!documentUploaded) {

        alert("Please upload a PDF document first.");

        return;

    }


    // Check question

    if (!question) {

        alert("Please enter a question.");

        return;

    }


    // Show loading

    loading.style.display = "flex";

    answerSection.style.display = "none";

    askButton.disabled = true;


    try {

        const response = await fetch(
            "/ask",
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


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.error || "Question failed"
            );

        }


        // ==========================================
        // DISPLAY ANSWER
        // ==========================================

        answerContent.textContent =
            data.answer;


        answerSection.style.display = "block";


        // ==========================================
        // DISPLAY SOURCES
        // ==========================================

        sourcesContainer.innerHTML = "";


        if (data.sources && data.sources.length > 0) {

            data.sources.forEach((source) => {

                const sourceElement =
                    document.createElement("div");

                sourceElement.className =
                    "source-item";


                sourceElement.innerHTML = `
                    <strong>Page ${source.page}</strong>
                    <span>
                        Similarity: ${source.score.toFixed(3)}
                    </span>
                `;


                sourcesContainer.appendChild(
                    sourceElement
                );

            });

        }
        else {

            sourcesContainer.innerHTML =
                "<p>No sources found.</p>";

        }

    }

    catch (error) {

        console.error("Question error:", error);

        answerContent.textContent =
            "An error occurred: " + error.message;

        answerSection.style.display = "block";

    }

    finally {

        loading.style.display = "none";

        askButton.disabled = false;

    }

});


// ==========================================
// ENTER KEY SHORTCUT
// ==========================================

questionInput.addEventListener("keydown", (event) => {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        askButton.click();

    }

});