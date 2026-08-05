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
  const focusWithoutScroll = (node) => {
    if (!node) return;
    try {
      node.focus({preventScroll: true});
    } catch {
      node.focus();
    }
  };

  const menuButton = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.primary-nav');
  const dropdowns = Array.from(document.querySelectorAll('.nav-dropdown'));
  let menuReturnFocus = null;
  let menuScrollY = 0;
  let menuLocked = false;

  const lockPageForMenu = () => {
    if (menuLocked) return;
    const body = document.body;
    menuScrollY = window.scrollY;
    const scrollbarGap = Math.max(0, window.innerWidth - document.documentElement.clientWidth);
    body.dataset.menuScrollY = String(menuScrollY);
    body.style.position = 'fixed';
    body.style.top = `-${menuScrollY}px`;
    body.style.left = '0';
    body.style.right = '0';
    body.style.width = '100%';
    if (scrollbarGap) body.style.paddingRight = `${scrollbarGap}px`;
    body.classList.add('menu-open');
    menuLocked = true;
  };

  const unlockPageForMenu = () => {
    const body = document.body;
    if (!menuLocked) {
      body.classList.remove('menu-open');
      return;
    }
    const restoreY = Number(body.dataset.menuScrollY || menuScrollY || 0);
    const root = document.documentElement;
    const previousScrollBehavior = root.style.scrollBehavior;
    body.classList.remove('menu-open');
    body.style.removeProperty('position');
    body.style.removeProperty('top');
    body.style.removeProperty('left');
    body.style.removeProperty('right');
    body.style.removeProperty('width');
    body.style.removeProperty('padding-right');
    delete body.dataset.menuScrollY;
    root.style.scrollBehavior = 'auto';
    window.scrollTo(0, restoreY);
    window.requestAnimationFrame(() => {
      root.style.scrollBehavior = previousScrollBehavior;
    });
    menuLocked = false;
  };

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
    if (wasOpen) unlockPageForMenu();
    else document.body.classList.remove('menu-open');
    closeDropdowns();
    if (restoreFocus && wasOpen) focusWithoutScroll(menuReturnFocus || menuButton);
  };

  menuButton?.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    if (open) menuReturnFocus = document.activeElement;
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Close navigation menu' : 'Open navigation menu');
    nav?.classList.toggle('open', open);
    if (open) lockPageForMenu();
    else unlockPageForMenu();
    if (open) {
      window.requestAnimationFrame(() => {
        focusWithoutScroll(focusablesIn(nav)[0]);
      });
    }
  });

  dropdowns.forEach((dropdown) => dropdown.querySelector(':scope > button')?.addEventListener('click', (event) => {
    event.stopPropagation();
    const open = !dropdown.classList.contains('open');
    closeDropdowns(dropdown);
    dropdown.classList.toggle('open', open);
    event.currentTarget.setAttribute('aria-expanded', String(open));
    if (open && window.matchMedia('(max-width: 1100px)').matches) {
      window.requestAnimationFrame(() => {
        focusWithoutScroll(dropdown.querySelector('.mega-menu a, .mini-menu a'));
      });
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
        focusWithoutScroll(last);
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        focusWithoutScroll(first);
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
    if (!field) return;
    const errorIds = Array.from(field.querySelectorAll('.field-error[id]'), (error) => error.id);
    field.querySelectorAll('[aria-describedby]').forEach((control) => {
      const tokens = String(control.getAttribute('aria-describedby') || '')
        .split(/\s+/)
        .filter(Boolean)
        .filter((token) => !errorIds.includes(token));
      if (tokens.length) control.setAttribute('aria-describedby', tokens.join(' '));
      else control.removeAttribute('aria-describedby');
    });
    field.classList.remove('invalid');
    field.querySelectorAll('.field-error').forEach((error) => error.remove());
    field.querySelectorAll('[aria-invalid="true"]').forEach((control) => control.removeAttribute('aria-invalid'));
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
          status.innerHTML = `${error.message || 'The request could not be submitted.'} Use <a href="mailto:business@techgrity.co.zw">business@techgrity.co.zw</a> or <a href="tel:+263771825554">+263 77 182 5554</a>.`;
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
