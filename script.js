// Header scroll state
const header = document.getElementById('siteHeader');
let lastY = 0;
window.addEventListener('scroll', () => {
  const y = window.scrollY;
  if (y > 24) header.classList.add('scrolled');
  else header.classList.remove('scrolled');
  lastY = y;
}, { passive: true });

// Reveal on scroll
const revealEls = document.querySelectorAll(
  '.section-eyebrow, .section-title, .section-lead, .hero-content > *, ' +
  '.benefit-item, .type-card, .lesson, .audience-list li, ' +
  '.schedule-info > div, .entry-card, .entry-notice, .pull-quote, ' +
  '.concept-text p, .concept-image, .classroom-image, ' +
  '.question-tag, .question-title, .question-lead, .typology-note, .curriculum-note, ' +
  '.typology-banner'
);
revealEls.forEach(el => el.classList.add('reveal'));

// Use IO when supported; fall back to immediate reveal.
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e, i) => {
      if (e.isIntersecting) {
        const delay = (i % 6) * 60;
        e.target.style.transitionDelay = delay + 'ms';
        e.target.classList.add('is-in');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.05, rootMargin: '0px 0px -4% 0px' });
  revealEls.forEach(el => io.observe(el));
  // Safety: anything not yet revealed after 3s gets shown
  setTimeout(() => {
    document.querySelectorAll('.reveal:not(.is-in)').forEach(el => el.classList.add('is-in'));
  }, 3000);
} else {
  revealEls.forEach(el => el.classList.add('is-in'));
}

// Smooth-scroll already handled by CSS scroll-behavior. Add header offset.
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', (e) => {
    const id = a.getAttribute('href');
    if (id.length <= 1) return;
    const el = document.querySelector(id);
    if (!el) return;
    e.preventDefault();
    const top = el.getBoundingClientRect().top + window.scrollY - 72;
    window.scrollTo({ top, behavior: 'smooth' });
  });
});
