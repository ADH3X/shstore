// ================
// Slider detalle
// ================
(function () {
  const sliders = document.querySelectorAll("[data-slider]");
  if (!sliders.length) return;

  sliders.forEach(setupSlider);

  function setupSlider(root) {
    const track = root.querySelector("[data-slider-track]");
    const slides = Array.from(track.children);
    const prevBtn = root.querySelector("[data-slider-prev]");
    const nextBtn = root.querySelector("[data-slider-next]");
    const dots = Array.from(
      root.parentElement.querySelectorAll("[data-slider-dot]")
    );

    if (slides.length <= 1) {
      if (prevBtn) prevBtn.style.display = "none";
      if (nextBtn) nextBtn.style.display = "none";
      return;
    }

    let index = 0;

    function update() {
      track.style.transform = `translateX(-${index * 100}%)`;

      dots.forEach((d, i) => d.classList.toggle("active", i === index));

      if (prevBtn) prevBtn.disabled = index === 0;
      if (nextBtn) nextBtn.disabled = index === slides.length - 1;
    }

    prevBtn?.addEventListener("click", () => {
      if (index > 0) {
        index--;
        update();
      }
    });

    nextBtn?.addEventListener("click", () => {
      if (index < slides.length - 1) {
        index++;
        update();
      }
    });

    dots.forEach((dot, i) => {
      dot.addEventListener("click", () => {
        index = i;
        update();
      });
    });

    // Swipe en móvil
    let startX = null;

    track.addEventListener(
      "touchstart",
      (e) => {
        startX = e.touches[0].clientX;
      },
      { passive: true }
    );

    track.addEventListener(
      "touchend",
      (e) => {
        if (startX === null) return;
        const endX = e.changedTouches[0].clientX;
        const dx = endX - startX;

        if (Math.abs(dx) > 40) {
          if (dx < 0 && index < slides.length - 1) {
            index++;
          } else if (dx > 0 && index > 0) {
            index--;
          }
          update();
        }
        startX = null;
      },
      { passive: true }
    );

    update();
  }
})();
