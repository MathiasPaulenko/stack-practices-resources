// Theme toggle with localStorage persistence and system-preference follow.
// Companion to https://stackpractices.com/recipes/css-dark-mode-prefers-color-scheme/

function setTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("theme", theme);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme");
  setTheme(current === "dark" ? "light" : "dark");
}

document.getElementById("theme-toggle").addEventListener("click", toggleTheme);

// Follow the OS when the user hasn't chosen a theme explicitly.
window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
  if (!localStorage.getItem("theme")) {
    document.documentElement.setAttribute("data-theme", e.matches ? "dark" : "light");
  }
});
