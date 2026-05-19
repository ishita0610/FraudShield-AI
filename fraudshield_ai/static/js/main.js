// Auto-dismiss alerts
document.addEventListener('DOMContentLoaded', () => {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(100%)';
      alert.style.transition = 'all 0.4s ease';
      setTimeout(() => alert.remove(), 400);
    }, 5000);
  });

  
  document.querySelectorAll('.alert-close').forEach(btn => {
    btn.addEventListener('click', () => {
      const alert = btn.closest('.alert');
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(100%)';
      alert.style.transition = 'all 0.3s ease';
      setTimeout(() => alert.remove(), 300);
    });
  });

  
  const fill = document.querySelector('.confidence-fill');
  if (fill) {
    const width = fill.dataset.width;
    setTimeout(() => { fill.style.width = width + '%'; }, 100);
  }
});

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".confidence-fill").forEach(el => {
    const width = el.getAttribute("data-width");
    if (width) {
      el.style.width = width + "%";
    }
  });
});
