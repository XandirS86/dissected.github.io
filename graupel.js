/* Alltagsgrau (seit 22.11.2026): die dritte Laune neben düster und heiter. Sie stellt sich von selbst ein, wenn nichts passiert.
   Bleibt die Seite eine Weile unberührt, zieht langsam ein Graupelschauer auf (etwa acht Sekunden, in Stufen): erst einzelne
   Körner, dann wird die Seite grau, dann wird der Graupel dicht. Die Seite wandert dabei auf die Laune zu, die gerade nicht gilt,
   und bleibt in der Mitte stehen. Der Knopf am Schalter gleitet in die Mitte.
   Die erste Regung (Maus, Scrollen, Tippen, Taste) blendet den Schauer wieder aus, die Seite kehrt in ihre Laune zurück.
   Zweiter Weg hinein: den Schalter dreimal kurz hintereinander umlegen, dann zieht der Schauer zügig auf.
   Gespeichert wird nichts, die gewählte Laune (hell/dunkel) bleibt unberührt.
   Aussehen (Grau, Graupel, Beschriftung) steht in styles.css unter „Alltagsgrau“. */
(function () {
  'use strict';
  var WARTEN_KURZ = 15000;   // Startseite und Archiv: so lange muss Ruhe sein (ms)
  var WARTEN_LANG = 90000;   // alle anderen Seiten, vor allem Artikel: Lesen heißt stillhalten
  var FENSTER = 3500;        // drei Klicks auf den Schalter in dieser Zeit lösen den Schauer sofort aus
  var SCHONFRIST = 3500;     // nach den drei Klicks zählt so lange keine Regung, sonst wäre der Schauer sofort vorbei
  var GRAU_AB = 2500;        // aus der Ruhe: erst nach den ersten Körnern wird es grau (passt zur Verzögerung in styles.css)
  var SCHONFRIST_RUHE = 400; // nach dem Einblenden aus der Ruhe: fängt Scheinbewegungen des Browsers ab
  var AUSBLENDEN = 800;      // muss zur Dauer in styles.css passen (.graupel.ab)

  function start() {
    var wurzel = document.documentElement;
    var schalter = document.querySelector('.kopfzeile .modus');
    if (!schalter) return;
    var englisch = (wurzel.lang || '').toLowerCase().indexOf('en') === 0;
    var wort = englisch ? 'sleet shower. nobody likes it.' : 'graupelschauer. mag ja keiner.';
    var ruhig = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    var uebersicht = /(^|\/)(index\.html|archiv\.html|archive\.html)?$/.test(location.pathname);
    var warten = uebersicht ? WARTEN_KURZ : WARTEN_LANG;

    var letzteRegung = Date.now();
    var decke = null, seit = 0, frist = 0;
    var mausX = null, mausY = null;
    var klicks = [];

    function regung() {
      letzteRegung = Date.now();
      if (decke && letzteRegung - seit >= frist) ende();
    }
    function maus(e) {
      if (mausX === null) {                       // erste bekannte Position: merken, aber nicht als Regung werten, wenn es gerade graupelt
        mausX = e.clientX; mausY = e.clientY;
        if (!decke) regung();
        return;
      }
      if (Math.abs(e.clientX - mausX) + Math.abs(e.clientY - mausY) < 4) return;   // Zittern und Scheinbewegungen
      mausX = e.clientX; mausY = e.clientY;
      regung();
    }
    window.addEventListener('mousemove', maus, { passive: true, capture: true });
    ['mousedown', 'wheel', 'keydown', 'touchstart', 'scroll'].forEach(function (name) {
      window.addEventListener(name, regung, { passive: true, capture: true });
    });
    document.addEventListener('visibilitychange', function () { letzteRegung = Date.now(); });

    // Aus der Ruhe: nur ohne die Systemeinstellung „weniger Bewegung“
    if (!ruhig) {
      setInterval(function () {
        if (!decke && document.visibilityState === 'visible' && Date.now() - letzteRegung >= warten) schauer(SCHONFRIST_RUHE, false);
      }, 1000);
    }

    // Zweiter Weg: dreimal kurz hintereinander umlegen
    schalter.addEventListener('click', function () {
      if (decke) return;
      var jetzt = Date.now();
      klicks.push(jetzt);
      klicks = klicks.filter(function (t) { return jetzt - t <= FENSTER; });
      if (klicks.length >= 3) { klicks = []; schauer(SCHONFRIST, true); }
    });

    function schauer(schonfrist, schnell) {
      frist = schonfrist; seit = Date.now();
      var d = document.createElement('div');
      d.className = schnell ? 'graupel schnell' : 'graupel';
      d.setAttribute('role', 'status');
      var grau = document.createElement('div');
      grau.className = 'graupel__grau';
      d.appendChild(grau);
      var schild = document.createElement('span');
      schild.className = 'graupel__wort';
      schild.textContent = wort;
      d.appendChild(schild);
      document.body.appendChild(d);
      decke = d;
      // Knopf und Beschriftung wandern erst, wenn es grau wird
      setTimeout(function () { if (decke === d) wurzel.setAttribute('data-wetter', 'grau'); }, schnell ? 0 : GRAU_AB);
      // zwei Bilder abwarten, damit das Einblenden als Übergang läuft
      requestAnimationFrame(function () { requestAnimationFrame(function () { d.classList.add('an'); }); });
    }

    function ende() {
      var d = decke;
      decke = null;
      wurzel.removeAttribute('data-wetter');
      d.classList.add('ab');
      setTimeout(function () { if (d.parentNode) d.parentNode.removeChild(d); }, AUSBLENDEN + 100);
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
