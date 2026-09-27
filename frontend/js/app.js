/**
 * Pyrites Grill Main Application JavaScript
 * Handles REST API fetch requests, UI state, rendering, and validation.
 */

// Generic API Client helper - uses window.API_BASE from config.js
async function apiFetch(endpoint, options = {}) {
  const url = `${window.API_BASE}${endpoint}`;
  const defaultHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  };

  options.headers = { ...defaultHeaders, ...options.headers };

  try {
    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok) {
      const errorMsg = data.error || data.message || `Request failed with status ${response.status}`;
      return { success: false, status: response.status, error: errorMsg, data };
    }

    return { success: true, status: response.status, data };
  } catch (err) {
    console.error(`API Fetch Error on ${endpoint}:`, err);
    return {
      success: false,
      status: 0,
      error: 'Unable to connect to Pyrites Grill API server. Please ensure backend is running.'
    };
  }
}

// Display UI Alert Banner
function showAlert(containerId, message, type = 'error') {
  const container = document.getElementById(containerId);
  if (!container) return;

  const icon = type === 'success' ? '✓' : type === 'info' ? 'ℹ' : '⚠';
  container.innerHTML = `
    <div class="alert alert-${type}">
      <span>${icon}</span>
      <div>${message}</div>
    </div>
  `;
}

function clearAlert(containerId) {
  const container = document.getElementById(containerId);
  if (container) container.innerHTML = '';
}

/* ==========================================================================
   MENU PAGE LOGIC
   ========================================================================== */
let allMenuItems = [];

async function initMenuPage() {
  const grid = document.getElementById('menu-grid');
  if (!grid) return;

  grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-muted);">Loading delicious items...</div>`;

  const res = await apiFetch('/menu');
  if (!res.success) {
    showAlert('menu-alert', res.error, 'error');
    grid.innerHTML = '';
    return;
  }

  allMenuItems = res.data.items || [];
  renderMenuItems(allMenuItems);

  // Bind category tabs
  const tabs = document.querySelectorAll('.category-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', (e) => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const cat = tab.dataset.category;
      if (cat === 'all') {
        renderMenuItems(allMenuItems);
      } else {
        const filtered = allMenuItems.filter(item => item.category.toLowerCase() === cat.toLowerCase());
        renderMenuItems(filtered);
      }
    });
  });
}

function renderMenuItems(items) {
  const grid = document.getElementById('menu-grid');
  if (!grid) return;

  if (items.length === 0) {
    grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-muted);">No menu items found in this category.</div>`;
    return;
  }

  grid.innerHTML = items.map(item => `
    <div class="menu-card">
      <div class="menu-img-wrapper">
        <img src="${item.image_url}" alt="${item.name}" class="menu-img" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80'">
        <span class="category-badge">${item.category}</span>
      </div>
      <div class="menu-body">
        <div class="menu-header">
          <h3 class="menu-item-title">${item.name}</h3>
          <span class="menu-item-price">₹${item.price_inr}</span>
        </div>
        <p class="menu-item-desc">${item.description}</p>
      </div>
    </div>
  `).join('');
}

/* ==========================================================================
   BOOKING PAGE LOGIC
   ========================================================================== */
function initBookingPage() {
  const bookingForm = document.getElementById('booking-form');
  const dateInput = document.getElementById('booking_date');
  
  if (!bookingForm) return;

  // Set min date to today YYYY-MM-DD
  if (dateInput) {
    const today = new Date().toISOString().split('T')[0];
    dateInput.min = today;
    dateInput.value = today;
  }

  // Handle availability check
  const btnCheck = document.getElementById('btn-check-availability');
  if (btnCheck) {
    btnCheck.addEventListener('click', handleCheckAvailability);
  }

  // Handle form submission
  bookingForm.addEventListener('submit', handleCreateBooking);
}

async function handleCheckAvailability() {
  const dateVal = document.getElementById('booking_date').value;
  const timeVal = document.getElementById('booking_time').value;
  const guestsVal = document.getElementById('guest_count').value;

  clearAlert('booking-alert');

  if (!dateVal || !timeVal || !guestsVal) {
    showAlert('booking-alert', 'Please select date, time, and guest count before checking availability.', 'error');
    return;
  }

  const btnCheck = document.getElementById('btn-check-availability');
  btnCheck.disabled = true;
  btnCheck.innerHTML = `<span class="spinner"></span> Checking...`;

  const res = await apiFetch(`/availability?date=${dateVal}&time=${timeVal}&guests=${guestsVal}`);
  
  btnCheck.disabled = false;
  btnCheck.innerHTML = `Check Availability`;

  if (!res.success) {
    showAlert('booking-alert', res.error, 'error');
    return;
  }

  if (res.data.available) {
    showAlert('booking-alert', `✓ ${res.data.message} (${res.data.available_tables_count} table(s) available)`, 'success');
  } else {
    showAlert('booking-alert', `⚠ ${res.data.message}`, 'error');
  }
}

async function handleCreateBooking(e) {
  e.preventDefault();
  clearAlert('booking-alert');

  const btnSubmit = document.getElementById('btn-submit-booking');
  const originalText = btnSubmit.innerHTML;

  const payload = {
    customer_name: document.getElementById('customer_name').value.trim(),
    customer_email: document.getElementById('customer_email').value.trim(),
    customer_phone: document.getElementById('customer_phone').value.trim(),
    booking_date: document.getElementById('booking_date').value,
    booking_time: document.getElementById('booking_time').value,
    guest_count: parseInt(document.getElementById('guest_count').value),
    special_requests: document.getElementById('special_requests').value.trim()
  };

  btnSubmit.disabled = true;
  btnSubmit.innerHTML = `<span class="spinner"></span> Confirming Table...`;

  const res = await apiFetch('/bookings', {
    method: 'POST',
    body: JSON.stringify(payload)
  });

  btnSubmit.disabled = false;
  btnSubmit.innerHTML = originalText;

  if (!res.success) {
    showAlert('booking-alert', res.error, 'error');
    return;
  }

  // Hide form and show confirmation card
  document.getElementById('booking-form-wrapper').style.display = 'none';
  renderBookingConfirmation(res.data.booking);
}

function renderBookingConfirmation(booking) {
  const resultWrapper = document.getElementById('booking-result-wrapper');
  if (!resultWrapper) return;

  resultWrapper.style.display = 'block';
  resultWrapper.innerHTML = `
    <div class="confirmation-card">
      <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎉</div>
      <h2 style="font-size: 2rem; margin-bottom: 0.5rem;">Reservation Confirmed!</h2>
      <p style="color: var(--text-muted);">Save your booking reference to manage your reservation.</p>

      <div class="ref-badge">${booking.booking_reference}</div>

      <div class="booking-details-grid">
        <div class="detail-item">
          <span class="detail-label">Guest Name</span>
          <span class="detail-value">${booking.customer_name}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Status</span>
          <span class="detail-value"><span class="status-tag confirmed">● CONFIRMED</span></span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Date & Time</span>
          <span class="detail-value">${booking.booking_date} @ ${booking.booking_time}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Party Size</span>
          <span class="detail-value">${booking.guest_count} Guests</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Table & Zone</span>
          <span class="detail-value">${booking.table_number} (${booking.location_zone})</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Contact Email</span>
          <span class="detail-value">${booking.customer_email}</span>
        </div>
        ${booking.special_requests ? `
        <div class="detail-item" style="grid-column: span 2;">
          <span class="detail-label">Special Requests</span>
          <span class="detail-value" style="font-weight: 400;">${booking.special_requests}</span>
        </div>` : ''}
      </div>

      <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 2rem;">
        <a href="index.html" class="btn btn-secondary">Return Home</a>
        <a href="my-booking.html?ref=${booking.booking_reference}&email=${encodeURIComponent(booking.customer_email)}" class="btn btn-primary">View / Manage Booking</a>
      </div>
    </div>
  `;

  // Scroll smoothly to confirmation
  resultWrapper.scrollIntoView({ behavior: 'smooth' });
}

/* ==========================================================================
   MY BOOKING (FIND / CANCEL) PAGE LOGIC
   ========================================================================== */
function initMyBookingPage() {
  const form = document.getElementById('search-booking-form');
  if (!form) return;

  // Check query params if pre-filled from confirmation page
  const urlParams = new URLSearchParams(window.location.search);
  const refParam = urlParams.get('ref');
  const emailParam = urlParams.get('email');

  if (refParam && emailParam) {
    document.getElementById('search_ref').value = refParam;
    document.getElementById('search_email').value = emailParam;
    fetchBookingDetails(refParam, emailParam);
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const ref = document.getElementById('search_ref').value.trim();
    const email = document.getElementById('search_email').value.trim();
    fetchBookingDetails(ref, email);
  });
}

async function fetchBookingDetails(reference, email) {
  clearAlert('search-alert');
  const resultWrapper = document.getElementById('booking-detail-wrapper');
  resultWrapper.innerHTML = `<div style="text-align: center; padding: 3rem; color: var(--text-muted);"><span class="spinner"></span> Retrieving reservation details...</div>`;

  if (!reference || !email) {
    showAlert('search-alert', 'Please provide both Booking Reference and Email.', 'error');
    resultWrapper.innerHTML = '';
    return;
  }

  const res = await apiFetch(`/bookings/${reference}?email=${encodeURIComponent(email)}`);

  if (!res.success) {
    showAlert('search-alert', res.error, 'error');
    resultWrapper.innerHTML = '';
    return;
  }

  renderBookingManagement(res.data.booking);
}

function renderBookingManagement(booking) {
  const resultWrapper = document.getElementById('booking-detail-wrapper');
  const isCancelled = booking.status === 'CANCELLED';

  resultWrapper.innerHTML = `
    <div class="confirmation-card">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem; margin-bottom: 1.5rem;">
        <h3 style="font-size: 1.5rem;">Reservation ${booking.booking_reference}</h3>
        <span class="status-tag ${isCancelled ? 'cancelled' : 'confirmed'}">
          ● ${booking.status}
        </span>
      </div>

      <div class="booking-details-grid">
        <div class="detail-item">
          <span class="detail-label">Guest Name</span>
          <span class="detail-value">${booking.customer_name}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Date & Time</span>
          <span class="detail-value">${booking.booking_date} @ ${booking.booking_time}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Party Size</span>
          <span class="detail-value">${booking.guest_count} Guests</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Assigned Table</span>
          <span class="detail-value">${booking.table_number} (${booking.location_zone})</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Customer Email</span>
          <span class="detail-value">${booking.customer_email}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Phone</span>
          <span class="detail-value">${booking.customer_phone}</span>
        </div>
        ${booking.special_requests ? `
        <div class="detail-item" style="grid-column: span 2;">
          <span class="detail-label">Special Requests</span>
          <span class="detail-value" style="font-weight: 400;">${booking.special_requests}</span>
        </div>` : ''}
      </div>

      ${!isCancelled ? `
      <div style="margin-top: 2rem; pt: 1rem; border-top: 1px solid var(--border-color);">
        <button id="btn-cancel-booking" class="btn btn-danger btn-full" onclick="handleCancelBooking('${booking.booking_reference}', '${booking.customer_email}')">
          Cancel Reservation
        </button>
      </div>` : `
      <div class="alert alert-info" style="margin-top: 1.5rem;">
        This reservation has been cancelled.
      </div>`}
    </div>
  `;
}

async function handleCancelBooking(reference, email) {
  if (!confirm(`Are you sure you want to cancel reservation ${reference}? This action cannot be undone.`)) {
    return;
  }

  const btn = document.getElementById('btn-cancel-booking');
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `<span class="spinner"></span> Cancelling...`;
  }

  const res = await apiFetch(`/bookings/${reference}/cancel`, {
    method: 'POST',
    body: JSON.stringify({ email })
  });

  if (!res.success) {
    showAlert('search-alert', res.error, 'error');
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = 'Cancel Reservation';
    }
    return;
  }

  showAlert('search-alert', 'Reservation cancelled successfully.', 'success');
  renderBookingManagement(res.data.booking);
}

// Global page initialization router
document.addEventListener('DOMContentLoaded', () => {
  initMenuPage();
  initBookingPage();
  initMyBookingPage();
});
