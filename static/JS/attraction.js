function attractionID()
{
    let s = location.href;
    let path = location.pathname;

    // 這邊是將頁面抓到輸入的字串
    fetch(`/api/${path}`, {})
    .then((response) => {
        // 這裡會得到一個 ReadableStream 的物件
        // 可以透過 blob(), json(), text() 轉成可用的資訊
        return response.json(); 
    }).then((jsonData) => {
        let title = jsonData.data.name;
        let category = jsonData.data.category;
        let mrt = jsonData.data.mrt;
        let description = jsonData.data.description;
        let address= jsonData.data.address;
        let transport= jsonData.data.transport;
        let images= jsonData.data.images;
    
        // 將景點名稱放進去
        let journeyCategory=document.getElementById("journey_category"); 
        categoryNode = document.createTextNode(category+" at "+mrt);
        journeyCategory.appendChild(categoryNode);

        // 將放進去
        let journeyTitle=document.getElementById("journey_title"); 
        titleNode = document.createTextNode(title);
        journeyTitle.appendChild(titleNode);
        
        // 將景點介紹放進去
        let informationContent=document.getElementById("attraction_description"); 
        informationNode = document.createTextNode(jsonData.data.description);
        informationContent.appendChild(informationNode);
        // 將景點地址放進去
        let addressContent=document.getElementById("address_name"); 
        addressNode = document.createTextNode(jsonData.data.address);
        addressContent.appendChild(addressNode);

        // 將交通資訊放進去
        let transportContent=document.getElementById("transport_content"); 
        transportNode = document.createTextNode(transport);
        transportContent.appendChild(transportNode);

        // 將圖片放進phot_list
        for(let i=0; i<images.length; i++){
            let photo_content=document.getElementById("photo_list");
            let photo_img = document.createElement("img");
            photo_img.className="photo_list_content";
            photo_img.src = images[i];
            photo_content.appendChild(photo_img);

            let dot_content=document.getElementById("dot_content");
            let dots = document.createElement("span");
            dots.className  = "dot";
            dots.setAttribute("onclick", `currentSlide(${i+1})`)
            dot_content.appendChild(dots);
        }
    })
}
attractionID();
function daynightCheck() {
    if (document.getElementById("daytime").checked) {
        document.getElementById("daytime_cost").style.display ="block";
    } else {
        document.getElementById("daytime_cost").style.display = 'none';
    }
    if (document.getElementById("nighttime").checked) {
        document.getElementById("nighttime_cost").style.display ="block";
    } else {
        document.getElementById("nighttime_cost").style.display = "none";
    }
}

let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusDivs(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.querySelectorAll(".photo_list_content");
    let dots = document.getElementsByClassName("dot");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " active";
}
// 預定行程按鈕函式
function newBooking()
{
    // 要先確認是否有登入！
    const loginOrnot = document.querySelector(".right_logout");
    const login = loginOrnot.style.display;
    // console.log(login)
    if(login=="none"){
        openLogin();
        return
    }

    const pathUrl = location.pathname ;
    const strAry = pathUrl.split('/attraction/');
    const id = strAry[1]
    // console.log(id);
    
    const dateElement = document.getElementById("date");
    const date = dateElement.value;
    // console.log(date);
    const dayElement = document.getElementById("daytime_cost");
    const day = dayElement.style.display;
    // console.log(day);
    let time="";
    let price="";
    if(day=="none"){
        time = "afternoon";
        price = 2500;

    }
    if(day=="block"){
        time = "morning";
        price = 2000;
    }
    else{

    }
    let data=
        {
            attraction:id,
            date:date,
            time:time,
            price:price
        };
    fetch("/api/booking",{
        method: "POST" ,
        credentials: "include",
        body:JSON.stringify(data),
        cache:"no-cache",
        headers:new Headers({
            "content-type":"application/json"
        })
    })
    .then(function(response){
        if(response.status ==400){
            document.getElementById("error_message").innerHTML = "請選擇日期和時間"
            return ;
        }
        if(response.status ==200){
            response.json().then(function(data){
                window.location.href="/booking";
            })
        }
    })
}