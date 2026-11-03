const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav-links');
toggle.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  toggle.setAttribute('aria-expanded', String(open));
});
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  nav.classList.remove('open');
  toggle.setAttribute('aria-expanded', 'false');
}));
document.getElementById('year').textContent = new Date().getFullYear();

const backTop = document.querySelector('.back-top');
window.addEventListener('scroll', () => backTop.classList.toggle('visible', window.scrollY > 450));
backTop.addEventListener('click', () => window.scrollTo({top: 0, behavior: 'smooth'}));

// PERSONALIZE: replace these example values with your real contact links.
const contact = {
  email: 'SEUEMAIL@EXEMPLO.COM',
  github: 'https://github.com/SEU-USUARIO',
  linkedin: 'https://www.linkedin.com/in/SEU-PERFIL'
};
document.getElementById('email-link').href = `mailto:${contact.email}`;
document.getElementById('github-link').href = contact.github;
document.getElementById('linkedin-link').href = contact.linkedin;
