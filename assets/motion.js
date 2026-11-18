const nav = document.querySelector('.nav-shell');
const hero = document.querySelector('.hero');
const progress = document.querySelector('.reading-progress');
const motion = matchMedia('(prefers-reduced-motion: reduce)');
let frame = 0;

function updateScroll() {
  frame = 0;
  const scroll = Math.max(0, window.scrollY);
  const available = document.documentElement.scrollHeight - innerHeight;
  nav.classList.toggle('scrolled', scroll > 24);
  progress.style.transform = 'scaleX(' + (available > 0 ? Math.min(scroll / available, 1) : 0) + ')';
  if (!motion.matches && scroll <= hero.offsetHeight) {
    hero.style.setProperty('--pan', (scroll * 0.23) + 'px');
    hero.style.setProperty('--fade', Math.min(1, scroll / hero.offsetHeight));
  } else if (motion.matches) {
    hero.style.removeProperty('--pan');
    hero.style.removeProperty('--fade');
  }
}

function requestScrollUpdate() {
  if (!frame) frame = requestAnimationFrame(updateScroll);
}

addEventListener('scroll', requestScrollUpdate, { passive: true });
addEventListener('resize', requestScrollUpdate);
motion.addEventListener('change', requestScrollUpdate);
updateScroll();

if ('IntersectionObserver' in window && !motion.matches) {
  const reveal = new IntersectionObserver(entries => {
    for (const { target, isIntersecting } of entries) {
      if (isIntersecting) {
        target.classList.add('in-view');
        reveal.unobserve(target);
      }
    }
  }, { rootMargin: '0px 0px 6% 0px' });

  const groups = document.querySelectorAll([
    '.section-head', '.dashboard', '.story-heading', '.story-list li',
    '.solution > *', '.process h2', '.steps li', '#features h2', '.features-grid li',
    '.editorial-grid > div', '.editorial-list li', '.partners-wrap h2',
    '.partners-intro', '.partners-card', '.partners-model', '.team h2',
    '.team-grid li', '.faq h2', '.faq details', '.closing .wrap',
  ].join(', '));

  for (const element of groups) {
    const index = element.matches('li, .partners-card')
      ? Array.from(element.parentElement.children).indexOf(element)
      : 0;
    element.style.setProperty('--stagger', Math.min(index, 3) * 75 + 'ms');
    element.classList.add('reveal-on-scroll');
    reveal.observe(element);
  }
}
