function showTab(tabName) {
    const contents = document.querySelectorAll(".tab-content");
    const buttons = document.querySelectorAll(".tab-btn");

    contents.forEach(content => {
        content.classList.remove("active");
    });

    buttons.forEach(button => {
        button.classList.remove("active");
    });

    document.getElementById(tabName).classList.add("active");

    if (tabName === "followers") {
        buttons[0].classList.add("active");
    } else {
        buttons[1].classList.add("active");
    }
}


// Check URL when page loads
const params = new URLSearchParams(window.location.search);
const tab = params.get("tab");

if (tab === "following") {
    showTab("following");
} else {
    showTab("followers");
}