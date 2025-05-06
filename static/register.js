document.getElementById("togglePassword").addEventListener("click", function() {
    var passwordField = document.getElementById("password");
    
    if (passwordField.type === "password") {
        passwordField.type = "text";  // Şifreyi metin olarak göster
        passwordField.classList.add("big-font");  // Yazı büyüsün
    } else {
        passwordField.type = "password";  // Şifreyi gizle
        passwordField.classList.remove("big-font");  // Yazı eski boyuta dönsün
    }
});

