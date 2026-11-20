/* Global language access for visitors worldwide.
   Google Translate is user-initiated; no visitor content is sent for translation until they choose a language. */
(() => {
  "use strict";
  let select = document.getElementById("globalLanguage");
  let button = document.getElementById("translateWebsite");
  if (!select || !button) {
    const panel = document.createElement("div");
    panel.id = "global-language-widget";
    panel.setAttribute("aria-label", "Website language");
    panel.style.cssText = "position:fixed;right:12px;bottom:12px;z-index:99999;display:flex;gap:6px;align-items:center;max-width:calc(100vw - 24px);padding:8px;background:#101d31;color:#fff;border:1px solid #53e0b2;border-radius:12px;box-shadow:0 4px 18px #0008;font:14px system-ui";
    select = document.createElement("select");
    select.id = "globalLanguage";
    select.setAttribute("aria-label", "Choose language");
    select.style.cssText = "max-width:170px;min-width:0;padding:8px;background:#17263d;color:#fff;border:1px solid #52627a;border-radius:8px;font:inherit";
    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "🌐 Language";
    select.appendChild(placeholder);
    button = document.createElement("button");
    button.id = "translateWebsite";
    button.type = "button";
    button.textContent = "Translate ↗";
    button.style.cssText = "padding:9px 11px;background:#53e0b2;color:#071925;border:0;border-radius:8px;font-weight:700;cursor:pointer";
    panel.append(select, button);
    document.body.appendChild(panel);
  }
  const extraLanguages = ("af sq am hy az eu be bs ceb ny co fy gl ka gu ht ha haw is ig ga jv kn kk km rw ku ky lo la lb mk mg mi mr mn my ne or pa sm gd st sn sd si so su tg tt te tk ug uz cy xh yi yo zu").split(" ");
  extraLanguages.forEach(code => {
    if (Array.from(select.options).some(option => option.value === code)) return;
    let nativeName = code;
    try { nativeName = new Intl.DisplayNames([code], { type: "language" }).of(code) || code; } catch (_) {}
    const option = document.createElement("option");
    option.value = code;
    option.textContent = nativeName;
    select.appendChild(option);
  });
  // Suggest the visitor's likely country from their browser locale; they can always change it.
  const countrySelect = document.getElementById("country");
  const hasCountryInLink = new URLSearchParams(window.location.search).has("country");
  if (countrySelect && !hasCountryInLink) {
    try {
      const region = new Intl.Locale(navigator.language || "en").region;
      if (region && Array.from(countrySelect.options).some(option => option.value === region)) {
        countrySelect.value = region;
        countrySelect.dispatchEvent(new Event("change", { bubbles: true }));
      }
    } catch (_) {}
  }
  const supported = new Set(Array.from(select.options).map(option => option.value).filter(Boolean));
  const browserLanguage = (navigator.languages && navigator.languages[0] || navigator.language || "en").toLowerCase();
  const preferred = browserLanguage.startsWith("zh-tw") || browserLanguage.startsWith("zh-hk") ? "zh-TW" : browserLanguage.split("-")[0];
  if (supported.has(preferred) && preferred !== "hu" && preferred !== "en") select.value = preferred;
  const labels = {
    hu: { placeholder: "🌐 További nyelvek", button: "Fordítás ↗", note: "A fordítás a Google Fordító szolgáltatásán keresztül, külső oldalon történik." },
    en: { placeholder: "🌐 More languages", button: "Translate ↗", note: "Translation is provided on an external page by Google Translate." }
  };
  const current = () => (document.documentElement.lang || "en").startsWith("hu") ? "hu" : "en";
  function localize() {
    const copy = labels[current()];
    select.options[0].textContent = copy.placeholder;
    button.textContent = copy.button;
    button.title = copy.note;
  }
  function translate() {
    const target = select.value;
    if (!target) { select.focus(); return; }
    const destination = new URL("https://translate.google.com/translate");
    destination.searchParams.set("sl", "auto");
    destination.searchParams.set("tl", target);
    destination.searchParams.set("u", window.location.href);
    window.location.assign(destination.toString());
  }
  button.addEventListener("click", translate);
  select.addEventListener("keydown", event => { if (event.key === "Enter") translate(); });
  document.getElementById("lang")?.addEventListener("change", localize);
  localize();
})();
