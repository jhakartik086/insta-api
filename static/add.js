const uploadBox = document.getElementById("uploadBox");
const fileInput = document.getElementById("fileInput");
const previewGrid = document.getElementById("previewGrid");
const placeholder = document.getElementById("placeholder");
const chooseBtn = document.getElementById("chooseBtn");

// Source of truth for selected files
const dt = new DataTransfer();

function fileKey(f) {
  return `${f.name}-${f.size}-${f.lastModified}`;
}

function addFiles(fileList) {
  const existing = new Set([...dt.files].map(fileKey));

  for (const file of fileList) {
    if (!file.type.startsWith("image/")) continue;
    if (existing.has(fileKey(file))) continue; // skip duplicates
    dt.items.add(file);
  }

  fileInput.files = dt.files;
  render();
}

function removeFile(index) {
  const newDt = new DataTransfer();
  [...dt.files].forEach((f, i) => {
    if (i !== index) newDt.items.add(f);
  });

  dt.items.clear();
  [...newDt.files].forEach((f) => dt.items.add(f));

  fileInput.files = dt.files;
  render();
}

function render() {
  // free old object URLs
  previewGrid.querySelectorAll("img").forEach((img) => URL.revokeObjectURL(img.src));
  previewGrid.innerHTML = "";

  const files = [...dt.files];
  placeholder.style.display = files.length ? "none" : "flex";
  previewGrid.style.display = files.length ? "grid" : "none";

  files.forEach((file, i) => {
    const item = document.createElement("div");
    item.className = "preview-item";

    const img = document.createElement("img");
    img.src = URL.createObjectURL(file);

    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "remove-btn";
    remove.innerHTML = "&times;";
    remove.setAttribute("aria-label", "Remove image");
    remove.addEventListener("click", (e) => {
      e.stopPropagation();
      removeFile(i);
    });

    item.append(img, remove);
    previewGrid.appendChild(item);
  });

  // "add more" tile
  if (files.length) {
    const more = document.createElement("button");
    more.type = "button";
    more.className = "add-more";
    more.textContent = "+";
    more.addEventListener("click", () => fileInput.click());
    previewGrid.appendChild(more);
  }
}

chooseBtn.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", function () {
  addFiles(this.files);
});

uploadBox.addEventListener("dragover", (e) => {
  e.preventDefault();
  uploadBox.classList.add("dragover");
});

uploadBox.addEventListener("dragleave", () => {
  uploadBox.classList.remove("dragover");
});

uploadBox.addEventListener("drop", (e) => {
  e.preventDefault();
  uploadBox.classList.remove("dragover");
  addFiles(e.dataTransfer.files);
});