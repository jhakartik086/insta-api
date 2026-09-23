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