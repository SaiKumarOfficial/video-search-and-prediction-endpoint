//selecting all required elements
const dropArea = document.querySelector(".drag-area")
const form = document.querySelector("form"),
    dragText = dropArea.querySelector("header"),
    button = dropArea.querySelector("button"),
    input = dropArea.querySelector("input")
    //let button_image_search = document.querySelector("#image_search");
    //button_image_search.disabled = true;

let file; //this is a global variable and we'll use it inside multiple functions

button.onclick = () => {
    input.click(); //if user click on the button then the input also clicked
}

input.addEventListener("change", function() {
    //getting user select file and [0] this means if user select multiple files then we'll select only the first one
    file = this.files[0];
    dropArea.classList.add("active");
    showFile(); //calling function
});


//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event) => {
    event.preventDefault(); //preventing from default behaviour
    dropArea.classList.add("active");
    dragText.textContent = "Release to Upload File";
});

//If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
});

//If user drop File on DropArea
dropArea.addEventListener("drop", (event) => {
    event.preventDefault(); //preventing from default behaviour
    //getting user select file and [0] this means if user select multiple files then we'll select only the first one
    file = event.dataTransfer.files[0];
    showFile(); //calling function

});

function showFile() {
    let fileType = file.type; // Getting selected file type
    let validImageExtensions = ["image/jpeg", "image/jpg", "image/png"]; // Valid image extensions
    let validVideoExtensions = ["video/mp4", "video/webm", "video/ogg"]; // Valid video extensions

    if (validImageExtensions.includes(fileType)) {
        handleImageFile();
    } else if (validVideoExtensions.includes(fileType)) {
        handleVideoFile();
    } else {
        alert("Unsupported file format. Please upload a valid image or video file.");
        dropArea.classList.remove("active");
        dragText.textContent = "Drag & Drop to Upload File";
    }
}

function handleImageFile() {
    let fileReader = new FileReader(); // Creating a new FileReader object
    fileReader.onload = () => {
        let fileURL = fileReader.result; // Passing user file source in fileURL variable
        let imgTag = `<img src="${fileURL}" alt="image">`; // Creating an img tag and passing user-selected file source inside src attribute
        dropArea.innerHTML = imgTag; // Adding that created img tag inside dropArea container
        myFunction();
        sendFileToServer('/image');
    };
    fileReader.readAsDataURL(file);
}

function handleVideoFile() {
    let fileReader = new FileReader(); // Creating a new FileReader object
    fileReader.onload = () => {
        let fileURL = fileReader.result; // Passing user file source in fileURL variable
        let videoTag = `<video src="${fileURL}" controls></video>`; // Creating a video tag and passing user-selected file source inside the src attribute
        dropArea.innerHTML = videoTag; // Adding the created video tag inside the dropArea container
        myFunction();
        sendFileToServer('/video');
    };
    fileReader.readAsDataURL(file);
}



function sendFileToServer(endpoint) {
    // Sending the file to the server using fetch API
    const formData = new FormData();
    formData.append('file', file);

    fetch(endpoint, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data); // Handle the response from the server if needed
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function myFunction() {
    var x = document.getElementById("btn_area");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}