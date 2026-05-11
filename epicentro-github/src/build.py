#!/usr/bin/env python3
"""
build.py — Lee data/noticias.json y genera public/index.html
Este script es ejecutado por el GitHub Action después del escaneo.
"""
import json
from pathlib import Path
from datetime import datetime

data_path = Path("data/noticias.json")
scan_path = Path("data/ultimo_escaneo.txt")
out_dir   = Path("public")
out_dir.mkdir(exist_ok=True)

with open(data_path, encoding="utf-8") as f:
    noticias = json.load(f)

escaneo = scan_path.read_text().strip() if scan_path.exists() else ""
try:
    dt = datetime.fromisoformat(escaneo.replace("Z","+00:00"))
    escaneo_fmt = dt.strftime("%d/%m/%Y %H:%M UTC")
except:
    escaneo_fmt = datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC")

noticias_js = json.dumps(noticias, ensure_ascii=False)
total = len(noticias)
medios_cnt = len(set(n["medio"] for n in noticias))
zonas_cnt  = len(set(n["zona"]  for n in noticias))

HTML = f"""<!DOCTYPE html>
<html lang="es" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Epicentro Radio — Monitor Red Completa</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300..700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{-webkit-font-smoothing:antialiased;scroll-behavior:smooth}}
:root,[data-theme="light"]{{
--bg:#f7f6f2;--s1:#f9f8f5;--s2:#fff;--soff:#edeae5;
--bd:rgba(0,0,0,0.09);--tx:#28251d;--mu:#7a7974;--fa:#b5b2ad;
--pr:#c0392b;--ph:#a93226;--pb:rgba(192,57,43,0.1);
--ac:#e67e22;--gn:#27ae60;--gnb:rgba(39,174,96,0.1);
--bl:#2471a3;--blb:rgba(36,113,163,0.1);
--ss:0 1px 3px rgba(0,0,0,0.07);--sm:0 4px 16px rgba(0,0,0,0.09);--sl:0 12px 40px rgba(0,0,0,0.13);
--rsm:.375rem;--rmd:.5rem;--rlg:.75rem;--rxl:1rem;--rfl:9999px;
--xs:clamp(.75rem,.7rem + .25vw,.875rem);--sm2:clamp(.875rem,.8rem + .35vw,1rem);
--bs:clamp(1rem,.95rem + .25vw,1.125rem);--lg:clamp(1.125rem,1rem + .75vw,1.5rem);
--xl:clamp(1.5rem,1.2rem + 1.25vw,2.25rem);
--s1u:.25rem;--s2u:.5rem;--s3:.75rem;--s4:1rem;--s5:1.25rem;--s6:1.5rem;--s8:2rem;--s12:3rem;
--fn:"Inter",sans-serif;--fd:"Instrument Serif",Georgia,serif;--tr:180ms cubic-bezier(.16,1,.3,1);
}}
[data-theme="dark"]{{
--bg:#0f0f0e;--s1:#161513;--s2:#1c1b19;--soff:#1e1d1b;
--bd:rgba(255,255,255,0.07);--tx:#cccac7;--mu:#78766f;--fa:#525049;
--pr:#e74c3c;--ph:#c0392b;--pb:rgba(231,76,60,0.13);
--ac:#f39c12;--gn:#2ecc71;--gnb:rgba(46,204,113,0.12);
--bl:#5dade2;--blb:rgba(93,173,226,0.12);
--ss:0 1px 3px rgba(0,0,0,0.35);--sm:0 4px 16px rgba(0,0,0,0.45);--sl:0 12px 40px rgba(0,0,0,0.6);
}}
body{{min-height:100dvh;font-family:var(--fn);font-size:var(--bs);color:var(--tx);background:var(--bg);}}
header{{position:sticky;top:0;z-index:100;background:var(--s1);border-bottom:1px solid var(--bd);
box-shadow:var(--ss);padding:var(--s3) var(--s6);display:flex;align-items:center;justify-content:space-between;gap:var(--s4);}}
.logo{{display:flex;align-items:center;gap:var(--s3);text-decoration:none;}}
.logo svg{{width:34px;height:34px;flex-shrink:0;}}
.logo-name{{font-family:var(--fd);font-style:italic;font-size:var(--lg);color:var(--pr);line-height:1;}}
.logo-sub{{font-size:var(--xs);color:var(--mu);text-transform:uppercase;letter-spacing:.06em;margin-top:2px;}}
.hdr-r{{display:flex;align-items:center;gap:var(--s2u);}}
.tag{{font-size:var(--xs);color:var(--mu);padding:var(--s1u) var(--s3);background:var(--soff);border-radius:var(--rfl);border:1px solid var(--bd);white-space:nowrap;}}
.ibtn{{width:34px;height:34px;border-radius:var(--rmd);display:flex;align-items:center;justify-content:center;color:var(--mu);cursor:pointer;transition:background var(--tr),color var(--tr);}}
.ibtn:hover{{background:var(--soff);color:var(--tx);}}
.layout{{display:grid;grid-template-columns:260px 1fr;min-height:calc(100dvh - 56px);}}
@media(max-width:860px){{.layout{{grid-template-columns:1fr;}}.sidebar{{display:none;}}}}
.sidebar{{background:var(--s1);border-right:1px solid var(--bd);padding:var(--s5) var(--s3);position:sticky;top:56px;height:calc(100dvh - 56px);overflow-y:auto;}}
.sb-ttl{{font-size:var(--xs);font-weight:700;text-transform:uppercase;letter-spacing:.07em;color:var(--mu);margin-bottom:var(--s3);padding-bottom:var(--s2u);border-bottom:1px solid var(--bd);}}
.sb-sec{{margin-bottom:var(--s5);}}
.sb-item{{padding:var(--s2u) var(--s3);border-radius:var(--rmd);cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:var(--s2u);transition:background var(--tr);font-size:var(--sm2);}}
.sb-item:hover{{background:var(--soff);}}
.sb-item.on{{background:var(--pb);color:var(--pr);font-weight:600;}}
.sb-cnt{{font-size:var(--xs);color:var(--mu);background:var(--soff);padding:1px 7px;border-radius:var(--rfl);}}
.sb-item.on .sb-cnt{{background:var(--pb);color:var(--pr);}}
.sb-dot{{width:6px;height:6px;border-radius:50%;background:var(--pr);flex-shrink:0;}}
.content{{padding:var(--s6);}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:var(--s3);margin-bottom:var(--s8);}}
.stat{{background:var(--s1);border:1px solid var(--bd);border-radius:var(--rlg);padding:var(--s4);text-align:center;}}
.stat-n{{font-family:var(--fd);font-style:italic;font-size:var(--xl);line-height:1;}}
.stat-l{{font-size:var(--xs);color:var(--mu);text-transform:uppercase;letter-spacing:.05em;margin-top:var(--s1u);}}
.alert-panel{{background:var(--s1);border:1px solid var(--bd);border-radius:var(--rxl);padding:var(--s6);margin-bottom:var(--s8);box-shadow:var(--ss);}}
.ph{{display:flex;align-items:center;justify-content:space-between;margin-bottom:var(--s5);flex-wrap:wrap;gap:var(--s3);}}
.pt{{font-size:var(--lg);font-weight:700;display:flex;align-items:center;gap:var(--s2u);}}
.pa{{display:flex;gap:var(--s2u);flex-wrap:wrap;}}
.sl-list{{display:flex;flex-direction:column;gap:var(--s3);margin-bottom:var(--s3);min-height:50px;}}
.si{{background:var(--s2);border:1px solid var(--bd);border-radius:var(--rmd);padding:var(--s3) var(--s4);display:flex;align-items:flex-start;justify-content:space-between;gap:var(--s3);}}
.si-t{{font-size:var(--sm2);font-weight:600;line-height:1.3;}}
.si-m{{font-size:var(--xs);color:var(--mu);margin-top:3px;}}
.si-m a{{color:var(--pr);}}
.si-x{{color:var(--pr);cursor:pointer;font-size:var(--lg);line-height:1;flex-shrink:0;opacity:.6;transition:opacity var(--tr);}}
.si-x:hover{{opacity:1;}}
.ep{{text-align:center;padding:var(--s8) var(--s4);color:var(--mu);font-size:var(--sm2);}}
.ep svg{{display:block;margin:0 auto var(--s3);color:var(--fa);}}
.controls{{display:flex;gap:var(--s3);margin-bottom:var(--s5);flex-wrap:wrap;align-items:center;}}
.sw{{position:relative;flex:1;min-width:200px;}}
.sw svg{{position:absolute;left:11px;top:50%;transform:translateY(-50%);width:15px;height:15px;color:var(--mu);pointer-events:none;}}
input[type=text]{{width:100%;background:var(--s1);border:1px solid var(--bd);border-radius:var(--rmd);padding:var(--s3) var(--s4) var(--s3) 34px;font:inherit;font-size:var(--sm2);color:var(--tx);transition:border-color var(--tr),box-shadow var(--tr);}}
input:focus{{outline:none;border-color:var(--pr);box-shadow:0 0 0 3px var(--pb);}}
select{{background:var(--s1);border:1px solid var(--bd);border-radius:var(--rmd);padding:var(--s3) var(--s8) var(--s3) var(--s4);font:inherit;font-size:var(--sm2);color:var(--tx);cursor:pointer;appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='13' height='13' viewBox='0 0 24 24' fill='none' stroke='%23797876' stroke-width='2'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 10px center;transition:border-color var(--tr);}}
select:focus{{outline:none;border-color:var(--pr);}}
.sec-l{{font-size:var(--xs);color:var(--mu);text-transform:uppercase;letter-spacing:.07em;font-weight:700;margin-bottom:var(--s4);display:flex;align-items:center;gap:var(--s2u);}}
.sec-c{{background:var(--pb);color:var(--pr);padding:1px 8px;border-radius:var(--rfl);font-size:.65rem;}}
.grid{{display:grid;gap:var(--s4);grid-template-columns:repeat(auto-fill,minmax(310px,1fr));}}
.card{{background:var(--s1);border:1px solid var(--bd);border-radius:var(--rxl);padding:var(--s5);display:flex;flex-direction:column;gap:var(--s3);box-shadow:var(--ss);transition:box-shadow var(--tr),transform var(--tr);position:relative;overflow:hidden;}}
.card:hover{{box-shadow:var(--sm);transform:translateY(-1px);}}
.ct{{display:flex;align-items:flex-start;justify-content:space-between;gap:var(--s2u);}}
.cb{{display:flex;gap:var(--s1u);flex-wrap:wrap;}}
.badge{{padding:2px 7px;border-radius:var(--rsm);font-size:.67rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;white-space:nowrap;}}
.bm{{background:var(--pb);color:var(--pr);}}.bz{{background:var(--blb);color:var(--bl);}}.br{{background:var(--gnb);color:var(--gn);font-size:.6rem;}}
.ctm{{font-size:var(--xs);color:var(--fa);flex-shrink:0;}}
.ctitle{{font-weight:700;font-size:var(--sm2);color:var(--tx);line-height:1.4;}}
.cdesc{{font-size:var(--xs);color:var(--mu);line-height:1.6;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;}}
.cf{{display:flex;align-items:center;justify-content:space-between;padding-top:var(--s3);border-top:1px solid var(--bd);margin-top:auto;gap:var(--s2u);}}
.badd{{padding:var(--s2u) var(--s3);border-radius:var(--rmd);font:inherit;font-size:var(--xs);font-weight:700;cursor:pointer;border:none;background:var(--pr);color:#fff;transition:background var(--tr),transform var(--tr);white-space:nowrap;}}
.badd:hover{{background:var(--ph);}}.badd:active{{transform:scale(.97);}}
.bver{{font-size:var(--xs);color:var(--mu);text-decoration:none;display:flex;align-items:center;gap:4px;transition:color var(--tr);flex-shrink:0;}}
.bver:hover{{color:var(--tx);}}
.card.sel{{border-color:var(--pr);box-shadow:0 0 0 2px var(--pb),var(--sm);}}
.card.sel::before{{content:"✓ En alertas";position:absolute;top:0;left:0;right:0;background:var(--pr);color:#fff;text-align:center;font-size:.62rem;font-weight:700;padding:3px;letter-spacing:.05em;text-transform:uppercase;}}
.btn{{padding:var(--s3) var(--s4);border-radius:var(--rmd);font:inherit;font-size:var(--sm2);font-weight:600;cursor:pointer;border:none;transition:background var(--tr),transform var(--tr);white-space:nowrap;}}
.btn:active{{transform:scale(.98);}}
.br2{{background:var(--pr);color:#fff;}}.br2:hover{{background:var(--ph);}}
.bg2{{background:var(--gn);color:#fff;}}.bg2:hover{{opacity:.9;}}
.bb2{{background:var(--bl);color:#fff;}}.bb2:hover{{opacity:.9;}}
.bgh{{background:transparent;color:var(--mu);border:1px solid var(--bd);}}.bgh:hover{{background:var(--soff);color:var(--tx);}}
.empty{{display:flex;flex-direction:column;align-items:center;text-align:center;padding:var(--s12) var(--s8);color:var(--mu);}}
.empty svg{{margin-bottom:var(--s4);color:var(--fa);}}
.empty h3{{color:var(--tx);font-size:var(--lg);margin-bottom:var(--s2u);}}
.empty p{{max-width:36ch;font-size:var(--sm2);}}
.toasts{{position:fixed;bottom:var(--s6);right:var(--s6);z-index:999;display:flex;flex-direction:column;gap:var(--s3);pointer-events:none;}}
.toast{{background:var(--s2);border:1px solid var(--bd);border-radius:var(--rlg);padding:var(--s3) var(--s5);box-shadow:var(--sl);font-size:var(--sm2);display:flex;align-items:center;gap:var(--s3);animation:ti .3s cubic-bezier(.16,1,.3,1);}}
@keyframes ti{{from{{opacity:0;transform:translateX(14px)}}to{{opacity:1;transform:none}}}}
@media(max-width:600px){{.content{{padding:var(--s4);}}header{{padding:var(--s3) var(--s4);}}.grid{{grid-template-columns:1fr;}}.tag{{display:none;}}.pa,.controls{{flex-direction:column;align-items:stretch;}}}}
</style>
</head>
<body>
<header>
  <a class="logo" href="#" aria-label="Epicentro Radio">
    <svg viewBox="0 0 34 34" fill="none"><circle cx="17" cy="17" r="16" stroke="var(--pr)" stroke-width="1.5"/><circle cx="17" cy="17" r="10" stroke="var(--pr)" stroke-width="1" opacity=".4"/><circle cx="17" cy="17" r="4.5" fill="var(--pr)"/><path d="M4.5 17 Q10 10 17 17 Q24 24 29.5 17" stroke="var(--pr)" stroke-width="1.5" fill="none" opacity=".35"/></svg>
    <div><div class="logo-name">Epicentro Radio</div><div class="logo-sub">Monitor Red Completa</div></div>
  </a>
  <div class="hdr-r">
    <span class="tag">🔄 {escaneo_fmt}</span>
    <button class="ibtn" data-theme-toggle aria-label="Cambiar modo"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg></button>
  </div>
</header>
<div class="layout">
  <aside class="sidebar">
    <div class="sb-sec"><div class="sb-ttl">📡 Zona / Cobertura</div><div id="sbZ"></div></div>
    <div class="sb-sec"><div class="sb-ttl">📰 Medio</div><div id="sbM"></div></div>
  </aside>
  <div class="content">
    <div class="stats">
      <div class="stat"><div class="stat-n" id="sT" style="color:var(--pr)">{total}</div><div class="stat-l">Noticias</div></div>
      <div class="stat"><div class="stat-n" style="color:var(--ac)">{medios_cnt}</div><div class="stat-l">Medios</div></div>
      <div class="stat"><div class="stat-n" style="color:var(--gn)">{zonas_cnt}</div><div class="stat-l">Zonas</div></div>
      <div class="stat"><div class="stat-n" id="sS" style="color:var(--bl)">0</div><div class="stat-l">Alertas</div></div>
    </div>
    <div class="alert-panel">
      <div class="ph">
        <div class="pt"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--pr)" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>Alertas para Epicentro</div>
        <div class="pa">
          <button class="btn br2" onclick="exportJSON()">⬇ JSON</button>
          <button class="btn bg2" onclick="exportCSV()">⬇ CSV</button>
          <button class="btn bb2" onclick="copyWP()">📋 WordPress</button>
          <button class="btn bgh" onclick="clearAll()">Limpiar</button>
        </div>
      </div>
      <div class="sl-list" id="slList"><div class="ep"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>Haz clic en <strong>+ Alerta</strong> en cualquier noticia</div></div>
    </div>
    <div class="controls">
      <div class="sw"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg><input type="text" id="sq" placeholder="Buscar noticias..."></div>
      <select id="sm"><option value="">Todos los medios</option></select>
      <select id="sz"><option value="">Todas las zonas</option></select>
    </div>
    <div class="sec-l">Noticias <span class="sec-c" id="cnt">{total}</span></div>
    <div class="grid" id="grid"></div>
    <div id="emp" class="empty" style="display:none"><svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg><h3>Sin resultados</h3><p>No hay noticias para ese filtro.</p></div>
  </div>
</div>
<div class="toasts" id="toasts"></div>
<script>
const N={noticias_js}.map((n,i)=>({{...n,id:"n"+i}}));
let sel=[],sq="",sm="",sz="",fz="",fm="";
function zonas(){{return[...new Set(N.map(n=>n.zona))].sort();}}
function medios(){{return[...new Set(N.map(n=>n.medio))].sort();}}
function initUI(){{
  medios().forEach(m=>{{const o=document.createElement("option");o.value=m;o.textContent=m;document.getElementById("sm").appendChild(o);}});
  zonas().forEach(z=>{{const o=document.createElement("option");o.value=z;o.textContent=z;document.getElementById("sz").appendChild(o);}});
  document.getElementById("sbZ").innerHTML=zonas().map(z=>`<div class="sb-item" data-z="${{z}}" onclick="fZone('${{z}}')">`+`<span>${{z}}</span><span class="sb-cnt">${{N.filter(n=>n.zona===z).length}}</span></div>`).join("");
  document.getElementById("sbM").innerHTML=medios().map(m=>`<div class="sb-item" data-m="${{m}}" onclick="fMedio('${{m}}')">`+`<span class="sb-dot"></span><span style="flex:1">${{m}}</span></div>`).join("");
}}
function fZone(z){{fz=fz===z?"":z;fm="";sm="";sz=fz;document.getElementById("sz").value=fz;document.getElementById("sm").value="";document.querySelectorAll(".sb-item[data-z]").forEach(e=>e.classList.toggle("on",e.dataset.z===fz));document.querySelectorAll(".sb-item[data-m]").forEach(e=>e.classList.remove("on"));render();}}
function fMedio(m){{fm=fm===m?"":m;fz="";sz="";sm=fm;document.getElementById("sm").value=fm;document.getElementById("sz").value="";document.querySelectorAll(".sb-item[data-m]").forEach(e=>e.classList.toggle("on",e.dataset.m===fm));document.querySelectorAll(".sb-item[data-z]").forEach(e=>e.classList.remove("on"));render();}}
function ta(s){{if(!s)return"";try{{const d=new Date(s),df=Math.floor((Date.now()-d)/1e3);if(df<60)return"ahora";if(df<3600)return Math.floor(df/60)+"m";if(df<86400)return Math.floor(df/3600)+"h";return Math.floor(df/86400)+"d";}}catch{{return"";}}}}
function render(){{
  const q=sq.toLowerCase();
  const list=N.filter(n=>(!q||[n.titulo,n.medio,n.zona,n.descripcion].join(" ").toLowerCase().includes(q))&&(!sm||n.medio===sm)&&(!sz||n.zona===sz));
  document.getElementById("cnt").textContent=list.length;
  const g=document.getElementById("grid"),e=document.getElementById("emp");
  if(!list.length){{g.innerHTML="";e.style.display="flex";return;}}
  e.style.display="none";
  g.innerHTML=list.map(n=>{{const is=sel.some(s=>s.id===n.id),t=ta(n.publicado);
    return`<div class="card${{is?" sel":""}}" id="c-${{n.id}}"><div class="ct"><div class="cb"><span class="badge bm">${{n.medio}}</span><span class="badge bz">${{n.zona}}</span><span class="badge br">📻 ${{n.cobertura_radio}}</span></div>${{t?`<span class="ctm">${{t}}</span>`:""}}</div><div class="ctitle">${{n.titulo}}</div>${{n.descripcion?`<div class="cdesc">${{n.descripcion}}</div>`:""}}<div class="cf"><button class="badd" onclick="tog('${{n.id}}')">${{is?"✓ Agregada":"+ Alerta"}}</button>${{n.enlace?`<a class="bver" href="${{n.enlace}}" target="_blank" rel="noopener">Ver <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg></a>`:""}}</div></div>`;}}).join("");
  document.getElementById("sS").textContent=sel.length;
}}
function tog(id){{const n=N.find(n=>n.id===id);if(!n)return;const i=sel.findIndex(s=>s.id===id);if(i>-1){{sel.splice(i,1);toast("Quitada","info");}}else{{sel.push(n);toast("Añadida a alertas","ok");}}rSel();render();}}
function rSel(){{const el=document.getElementById("slList");document.getElementById("sS").textContent=sel.length;if(!sel.length){{el.innerHTML=`<div class="ep"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>Haz clic en <strong>+ Alerta</strong> en cualquier noticia</div>`;return;}}el.innerHTML=sel.map(n=>`<div class="si"><div><div class="si-t">${{n.titulo}}</div><div class="si-m">📻 ${{n.cobertura_radio}} · ${{n.medio}}${{n.enlace?` · <a href="${{n.enlace}}" target="_blank" rel="noopener">ver nota</a>`:""}}</div></div><span class="si-x" onclick="tog('${{n.id}}')" title="Quitar">×</span></div>`).join("");}}
function exportJSON(){{if(!sel.length){{toast("Sin alertas","err");return;}}const b=new Blob([JSON.stringify(sel,null,2)],{{type:"application/json"}});const a=document.createElement("a");a.href=URL.createObjectURL(b);a.download="alertas_epicentro_"+new Date().toISOString().slice(0,10)+".json";a.click();toast("JSON exportado","ok");}}
function exportCSV(){{if(!sel.length){{toast("Sin alertas","err");return;}}const h=["titulo","medio","zona","cobertura_radio","publicado","enlace"];const r=sel.map(n=>h.map(k=>`"${{(n[k]||"").replace(/"/g,'""')}}"`).join(","));const b=new Blob([[h.join(","),...r].join("\\n")],{{type:"text/csv;charset=utf-8;"}});const a=document.createElement("a");a.href=URL.createObjectURL(b);a.download="alertas_epicentro_"+new Date().toISOString().slice(0,10)+".csv";a.click();toast("CSV exportado","ok");}}
function copyWP(){{if(!sel.length){{toast("Sin alertas","err");return;}}const t=sel.map(n=>`<!-- ${{n.medio}} | ${{n.cobertura_radio}} -->\\n<strong>${{n.titulo}}</strong>\\n${{n.descripcion}}\\n<a href="${{n.enlace}}" target="_blank" rel="noopener">Leer más →</a>`).join("\\n\\n---\\n\\n");navigator.clipboard.writeText(t).then(()=>toast("Copiado para WordPress","ok")).catch(()=>toast("Error al copiar","err"));}}
function clearAll(){{sel=[];rSel();render();toast("Lista limpiada","info");}}
function toast(m,t="ok"){{const c=document.getElementById("toasts"),el=document.createElement("div");el.className="toast";const ic={{ok:`<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--gn)" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>`,err:`<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--pr)" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6M9 9l6 6"/></svg>`,info:`<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--ac)" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>`}};el.innerHTML=(ic[t]||ic.info)+`<span>${{m}}</span>`;c.appendChild(el);setTimeout(()=>{{el.style.opacity="0";el.style.transition="opacity .3s";setTimeout(()=>el.remove(),300);}},2500);}}
(function(){{const t=document.querySelector("[data-theme-toggle]"),r=document.documentElement;let d=r.getAttribute("data-theme")||"dark";function ui(){{t.innerHTML=d==="dark"?`<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>`:`<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;}}ui();t&&t.addEventListener("click",()=>{{d=d==="dark"?"light":"dark";r.setAttribute("data-theme",d);ui();}});}})(  );
document.getElementById("sq").addEventListener("input",e=>{{sq=e.target.value;render();}});
document.getElementById("sm").addEventListener("change",e=>{{sm=e.target.value;fm=sm;sz="";fz="";document.querySelectorAll(".sb-item[data-m]").forEach(el=>el.classList.toggle("on",el.dataset.m===sm));document.querySelectorAll(".sb-item[data-z]").forEach(el=>el.classList.remove("on"));render();}});
document.getElementById("sz").addEventListener("change",e=>{{sz=e.target.value;fz=sz;sm="";fm="";document.querySelectorAll(".sb-item[data-z]").forEach(el=>el.classList.toggle("on",el.dataset.z===sz));document.querySelectorAll(".sb-item[data-m]").forEach(el=>el.classList.remove("on"));render();}});
initUI();render();
</script>
</body>
</html>"""

with open(out_dir / "index.html", "w", encoding="utf-8") as f:
    f.write(HTML)

print(f"✅ public/index.html generado — {total} noticias, {medios_cnt} medios")
