// const input = document.getElementById("searchInput");
// const results = document.getElementById("search-results");

// input.addEventListener("input", async () => {
//     const query = input.value.trim();

//     if (query === "") {
//         results.innerHTML = "";
//         return;
//     }

//     const response = await fetch(`/search?q=${query}`);
//     const users = await response.json();

//     results.innerHTML = "";

//     users.forEach(user => {
//         results.innerHTML += `
//             <div class="user">
//                 <img src="${user.profile_pic}" width="50">
//                 <span>${user.username}</span>
//             </div>
//         `;
//     });
// });

const input = document.getElementById("searchInput");
const results = document.getElementById("search-results");

input.addEventListener("input", async () => {
    const query = input.value.trim();

    if (query === "") {
        results.innerHTML = "";
        return;
    }

    const response = await fetch(`/search_api?q=${query}`);
    const users = await response.json();

    results.innerHTML = "";

    users.forEach(user => {
        results.innerHTML += `
            <a href="/view/${user.username}" class="user-card">
                <img src="/static/profile_pics/${user.profile_pic}" class="profile-pic">
                <div class="user-info">
                    <div class="username">${user.username}</div>
                </div>
            </a>
        `;
    });
});
