/* Global Support Radar — privacy-friendly aggregate analytics.
 * No cookies, no local fingerprinting, no IP/geolocation collection by this code.
 * The third-party counter loads only after an owner supplies a GoatCounter site code.
 */
(() => {
  "use strict";
  const cfg = window.GSR_ANALYTICS || {};
  if (cfg.provider !== "goatcounter" || !/^[a-z0-9-]{3,40}$/i.test(cfg.siteCode || "")) {
    window.GSR_ANALYTICS_STATUS = "inactive-needs-free-provider-site-code";
    return;
  }
  if (window.__gsrAnalyticsLoaded) return;
  window.__gsrAnalyticsLoaded = true;
  const script = document.createElement("script");
  script.async = true;
  script.dataset.goatcounter = "https://" + cfg.siteCode + ".goatcounter.com/count";
  script.src = "https://gc.zgo.at/count.js";
  script.onerror = () => { window.GSR_ANALYTICS_STATUS = "provider-load-error"; };
  script.onload = () => { window.GSR_ANALYTICS_STATUS = "active"; };
  document.head.appendChild(script);
})();
