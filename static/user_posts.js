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
