function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// 0 name 1 password
var charset = ['ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?'];

// https://stackoverflow.com/questions/1349404/generate-random-string-characters-in-javascript?page=1&tab=votes#tab-top
function getRandomStr(length, subset) {
    var result           = '';
    var charactersLength = charset[subset].length;
    for ( var i = 0; i < length; i++ ) {
      result += charset[subset].charAt(Math.floor(Math.random() * 
 charactersLength));
   }
   return result;
}

var pw = "";
var first_name = getRandomStr(getRandomInt(5,10), 0);
var last_name = getRandomStr(getRandomInt(5,10),0);
var number_pattern = /\d/;
var special_char_pattern = /[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]/;
var uppercase_pattern = /[A-Z]/;
var lowercase_pattern = /[a-z]/;

do {
  try {
    pw = decodeURI(getRandomStr(getRandomInt(8,12),1));
  } catch(e) {
    console.log("decodeURI exception", e);
  }
} while (!special_char_pattern.test(pw) || !number_pattern.test(pw) || !uppercase_pattern.test(pw) || !lowercase_pattern.test(pw))

setTimeout(function(){},1000);

document.querySelector("#field_email").value = "";
document.querySelector("#field_firstname").value = first_name;
document.querySelector("#field_lastname").value = last_name;
document.querySelector("#field_password").value = pw;
document.querySelector("#field_password2").value = pw;

console.log("E-Mail ", "", "First Name ", first_name, "Last Name ", last_name, "Password ", pw);
