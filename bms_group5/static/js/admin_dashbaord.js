// Subtle card hover animation
document.querySelectorAll('.hover-animate').forEach(card => {
  card.addEventListener('mouseenter', () => {
    card.style.transform = 'translateY(-4px)';
    card.style.boxShadow = '0 10px 18px rgba(0,0,0,0.1)';
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = 'translateY(0)';
    card.style.boxShadow = '0 2px 6px rgba(0,0,0,0.08)';
  });
});
