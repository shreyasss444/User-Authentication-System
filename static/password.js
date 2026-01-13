document.addEventListener("DOMContentLoaded", () => {
    const password = document.getElementById("password");
    const strength = document.getElementById("strength");

    if (!password) return;

    password.addEventListener("input", () => {
        const value = password.value;

        if (value.length < 6) {
            strength.textContent = "Weak";
            strength.style.color = "red";
        } else if (value.match(/[A-Z]/) && value.match(/[0-9]/)) {
            strength.textContent = "Strong";
            strength.style.color = "green";
        } else {
            strength.textContent = "Medium";
            strength.style.color = "orange";
        }
    });
});
