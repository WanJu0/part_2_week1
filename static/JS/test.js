
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
    console.log(bookingName)
    // 將基本資訊自動填入
    document.getElementById("input_name").value = bookingName;
    document.getElementById("input_mail").value = bookingEmail;
    
})

const inputElement = document.querySelector('#img_input2');

inputElement.addEventListener('change', (e) => {
    const file = e.target.files[0]; //取得檔案資訊

    // 只选择图片文件
    if (!file.type.match('image.*')) {
        return false;
    }
    const reader = new FileReader();
    reader.readAsDataURL(file); // 读取文件

    // 渲染文件
    reader.onload = (arg) => {
    const previewBox = document.querySelector('.add_photo');    
    previewBox.src = arg.target.result;
    console.log(arg)
    console.log(arg.target)
    console.log(arg.target.result)

   
    }
});

// firebase

const firebaseConfig = {
    apiKey: "AIzaSyDf5oUqcdru4Lt5hMDx3HJryuOkSqhx_Bw",
    authDomain: "taipei-day-trip-fc62c.firebaseapp.com",
    projectId: "taipei-day-trip-fc62c",
    storageBucket: "taipei-day-trip-fc62c.appspot.com",
    messagingSenderId: "340447976763",
    appId: "1:340447976763:web:3c0bfa2ec73260e1bd2b1e",
    measurementId: "G-Z1M05RKL8P"
};
firebase.initializeApp(firebaseConfig);
const storage = firebase.storage(); // 取得 Firebase 儲存物件
const storageRef = storage.ref(); // 取得儲存參考
const imagesRef = storageRef.child('images'); // 取得圖像儲存參考
const file = inputElement.files[0]; // 取得檔案資訊
const fileName = file.name; // 取得檔案名稱
const uploadTask = imagesRef.child(fileName).put(file); // 將檔案上傳至 Firebase

// 監聽上傳進度並顯示進度條
uploadTask.on('state_changed', function(snapshot) {
  var progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
  console.log('Upload is ' + progress + '% done');
  switch (snapshot.state) {
    case firebase.storage.TaskState.PAUSED: // 上傳已暫停
      console.log('Upload is paused');
      break;
    case firebase.storage.TaskState.RUNNING: // 上傳中
      console.log('Upload is running');
      break;
  }
}, function(error) {
  // 在失敗時處理錯誤
  console.log(error);
}, function() {
  // 在完成時取得圖像 URL
  uploadTask.snapshot.ref.getDownloadURL().then(function(downloadURL) {
    console.log('File available at', downloadURL);
  });
});

// // Initialize Firebase
// // const app = initializeApp(firebaseConfig);
// // console.log(app)

// // const inputElement = document.querySelector('#img_input2');

// // inputElement.addEventListener('change', (e) => {
// //     const file = e.target.files[0]; //取得檔案資訊

// //     // 只选择图片文件
// //     if (!file.type.match('image.*')) {
// //         return false;
// //     }
// //     const reader = new FileReader();
// //     reader.readAsDataURL(file); // 读取文件

// //     // 渲染文件
// //     reader.onload = (arg) => {
// //     const previewBox = document.querySelector('.add_photo');    
// //     previewBox.src = arg.target.result;
// //     console.log(arg)
// //     console.log(arg.target)
// //     console.log(arg.target.result)


// // const inputElement = document.querySelector('#img_input2');
// // inputElement.addEventListener('change', (e) => {
// //     // Get the selected file
// //     const file = e.target.files[0];
  
// //     // Only select image files
// //     if (!file.type.match('image.*')) {
// //       return false;
// //     }
  
// //     // Read the file
// //     const reader = new FileReader();
// //     reader.readAsDataURL(file);
  
// //     // Render the file
// //     reader.onload = (arg) => {
// //       const previewBox = document.querySelector('.add_photo');    
// //       previewBox.src = arg.target.result;
  
// //       // Upload the file to Firebase Storage
// //       firebase.auth().signInAnonymously().then(function() {
// //         return firebase.storage().ref('images/' + file.name).put(file);
// //       }).then(function(snapshot) {
// //         // Get the download URL for the image
// //         return snapshot.ref.getDownloadURL();
// //       }).then(function(downloadURL) {
// //         // Set the image src to the download URL
// //         document.getElementById('.add_photo').src = downloadURL;
// //       }).catch(function(error) {
// //         console.error('Error uploading image:', error);
// //       });
// //     }
// //   });
  
   
//     // }
// // });

// const firebase = require('firebase');
// import * as firebase from "firebase/app";

// import "firebase/auth";
// import "firebase/database";
// var ref = new Firebase("gs://taipei-day-trip-fc62c.appspot.com");
// // // 初始化 Firebase
// const firebaseConfig = {
//     apiKey: "AIzaSyDf5oUqcdru4Lt5hMDx3HJryuOkSqhx_Bw",
//     authDomain: "taipei-day-trip-fc62c.firebaseapp.com",
//     projectId: "taipei-day-trip-fc62c",
//     storageBucket: "taipei-day-trip-fc62c.appspot.com",
//     messagingSenderId: "340447976763",
//     appId: "1:340447976763:web:3c0bfa2ec73260e1bd2b1e",
//     measurementId: "G-Z1M05RKL8P"
// };
// firebase.initializeApp(firebaseConfig);
// var storage = firebase.storage();
// const inputElement = document.querySelector('#img_input2');

// inputElement.addEventListener('change', (e) => {
//     const file = e.target.files[0]; //取得檔案資訊

//     // 只选择图片文件
//     if (!file.type.match('image.*')) {
//         return false;
//     }
//     const reader = new FileReader();
//     reader.readAsDataURL(file); // 读取文件

//     // 渲染文件
//     reader.onload = (arg) => {
//     const previewBox = document.querySelector('.add_photo');    
//     previewBox.src = arg.target.result;
//     console.log(arg)
//     console.log(arg.target)
//     console.log(arg.target.result)

//     var storageRef = firebase.storage().ref('gs://taipei-day-trip-fc62c.appspot.com/'+file.name);
//     storageRef.put(file);
   
//     }
// });

// // const inputElement = document.querySelector('#img_input2');
// // inputElement.addEventListener('change', (e) => {
// //     // Get the selected file
// //     const file = e.target.files[0];
  
// //     // Only select image files
// //     if (!file.type.match('image.*')) {
// //       return false;
// //     }
  
// //     // Read the file
// //     const reader = new FileReader();
// //     reader.readAsDataURL(file);
  
// //     // Render the file
// //     reader.onload = (arg) => {
// //       const previewBox = document.querySelector('.add_photo');    
// //       previewBox.src = arg.target.result;
  
// //       // Upload the file to Firebase Storage
// //       firebase.auth().signInAnonymously().then(function() {
// //         return firebase.storage().ref('images/' + file.name).put(file);
// //       }).then(function(snapshot) {
// //         // Get the download URL for the image
// //         return snapshot.ref.getDownloadURL();
// //       }).then(function(downloadURL) {
// //         // Set the image src to the download URL
// //         document.getElementById('.add_photo').src = downloadURL;
// //       }).catch(function(error) {
// //         console.error('Error uploading image:', error);
// //       });
// //     }
// //   });





