document.querySelectorAll(".delete-btn").forEach((button) => {
  button.addEventListener("click", async function () {
    const post = this.closest(".post");
    const url = this.dataset.url;

    const response = await fetch(url, {
      method: "POST",
    });

    if (response.ok) {
      post.remove();
    } else {
      alert("Failed to delete post");
    }
  });
});

document.querySelectorAll(".delete-btn").forEach((button) => {
  button.addEventListener("click", async function () {
    const post = this.closest(".post");
    const url = this.dataset.url;

    const response = await fetch(url, {
      method: "POST",
    });

    if (response.ok) {
      post.remove();
    } else {
      alert("Failed to delete post");
    }
  });
});

// ---------- Sort posts (Latest / Oldest) ----------
const sortSelect = document.getElementById("sortSelect");
const postsContainer = document.getElementById("posts-container");

if (sortSelect && postsContainer) {
  // Snapshot the original server-rendered order (assumed latest-first)
  const originalOrder = Array.from(postsContainer.children);

  sortSelect.addEventListener("change", function () {
    const posts = Array.from(postsContainer.children);

    if (this.value === "oldest") {
      posts.reverse().forEach((post) => postsContainer.appendChild(post));
    } else {
      originalOrder.forEach((post) => postsContainer.appendChild(post));
    }
  });
}

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