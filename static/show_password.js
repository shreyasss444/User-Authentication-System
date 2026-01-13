function togglePassword(inputId, icon) {
    const field = document.getElementById(inputId);

    if (!field) return;

    if (field.type === "password") {
        field.type = "text";
        icon.textContent = "🙈";
    } else {
        field.type = "password";
        icon.textContent = "👁️";
    }
}
