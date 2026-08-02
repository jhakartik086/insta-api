const uploadBox = document.getElementById("uploadBox");
const fileInput = document.getElementById("fileInput");
const preview = document.getElementById("preview");

function showImage(file){

    if(file && file.type.startsWith("image/")){

        const imageURL = URL.createObjectURL(file);

        preview.src = imageURL;
        preview.style.display = "block";
    }
}

fileInput.addEventListener("change", function(){
    showImage(this.files[0]);
});

uploadBox.addEventListener("dragover", function(e){
    e.preventDefault();
    uploadBox.classList.add("dragover");
});

uploadBox.addEventListener("dragleave", function(){
    uploadBox.classList.remove("dragover");
});

uploadBox.addEventListener("drop", function(e){
    e.preventDefault();

    uploadBox.classList.remove("dragover");

    const file = e.dataTransfer.files[0];

    showImage(file);
});

uploadBox.addEventListener("drop", function(e){
    e.preventDefault();

    uploadBox.classList.remove("dragover");

    const file = e.dataTransfer.files[0];

    fileInput.files = e.dataTransfer.files;

    showImage(file);
});