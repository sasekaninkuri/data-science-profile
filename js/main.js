/* ══════════════════════════════════════════
   Sasekani Maluleke — Portfolio JS
   ══════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ── CUSTOM CURSOR ──────────────────────────
  const cursor = document.getElementById('cursor');
  const ring = document.getElementById('cursorRing');
  let mx = 0, my = 0, rx = 0, ry = 0;

  document.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
    cursor.style.transform = `translate(${mx - 5}px, ${my - 5}px)`;
  });

  function animateRing() {
    rx += (mx - rx - 16) * 0.13;
    ry += (my - ry - 16) * 0.13;
    ring.style.transform = `translate(${rx}px, ${ry}px)`;
    requestAnimationFrame(animateRing);
  }
  animateRing();

  // Cursor hover state
  const hoverEls = document.querySelectorAll('a, button, .badge, .skill-card, .exp-card, .photo-badge, .stack-pill');
  hoverEls.forEach(el => {
    el.addEventListener('mouseenter', () => ring.classList.add('hover'));
    el.addEventListener('mouseleave', () => ring.classList.remove('hover'));
  });


  // ── NAVBAR SCROLL ──────────────────────────
  const navbar = document.getElementById('navbar');
  const navLinks = document.querySelectorAll('.nav-link');

  window.addEventListener('scroll', () => {
    // Sticky nav style
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }

    // Active nav link
    const sections = document.querySelectorAll('section[id]');
    let current = '';
    sections.forEach(sec => {
      if (window.scrollY >= sec.offsetTop - 120) current = sec.getAttribute('id');
    });
    navLinks.forEach(link => {
      link.classList.toggle('active', link.getAttribute('href') === `#${current}`);
    });
  });


  // ── MOBILE HAMBURGER ──────────────────────
  const hamburger = document.getElementById('hamburger');
  const navLinksEl = document.getElementById('navLinks');
  hamburger.addEventListener('click', () => {
    navLinksEl.classList.toggle('open');
    const spans = hamburger.querySelectorAll('span');
    if (navLinksEl.classList.contains('open')) {
      spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
      spans[1].style.opacity = '0';
      spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
    } else {
      spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    }
  });

  // Close nav on link click (mobile)
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      navLinksEl.classList.remove('open');
      hamburger.querySelectorAll('span').forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    });
  });


  // ── SCROLL REVEAL ─────────────────────────
  // Hero elements (on load)
  const heroReveal = document.querySelectorAll('.reveal, .reveal-right');
  setTimeout(() => {
    heroReveal.forEach(el => el.classList.add('visible'));
  }, 100);

  // Scroll-triggered reveals
  const scrollReveal = document.querySelectorAll('.scroll-reveal');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => entry.target.classList.add('visible'), i * 80);
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });

  scrollReveal.forEach(el => revealObserver.observe(el));


  // ── ANIMATED COUNTERS ─────────────────────
  const counters = document.querySelectorAll('.counter-num');
  let countersStarted = false;

  function startCounters() {
    if (countersStarted) return;
    countersStarted = true;
    counters.forEach(counter => {
      const target = parseInt(counter.dataset.target);
      const duration = 1600;
      const step = target / (duration / 16);
      let current = 0;
      const timer = setInterval(() => {
        current += step;
        if (current >= target) { current = target; clearInterval(timer); }
        counter.textContent = Math.floor(current);
      }, 16);
    });
  }

  const heroSection = document.querySelector('.hero');
  const counterObserver = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) startCounters();
  }, { threshold: 0.3 });
  if (heroSection) counterObserver.observe(heroSection);


  // ── PARTICLE CANVAS ───────────────────────
  const canvas = document.getElementById('particleCanvas');
  const ctx = canvas.getContext('2d');
  let particles = [];
  let W, H;

  function resizeCanvas() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);

  class Particle {
    constructor() { this.reset(); }
    reset() {
      this.x = Math.random() * W;
      this.y = Math.random() * H;
      this.size = Math.random() * 1.2 + 0.3;
      this.speedX = (Math.random() - 0.5) * 0.25;
      this.speedY = (Math.random() - 0.5) * 0.25;
      this.opacity = Math.random() * 0.4 + 0.1;
      this.color = Math.random() > 0.7 ? '#00d4ff' : Math.random() > 0.5 ? '#7b61ff' : '#e8f0fe';
    }
    update() {
      this.x += this.speedX;
      this.y += this.speedY;
      if (this.x < 0 || this.x > W || this.y < 0 || this.y > H) this.reset();
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.globalAlpha = this.opacity;
      ctx.fill();
    }
  }

  for (let i = 0; i < 70; i++) particles.push(new Particle());

  function animateParticles() {
    ctx.clearRect(0, 0, W, H);
    ctx.globalAlpha = 1;
    particles.forEach(p => { p.update(); p.draw(); });

    // Draw connecting lines
    ctx.globalAlpha = 1;
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 90) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(0,212,255,${0.06 * (1 - dist / 90)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(animateParticles);
  }
  animateParticles();


  // ── CHART BAR ANIMATION ───────────────────
  const chartBars = document.querySelectorAll('.chart-bar-fill, .model-fill');
  const chartObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animationPlayState = 'running';
      }
    });
  }, { threshold: 0.3 });

  chartBars.forEach(bar => {
    bar.style.animationPlayState = 'paused';
    chartObserver.observe(bar);
  });


  // ── SKILL CARD GLOW ON HOVER ──────────────
  document.querySelectorAll('.skill-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 100;
      const y = ((e.clientY - rect.top) / rect.height) * 100;
      card.style.setProperty('--mouse-x', `${x}%`);
      card.style.setProperty('--mouse-y', `${y}%`);
    });
  });


  // ── BADGE ACTIVE TOGGLE ───────────────────
  document.querySelectorAll('.hero-badges .badge').forEach(badge => {
    badge.addEventListener('click', () => {
      document.querySelectorAll('.hero-badges .badge').forEach(b => b.classList.remove('active'));
      badge.classList.add('active');
    });
  });


  // ── SMOOTH SCROLL ─────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });


  // ── CONTACT FORM ──────────────────────────
  const contactForm = document.getElementById('contactForm');
  const formSuccess = document.getElementById('formSuccess');

  if (contactForm) {
    contactForm.addEventListener('submit', e => {
      e.preventDefault();
      const btn = contactForm.querySelector('button[type="submit"]');
      btn.textContent = 'Sending...';
      btn.disabled = true;

      setTimeout(() => {
        contactForm.reset();
        formSuccess.classList.add('show');
        btn.textContent = 'Send Message →';
        btn.disabled = false;
        setTimeout(() => formSuccess.classList.remove('show'), 5000);
      }, 1200);
    });
  }


  // ── TYPING EFFECT ON HERO TITLE ───────────
  const highlight = document.querySelector('.hero-title .highlight');
  if (highlight) {
    const roles = ['Data Scientist', 'ML Engineer', 'Data Analyst', 'BI Developer'];
    let roleIndex = 0, charIndex = 0, deleting = false;

    function typeRole() {
      const current = roles[roleIndex];
      if (!deleting) {
        highlight.textContent = current.substring(0, charIndex + 1);
        charIndex++;
        if (charIndex === current.length) {
          deleting = true;
          setTimeout(typeRole, 2200);
          return;
        }
      } else {
        highlight.textContent = current.substring(0, charIndex - 1);
        charIndex--;
        if (charIndex === 0) {
          deleting = false;
          roleIndex = (roleIndex + 1) % roles.length;
        }
      }
      setTimeout(typeRole, deleting ? 55 : 95);
    }

    setTimeout(typeRole, 1800);
  }


  // ── TILT EFFECT ON PHOTO ──────────────────
  const photoFrame = document.querySelector('.photo-frame');
  if (photoFrame) {
    photoFrame.addEventListener('mousemove', e => {
      const rect = photoFrame.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      photoFrame.style.transform = `perspective(800px) rotateY(${x * 8}deg) rotateX(${-y * 6}deg)`;
    });
    photoFrame.addEventListener('mouseleave', () => {
      photoFrame.style.transform = 'perspective(800px) rotateY(0) rotateX(0)';
    });
  }


  // ── SCROLL PROGRESS BAR ───────────────────
  const progressBar = document.createElement('div');
  progressBar.style.cssText = `
    position: fixed; top: 0; left: 0; height: 2px; z-index: 9999;
    background: linear-gradient(90deg, #00d4ff, #7b61ff);
    transition: width 0.1s; width: 0%;
  `;
  document.body.appendChild(progressBar);

  window.addEventListener('scroll', () => {
    const scrolled = window.scrollY;
    const total = document.body.scrollHeight - window.innerHeight;
    progressBar.style.width = `${(scrolled / total) * 100}%`;
  });


  // ── BACK TO TOP ───────────────────────────
  const backTop = document.createElement('button');
  backTop.innerHTML = '↑';
  backTop.style.cssText = `
    position: fixed; bottom: 32px; right: 32px;
    width: 42px; height: 42px;
    background: rgba(13,21,32,0.9); color: #00d4ff;
    border: 1px solid rgba(0,212,255,0.3); cursor: none;
    font-size: 18px; z-index: 999;
    opacity: 0; transition: opacity 0.3s, border-color 0.2s;
    display: flex; align-items: center; justify-content: center;
    backdrop-filter: blur(10px);
  `;
  document.body.appendChild(backTop);

  window.addEventListener('scroll', () => {
    backTop.style.opacity = window.scrollY > 400 ? '1' : '0';
  });
  backTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  backTop.addEventListener('mouseenter', () => {
    backTop.style.borderColor = '#00d4ff';
    ring.classList.add('hover');
  });
  backTop.addEventListener('mouseleave', () => {
    backTop.style.borderColor = 'rgba(0,212,255,0.3)';
    ring.classList.remove('hover');
  });


  console.log('%c Sasekani Maluleke — Portfolio ', 'background: #00d4ff; color: #060910; font-size: 14px; font-weight: bold; padding: 8px 16px;');
  console.log('%c Data Scientist · Full Stack · Cybersecurity ', 'color: #7b61ff; font-size: 12px;');

});
