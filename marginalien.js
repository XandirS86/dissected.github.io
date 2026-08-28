/* Richtet jede .marginalie[data-ref="n"] an ihrer Fußnotenziffer sup.ref im Text aus.
   Läuft nur auf breiten Bildschirmen; mobil stehen Marginalien im Textfluss. */
(function () {
  function ausrichten() {
    var artikel = document.querySelector('.artikel');
    var rand = document.querySelector('.artikel__rand');
    if (!artikel || !rand) return;
    var breit = window.innerWidth > 760;
    var unten = 0;
    document.querySelectorAll('.marginalie').forEach(function (m) {
      if (!breit) { m.style.top = ''; return; }
      var ref = artikel.querySelector('sup.ref[data-ref="' + m.dataset.ref + '"]');
      if (!ref) return;
      var top = ref.getBoundingClientRect().top - rand.getBoundingClientRect().top - 2;
      if (top < unten) top = unten;
      m.style.top = top + 'px';
      unten = top + m.offsetHeight + 24;
    });
  }
  window.addEventListener('load', ausrichten);
  window.addEventListener('resize', ausrichten);
  if (document.fonts) document.fonts.ready.then(ausrichten);
})();
