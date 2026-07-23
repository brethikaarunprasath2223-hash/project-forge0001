// static/js/main.js — global site behaviors: theme toggle, mobile sidebar, idea chips

document.addEventListener("DOMContentLoaded", () => {
  initThemeToggle();
  initMobileSidebar();
  initIdeaChips();
});

// ---------------- Theme toggle (dark / light) ----------------
function initThemeToggle() {
  const body = document.body;
  const toggleBtn = document.getElementById("themeToggle");
  const saved = localStorage.getItem("pf-theme");

  if (saved === "dark") {
    body.setAttribute("data-theme", "dark");
    if (toggleBtn) toggleBtn.textContent = "☀️";
  }

  if (!toggleBtn) return;

  toggleBtn.addEventListener("click", () => {
    const isDark = body.getAttribute("data-theme") === "dark";
    if (isDark) {
      body.removeAttribute("data-theme");
      toggleBtn.textContent = "🌙";
      localStorage.setItem("pf-theme", "light");
    } else {
      body.setAttribute("data-theme", "dark");
      toggleBtn.textContent = "☀️";
      localStorage.setItem("pf-theme", "dark");
    }

    // Persist to backend if logged in (fails silently if not authenticated)
    fetch("/settings/dark-mode", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ enabled: !isDark }),
    }).catch(() => {});
  });
}

// ---------------- Mobile sidebar ----------------
function initMobileSidebar() {
  const toggle = document.getElementById("mobileToggle");
  const sidebar = document.getElementById("sidebar");
  if (!toggle || !sidebar) return;
  toggle.addEventListener("click", () => sidebar.classList.toggle("open"));
}

// ---------------- Idea example chips ----------------
function initIdeaChips() {
  const chips = document.querySelectorAll(".idea-chip");
  const textarea = document.getElementById("ideaText");
  if (!textarea) return;
  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      textarea.value = chip.dataset.idea;
      textarea.focus();
    });
  });
}

// ---------------- Modal helpers (used by mentor request modal, etc.) ----------------
function openModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.add("active");
}
function closeModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.remove("active");
}
