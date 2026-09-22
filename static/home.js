async function toggleFollow(button){

    const username = button.dataset.user;

    const response = await fetch("/follow",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            username:username
        })
    });

    const data = await response.json();

    if(data.following){
        button.innerText = "Following";
        button.classList.add("following");
    }else{
        button.innerText = "Follow";
        button.classList.remove("following");
    }

}