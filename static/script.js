const passwordInput = document.getElementById("password");
const strengthBar = document.getElementById("strength-bar");

passwordInput.addEventListener("input", () => {
    const val = passwordInput.value;
    let strength = 0;

    if (val.length >= 12) strength += 25;
    if (/[A-Z]/.test(val)) strength += 15;
    if (/[a-z]/.test(val)) strength += 15;
    if (/[0-9]/.test(val)) strength += 15;
    if (/[^A-Za-z0-9]/.test(val)) strength += 15;

    strengthBar.style.width = strength + "%";
    strengthBar.style.backgroundColor =
        strength < 50 ? "red" : strength < 75 ? "orange" : "green";
});
