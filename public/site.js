(() => {
  'use strict';

  const focusableSelector = [
    'a[href]',
    'button:not([disabled])',
    'input:not([disabled]):not([type="hidden"])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])',
  ].join(',');

  const focusablesIn = (root) => root ? Array.from(root.querySelectorAll(focusableSelector)).filter((node) => !node.hidden && node.offsetParent !== null) : [];

  const menuButton = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.primary-nav');
  const dropdowns = Array.from(document.querySelectorAll('.nav-dropdown'));
  let menuReturnFocus = null;

  const closeDropdowns = (except = null) => dropdowns.forEach((dropdown) => {
    if (dropdown === except) return;
    dropdown.classList.remove('open');
    dropdown.querySelector(':scope > button')?.setAttribute('aria-expanded', 'false');
  });

  const closeMenu = ({restoreFocus = false} = {}) => {
    const wasOpen = menuButton?.getAttribute('aria-expanded') === 'true';
    menuButton?.setAttribute('aria-expanded', 'false');
    menuButton?.setAttribute('aria-label', 'Open navigation menu');
    nav?.classList.remove('open');
    document.body.classList.remove('menu-open');
    closeDropdowns();
    if (restoreFocus && wasOpen) (menuReturnFocus || menuButton)?.focus();
  };

  menuButton?.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    if (open) menuReturnFocus = document.activeElement;
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Close navigation menu' : 'Open navigation menu');
    nav?.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
    if (open) window.requestAnimationFrame(() => focusablesIn(nav)[0]?.focus());
  });

  dropdowns.forEach((dropdown) => dropdown.querySelector(':scope > button')?.addEventListener('click', (event) => {
    event.stopPropagation();
    const open = !dropdown.classList.contains('open');
    closeDropdowns(dropdown);
    dropdown.classList.toggle('open', open);
    event.currentTarget.setAttribute('aria-expanded', String(open));
    if (open && window.matchMedia('(max-width: 1100px)').matches) {
      window.requestAnimationFrame(() => dropdown.querySelector('.mega-menu a, .mini-menu a')?.focus());
    }
  }));

  document.addEventListener('click', (event) => {
    if (!event.target.closest('.nav-dropdown')) closeDropdowns();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      if (menuButton?.getAttribute('aria-expanded') === 'true') closeMenu({restoreFocus: true});
      else closeDropdowns();
      return;
    }
    if (event.key === 'Tab' && menuButton?.getAttribute('aria-expanded') === 'true' && window.matchMedia('(max-width: 1100px)').matches) {
      const items = focusablesIn(nav);
      if (!items.length) return;
      const first = items[0];
      const last = items[items.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  });

  nav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => closeMenu()));
  window.addEventListener('resize', () => {
    if (window.innerWidth > 1100) closeMenu();
  });

  const year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());

  const revealItems = Array.from(document.querySelectorAll('.reveal'));
  if (revealItems.length && !window.matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('reveal-ready');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      });
    }, {rootMargin: '0px 0px -7% 0px', threshold: 0.08});
    revealItems.forEach((item) => observer.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add('visible'));
  }

  const fieldContainer = (control) => control.closest('.field, .form-field');
  const clearFieldError = (field) => {
    field?.classList.remove('invalid');
    field?.querySelector('.field-error')?.remove();
    field?.querySelector('[aria-invalid="true"]')?.removeAttribute('aria-invalid');
  };
  const setFieldError = (control, message) => {
    const field = fieldContainer(control);
    if (!field) return;
    clearFieldError(field);
    field.classList.add('invalid');
    control.setAttribute('aria-invalid', 'true');
    const id = `${control.id || control.name}-error`;
    const error = document.createElement('span');
    error.className = 'field-error';
    error.id = id;
    error.textContent = message;
    field.append(error);
    const describedBy = new Set(String(control.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean));
    describedBy.add(id);
    control.setAttribute('aria-describedby', Array.from(describedBy).join(' '));
  };

  const validateForm = (form) => {
    let valid = true;
    form.querySelectorAll('.field, .form-field').forEach(clearFieldError);
    form.querySelectorAll('[required]').forEach((control) => {
      const missing = control.type === 'checkbox' ? !control.checked : !String(control.value || '').trim();
      const invalidEmail = control.type === 'email' && control.value && !/^\S+@\S+\.\S+$/.test(control.value);
      if (missing || invalidEmail) {
        valid = false;
        setFieldError(control, invalidEmail ? 'Enter a valid email address.' : 'This field is required.');
      }
    });
    const first = form.querySelector('[aria-invalid="true"]');
    first?.focus();
    return valid;
  };

  document.querySelectorAll('form[data-form]').forEach((form) => {
    form.dataset.startedAt = String(Date.now());
    const status = form.querySelector('.form-status');
    status?.setAttribute('aria-live', 'polite');
    status?.setAttribute('aria-atomic', 'true');
    form.addEventListener('input', (event) => clearFieldError(fieldContainer(event.target)));
    form.addEventListener('change', (event) => clearFieldError(fieldContainer(event.target)));
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (!validateForm(form)) return;
      const button = form.querySelector('button[type="submit"]');
      const payload = Object.fromEntries(new FormData(form).entries());
      payload.formType = form.dataset.form;
      payload.startedAt = form.dataset.startedAt || String(Date.now());
      if (button) {
        button.disabled = true;
        button.setAttribute('aria-busy', 'true');
      }
      if (status) {
        status.className = 'form-status visible';
        status.textContent = 'Submitting your request…';
      }
      try {
        const response = await fetch(form.action, {
          method: 'POST',
          headers: {'Content-Type': 'application/json', Accept: 'application/json'},
          credentials: 'same-origin',
          body: JSON.stringify(payload),
        });
        const result = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(result.message || 'The request could not be submitted.');
        if (status) {
          status.className = 'form-status visible success';
          status.textContent = result.message || 'Your request has been received.';
        }
        form.reset();
        form.dataset.startedAt = String(Date.now());
        if (result.redirect) window.setTimeout(() => { window.location.href = result.redirect; }, 650);
      } catch (error) {
        if (status) {
          status.className = 'form-status visible error';
          status.innerHTML = `${error.message || 'The request could not be submitted.'} Use <a href="mailto:business@techgrity.co.zw">business@techgrity.co.zw</a> or <a href="tel:+263783304307">+263 78 330 4307</a>.`;
        }
      } finally {
        if (button) {
          button.disabled = false;
          button.removeAttribute('aria-busy');
        }
      }
    });
  });

  const panel = document.querySelector('[data-cookie-panel]');
  const manage = document.querySelector('[data-cookie-manage]');
  const key = 'techgrity-cookie-preference';
  let cookieReturnFocus = null;
  const storageGet = (name) => { try { return window.localStorage.getItem(name); } catch { return null; } };
  const storageSet = (name, value) => { try { window.localStorage.setItem(name, value); } catch { /* Storage can be unavailable. */ } };
  const showCookiePanel = () => {
    if (!panel) return;
    cookieReturnFocus = document.activeElement instanceof HTMLElement && document.activeElement !== document.body ? document.activeElement : manage;
    panel.hidden = false;
    manage?.setAttribute('aria-expanded', 'true');
    window.requestAnimationFrame(() => focusablesIn(panel)[0]?.focus());
  };
  const hideCookiePanel = ({restoreFocus = true} = {}) => {
    if (!panel) return;
    panel.hidden = true;
    manage?.setAttribute('aria-expanded', 'false');
    if (restoreFocus) (cookieReturnFocus || manage)?.focus();
  };
  manage?.setAttribute('aria-expanded', 'false');
  if (panel?.id) manage?.setAttribute('aria-controls', panel.id);
  manage?.addEventListener('click', showCookiePanel);
  panel?.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      event.preventDefault();
      hideCookiePanel();
      return;
    }
    if (event.key !== 'Tab') return;
    const items = focusablesIn(panel);
    if (!items.length) return;
    const first = items[0];
    const last = items[items.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });
  panel?.querySelector('[data-cookie-accept]')?.addEventListener('click', () => {
    storageSet(key, 'current-settings');
    hideCookiePanel();
  });
  panel?.querySelector('[data-cookie-reject]')?.addEventListener('click', () => {
    storageSet(key, 'essential-only');
    hideCookiePanel();
  });
})();
