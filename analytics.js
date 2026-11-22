/* Wearhue traffic tracking (shared by every page).
   1. Create a free Google Analytics 4 property for https://sheihab.github.io/wearhue/
   2. Paste its Measurement ID (looks like G-XXXXXXXXXX) below. Leave blank = no tracking. */
(function () {
  var GA_ID = "";
  if (!GA_ID) return;
  var s = document.createElement("script");
  s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { dataLayer.push(arguments); };
  gtag("js", new Date());
  gtag("config", GA_ID, { anonymize_ip: true });
})();
