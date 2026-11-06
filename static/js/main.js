(function () {
  /* ---------- Dark mode ---------- */
  const root = document.documentElement;
  const toggle = document.getElementById("themeToggle");
  function paint() {
    if (!toggle) return;
    const dark = root.getAttribute("data-bs-theme") === "dark";
    toggle.innerHTML = dark ? '<i class="bi bi-sun"></i>' : '<i class="bi bi-moon-stars"></i>';
  }
  if (toggle) {
    paint();
    toggle.addEventListener("click", () => {
      const next = root.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-bs-theme", next);
      localStorage.setItem("theme", next);
      paint();
    });
  }

  /* ---------- Hide loading overlay when returning with the Back button ---------- */
  window.addEventListener("pageshow", () => {
    const o = document.getElementById("overlay");
    if (o) o.classList.add("d-none");
  });

  /* ---------- Upload ---------- */
  const form = document.getElementById("uploadForm");
  if (!form) return;

  const main = document.getElementById("image");
  const camera = document.getElementById("cameraInput");
  const gallery = document.getElementById("galleryInput");
  const drop = document.getElementById("dropzone");
  const previewWrap = document.getElementById("previewWrap");
  const preview = document.getElementById("preview");
  const submitBtn = document.getElementById("submitBtn");
  const clearBtn = document.getElementById("clearBtn");
  const msg = document.getElementById("uploadMsg");
  const overlay = document.getElementById("overlay");
  const MAX_DIM = 1280;

  function showMsg(text) { msg.textContent = text; msg.classList.toggle("d-none", !text); }

  // Shrink and convert to JPEG in the browser: faster uploads on mobile data
  function shrink(file) {
    return new Promise(resolve => {
      const url = URL.createObjectURL(file);
      const img = new Image();
      img.onload = () => {
        const scale = Math.min(1, MAX_DIM / Math.max(img.width, img.height));
        const w = Math.round(img.width * scale), h = Math.round(img.height * scale);
        const c = document.createElement("canvas");
        c.width = w; c.height = h;
        c.getContext("2d").drawImage(img, 0, 0, w, h);
        c.toBlob(b => {
          URL.revokeObjectURL(url);
          resolve(b ? new File([b], "photo.jpg", { type: "image/jpeg" }) : file);
        }, "image/jpeg", 0.88);
      };
      img.onerror = () => { URL.revokeObjectURL(url); resolve(file); };
      img.src = url;
    });
  }

  async function handle(file) {
    showMsg("");
    if (!file) return;
    if (!file.type.startsWith("image/")) { showMsg("Please choose an image file (JPG or PNG)."); return; }
    const ready = await shrink(file);
    if (ready.size > 5 * 1024 * 1024) { showMsg("Image is too large. Please choose a smaller one."); return; }
    const dt = new DataTransfer();
    dt.items.add(ready);
    main.files = dt.files;
    preview.src = URL.createObjectURL(ready);
    previewWrap.classList.remove("d-none");
    drop.classList.add("d-none");
    submitBtn.disabled = false;
  }

  function reset() {
    main.value = ""; camera.value = ""; gallery.value = "";
    previewWrap.classList.add("d-none");
    drop.classList.remove("d-none");
    submitBtn.disabled = true;
    showMsg("");
  }

  camera.addEventListener("change", e => handle(e.target.files[0]));
  gallery.addEventListener("change", e => handle(e.target.files[0]));
  document.getElementById("cameraBtn").addEventListener("click", () => camera.click());
  document.getElementById("galleryBtn").addEventListener("click", () => gallery.click());
  clearBtn.addEventListener("click", reset);

  drop.addEventListener("click", () => gallery.click());
  drop.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); gallery.click(); } });
  ["dragenter", "dragover"].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.add("drag"); }));
  ["dragleave", "drop"].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.remove("drag"); }));
  drop.addEventListener("drop", e => handle(e.dataTransfer.files[0]));

  form.addEventListener("submit", e => {
    if (!main.files.length) { e.preventDefault(); showMsg("Please choose or take a photo first."); return; }
    overlay.classList.remove("d-none");
    submitBtn.disabled = true;
  });
})();