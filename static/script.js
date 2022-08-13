if (!localStorage.theme) localStorage.theme = "light"
document.body.className = localStorage.theme
toggleThemeImage.src = document.body.classList.contains("dark") ? "static/light.svg" : "static/dark.svg"

toggleThemeBtn.onclick = () => {
    document.body.classList.toggle("dark")
    toggleThemeImage.src = document.body.classList.contains("dark") ? "static/light.svg" : "static/dark.svg"
    localStorage.theme = document.body.className || "light"
}