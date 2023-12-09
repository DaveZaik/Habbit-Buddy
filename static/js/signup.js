document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.querySelector(".signup-form");
    const loginForm = document.querySelector(".login-form");

    document.querySelector(".toggle-signup").addEventListener("click", function () {
        signupForm.classList.remove("slide-up");
        loginForm.classList.add("slide-up");
    });

    document.querySelector(".toggle-login").addEventListener("click", function () {
        loginForm.classList.remove("slide-up");
        signupForm.classList.add("slide-up");
    });
});
