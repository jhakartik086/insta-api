const profileInput = document.getElementById("profileInput");
const profilePreview = document.getElementById("profilePreview");

profileInput.addEventListener("change", function(){

    const file = this.files[0];

    if(file){

        const reader = new FileReader();

        reader.onload = function(e){
            profilePreview.src = e.target.result;
        }

        reader.readAsDataURL(file);
    }

});