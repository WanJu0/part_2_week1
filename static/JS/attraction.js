function attractionID()
{
    let s = location.href;
    let path = location.pathname;
    console.log(s);
    console.log(path);
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
        console.log(description);
        console.log(address);
        console.log(transport);
        console.log(images);
        // 有幾張圖片
        console.log(images.length);
        
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

// 點擊或關閉註冊和登入div
function openLogin() {
    let element = document.getElementById("overlay_login")
    element.style.display = "block"
}
function closeLogin() {
    let element = document.getElementById("overlay_login")
    element.style.display = "none"
} 
// 開關註冊
function openSignup() {
    let element = document.getElementById("overlay_signup")
    element.style.display = "block"
}
function closeSignup() {
    let element = document.getElementById("overlay_signup")
    element.style.display = "none"
} 
// 註冊系統
function apiSingup(){
    const nameElement = document.getElementById("input_signup_name");
    const name = nameElement.value;
    const emailElement = document.getElementById("input_signup_email");
    const email = emailElement.value;
    const passwordElement = document.getElementById("input_signup_password");
    const password = passwordElement.value;

    console.log(name);
    console.log(email);
    console.log(password);
    let data=
        {
            name:name,
            email:email,
            password:password
        };
        console.log(data,"你好")
    fetch("/api/user",{
        method: "POST" ,
        credentials: "include",
        body:JSON.stringify(data),
        cache:"no-cache",
        headers:new Headers({
            "content-type":"application/json"
        })
    })
    .then((response) => {
        // 這裡會得到一個 ReadableStream 的物件
        // 可以透過 blob(), json(), text() 轉成可用的資訊
        return response.json(); 
    }).then((jsonData) => {
        console.log(jsonData,"check 33")
        console.log(jsonData.message)
        if(jsonData.error==true){
            document.getElementById("signup_message").innerHTML = jsonData.message 
        }
        if(jsonData.ok==true){
            document.getElementById("signup_message").innerHTML = "註冊成功" 
        }
    }) 
}
// 登入系統的js 
function apiSingin()
{
    const emailElement = document.getElementById("input_email");
    const email = emailElement.value;
    const passwordElement = document.getElementById("input_password");
    const password = passwordElement.value;

    console.log(email);
    console.log(password);
    let data=
        {
            email:email,
            password:password
        };
    
    console.log(data);
    fetch("/api/user/auth",{
        method: "PUT" ,
        credentials: "include",
        body:JSON.stringify(data),
        cache:"no-cache",
        headers:new Headers({
            "content-type":"application/json"
        })
    })
    .then(function(response){
        if(response.status ==400){
            console.log(`Response status was not 200:${response.status}`);
            console.log(data)
            document.getElementById("signin_message").innerHTML = "帳號密碼有誤"
            return ;
        }
        if(response.status ==200){
            response.json().then(function(data){
                console.log(data)
                // document.getElementById("signin_message").innerHTML = "登入成功"
                window.location.replace(location.href)
            })
        }
    })
}
// 寫一個函式可以判斷使用者是否有登入
function check()
{
    fetch("/api/user/auth",{
        method: "GET" ,
    })
    .then((response) => {
        // 這裡會得到一個 ReadableStream 的物件
        // 可以透過 blob(), json(), text() 轉成可用的資訊
        return response.json(); 
    }).then((jsonData) => {
        console.log(jsonData,"check 1");
        console.log(jsonData.data);
        if(jsonData.data!=false){
            let element = document.querySelector(".right_login");
            element.style.display="none";
            let signoutElement = document.querySelector(".right_logout");
            signoutElement.style.display="block";
            signoutElement.style.display="flex";
        }
        else{
            let element = document.querySelector(".right_login");
            element.style.display="block";
            element.style.display="flex";
            let signoutElement = document.querySelector(".right_logout");
            signoutElement.style.display="none";
        }
    })
}

// 登出系統
function logout()
{
    fetch("/api/user/auth",{
        method: "DELETE" ,
    })
    .then((response) => {
        // 這裡會得到一個 ReadableStream 的物件
        // 可以透過 blob(), json(), text() 轉成可用的資訊
        return response.json(); 
    }).then((jsonData) => {
        console.log(jsonData,"check 2")
        window.location.replace(location.href)
        
    })
}
check();
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