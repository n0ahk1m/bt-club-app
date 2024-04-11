/*!
* Start Bootstrap - Heroic Features v5.0.6 (https://startbootstrap.com/template/heroic-features)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-heroic-features/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project
// When the user scrolls the page, execute myFunction
const cards = document.querySelectorAll('.card');

function toggleVisibility() {
  cards.forEach((card) => {
    const rect = card.getBoundingClientRect();
    const isVisible = rect.top < window.innerHeight && rect.bottom >= 0;
    if (isVisible) {
      card.classList.add('visible');
      card.classList.remove('hidden');
    } else {
      card.classList.add('hidden');
      card.classList.remove('visible');
    }
  });
}

// Initial check
toggleVisibility();

// Listen for scroll events
window.addEventListener('scroll', toggleVisibility);