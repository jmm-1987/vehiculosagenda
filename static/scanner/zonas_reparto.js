/* Buscador de zonas de reparto. Los datos están en zonas_datos.js. */
(function () {
  const RAW = window.ZONAS_RAW || [];
  const norm = (s) => s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
  const MINOR = new Set(["de", "del", "la", "las", "los", "el", "y"]);
  const zoneName = (z) => z.trim().toLowerCase().split(/\s+/).map((w, i) => (
    i > 0 && MINOR.has(w) ? w : w.charAt(0).toUpperCase() + w.slice(1)
  )).join(" ");
  const D = RAW.map(([n, c, z, p]) => ({ n, c, z: zoneName(z), p, k: norm(n) }));
  const PROV = { BA: "Badajoz", CC: "Cáceres" };
  const esc = (s) => String(s).replace(/[&<>"]/g, (ch) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"
  }[ch]));

  function hl(name, qq) {
    if (!qq) return esc(name);
    const i = norm(name).indexOf(qq);
    if (i < 0) return esc(name);
    return esc(name.slice(0, i)) + "<mark>" + esc(name.slice(i, i + qq.length)) + "</mark>" + esc(name.slice(i + qq.length));
  }

  window.iniciarZonasReparto = function (root) {
    if (!root || root.dataset.listo === "1") {
      const ya = root && root.querySelector("#zr-q");
      if (ya) ya.focus();
      return;
    }
    root.dataset.listo = "1";

    const q = root.querySelector("#zr-q");
    const ans = root.querySelector("#zr-answer");
    const res = root.querySelector("#zr-results");
    const rlist = root.querySelector("#zr-rlist");
    const rtitle = root.querySelector("#zr-rtitle");
    const clr = root.querySelector("#zr-clear");
    const zonesec = root.querySelector("#zr-zonesec");
    const zones = root.querySelector("#zr-zones");
    const foot = root.querySelector("#zr-foot");
    const btnPob = root.querySelector("#zr-m-pob");
    const btnCp = root.querySelector("#zr-m-cp");
    let mode = "pob";

    function row(r, qq) {
      const cp = mode === "cp" && qq
        ? "<mark>" + r.c.slice(0, qq.length) + "</mark>" + r.c.slice(qq.length)
        : r.c;
      return `<li><span class="name">${mode === "pob" ? hl(r.n, qq) : esc(r.n)}</span><span class="z">${esc(r.z)}</span><span class="meta">CP ${cp} · ${PROV[r.p] || r.p}</span></li>`;
    }

    function showAnswer(zonesSet, label, sub) {
      const zs = [...zonesSet];
      ans.innerHTML = `<small>${esc(label)}</small><div class="zone">${zs.map(esc).join(" / ")}</div>${sub ? `<p>${sub}</p>` : ""}`;
      ans.hidden = false;
    }

    function render() {
      const raw = q.value;
      clr.hidden = !raw;
      ans.hidden = true;
      if (!raw.trim()) {
        res.hidden = true;
        zonesec.hidden = false;
        return;
      }
      zonesec.hidden = true;
      let hits;
      let qq;
      if (mode === "cp") {
        qq = raw.replace(/\D/g, "").slice(0, 5);
        hits = qq ? D.filter((r) => r.c.startsWith(qq)) : [];
        hits.sort((a, b) => a.c.localeCompare(b.c) || a.n.localeCompare(b.n, "es"));
        if (qq.length === 5 && hits.length) {
          const zs = new Set(hits.map((r) => r.z));
          showAnswer(
            zs,
            `Zona de reparto · CP ${qq}`,
            zs.size > 1
              ? "Este código postal cubre varias zonas: revisa la población en la lista."
              : `${hits.length} ${hits.length === 1 ? "localidad" : "localidades"} con este código postal.`
          );
        }
      } else {
        qq = norm(raw);
        hits = D.filter((r) => r.k.includes(qq));
        hits.sort((a, b) => (b.k.startsWith(qq) - a.k.startsWith(qq)) || a.n.localeCompare(b.n, "es"));
        const exact = hits.filter((r) => r.k === qq);
        const pick = exact.length ? exact : (hits.length === 1 ? hits : null);
        if (pick) {
          showAnswer(
            new Set(pick.map((r) => r.z)),
            `Zona de reparto · ${pick[0].n}`,
            `CP ${[...new Set(pick.map((r) => r.c))].join(", ")} · ${PROV[pick[0].p] || pick[0].p}`
          );
        }
      }
      res.hidden = false;
      if (!hits.length) {
        rtitle.textContent = "Sin resultados";
        rlist.innerHTML = `<li class="empty">${mode === "cp"
          ? `No hay ninguna localidad con un código postal que empiece por «${esc(qq)}».`
          : `No hay ninguna población que contenga «${esc(raw.trim())}».`}</li>`;
        return;
      }
      rtitle.textContent = hits.length === 1 ? "1 resultado" : `${hits.length} resultados`;
      rlist.innerHTML = hits.slice(0, 80).map((r) => row(r, qq)).join("")
        + (hits.length > 80 ? `<li class="meta">Mostrando 80 de ${hits.length}. Escribe más para afinar.</li>` : "");
    }

    function setMode(m) {
      mode = m;
      btnPob.setAttribute("aria-pressed", m === "pob" ? "true" : "false");
      btnCp.setAttribute("aria-pressed", m === "cp" ? "true" : "false");
      q.inputMode = m === "cp" ? "numeric" : "text";
      q.placeholder = m === "cp" ? "Escribe el código postal…" : "Escribe la población…";
      q.value = "";
      render();
      q.focus();
    }

    btnPob.onclick = () => setMode("pob");
    btnCp.onclick = () => setMode("cp");
    q.addEventListener("input", () => {
      if (/^\d/.test(q.value) && mode === "pob") {
        const v = q.value;
        setMode("cp");
        q.value = v;
      }
      render();
    });
    clr.onclick = () => {
      q.value = "";
      render();
      q.focus();
    };

    const byZone = {};
    D.forEach((r) => { (byZone[r.z] = byZone[r.z] || []).push(r); });
    const zn = Object.keys(byZone).sort((a, b) => a.localeCompare(b, "es"));
    zones.innerHTML = zn.map((z) => `<button type="button" data-z="${esc(z)}">${esc(z)}<span>${byZone[z].length}</span></button>`).join("");
    zones.onclick = (e) => {
      const b = e.target.closest("button");
      if (!b) return;
      const z = b.dataset.z;
      const list = byZone[z].slice().sort((a, b) => a.n.localeCompare(b.n, "es"));
      zonesec.hidden = true;
      res.hidden = false;
      clr.hidden = false;
      showAnswer(new Set([z]), "Zona de reparto", `${list.length} localidades en esta zona.`);
      rtitle.textContent = `Localidades de ${z}`;
      rlist.innerHTML = list.map((r) => row(r, "")).join("");
      root.scrollTop = 0;
    };
    foot.textContent = `${D.length} localidades · ${zn.length} zonas · Badajoz y Cáceres`;
    render();
    q.focus();
  };
})();
