// Selecting all required elements
const dropArea = document.querySelector(".drag-area");
const form = document.querySelector("form");
const dragText = dropArea.querySelector("header");
const button = dropArea.querySelector("button");
const input = dropArea.querySelector("input");

button.onclick = () => {
    input.click(); // If user clicks on the button then the input is also clicked
};

input.addEventListener("change", function() {
    // Getting the user-selected file and [0] means if the user selects multiple files, we'll select only the first one
    file = this.files[0];
    dropArea.classList.add("active");
    showFile(); // Calling function
});

// If user Drags File Over DropArea
dropArea.addEventListener("dragover", (event) => {
    event.preventDefault(); // Preventing default behavior
    dropArea.classList.add("active");
    dragText.textContent = "Release to Upload File";
});

// If user leaves dragged File from DropArea
dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
});

// If user drops File on DropArea
dropArea.addEventListener("drop", (event) => {
    event.preventDefault(); // Preventing default behavior
    // Getting user-selected file and [0] means if the user selects multiple files, we'll select only the first one
    file = event.dataTransfer.files[0];
    showFile(); // Calling function
});

function showFile() {
    let fileType = file.type; // Getting selected file type
    let validExtensions = ["video/mp4", "video/webm", "video/ogg"]; // Adding some valid video extensions in array

    if (validExtensions.includes(fileType)) { // If the user-selected file is a video file
        let fileReader = new FileReader(); // Creating a new FileReader object
        fileReader.onload = () => {
            let fileURL = fileReader.result; // Passing user file source in fileURL variable
            let videoTag = `<video src="${fileURL}" controls></video>`; // Creating a video tag and passing user-selected file source inside the src attribute
            dropArea.innerHTML = videoTag; // Adding the created video tag inside the dropArea container
            myFunction();
        };
        fileReader.readAsDataURL(file);
    } else {
        alert("This is not a Video File!");
        dropArea.classList.remove("active");
        dragText.textContent = "Drag & Drop to Upload File";
    }

    // Sending the video file to the server using XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/video', true);
    let data = new FormData(form);
    xhr.send(data);
}

function myFunction() {
    var x = document.getElementById("btn_area");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}