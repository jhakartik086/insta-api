function showTab(tabName){

    document.querySelectorAll(".tab-content").forEach(tab=>{
        tab.classList.remove("active");
    });

    document.querySelectorAll(".tab-btn").forEach(btn=>{
        btn.classList.remove("active");
    });

    document.getElementById(tabName).classList.add("active");

    if(tabName === "followers"){
        document.querySelectorAll(".tab-btn")[0].classList.add("active");
    }else{
        document.querySelectorAll(".tab-btn")[1].classList.add("active");
    }
}