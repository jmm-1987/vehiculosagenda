# -*- coding: utf-8 -*-
"""Genera templates/rectificaciones.html desde el HTML de muestra."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
src = ROOT / "Rectificaciones .html"
text = src.read_text(encoding="utf-8")

i = text.find("<style>")
j = text.find("</style>") + len("</style>")
css = text[i:j]

# Extra CSS for top-bar integration
extra_css = """
<style>
  .app-top-bar{
    display:flex; justify-content:space-between; align-items:center;
    padding:2px 30px; background:linear-gradient(to right,#ffffff,#343a40);
    color:white; height:50px; box-sizing:border-box;
  }
  .app-top-bar img{ width:200px; height:45px; object-fit:contain; }
  .app-top-user{ font-weight:bold; font-size:14px; margin-left:auto; margin-right:20px; }
  .app-top-button{
    padding:2px 8px; background-color:#c51500; color:white; text-decoration:none;
    border-radius:3px; font-size:12px; margin-left:8px;
  }
  .app-top-button:hover{ opacity:.9; color:#fff; }
</style>
"""

h = text.find("<header")
toast_start = text.find('<div id="toast"')
toast_end = text.find("</div>", toast_start) + len("</div>")
body_html = text[h:toast_end]
body_html = re.sub(
    r'<img class="brand-logo" src="data:image/png;base64,[^"]+" alt="Alditraex">',
    '<img class="brand-logo" src="{{ url_for(\'static\', filename=\'logo.png\') }}" alt="Alditraex">',
    body_html,
    count=1,
)

js = r'''
<script>
(function(){
  const $ = (id) => document.getElementById(id);
  const fecha=$('fecha'), expedicion=$('expedicion'), agencia=$('agencia'), pesoDoc=$('pesoDoc'), pesoReal=$('pesoReal'),
        volDoc=$('volDoc'), volReal=$('volReal'),
        diffPesoOut=$('diffPeso'), diffVolOut=$('diffVol'), pvkgDocOut=$('pvkgDoc'), pvkgRealOut=$('pvkgReal'),
        form=$('rectForm'), saveBtn=$('saveBtn'),
        logBody=$('logBody'), countBadge=$('countBadge'), syncText=$('syncText'), syncDot=$('syncStatus'),
        exportBtn=$('exportBtn'), exportPanel=$('exportPanel'), exportFrom=$('exportFrom'), exportTo=$('exportTo'),
        exportCancel=$('exportCancel'), exportConfirm=$('exportConfirm'), toast=$('toast'),
        toggleFormBtn=$('toggleFormBtn'), formCardBody=$('formCardBody'),
        dateFilterBtn=$('dateFilterBtn'), dateFilterPanel=$('dateFilterPanel'),
        filterFrom=$('filterFrom'), filterTo=$('filterTo'),
        filterDateClear=$('filterDateClear'), filterDateApply=$('filterDateApply'),
        filterAgencia=$('filterAgencia'), filterEstado=$('filterEstado');

  let allRows = [];
  let activeFrom = '', activeTo = '';
  const ESTADOS = ['Pendiente', 'Aceptada', 'Rechazada'];
  const todayStr = new Date().toISOString().slice(0,10);
  fecha.value = todayStr;
  exportTo.value = todayStr;
  exportFrom.value = todayStr.slice(0,8) + '01';

  function hasActiveFilters(){
    return !!(activeFrom || activeTo || filterAgencia.value || filterEstado.value);
  }
  function passesFilters(r){
    if (activeFrom && (!r.fecha || r.fecha < activeFrom)) return false;
    if (activeTo && (!r.fecha || r.fecha > activeTo)) return false;
    if (filterAgencia.value && r.agencia !== filterAgencia.value) return false;
    if (filterEstado.value && (r.estado || 'Pendiente') !== filterEstado.value) return false;
    return true;
  }
  function applyAndRender(){
    const filtered = allRows.filter(passesFilters);
    countBadge.textContent = filtered.length + (filtered.length === 1 ? ' registro' : ' registros')
      + (hasActiveFilters() ? ' (filtrado)' : '');
    renderRows(filtered, hasActiveFilters());
  }

  dateFilterBtn.addEventListener('click', () => { dateFilterPanel.hidden = !dateFilterPanel.hidden; });
  document.addEventListener('click', (e) => {
    if (!dateFilterPanel.hidden && !dateFilterPanel.contains(e.target) && e.target !== dateFilterBtn){
      dateFilterPanel.hidden = true;
    }
  });
  filterDateApply.addEventListener('click', () => {
    activeFrom = filterFrom.value || '';
    activeTo = filterTo.value || '';
    dateFilterBtn.classList.toggle('active', !!(activeFrom || activeTo));
    dateFilterPanel.hidden = true;
    applyAndRender();
  });
  filterDateClear.addEventListener('click', () => {
    filterFrom.value = ''; filterTo.value = ''; activeFrom = ''; activeTo = '';
    dateFilterBtn.classList.remove('active');
    dateFilterPanel.hidden = true;
    applyAndRender();
  });
  filterAgencia.addEventListener('change', applyAndRender);
  filterEstado.addEventListener('change', applyAndRender);

  toggleFormBtn.addEventListener('click', () => {
    const expanded = !formCardBody.hidden;
    formCardBody.hidden = expanded;
    toggleFormBtn.setAttribute('aria-expanded', String(!expanded));
    toggleFormBtn.textContent = expanded ? '+ Nueva rectificación' : '− Ocultar formulario';
    if (!expanded) fecha.focus();
  });

  function fmtNum(n, decimals){
    if (n === null || n === undefined || typeof n !== 'number' || Number.isNaN(n)) return '—';
    return n.toLocaleString('es-ES', {minimumFractionDigits: decimals, maximumFractionDigits: decimals});
  }
  function fmtDate(iso){
    if(!iso || typeof iso !== 'string') return '—';
    const parts = iso.split('-');
    if (parts.length !== 3) return iso;
    return `${parts[2]}/${parts[1]}/${parts[0]}`;
  }
  function diffClass(v){
    if (v === null || v === undefined || Number.isNaN(v)) return '';
    if (v > 0) return 'diff-pos';
    if (v < 0) return 'diff-neg';
    return 'diff-zero';
  }
  function escapeHtml(s){
    return String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }
  function updateDiffs(){
    const pd = parseFloat(pesoDoc.value), pr = parseFloat(pesoReal.value);
    const vd = parseFloat(volDoc.value), vr = parseFloat(volReal.value);
    if (!Number.isNaN(pd) && !Number.isNaN(pr)){
      const d = pd - pr;
      diffPesoOut.textContent = (d>0?'+':'') + fmtNum(d,2) + ' kg';
      diffPesoOut.className = 'diff-output ' + diffClass(d);
    } else { diffPesoOut.textContent = '—'; diffPesoOut.className = 'diff-output'; }
    if (!Number.isNaN(vd) && !Number.isNaN(vr)){
      const d = vd - vr;
      diffVolOut.textContent = (d>0?'+':'') + fmtNum(d,3) + ' m³';
      diffVolOut.className = 'diff-output ' + diffClass(d);
    } else { diffVolOut.textContent = '—'; diffVolOut.className = 'diff-output'; }
  }
  [pesoDoc, pesoReal, volDoc, volReal].forEach(el => el.addEventListener('input', updateDiffs));
  updateDiffs();

  function pvkgFactor(){ return agencia.value === 'NTL' ? 200 : 250; }
  function updatePvkg(){
    const vd = parseFloat(volDoc.value), vr = parseFloat(volReal.value);
    const factor = pvkgFactor();
    pvkgDocOut.textContent = Number.isNaN(vd) ? '—' : fmtNum(vd*factor,2) + ' kg';
    pvkgRealOut.textContent = Number.isNaN(vr) ? '—' : fmtNum(vr*factor,2) + ' kg';
  }
  [volDoc, volReal].forEach(el => el.addEventListener('input', updatePvkg));
  agencia.addEventListener('change', updatePvkg);
  updatePvkg();

  let toastTimer = null;
  function showToast(msg, isError){
    toast.textContent = msg;
    toast.className = 'toast show' + (isError ? ' toast-error' : '');
    toast.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { toast.hidden = true; }, 3800);
  }

  function estadoOptionsHtml(current){
    return ESTADOS.map(e => `<option value="${e}" ${e===current?'selected':''}>${e}</option>`).join('');
  }

  function renderRows(rows, filtered){
    if (!rows || rows.length === 0){
      const msg = filtered ? 'Ningún registro coincide con los filtros aplicados.' : 'Aún no hay rectificaciones registradas.';
      logBody.innerHTML = `<tr><td colspan="13" class="empty-row">${msg}</td></tr>`;
      return;
    }
    const frag = document.createDocumentFragment();
    rows.forEach(r => {
      const dPeso = (typeof r.pesoReal === 'number' && typeof r.pesoDocumentado === 'number') ? r.pesoDocumentado - r.pesoReal : (typeof r.diferenciaPeso === 'number' ? r.diferenciaPeso : null);
      const dVol = (typeof r.volReal === 'number' && typeof r.volDocumentado === 'number') ? r.volDocumentado - r.volReal : (typeof r.diferenciaVol === 'number' ? r.diferenciaVol : null);
      const factor = r.agencia === 'NTL' ? 200 : 250;
      const pvkgDoc = typeof r.pvkgDocumentado === 'number' ? r.pvkgDocumentado : (typeof r.volDocumentado === 'number' ? r.volDocumentado*factor : null);
      const pvkgReal = typeof r.pvkgReal === 'number' ? r.pvkgReal : (typeof r.volReal === 'number' ? r.volReal*factor : null);
      const estado = r.estado || 'Pendiente';
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${fmtDate(r.fecha)}</td>
        <td>${escapeHtml(r.expedicion || '—')}</td>
        <td>${escapeHtml(r.agencia || '—')}</td>
        <td>${fmtNum(r.pesoDocumentado, 2)}</td>
        <td>${fmtNum(r.pesoReal, 2)}</td>
        <td class="${diffClass(dPeso)}">${dPeso===null?'—':((dPeso>0?'+':'')+fmtNum(dPeso,2))}</td>
        <td>${fmtNum(r.volDocumentado, 3)}</td>
        <td>${fmtNum(r.volReal, 3)}</td>
        <td class="${diffClass(dVol)}">${dVol===null?'—':((dVol>0?'+':'')+fmtNum(dVol,3))}</td>
        <td>${fmtNum(pvkgDoc, 2)}</td>
        <td>${fmtNum(pvkgReal, 2)}</td>
        <td><select class="estado-select estado-${estado.toLowerCase()}" data-id="${r.id}">${estadoOptionsHtml(estado)}</select></td>
        <td><button type="button" class="btn-delete" data-id="${r.id}">Eliminar</button></td>`;
      frag.appendChild(tr);
    });
    logBody.innerHTML = '';
    logBody.appendChild(frag);
  }

  logBody.addEventListener('change', async (e) => {
    const sel = e.target.closest('.estado-select');
    if (!sel) return;
    const id = sel.dataset.id;
    const nuevoEstado = sel.value;
    try {
      const res = await fetch(`/api/rectificaciones/${id}/estado`, {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ estado: nuevoEstado })
      });
      const data = await res.json();
      if (!data.ok) throw new Error();
      const row = allRows.find(r => String(r.id) === String(id));
      if (row) row.estado = nuevoEstado;
      sel.className = `estado-select estado-${nuevoEstado.toLowerCase()}`;
      showToast('Estado actualizado.');
    } catch (err) {
      showToast('No se pudo actualizar el estado.', true);
      await cargar();
    }
  });

  logBody.addEventListener('click', async (e) => {
    const btn = e.target.closest('.btn-delete');
    if (!btn) return;
    if (!confirm('¿Eliminar esta rectificación?')) return;
    const id = btn.dataset.id;
    try {
      const res = await fetch(`/api/rectificaciones/${id}`, { method: 'DELETE' });
      const data = await res.json();
      if (!data.ok) throw new Error();
      allRows = allRows.filter(r => String(r.id) !== String(id));
      applyAndRender();
      showToast('Rectificación eliminada.');
    } catch (err) {
      showToast('No se pudo eliminar.', true);
    }
  });

  async function cargar(){
    syncText.textContent = 'Cargando…';
    syncDot.className = 'status-dot';
    try {
      const res = await fetch('/api/rectificaciones');
      const data = await res.json();
      if (!data.ok) throw new Error();
      allRows = data.items || [];
      applyAndRender();
      syncText.textContent = 'Conectado — datos en servidor';
      syncDot.className = 'status-dot status-dot-ok';
    } catch (err) {
      syncText.textContent = 'Error al cargar';
      syncDot.className = 'status-dot status-dot-error';
      showToast('No se pudieron cargar las rectificaciones.', true);
    }
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    saveBtn.disabled = true;
    saveBtn.textContent = 'Guardando…';
    try {
      const res = await fetch('/api/rectificaciones', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({
          fecha: fecha.value || null,
          expedicion: expedicion.value.trim() || '',
          agencia: agencia.value || '',
          pesoDocumentado: pesoDoc.value,
          pesoReal: pesoReal.value,
          volDocumentado: volDoc.value,
          volReal: volReal.value,
          estado: 'Pendiente'
        })
      });
      const data = await res.json();
      if (!data.ok) throw new Error();
      showToast('Rectificación guardada correctamente.');
      const keepFecha = fecha.value, keepAgencia = agencia.value;
      form.reset();
      fecha.value = keepFecha;
      agencia.value = keepAgencia;
      updateDiffs(); updatePvkg();
      await cargar();
    } catch (err) {
      showToast('No se pudo guardar. Inténtalo de nuevo.', true);
    } finally {
      saveBtn.disabled = false;
      saveBtn.textContent = 'Guardar rectificación';
    }
  });

  exportBtn.addEventListener('click', () => { exportPanel.hidden = !exportPanel.hidden; });
  exportCancel.addEventListener('click', () => { exportPanel.hidden = true; });
  document.addEventListener('click', (e) => {
    if (!exportPanel.hidden && !exportPanel.contains(e.target) && e.target !== exportBtn){
      exportPanel.hidden = true;
    }
  });

  exportConfirm.addEventListener('click', () => {
    const params = new URLSearchParams();
    if (exportFrom.value) params.set('desde', exportFrom.value);
    if (exportTo.value) params.set('hasta', exportTo.value);
    window.location.href = '/api/rectificaciones/exportar?' + params.toString();
    exportPanel.hidden = true;
    showToast('Descarga iniciada.');
  });

  cargar();
})();
</script>
'''

out = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Rectificaciones Peso-Volumen — Alditraex</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Fraunces:ital,wght@1,400;1,500&display=swap">
""" + css + "\n" + extra_css + """
</head>
<body>
<div class="app-top-bar">
  <a href="{{ url_for('portada') }}"><img src="{{ url_for('static', filename='logo.png') }}" alt="Logo"></a>
  <span class="app-top-user">{{ current_user.username }}</span>
  <a href="{{ url_for('portada') }}" class="app-top-button" style="background-color:#343a40;">Portada</a>
  <a href="{{ url_for('logout') }}" class="app-top-button">Cerrar sesión</a>
</div>
""" + body_html + "\n" + js + """
</body>
</html>
"""

dest = ROOT / "templates" / "rectificaciones.html"
dest.write_text(out, encoding="utf-8")
print(f"OK {dest} ({dest.stat().st_size} bytes)")
