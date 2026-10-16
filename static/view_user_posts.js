const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightboxImg");
const lightboxClose = document.getElementById("lightboxClose");

function openLightbox(src) {
    lightboxImg.src = src;
    lightbox.classList.add("open");
    lightbox.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden"; // stop feed scrolling behind
}

function closeLightbox() {
    lightbox.classList.remove("open");
    lightbox.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
}

// event delegation: works for every post in the loop
document.addEventListener("click", function (e) {
    const img = e.target.closest(".post-image");
    if (img) openLightbox(img.src);
});

// tap anywhere on the overlay (or the X) to close
lightbox.addEventListener("click", closeLightbox);
lightboxClose.addEventListener("click", function (e) {
    e.stopPropagation();
    closeLightbox();
});

document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && lightbox.classList.contains("open")) {
        closeLightbox();
    }
});