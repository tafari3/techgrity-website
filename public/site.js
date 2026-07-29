(() => {
  'use strict';

  const menuButton = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.primary-nav');
  const dropdowns = Array.from(document.querySelectorAll('.nav-dropdown'));
  const closeDropdowns = (except = null) => dropdowns.forEach((dropdown) => {
    if (dropdown === except) return;
    dropdown.classList.remove('open');
    dropdown.querySelector(':scope > button')?.setAttribute('aria-expanded', 'false');
  });
  const closeMenu = () => {
    menuButton?.setAttribute('aria-expanded', 'false');
    menuButton?.setAttribute('aria-label', 'Open navigation menu');
    nav?.classList.remove('open'); document.body.classList.remove('menu-open'); closeDropdowns();
  };
  menuButton?.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Close navigation menu' : 'Open navigation menu');
    nav?.classList.toggle('open', open); document.body.classList.toggle('menu-open', open);
  });
  dropdowns.forEach((dropdown) => dropdown.querySelector(':scope > button')?.addEventListener('click', (event) => {
    event.stopPropagation(); const open = !dropdown.classList.contains('open'); closeDropdowns(dropdown);
    dropdown.classList.toggle('open', open); event.currentTarget.setAttribute('aria-expanded', String(open));
  }));
  document.addEventListener('click', (event) => { if (!event.target.closest('.nav-dropdown')) closeDropdowns(); });
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') closeMenu(); });
  nav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
  window.addEventListener('resize', () => { if (window.innerWidth > 1100) closeMenu(); });

  const year = document.getElementById('year'); if (year) year.textContent = String(new Date().getFullYear());

  const validateForm = (form) => {
    let valid = true;
    form.querySelectorAll('.field').forEach((field) => field.classList.remove('invalid'));
    form.querySelectorAll('[required]').forEach((control) => {
      const field = control.closest('.field');
      const missing = control.type === 'checkbox' ? !control.checked : !String(control.value || '').trim();
      const invalidEmail = control.type === 'email' && control.value && !/^\S+@\S+\.\S+$/.test(control.value);
      if (missing || invalidEmail) { valid = false; field?.classList.add('invalid'); }
    });
    const first = form.querySelector('.field.invalid input,.field.invalid select,.field.invalid textarea'); first?.focus();
    return valid;
  };
  document.querySelectorAll('form[data-form]').forEach((form) => form.addEventListener('submit', async (event) => {
    event.preventDefault(); if (!validateForm(form)) return;
    const button = form.querySelector('button[type="submit"]'); const status = form.querySelector('.form-status');
    const payload = Object.fromEntries(new FormData(form).entries()); payload.formType = form.dataset.form; payload.startedAt = form.dataset.startedAt || String(Date.now());
    button.disabled = true; button.setAttribute('aria-busy', 'true');
    status.className = 'form-status visible'; status.textContent = 'Submitting your request…';
    try {
      const response = await fetch(form.action, {method:'POST', headers:{'Content-Type':'application/json','Accept':'application/json'}, credentials:'same-origin', body:JSON.stringify(payload)});
      const result = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(result.message || 'The request could not be submitted.');
      status.className = 'form-status visible success'; status.textContent = result.message || 'Your request has been received.';
      form.reset();
      if (result.redirect) window.setTimeout(() => { window.location.href = result.redirect; }, 650);
    } catch (error) {
      status.className = 'form-status visible error';
      status.innerHTML = `${error.message || 'The request could not be submitted.'} Use <a href="mailto:business@techgrity.co.zw">business@techgrity.co.zw</a> or <a href="tel:+263783304307">+263 78 330 4307</a>.`;
    } finally { button.disabled = false; button.removeAttribute('aria-busy'); }
  }));
  document.querySelectorAll('form[data-form]').forEach((form) => { form.dataset.startedAt = String(Date.now()); });

  const panel = document.querySelector('[data-cookie-panel]');
  const manage = document.querySelector('[data-cookie-manage]');
  const key = 'techgrity-cookie-preference';
  const show = () => { if (panel) panel.hidden = false; };
  const hide = () => { if (panel) panel.hidden = true; };
  const storageGet = (name) => { try { return window.localStorage.getItem(name); } catch { return null; } };
  const storageSet = (name, value) => { try { window.localStorage.setItem(name, value); } catch { /* Storage may be unavailable in privacy-restricted contexts. */ } };
  manage?.addEventListener('click', show);
  panel?.querySelector('[data-cookie-accept]')?.addEventListener('click', () => { storageSet(key, 'current-settings'); hide(); });
  panel?.querySelector('[data-cookie-reject]')?.addEventListener('click', () => { storageSet(key, 'essential-only'); hide(); });
  if (!storageGet(key)) window.setTimeout(show, 700);
})();
