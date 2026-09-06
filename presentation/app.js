/* ==========================================================
   TET4100 SLT-1 Presentation Engine (app.js)
   18 Slides, Lys Profil, KaTeX auto-rendering & hurtigtaster
   ========================================================== */

document.addEventListener('DOMContentLoaded', () => {
  const slides = document.querySelectorAll('.slide');
  const totalSlides = slides.length;
  let currentSlide = 1;

  const currentSlideNumEl = document.getElementById('current-slide-num');
  const totalSlidesNumEl = document.getElementById('total-slides-num');
  const progressBar = document.getElementById('progress-bar');
  const slideSelect = document.getElementById('slide-select');
  
  const btnPrev = document.getElementById('btn-prev');
  const btnNext = document.getElementById('btn-next');
  const btnFullscreen = document.getElementById('btn-fullscreen');
  const btnGrid = document.getElementById('btn-grid');
  
  const gridModal = document.getElementById('grid-modal');
  const btnCloseGrid = document.getElementById('btn-close-grid');
  const gridCardsContainer = document.getElementById('grid-cards-container');

  // Set total count in UI
  if (totalSlidesNumEl) totalSlidesNumEl.textContent = totalSlides;

  // Slide metadata for dropdown and modal grid
  const slideTitles = [
    "1. Tittel & Intro",
    "2. Det Store Bildet (Veikart)",
    "3. Task 1 (Del 1): Kretsskjema & Oppgavetekst",
    "4. Task 1 (Del 2): Flyback-spiss & Strøm",
    "5. Task 1 i Virkeligheten (Relébeskyttelse)",
    "6. Task 2 (Del 1): Kretsskjema & Oppgavetekst",
    "7. Task 2 (Del 2): Reversering & Strømsprang",
    "8. Task 2 & 4 i Virkeligheten (Elbil Pre-charge)",
    "9. Task 3 (Del 1): Kretsskjema & Oppgavetekst",
    "10. Task 3 (Del 2): Ustabil vs Stabil",
    "11. Task 3 i Virkeligheten (Kraftnett-svingninger)",
    "12. Task 4 (Del 1): Kretsskjema & Oppgavetekst",
    "13. Task 4 (Del 2): 90% Energitap-paradokset",
    "14. Task 5: Kretsskjema & Oppgavetekst",
    "15. Task 6 (Del 1): Kretsskjema & Oppgavetekst",
    "16. Task 6 (Del 2): Digital PI-Regulering",
    "17. Task 6 i Virkeligheten (MCU & FOC-kode)",
    "18. Oppsummering & Eksamenssammendrag"
  ];

  // Populate Grid Modal
  if (gridCardsContainer) {
    gridCardsContainer.innerHTML = '';
    slideTitles.forEach((title, index) => {
      const card = document.createElement('div');
      card.className = `grid-card-item ${index + 1 === currentSlide ? 'active' : ''}`;
      card.dataset.slide = index + 1;
      card.innerHTML = `
        <div class="grid-card-num">SLIDE ${index + 1}</div>
        <div class="grid-card-title">${title}</div>
      `;
      card.addEventListener('click', () => {
        goToSlide(index + 1);
        closeGridModal();
      });
      gridCardsContainer.appendChild(card);
    });
  }

  // Go to specific slide function
  function goToSlide(slideNum) {
    if (slideNum < 1) slideNum = 1;
    if (slideNum > totalSlides) slideNum = totalSlides;

    slides.forEach((slide) => {
      const idx = parseInt(slide.dataset.slide, 10);
      if (idx === slideNum) {
        slide.classList.add('active');
      } else {
        slide.classList.remove('active');
      }
    });

    currentSlide = slideNum;
    if (currentSlideNumEl) currentSlideNumEl.textContent = currentSlide;

    // Update Progress Bar
    if (progressBar) {
      const percent = (currentSlide / totalSlides) * 100;
      progressBar.style.width = `${percent}%`;
    }

    // Update Dropdown
    if (slideSelect) {
      slideSelect.value = currentSlide;
    }

    // Update Grid active card
    const gridCards = document.querySelectorAll('.grid-card-item');
    gridCards.forEach((c) => {
      if (parseInt(c.dataset.slide, 10) === currentSlide) {
        c.classList.add('active');
      } else {
        c.classList.remove('active');
      }
    });

    // Re-render KaTeX on the newly activated slide
    renderMathOnActiveSlide();
  }

  function nextSlide() {
    if (currentSlide < totalSlides) {
      goToSlide(currentSlide + 1);
    }
  }

  function prevSlide() {
    if (currentSlide > 1) {
      goToSlide(currentSlide - 1);
    }
  }

  // Button Listeners
  if (btnNext) btnNext.addEventListener('click', nextSlide);
  if (btnPrev) btnPrev.addEventListener('click', prevSlide);

  if (slideSelect) {
    slideSelect.addEventListener('change', (e) => {
      goToSlide(parseInt(e.target.value, 10));
    });
  }

  // Grid Modal Listeners
  if (btnGrid) {
    btnGrid.addEventListener('click', () => {
      gridModal.classList.add('open');
    });
  }

  function closeGridModal() {
    if (gridModal) gridModal.classList.remove('open');
  }

  if (btnCloseGrid) btnCloseGrid.addEventListener('click', closeGridModal);
  if (gridModal) {
    gridModal.addEventListener('click', (e) => {
      if (e.target === gridModal) closeGridModal();
    });
  }

  // Fullscreen Toggle
  if (btnFullscreen) {
    btnFullscreen.addEventListener('click', () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => {
          console.warn(`Fullscreen error: ${err.message}`);
        });
      } else {
        if (document.exitFullscreen) document.exitFullscreen();
      }
    });
  }

  // Keyboard Shortcuts
  window.addEventListener('keydown', (e) => {
    // If modal is open, Escape closes it
    if (gridModal && gridModal.classList.contains('open')) {
      if (e.key === 'Escape') closeGridModal();
      return;
    }

    switch (e.key) {
      case 'ArrowRight':
      case 'PageDown':
      case ' ': // Space
        e.preventDefault();
        nextSlide();
        break;
      case 'ArrowLeft':
      case 'PageUp':
        e.preventDefault();
        prevSlide();
        break;
      case 'Home':
        e.preventDefault();
        goToSlide(1);
        break;
      case 'End':
        e.preventDefault();
        goToSlide(totalSlides);
        break;
      case 'f':
      case 'F':
        if (btnFullscreen) btnFullscreen.click();
        break;
      case 'g':
      case 'G':
        if (btnGrid) btnGrid.click();
        break;
      case 'Escape':
        closeGridModal();
        break;
    }
  });

  // KaTeX Auto Render
  function renderMathOnActiveSlide() {
    if (window.renderMathInElement) {
      const activeSlideEl = document.querySelector('.slide.active');
      if (activeSlideEl) {
        window.renderMathInElement(activeSlideEl, {
          delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '$', right: '$', display: false }
          ],
          throwOnError: false
        });
      }
    }
  }

  // Initial render when script loads
  setTimeout(() => {
    if (window.renderMathInElement) {
      window.renderMathInElement(document.body, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$', right: '$', display: false }
        ],
        throwOnError: false
      });
    }
  }, 250);

  // Initialize on Slide 1
  goToSlide(1);
});
