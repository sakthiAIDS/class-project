/* ==========================================================================
   Food Donation Management System — main.js
   Handles: dark mode, mobile sidebar, animated stat counters, toasts
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {

  /* ---------- Dark mode ---------- */
  const root = document.documentElement;
  const darkToggle = document.getElementById("darkModeToggle");
  const savedTheme = localStorage.getItem("fs_theme") || "light";
  root.setAttribute("data-theme", savedTheme);
  updateDarkIcon(savedTheme);

  darkToggle?.addEventListener("click", () => {
    const current = root.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    localStorage.setItem("fs_theme", next);
    updateDarkIcon(next);
  });

  function updateDarkIcon(theme) {
    const icon = darkToggle?.querySelector("i");
    if (!icon) return;
    icon.className = theme === "dark" ? "fa-solid fa-sun" : "fa-solid fa-moon";
  }

  /* ---------- Mobile sidebar ---------- */
  const sidebar = document.getElementById("sidebar");
  const sidebarToggle = document.getElementById("sidebarToggle");
  const backdrop = document.getElementById("sidebarBackdrop");

  sidebarToggle?.addEventListener("click", () => {
    sidebar.classList.add("open");
    backdrop.classList.add("show");
  });
  backdrop?.addEventListener("click", () => {
    sidebar.classList.remove("open");
    backdrop.classList.remove("show");
  });

  /* ---------- Animated stat counters ---------- */
  document.querySelectorAll("[data-count]").forEach(el => {
    const target = parseInt(el.dataset.count, 10) || 0;
    let current = 0;
    const step = Math.max(1, Math.ceil(target / 40));
    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        el.textContent = target.toLocaleString();
        clearInterval(timer);
      } else {
        el.textContent = current.toLocaleString();
      }
    }, 20);
  });

  /* ---------- Auto-dismiss toasts ---------- */
  document.querySelectorAll(".toast").forEach(toastEl => {
    setTimeout(() => {
      const toast = bootstrap.Toast.getOrCreateInstance(toastEl);
      toast.hide();
    }, 4500);
  });

});
