
// 在member 頁面時也要確認是否有登入
function member() {
    // 要先確認是否有登入！
    const loginOrnot = document.querySelector(".right_logout");
    const login = loginOrnot.style.display;

    if (login == "none") {
        openLogin();
        return
    }
    // 如有登入就跳轉到booking
    window.location.replace("/member");
}
let user_id="";
fetch("/api/user/auth", {
    method: "GET",
})
.then((response) => {
    // 這裡會得到一個 ReadableStream 的物件
    // 可以透過 blob(), json(), text() 轉成可用的資訊
    return response.json();
}).then((jsonData) => {
    if (jsonData.data == false) {
        // 使用者沒有登入的話就導向首頁
        window.location.href = "/";
    }
    // console.log(jsonData.data);
    user_id=jsonData.data["id"];
    // 將基本資訊自動填入
    document.getElementById("input_name").value = bookingName;
    document.getElementById("input_mail").value = bookingEmail;
    // 去抓歷史訂單
    fetch(`/api/historyOrders/${user_id}`, {})
    .then((response) => {
        // 這裡會得到一個 ReadableStream 的物件
        // 可以透過 blob(), json(), text() 轉成可用的資訊
        return response.json();
    }).then((jsonData) => {
        // 將歷史訂單放進頁面中
       
        if(jsonData.history_list!=null){
            for (let i = 0; i < jsonData.history_list.length; i++) {
                const historycontent = document.getElementById("history_div");
                const historyDiv = document.createElement("div");
                historyDiv.id = `history_number${i}`;
                historyDiv.setAttribute("onclick", `order(event)`);
                const historyNode = document.createTextNode(jsonData.history_list[i]);
                historyDiv.appendChild(historyNode);
                historycontent.appendChild(historyDiv);
            }
        }
    })
})

// 點擊訂單編號出現詳細訂單資訊
function order(event){
    let div = event.target;
    let idName = div.id;
    let orderNumber = div.innerHTML;
    

    fetch(`/api/orders/${orderNumber}`, {})
    .then((response) => {
        // 這裡會得到一個 ReadableStream 的物件
        // 可以透過 blob(), json(), text() 轉成可用的資訊
        return response.json();
    }).then((jsonData) => {
        
        for (let i = 0; i < jsonData.data["trip"].length; i++){
            let ordercontent = document.querySelector(`#${idName}`);
            // 建立訂單的div
            let orderDiv = document.createElement("div");
            orderDiv.id = `order_detail${i}`;
            ordercontent.appendChild(orderDiv);
            
            // 建立圖片的容器
            
            let attraction_content = document.querySelector(`#${idName} #order_detail${i}`);
            // console.log(attraction_content)
            let img = document.createElement("img");
            img.id = "order_photo";
            img.src = jsonData.data["trip"][i].attraction.image;
            // 將圖片放在attraction_content容器下面
            attraction_content.appendChild(img);
            

            // 建立information
            let informationElement = document.createElement("div");
            informationElement.id = `order_information${i}`;
            attraction_content.appendChild(informationElement);

            // information底下建立booking_attraction
            let informationDiv = document.querySelector(`#${idName} #order_information${i}`);
            // 建立booking_attraction
            let bookingAttraction = document.createElement("div");
            bookingAttraction.id = "order_attraction";
            let attractionNode = document.createTextNode("台北一日遊 : " + jsonData.data["trip"][i].attraction.name);
            bookingAttraction.appendChild(attractionNode);
            informationDiv.appendChild(bookingAttraction);

            // 建立booking_date
            let bookingDate = document.createElement("div");
            bookingDate.id = `order_date${i}`;
            let dateNode = document.createTextNode("日期 : ");
            bookingDate.appendChild(dateNode);
            informationDiv.appendChild(bookingDate);

            // 建立booking_time
            let bookingTime = document.createElement("div");
            bookingTime.id = `order_time${i}`;
            let timeNode = document.createTextNode("時間 : ");
            bookingTime.appendChild(timeNode);
            informationDiv.appendChild(bookingTime);
            // 建立booking_cost
            let bookingCost = document.createElement("div");
            bookingCost.id = `order_cost${i}`;
            let costNode = document.createTextNode("費用 : ");
            bookingCost.appendChild(costNode);
            informationDiv.appendChild(bookingCost);

            // 建立booking_location
            let bookingLocation = document.createElement("div");
            bookingLocation.id = `order_location${i}`;
            let locationNode = document.createTextNode("地點 : ");
            bookingLocation.appendChild(locationNode);
            informationDiv.appendChild(bookingLocation);

            // 加入資訊內容

            let addDate = document.querySelector(`#${idName} #order_date${i}`);
            // 新增一個連結在最外層
            let addDatediv = document.createElement("div");
            addDatediv.id = "add_Date";
            let adddateNode = document.createTextNode(jsonData.data["trip"][i].date);
            addDatediv.appendChild(adddateNode);
            addDate.appendChild(addDatediv);
            //  加入時間
            if (jsonData.data["trip"][i].time == "afternoon") {
                let addTime = document.querySelector(`#${idName} #order_time${i}`);
                // 新增一個連結在最外層
                let addTimediv = document.createElement("div");
                addTimediv.id = "add_time";
                let addtimeNode = document.createTextNode("下午1點到5點");
                addTimediv.appendChild(addtimeNode);
                addTime.appendChild(addTimediv);
            }
            if (jsonData.data["trip"][i].time == "morning") {
                let addTime = document.querySelector(`#${idName} #order_time${i}`);
                // 新增一個連結在最外層
                let addTimediv = document.createElement("div");
                addTimediv.id = "add_time";
                let addtimeNode = document.createTextNode("上午9點到12點");
                addTimediv.appendChild(addtimeNode);
                addTime.appendChild(addTimediv);
            }
            // 加入價錢資訊
            let addCost = document.querySelector(`#${idName} #order_cost${i}`);
            let addCostdiv = document.createElement("div");
            addCostdiv.id = "add_cost";
            let addcostNode = document.createTextNode(jsonData.data["trip"][i]["attraction"].price);
            addCostdiv.appendChild(addcostNode);
            addCost.appendChild(addCostdiv);

            // 地點內容
            let addLocation = document.querySelector(`#${idName} #order_location${i}`);
            let addLocationdiv = document.createElement("div");
            addLocationdiv.id = "add_cost";
            let addlocationNode = document.createTextNode(jsonData.data["trip"][i].attraction.address);
            addLocationdiv.appendChild(addlocationNode);
            addLocation.appendChild(addLocationdiv);
        }
    })
}
function update_photo(){
    const inputElement = document.querySelector('#img_input2');
    inputElement.addEventListener('change', (e) => {
    let file = e.target.files[0]; //取得檔案資訊
    // 创建一个包含原文件内容的 Blob
    const fileBlob = new Blob([file], { type: file.type });

    // 將名字改成想要的名稱,這邊用id來命名
    const newFile = new File([fileBlob], `${user_id}.jpg`, { type: file.type });
    
    if (!file.type.match('image.*')) {
        return false;
    }
    const reader = new FileReader();
    reader.readAsDataURL(file); // 读取文件
   
    // 渲染文件
    reader.onload = (arg) => {
    const previewBox = document.querySelector('.add_photo');    
    previewBox.src = arg.target.result;
    }
    
    const formData = new FormData();
    const a=formData.append('img', newFile);
    fetch("/api/images", {
        method: 'POST',
        body: formData,
    })
    .then((response) => {
        // 這裡會得到一個 ReadableStream 的物件
        // 可以透過 blob(), json(), text() 轉成可用的資訊
        return response.json();
    }).then((jsonData) => {
      
    })
});
}

fetch("/api/images", {
    method: 'GET',
})
.then((response) => {
    // 這裡會得到一個 ReadableStream 的物件
    // 可以透過 blob(), json(), text() 轉成可用的資訊
    return response.text();
}).then((jsonData) => {
    let personImg = document.querySelector(".add_photo");
    if (jsonData!=="False"){
        personImg.src =jsonData;
    }
    else{
        personImg.src ="/static/images/member.png";
    }
})

// 會員頁面資料更新

function updateMember(){
    let nameElement = document.querySelector("#input_name");
    let name = nameElement.value;
    let emailElement = document.querySelector("#input_mail");
    let email = emailElement.value;
    let phoneElement = document.querySelector("#input_phone");
    let phone = phoneElement.value;
    let birthdayElement = document.querySelector("#member_date");
    let birthday = birthdayElement.value;
    let emergencyElement = document.querySelector("#Emergency_Contact");
    let emergencyName = emergencyElement.value;
    let emergencyPhoneElement = document.querySelector("#Emergency_phone");
    let emergencyPhone = emergencyPhoneElement.value;
    let maleElement= document.querySelector("#male") ;
    let male= maleElement.checked ;
    let femaleElement = document.querySelector("#female") ;
    let female= femaleElement.checked ;
    let genderResult="";
    // console.log(name);
    // console.log(email);
    // console.log(phone);
    // console.log(birthday);
    // console.log(emergencyName);
    // console.log(emergencyPhone);
    if(male==false & female==false){
        genderResult="";
    }
    if(male==true){
        genderResult="男生";
    }
    if(female==true){
        genderResult="女生";
    }
    
    // 將輸入的資訊更新到資料庫中
    let data=
        {
            name:name,
            email:email,
            phone:phone,
            birthday:birthday,
            emergencyName:emergencyName,
            emergencyPhone:emergencyPhone,
            gender:genderResult,
        };
    console.log(data)
    fetch("/api/member",{
        method:"POST",
        credentials:"include",
        body:JSON.stringify(data),
        headers:new Headers({
            "content-type":"application/json"
        })
    })
}

fetch("/api/member", {
    method: "GET",
})
.then((response) => {
    // 這裡會得到一個 ReadableStream 的物件
    // 可以透過 blob(), json(), text() 轉成可用的資訊
    return response.json();
}).then((jsonData) => {
    
    let name=jsonData.name;
    let email=jsonData.email;
    let member_phone=jsonData.member_phone;
    let birthday=jsonData.birthday;
    let emergency_name=jsonData.emergency_name;
    let emergency_phone=jsonData.emergency_phone;
    let gender=jsonData.gender;
    // user_id=jsonData.data["id"];
    // // 將基本資訊自動填入
    document.querySelector("#input_name").value = name;
    document.querySelector("#input_mail").value = email;
    document.querySelector("#input_phone").value = member_phone;
    document.querySelector("#Emergency_Contact").value = emergency_name;
    document.querySelector("#Emergency_phone").value = emergency_phone;
    document.querySelector("#member_date").value = birthday;
    if(gender=="男生"){
        document.querySelector("#male").checked=true;
    }
    if(gender=="女生"){
        document.querySelector("#female").checked=true;
    }
})