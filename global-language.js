/* Global language access for visitors worldwide.
   Google Translate is user-initiated; no visitor content is sent for translation until they choose a language. */
(() => {
  "use strict";
  const select = document.getElementById("globalLanguage");
  const button = document.getElementById("translateWebsite");
  if (!select || !button) return;
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
