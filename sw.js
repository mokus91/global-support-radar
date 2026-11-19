"use strict";
const CACHE_NAME = "global-support-radar-shell-v1";
const SHELL = ["./", "./manifest.webmanifest", "./icon.svg"];

self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(key => key.startsWith("global-support-radar-shell-") && key !== CACHE_NAME).map(key => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  // Never cache opportunity feeds or other JSON: offline data must not look current.
  if (url.pathname.endsWith(".json") || url.pathname.includes("/data/")) return;

  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request).then(response => {
        if (response.ok) {
          const copy = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put("./", copy));
        }
        return response;
      }).catch(async () => (await caches.match("./")) || Response.error())
    );
    return;
  }

  if (url.pathname.endsWith("manifest.webmanifest") || url.pathname.endsWith("icon.svg")) {
    event.respondWith(caches.match(request).then(cached => cached || fetch(request)));
  }
});
