/**
 * Trip App Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  initScrollAnimations();
  initBaggageVisualizer();
  initTippingCalculator();
});

// Scroll Reveal for Timeline and Sections
function initScrollAnimations() {
  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.15
  };

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        // If it's a bag visualizer, trigger the bars
        if (entry.target.id === 'baggage-section') {
          triggerBaggageBars();
        }
      }
    });
  }, observerOptions);

  const timelineItems = document.querySelectorAll('.trip-timeline-item');
  timelineItems.forEach(item => observer.observe(item));
  
  const sections = document.querySelectorAll('.trip-section');
  sections.forEach(sec => observer.observe(sec));
}

// Baggage Visualizer Animation
function initBaggageVisualizer() {
  // Set initial height to 0
  const zipair = document.getElementById('bag-zipair');
  const united = document.getElementById('bag-united');
  if (zipair) zipair.style.height = '0%';
  if (united) united.style.height = '0%';
}

function triggerBaggageBars() {
  setTimeout(() => {
    const zipair = document.getElementById('bag-zipair');
    const united = document.getElementById('bag-united');
    // ZIPAIR allows 7kg total (represented as 100% filling the container)
    if (zipair) zipair.style.height = '100%';
    // United allows Personal Item only (represented as smaller height)
    if (united) united.style.height = '40%';
  }, 300);
}

// Tipping Calculator Logic
function initTippingCalculator() {
  const billInput = document.getElementById('tip-bill');
  const tipButtons = document.querySelectorAll('.trip-calc-btn');
  const tipAmountEl = document.getElementById('tip-amount');
  const totalAmountEl = document.getElementById('tip-total');
  
  let currentTipPercent = 18; // default to 18% (full service restaurant min)

  if(!billInput) return;

  function calculate() {
    const bill = parseFloat(billInput.value) || 0;
    const tip = bill * (currentTipPercent / 100);
    const total = bill + tip;
    
    tipAmountEl.textContent = '$' + tip.toFixed(2);
    totalAmountEl.textContent = '$' + total.toFixed(2);
  }

  billInput.addEventListener('input', calculate);

  tipButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      // Remove active class from all
      tipButtons.forEach(b => b.classList.remove('active'));
      // Add active to clicked
      e.target.classList.add('active');
      // Set new percent
      currentTipPercent = parseFloat(e.target.dataset.tip);
      calculate();
    });
  });
}
