'use strict';

// Wait for Ionic custom elements to be defined
window.addEventListener('DOMContentLoaded', () => {

  const toast = document.getElementById('app-toast');

  async function showToast(msg, dur = 2800) {
    toast.message = msg;
    toast.duration = dur;
    await toast.present();
  }

  // ── Back button ────────────────────────────
  document.getElementById('back-btn').addEventListener('click', () => {
    if (history.length > 1) history.back();
    else showToast('Nothing to go back to in this demo');
  });

  // ── Save cart ──────────────────────────────
  document.getElementById('save-btn').addEventListener('click', () => {
    showToast('Cart saved — continue anytime');
  });

  // ── Promo ───────────────────────────────────
  document.getElementById('promo-apply-btn').addEventListener('click', applyPromo);
  document.getElementById('promo-field').addEventListener('keydown', e => {
    if (e.key === 'Enter') applyPromo();
  });

  function applyPromo() {
    const field = document.getElementById('promo-field');
    const val = (field.value || '').trim().toUpperCase();
    if (val === 'ACME20') {
      document.getElementById('promo-input-list').classList.add('hidden');
      document.getElementById('promo-applied-list').classList.remove('hidden');
      document.getElementById('discount-row').classList.remove('hidden');
      document.getElementById('total-amount').textContent = '$150.29';
      showToast('Promo applied — you saved $12.62 🎉');
    } else if (val) {
      showToast('Code not recognised. Try ACME20');
    }
  }

  document.getElementById('promo-remove-btn').addEventListener('click', () => {
    document.getElementById('promo-field').value = '';
    document.getElementById('promo-input-list').classList.remove('hidden');
    document.getElementById('promo-applied-list').classList.add('hidden');
    document.getElementById('discount-row').classList.add('hidden');
    document.getElementById('total-amount').textContent = '$162.91';
    showToast('Promo removed');
  });

  // ── Address ─────────────────────────────────
  document.getElementById('address-btn').addEventListener('click', () => {
    showToast('Address picker coming soon');
  });

  // ── Payment ─────────────────────────────────
  document.getElementById('pay-group').addEventListener('ionChange', e => {
    const labels = { visa: 'Visa ••4284', paypal: 'PayPal', applepay: 'Apple Pay' };
    showToast((labels[e.detail.value] || e.detail.value) + ' selected');
  });

  // ── Place order ─────────────────────────────
  document.getElementById('place-order-btn').addEventListener('click', () => {
    const total = document.getElementById('total-amount').textContent;
    showToast(`Order placed! ${total} charged. Thank you 🙌`, 3500);
  });

  // ── Tab bar ─────────────────────────────────
  ['shop', 'bag', 'orders', 'account'].forEach(name => {
    document.getElementById('tab-' + name).addEventListener('click', function () {
      document.querySelectorAll('ion-tab-button').forEach(b => b.classList.remove('tab-selected'));
      this.classList.add('tab-selected');
      if (name !== 'bag') showToast(name.charAt(0).toUpperCase() + name.slice(1) + ' — coming soon');
    });
  });

  // ── Swipe-back gesture (left-edge drag) ─────
  (() => {
    let startX = 0, startY = 0, tracking = false;
    const EDGE = 22, THRESHOLD = 80;
    const app  = document.querySelector('ion-app');

    document.addEventListener('touchstart', e => {
      const t = e.touches[0];
      if (t.clientX <= EDGE) { startX = t.clientX; startY = t.clientY; tracking = true; }
    }, { passive: true });

    document.addEventListener('touchmove', e => {
      if (!tracking) return;
      const dx = e.touches[0].clientX - startX;
      const dy = Math.abs(e.touches[0].clientY - startY);
      if (dy > 30) { tracking = false; app.style.transform = ''; return; }
      if (dx > 0) app.style.transform = `translateX(${Math.min(dx * 0.35, 55)}px)`;
    }, { passive: true });

    document.addEventListener('touchend', e => {
      if (!tracking) return;
      tracking = false;
      const dx = e.changedTouches[0].clientX - startX;
      app.style.transition = 'transform .25s';
      app.style.transform  = '';
      setTimeout(() => { app.style.transition = ''; }, 260);
      if (dx > THRESHOLD) {
        if (history.length > 1) history.back();
        else showToast('Swiped back — nothing behind this page');
      }
    });
  })();

});
