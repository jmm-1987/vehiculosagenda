
"use strict";
/* ===================== DATOS FIJOS ===================== */
const EMPRESA={nombre:"Alditraex SL",dir:"C/ Cádiz, 15 · Pol. Ind. El Prado",cpPob:"06800 Mérida (Badajoz)",cif:"B06422208",iban:"ES38 0078 0076 4440 0000 3347",admin:"administracion@alditraex.es"};
const DELEG={MER:{nombre:"Mérida",origen:{cp:"06800",pob:"MÉRIDA",prov:"BADAJOZ",pais:"ES"}},NAV:{nombre:"Navalmoral de la Mata",origen:{cp:"10300",pob:"NAVALMORAL DE LA MATA",prov:"CÁCERES",pais:"ES"}}};
const PAISES=[["ES","España"],["PT","Portugal"],["DE","Alemania"],["AD","Andorra"],["AL","Albania"],["AT","Austria"],["BE","Bélgica"],["BY","Bielorrusia"],["BA","Bosnia y Herzegovina",1],["BG","Bulgaria"],["CZ","Chequia"],["HR","Croacia"],["DK","Dinamarca"],["SK","Eslovaquia"],["SI","Eslovenia"],["EE","Estonia"],["FI","Finlandia"],["FR","Francia"],["GR","Grecia",1],["HU","Hungría"],["IT","Italia"],["XK","Kosovo",1],["LV","Letonia"],["LI","Liechtenstein"],["LT","Lituania"],["LU","Luxemburgo"],["MK","Macedonia del Norte"],["MD","Moldavia"],["MC","Mónaco"],["ME","Montenegro",1],["NO","Noruega"],["NL","Países Bajos"],["PL","Polonia"],["RO","Rumanía"],["RU","Rusia"],["SM","San Marino"],["RS","Serbia"],["SE","Suecia"],["CH","Suiza"],["UA","Ucrania"],["VA","Vaticano"]];
const PAIS_NOM=Object.fromEntries(PAISES.map(p=>[p[0],p[1]]));
const NODATA=new Set(PAISES.filter(p=>p[2]).map(p=>p[0]));
const TIERS=[10,20,30,40,50,60,70,80,90,100,150,200,250,300,350,400,450,500,600,700,800,900,1000];
const ZN={REGIONAL:"Regional",CORTO:"1-Corto",MEDIO:"2-Medio",LARGO:"3-Largo",PORTUGAL:"Portugal",MALLORCA:"Mallorca",BALEARES:"Resto Baleares",COTIZACION:"Cotización"};
const TARIFAS={
 MER:{nombre:"TG 2026 Mérida",zonas:{REGIONAL:["badajoz","caceres"],CORTO:["almeria","cadiz","cordoba","granada","guadalajara","huelva","jaen","madrid","malaga","sevilla"],MEDIO:["ciudad real","cuenca","segovia","toledo","valladolid"]},
  R:{REGIONAL:{p:[7.64,9.71,10.11,11.37,12.88,14.14,15.20,16.67,18.12,21.70,26.01,31.12,35.74,39.84,43.34,46.75,49.51,55.16,65.66,72.69,79.75,86.72,93.83],k:[0.0859,0.0806,null]},
   CORTO:{p:[22.23,24.22,25.46,27.64,29.56,31.66,33.67,36.70,39.44,42.17,54.64,64.21,68.06,76.33,83.48,91.59,98.27,110.96,118.66,133.45,154.54,174.06,198.29],k:[0.1793,0.1666,0.1570]},
   MEDIO:{p:[22.93,24.92,26.58,29.12,31.42,33.91,36.39,39.67,42.79,45.89,58.80,70.51,75.55,85.30,94.23,103.86,111.74,125.58,135.65,153.29,177.21,199.54,226.62],k:[0.2069,0.1941,0.1846]},
   LARGO:{p:[23.61,25.64,27.68,30.62,33.28,36.13,38.88,42.66,46.13,49.62,62.95,76.80,83.03,94.28,104.98,116.15,125.20,140.86,153.29,173.12,199.87,225.05,254.96],k:[0.2334,0.2217,0.2122]},
   PORTUGAL:{p:[27.15,30.83,33.92,37.85,41.54,45.43,49.20,52.42,58.49,63.01,79.96,101.67,112.92,129.84,146.74,163.68,180.75,202.24,226.62,260.46,299.01,336.00,377.70],k:[0.3512,0.3374,0.3257]},
   MALLORCA:{p:[27.15,30.83,33.92,37.85,41.54,45.43,49.20,52.42,58.49,63.01,79.96,101.67,112.92,129.84,146.74,163.68,180.75,202.24,226.62,260.46,299.01,336.00,377.70],k:[0.3512,0.3374,0.3257]},
   BALEARES:{p:[32.10,44.94,44.94,62.61,62.61,79.75,79.75,79.75,79.75,79.75,88.92,105.94,153.46,153.46,190.44,190.44,212.66,212.66,null,null,null,null,null],k:[null,null,null]}}},
 NAV:{nombre:"TG 2026 Navalmoral",zonas:{REGIONAL:["badajoz","caceres"],CORTO:["madrid"],MEDIO:["ciudad real","guadalajara","segovia","sevilla","toledo"]},
  R:{REGIONAL:{p:[10.3,11.25,14.38,16.29,17.89,19.23,21.09,23.27,25.13,27.01,32.63,36.39,40.12,42.0,45.76,55.31,60.34,64.91,75.11,82.55,90.54,98.58,104.49],k:[0.0947,0.0916,null]},
   CORTO:{p:[16.45,17.74,21.33,24.23,25.43,27.01,29.9,33.08,35.43,39.89,43.72,53.37,57.44,65.17,68.68,72.07,76.51,80.94,82.79,94.37,97.7,105.98,109.29],k:[0.1087,0.101,0.0963]},
   MEDIO:{p:[21.23,22.49,24.08,27.63,29.36,32.11,35.68,38.97,42.85,47.25,54.78,65.73,70.07,77.79,82.99,89.12,94.53,102.23,105.98,121.35,130.04,137.79,158.79],k:[0.1569,0.1507,0.1507]},
   LARGO:{p:[22.32,24.04,26.59,31.02,33.57,37.15,41.58,46.38,50.43,55.67,63.05,72.94,77.43,82.99,94.53,105.15,112.95,119.01,126.53,140.58,152.68,173.47,188.45],k:[0.1942,0.1646,0.1631]},
   PORTUGAL:{p:[28.13,32.45,36.07,40.68,45.01,49.55,53.96,59.6,64.86,70.16,80.8,106.23,119.41,139.23,159.07,178.89,198.91,224.09,252.68,292.32,337.5,380.85,429.73],k:[0.3961,0.3868,0.3743]},
   MALLORCA:{p:[28.13,32.45,36.07,40.68,45.01,49.55,53.96,59.6,64.86,70.16,80.8,106.23,119.41,139.23,159.07,178.89,198.91,224.09,252.68,292.32,337.5,380.85,429.73],k:[0.3961,0.3868,0.3743]},
   BALEARES:{p:[46.12,64.55,64.09,89.92,89.92,114.54,114.54,114.54,114.54,114.54,127.71,152.16,220.39,220.39,273.51,273.51,305.41,305.41,null,null,null,null,null],k:[null,null,null]}}}
};
const RECARGO_KG=0.05, RECARGO_PALLET=17, SUPL_NO_EUR=0.08;
/* TP3 2026 pallets EUR 1,20×0,80 (hasta 2,30 m alto, 451-1.000 kg). Columnas: 1, 2, 3-4, 5-6, 7-8, 9-10, 11-12 pallets (null = cotización) */
const TP3={"alava":[91,84,78,74,70,67,null],"albacete":[85,80,73,69,65,62,null],"alicante":[98,90,83,79,75,72,null],"almeria":[95,88,80,73,69,66,null],"asturias":[100,94,85,82,79,76,null],"avila":[91,84,79,75,72,69,null],"badajoz":[59,54,54,52,50,48,null],"barcelona":[101,96,90,85,81,78,null],"burgos":[93,84,79,75,72,69,null],"caceres":[64,62,62,60,60,58,null],"cadiz":[95,88,80,73,69,66,null],"cantabria":[98,91,83,80,77,73,null],"castellon":[101,96,89,84,81,78,null],"ciudad real":[91,84,78,74,70,67,null],"cordoba":[95,88,80,73,69,66,null],"a coruna":[102,99,93,88,83,80,null],"cuenca":[83,77,70,67,63,60,null],"girona":[108,101,95,90,85,82,null],"granada":[95,88,80,73,69,66,null],"guadalajara":[79,73,67,63,60,57,null],"guipuzcoa":[101,95,88,83,80,77,null],"huelva":[95,88,80,73,69,66,null],"huesca":[113,106,99,93,88,83,null],"jaen":[95,88,80,73,69,66,null],"la rioja":[88,81,74,70,67,63,null],"leon":[89,83,77,73,69,66,null],"lleida":[116,109,102,96,93,89,null],"lugo":[102,96,89,84,81,78,null],"madrid":[77,70,64,60,57,53,null],"malaga":[95,88,80,73,69,66,null],"murcia":[98,90,83,79,75,72,null],"navarra":[94,88,81,77,73,70,null],"ourense":[102,96,89,84,81,78,null],"palencia":[85,81,74,70,67,63,null],"pontevedra":[104,100,93,89,84,81,null],"salamanca":[85,80,74,70,67,63,null],"segovia":[89,83,77,73,69,66,null],"sevilla":[81,74,68,64,61,58,null],"soria":[100,94,87,82,77,73,null],"tarragona":[102,95,89,83,80,77,null],"teruel":[91,84,79,74,70,67,null],"toledo":[83,78,70,67,63,60,null],"valencia":[89,82,75,72,68,64,null],"valladolid":[83,78,70,67,63,60,null],"vizcaya":[98,90,83,79,75,72,null],"zamora":[85,80,74,70,67,63,null],"zaragoza":[89,81,75,72,68,64,null],"palma mallorca":[196,190,183,180,174,null,null]};
const TP3_COLS=["1","2","3-4","5-6","7-8","9-10","11-12"];
const PROV_ALIAS={"araba":"alava","araba/alava":"alava","gerona":"girona","lerida":"lleida","orense":"ourense","la coruna":"a coruna","coruna":"a coruna","gipuzkoa":"guipuzcoa","bizkaia":"vizcaya","castello":"castellon","valencia/valencia":"valencia","alacant":"alicante","alicante/alacant":"alicante","castellon/castello":"castellon"};
/* TP3 Pallets Portugal (solo delegación Mérida). Columnas: 1, 2, 3-4, 5-6, 7, 8, 9-10 pallets */
const TP3PT=[[10,19,"Lisboa",[75,69,63,59,56,54,52]],[20,23,"Santarém",[80,75,68,65,62,59,57]],[24,27,"Leiria",[79,74,67,64,61,58,55]],[28,29,"Setúbal",[79,75,68,65,62,59,57]],[30,34,"Coimbra",[110,105,97,92,88,85,78]],[35,37,"Viseu",[91,81,80,77,74,70,67]],[38,38,"Aveiro",[91,87,80,77,74,70,67]],[40,46,"Porto",[89,83,77,74,70,67,65]],[47,48,"Braga",[88,82,76,72,69,68,66]],[49,49,"Viana do Castelo",[91,87,80,77,74,71,69]],[50,52,"Vila Real",[102,95,88,83,79,77,75]],[53,54,"Bragança",[102,95,88,83,79,77,75]],[60,62,"Castelo Branco",[102,95,88,83,79,77,75]],[63,64,"Guarda",[102,95,88,83,79,77,75]],[70,72,"Évora",[96,89,82,78,74,71,69]],[73,74,"Portalegre",[85,81,75,71,68,66,64]],[75,79,"Beja",[96,89,82,78,74,71,69]],[80,89,"Faro",[96,89,82,78,74,71,69]]];
const TP3PT_COLS=["1","2","3-4","5-6","7","8","9-10"];
const MOTIVOS=["PRECIO","YA NO LE INTERESA CLIENTE","ERROR AL GRABAR","OTROS"];

/* ===================== UTILIDADES ===================== */
const $=s=>document.querySelector(s);
const norm=s=>(s||"").toString().normalize("NFD").replace(/\p{M}/gu,"").toLowerCase().trim();
const U=s=>(s||"").toString().trim().toUpperCase();
const L=s=>(s||"").toString().trim().toLowerCase();
const eur=n=>(Number(n)||0).toLocaleString("es-ES",{minimumFractionDigits:2,maximumFractionDigits:2})+" €";
const num=(n,d=0)=>(Number(n)||0).toLocaleString("es-ES",{minimumFractionDigits:d,maximumFractionDigits:d,useGrouping:true});
const r2=n=>Math.round((Number(n)||0)*100)/100;
const today=()=>{const d=new Date();return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")};
const fmtDate=iso=>iso?iso.split("-").reverse().join("/"):"";
const esc=s=>(s==null?"":String(s)).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const numCode=(serie,n,anio)=>serie+"-"+n+"/"+String(anio).slice(-2);
const delegNombre=s=>(DELEG[s]||{}).nombre||s||"";
function toast(msg){const t=document.createElement("div");t.className="toast";t.textContent=msg;document.body.appendChild(t);setTimeout(()=>t.remove(),3200)}
function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
function fillPaises(sel,val){sel.innerHTML=PAISES.map(p=>`<option value="${p[0]}">${esc(p[1])}</option>`).join("")+`<option value="OT">Otro país</option>`;sel.value=val||"ES"}
const paisNombre=c=>PAIS_NOM[c]||(c==="OT"?"Otro país":c||"");

/* ===================== ZONAS Y PRECIO ===================== */
function isExtremadura(p){return p&&p.pais==="ES"&&["badajoz","caceres"].includes(norm(p.prov))}
function zoneOf(p,serie){
  if(!p||!(p.cp||p.prov||p.pob))return null;
  if(p.pais==="PT")return "PORTUGAL";
  if(p.pais&&p.pais!=="ES")return "COTIZACION";
  const cp=(p.cp||"").trim(), pr=norm(p.prov);
  if(/^(35|38|51|52)/.test(cp)||/palmas|tenerife|ceuta|melilla/.test(pr))return "COTIZACION";
  if(cp.startsWith("07")||pr.includes("baleares")||pr.includes("illes"))return (cp.startsWith("077")||cp.startsWith("078"))?"BALEARES":"MALLORCA";
  const Z=TARIFAS[serie].zonas;
  for(const z of ["REGIONAL","CORTO","MEDIO"]) if(Z[z].includes(pr))return z;
  return "LARGO";
}
function tariff(serie,zone,kg){
  const R=TARIFAS[serie].R[zone];
  if(!R)return {price:null,detail:"Cotización"};
  if(kg<=0)return {price:0,detail:""};
  if(kg<=1000){const i=TIERS.findIndex(t=>kg<=t);const p=R.p[i];return p==null?{price:null,detail:"Cotización"}:{price:p,detail:"Tramo hasta "+num(TIERS[i])+" kg"}}
  const idx=kg<=2000?0:kg<=3000?1:kg<=10000?2:-1;
  if(idx<0)return {price:null,detail:"Cotización (> 10.000 kg)"};
  const k=R.k[idx]; if(k==null)return {price:null,detail:"Cotización"};
  return {price:r2(kg*k),detail:num(kg)+" kg × "+k.toLocaleString("es-ES",{minimumFractionDigits:4})+" €/kg"};
}

const isNoEur=b=>{const mx=Math.max(b.l||0,b.a||0),mn=Math.min(b.l||0,b.a||0);return mx>1.205||mn>0.805};
function provKey(p){let k=norm(p.prov);k=PROV_ALIAS[k]||k;if(k.includes("/"))k=PROV_ALIAS[k]||norm(k.split("/")[1]||k.split("/")[0]);return k}
/* Devuelve {precioUd, zonaNombre, detalle, extra17, aviso} o precioUd null = cotización */
function palletQuote(serie,o,d,n){
  const res={precioUd:null,zona:"",detalle:"",extra17:false,aviso:""};
  if(!n){res.detalle="Indica el número de pallets";return res}
  const ptEnd=d.pais==="PT"?d:(o.pais==="PT"?o:null);
  const otherEnd=ptEnd===d?o:d;
  if((o.pais!=="ES"&&o.pais!=="PT")||(d.pais!=="ES"&&d.pais!=="PT")){res.zona="Internacional";res.detalle="Buscar cotización";return res}
  if(ptEnd){
    res.zona="TP3 Portugal";
    if(serie==="NAV"){res.detalle="Buscar cotización (Navalmoral sin tarifa pallets Portugal)";return res}
    if(otherEnd.pais==="PT"){res.detalle="Buscar cotización";return res}
    const two=parseInt((ptEnd.cp||"").replace(/\D/g,"").slice(0,2),10);
    const row=TP3PT.find(r=>two>=r[0]&&two<=r[1]);
    if(!row){res.detalle="Buscar cotización (Madeira, Azores o CP no reconocido)";return res}
    res.zona="TP3 PT · "+row[2];
    const i=n===1?0:n===2?1:n<=4?2:n<=6?3:n===7?4:n===8?5:n<=10?6:-1;
    if(i<0){res.detalle="Buscar cotización (más de 10 pallets)";return res}
    res.precioUd=row[3][i];res.detalle=n+" pallets · columna "+TP3PT_COLS[i];
    if(!isExtremadura(o)){res.extra17=true;if(!isExtremadura(d))res.aviso="Ni origen ni destino en Badajoz/Cáceres: se suman 17 € por pallet. Revisa el precio."}
    return res;
  }
  let target,extra=false;
  if(isExtremadura(o))target=d;
  else if(isExtremadura(d)){target=o;extra=true}
  else{target=d;extra=true;res.aviso="Ni origen ni destino en Badajoz/Cáceres: tarifa de la provincia de destino + 17 € por pallet. Revisa el precio."}
  const cp=target.cp||"",pk=provKey(target);
  if(/^(35|38|51|52)/.test(cp)||/palmas|tenerife|ceuta|melilla/.test(pk)){res.zona="TP3 · "+U(target.prov);res.detalle="Buscar cotización";return res}
  let key=pk;
  if(cp.startsWith("07")||pk.includes("baleares")||pk.includes("illes")){if(cp.startsWith("077")||cp.startsWith("078")){res.zona="TP3 · Islas menores";res.detalle="Buscar cotización";return res}key="palma mallorca"}
  const row=TP3[key];
  res.zona="TP3 · "+(key==="palma mallorca"?"Palma Mallorca":U(target.prov));
  if(!row){res.detalle="Buscar cotización (provincia no encontrada)";return res}
  const i=n===1?0:n===2?1:n<=4?2:n<=6?3:n<=8?4:n<=10?5:n<=12?6:-1;
  if(i<0||row[i]==null){res.detalle="Buscar cotización ("+n+" pallets)";return res}
  res.precioUd=row[i];res.detalle=n+" pallets · columna "+TP3_COLS[i];res.extra17=extra;
  return res;
}

/* ===================== ALMACÉN ===================== */
const Store={mode:"server",cbs:{},
  async init(){},
  async _list(c){
    const r=await fetch("/api/presupuestos2/"+encodeURIComponent(c));
    if(!r.ok)throw new Error("No se pudo leer "+c);
    return r.json();
  },
  listen(c,cb){
    this.cbs[c]=cb;
    const pull=async()=>{try{cb(await this._list(c))}catch(e){toast(e.message||String(e))}};
    pull();
    const timer=setInterval(pull,8000);
    return ()=>clearInterval(timer);
  },
  async set(c,id,data){
    const r=await fetch("/api/presupuestos2/"+encodeURIComponent(c)+"/"+encodeURIComponent(id),{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});
    if(!r.ok)throw new Error("No se pudo guardar");
    if(this.cbs[c])this.cbs[c](await this._list(c));
  },
  async del(c,id){
    const r=await fetch("/api/presupuestos2/"+encodeURIComponent(c)+"/"+encodeURIComponent(id),{method:"DELETE"});
    if(!r.ok)throw new Error("No se pudo borrar");
    if(this.cbs[c])this.cbs[c](await this._list(c));
  },
  async nextNumber(key,usados){
    const r=await fetch("/api/presupuestos2/siguiente-numero",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({key,usados})});
    const d=await r.json();
    if(!d.ok)throw new Error(d.error||"No se pudo reservar número");
    return d.numero;
  }
};

/* ===================== USUARIO ===================== */
const Me={id:null,name:"",avatar:"",api:null,manual:""};
async function initUser(){
  if(window.PRES2_USER){Me.name=window.PRES2_USER;Me.manual=window.PRES2_USER}
  renderWho();
}
function renderWho(){
  const w=$("#who");w.textContent="";
  if(Me.name){const img=document.createElement("img");img.src=Me.avatar;img.alt="";const s=document.createElement("span");s.append("Tarifica: ");const b=document.createElement("b");b.textContent=Me.name;s.append(b);w.append(img,s);return}
  const lab=document.createElement("label");lab.htmlFor="whoName";lab.textContent="Usuario:";
  const inp=document.createElement("input");inp.id="whoName";inp.placeholder="Tu nombre";inp.value=ls("ald_user")||"";Me.manual=U(inp.value);
  inp.addEventListener("change",()=>{Me.manual=U(inp.value);ls("ald_user",Me.manual)});
  w.append(lab,inp);
}
async function userNames(ids){
  const out={};const need=[...new Set(ids.filter(Boolean))];
  if(Me.api&&need.length){try{const ps=await Me.api.profiles(need);need.forEach(id=>{out[id]=(ps[id]&&ps[id].name)||""})}catch(e){}}
  return out;
}

/* ===================== CÓDIGOS POSTALES ===================== */
const CPC={},cpLoad={};
async function getCountryJSON(cc){
  if(window.CPGZ&&window.CPGZ[cc]){
    const bin=Uint8Array.from(atob(window.CPGZ[cc]),c=>c.charCodeAt(0));
    const txt=await new Response(new Blob([bin]).stream().pipeThrough(new DecompressionStream("gzip"))).text();
    return JSON.parse(txt);
  }
  const r=await fetch("cp/"+cc+".json");return r.json();
}
function loadCountry(cc){
  if(CPC[cc])return Promise.resolve(CPC[cc]);
  if(NODATA.has(cc)||cc==="OT")return Promise.resolve([]);
  if(!cpLoad[cc])cpLoad[cc]=getCountryJSON(cc).then(d=>{CPC[cc]=d.map(r=>({cp:U(r[0]),pob:U(r[1]),prov:U(r[2]),mun:U(r[3]||""),pais:cc,cpn:r[0].replace(/[^0-9A-Za-z]/g,"").toUpperCase(),k:norm(r[1]),km:norm(r[3]||"")}));return CPC[cc]}).catch(()=>{CPC[cc]=[];return CPC[cc]});
  return cpLoad[cc];
}
function searchCP(list,q,mode){
  q=(q||"").trim(); if(!q||!list.length)return [];
  if(mode==="cp"){const qn=q.replace(/[^0-9A-Za-z]/g,"").toUpperCase();if(!qn)return [];return list.filter(r=>r.cpn.startsWith(qn)).slice(0,40)}
  const qq=norm(q),starts=[],words=[],contains=[];
  for(const r of list){if(r.k.startsWith(qq))starts.push(r);else if(r.k.includes(" "+qq)||r.k.includes("-"+qq))words.push(r);else if(r.k.includes(qq)||(r.km&&r.km.startsWith(qq))||norm(r.prov).startsWith(qq))contains.push(r)}
  const s=(a,b)=>a.k.length-b.k.length||a.cp.localeCompare(b.cp);
  return starts.sort(s).concat(words.sort(s),contains.sort(s)).slice(0,40);
}
const cpRender=r=>`<span class="cp">${esc(r.cp)}</span><span>${esc(r.pob)}${r.mun?` <span class="hint">(${esc(r.mun)})</span>`:""}</span><span class="pr">${esc(r.prov)}</span>`;
function cpProvider(paisSel,mode){return async q=>{const cc=paisSel.value;if(NODATA.has(cc)||cc==="OT")return [];const l=await loadCountry(cc);return searchCP(l,q,mode)}}

/* ===================== AUTOCOMPLETAR ===================== */
function attachAC(input,box,provider,render,onPick,emptyMsg){
  let items=[],idx=-1,seq=0;
  const close=()=>{box.hidden=true;input.setAttribute("aria-expanded","false");idx=-1};
  const draw=()=>{
    box.textContent="";
    if(!items.length){if(!input.value.trim()){close();return}const e=document.createElement("div");e.className="empty";e.textContent=(emptyMsg&&emptyMsg())||"Sin resultados";box.append(e)}
    items.forEach((it,i)=>{const b=document.createElement("button");b.type="button";if(i===idx)b.className="on";b.innerHTML=render(it);b.addEventListener("mousedown",ev=>{ev.preventDefault();onPick(it);close()});box.append(b)});
    box.hidden=false;input.setAttribute("aria-expanded","true");
    const on=box.querySelector(".on");if(on)on.scrollIntoView({block:"nearest"});
  };
  const update=async()=>{const my=++seq;const r=await provider(input.value);if(my!==seq)return;items=r;idx=items.length?0:-1;draw()};
  input.addEventListener("input",update);
  input.addEventListener("focus",()=>{if(input.value.trim()||input.dataset.openEmpty)update()});
  input.addEventListener("blur",()=>setTimeout(close,120));
  input.addEventListener("keydown",e=>{
    if(box.hidden)return;
    if(e.key==="ArrowDown"){idx=Math.min(items.length-1,idx+1);draw();e.preventDefault()}
    else if(e.key==="ArrowUp"){idx=Math.max(0,idx-1);draw();e.preventDefault()}
    else if(e.key==="Enter"&&idx>=0){onPick(items[idx]);close();e.preventDefault()}
    else if(e.key==="Escape")close();
  });
}
function wirePlace(prefix,onChange){
  const pais=$("#"+prefix+"Pais"),cp=$("#"+prefix+"CP"),pob=$("#"+prefix+"Pob"),prov=$("#"+prefix+"Prov");
  const pick=r=>{cp.value=r.cp;pob.value=r.pob;prov.value=r.prov;onChange&&onChange()};
  const noData=()=>NODATA.has(pais.value)||pais.value==="OT"?"Sin base de CP para este país: escribe los datos a mano":"Sin resultados";
  attachAC(cp,cp.nextElementSibling,cpProvider(pais,"cp"),cpRender,pick,noData);
  attachAC(pob,pob.nextElementSibling,cpProvider(pais,"pob"),cpRender,pick,noData);
  pais.addEventListener("change",()=>{cp.value="";pob.value="";prov.value="";loadCountry(pais.value);onChange&&onChange()});
}

/* ===================== ESTADO ===================== */
let CLIENTES=[],PRES=[],SETTINGS={combustible:5.07};
let editing=null,selCliente=null,motivoRech="",prevEstado="Pendiente";
let bultos=[{tipo:"Palet",cant:1,l:1.2,a:0.8,h:1.2}];
const serieSel=()=>$("#pDeleg").value;

/* ===================== FORMULARIO ===================== */
function placeGet(p){return {cp:U($("#"+p+"CP").value),pob:U($("#"+p+"Pob").value),prov:U($("#"+p+"Prov").value),pais:$("#"+p+"Pais").value}}
function placeSet(p,v){$("#"+p+"Pais").value=v.pais||"ES";$("#"+p+"CP").value=v.cp||"";$("#"+p+"Pob").value=v.pob||"";$("#"+p+"Prov").value=v.prov||"";loadCountry(v.pais||"ES")}

function drawBultos(){
  const tb=$("#tBultos tbody");const peso=$("#pPeso"),merc=$("#pMerc");$("#sharedInputs").append(peso,merc);tb.textContent="";
  bultos.forEach((b,i)=>{
    const tr=document.createElement("tr");
    tr.innerHTML=`<td><select data-k="tipo" aria-label="Tipo"><option>Palet</option><option>Bulto</option><option>Caja</option><option>Otro</option></select></td>
      <td><input data-k="cant" type="number" min="1" step="1" inputmode="numeric" aria-label="Cantidad"></td>
      <td><input data-k="l" type="number" min="0" step="0.01" inputmode="decimal" aria-label="Largo en metros"></td>
      <td><input data-k="a" type="number" min="0" step="0.01" inputmode="decimal" aria-label="Ancho en metros"></td>
      <td><input data-k="h" type="number" min="0" step="0.01" inputmode="decimal" aria-label="Alto en metros"></td>
      <td><input data-k="kg" type="number" min="0" step="0.1" inputmode="decimal" placeholder="kg" aria-label="Peso por unidad en kg"></td>
      <td class="vol"></td>${i===0?`<td class="shared desc" rowspan="${bultos.length}"></td>`:""}
      <td><button type="button" class="btn ghost small danger" aria-label="Quitar línea">✕</button></td>`;
    tr.querySelectorAll("[data-k]").forEach(el=>{el.value=b[el.dataset.k]==null?"":b[el.dataset.k];el.addEventListener("input",()=>{b[el.dataset.k]=el.dataset.k==="tipo"?el.value:parseFloat(String(el.value).replace(",","."))||0;calc()})});
    tr.querySelector("button").addEventListener("click",()=>{bultos.splice(i,1);if(!bultos.length)bultos.push({tipo:"Palet",cant:1,l:0,a:0,h:0});drawBultos();calc()});
    if(i===0)tr.querySelector("td.shared").append(merc)
    tb.append(tr);
  });
}
function currentIVA(){
  const m=$("#pIvaMode").value;
  if(m==="21")return {pct:21,why:"forzado"};
  if(m==="0")return {pct:0,why:"forzado"};
  if(!selCliente)return {pct:21,why:"sin cliente"};
  return (selCliente.pais||"ES")==="ES"?{pct:21,why:"cliente España"}:{pct:0,why:"cliente "+paisNombre(selCliente.pais)};
}
function calc(){
  const serie=serieSel();
  let nb=0,vol=0;
  let peso=0;
  bultos.forEach((b,i)=>{const v=(b.cant||0)*(b.l||0)*(b.a||0)*(b.h||0),w=(b.cant||0)*(b.kg||0);nb+=b.cant||0;vol+=v;peso+=w;const row=$("#tBultos tbody").children[i];if(row){const c=row.querySelector(".vol");c.textContent=num(v,3)+" m³";const sm=document.createElement("small");sm.textContent=num(w,w%1?1:0)+" kg";c.append(sm)}});
  peso=r2(peso);$("#pPeso").value=peso||"";
  const pvkg=r2(vol*250);
  const kg=Math.ceil(Math.max(peso,pvkg));
  const o=placeGet("o"),d=placeGet("d");
  const zo=zoneOf(o,serie),zd=zoneOf(d,serie);
  const isPal=$("#pModo").value==="PALLETS";
  $("#zOrigen").textContent=zo&&!isPal?"· "+ZN[zo]:"";$("#zDestino").textContent=zd&&!isPal?"· "+ZN[zd]:"";
  $("#optTG").textContent="TG "+serie+" (por kg)";
  $("#modoHint").textContent=isPal?"Pallet EUR 1,20 × 0,80 (hasta 2,30 m y 1.000 kg). Medidas mayores: +8 %. Cada línea de la tabla cuenta como pallets.":"Precio por kg facturable con la tarifa TG de "+delegNombre(serie)+".";
  const modo=$("#pModo").value;
  const mr=$("#pManual").value;const manual=mr!==""?parseFloat(mr):null;
  let zona=null,zonaNombre="",aviso="",price=null,detail="",rec=0,supl=0,recLbl="",nPal=0,precioUd=null,tarifaNombre="";
  const avisos=[];
  if(modo==="PALLETS"){
    tarifaNombre="T PALLETS (TP3 2026)";
    nPal=bultos.reduce((s,b)=>s+(b.cant||0),0);
    if(zo&&zd){
      const q=palletQuote(serie,o,d,nPal);zona="PALLETS";zonaNombre=q.zona;detail=q.detalle;aviso=q.aviso;precioUd=q.precioUd;
      if(q.precioUd!=null){
        price=r2(nPal*q.precioUd);
        if(manual==null){
          supl=r2(bultos.filter(isNoEur).reduce((s,b)=>s+(b.cant||0)*q.precioUd*SUPL_NO_EUR,0));
          if(q.extra17){rec=r2(nPal*RECARGO_PALLET);recLbl=nPal+" pallets × 17 €"}
        }
        detail=nPal+" × "+eur(q.precioUd)+" ("+detail+")";
      }
    }
    if(bultos.some(b=>(b.h||0)>2.305))avisos.push("Algún pallet supera 2,30 m de altura: fuera de tarifa, revisa el precio.");
    if(bultos.some(b=>(b.kg||0)>1000)||(nPal&&peso/nPal>1000))avisos.push("Más de 1.000 kg por pallet: fuera de tarifa, revisa el precio.");
  }else{
    tarifaNombre=TARIFAS[serie].nombre;
    let recargo=false;
    if(zo&&zd){
      if(isExtremadura(o))zona=zd;
      else if(isExtremadura(d)){zona=zo;recargo=true}
      else{zona=zd;recargo=true;aviso="Ni origen ni destino están en Badajoz/Cáceres: se aplica la zona del destino + 0,05 €/kg. Revisa el precio."}
    }
    const t=zona?tariff(serie,zona,kg):{price:null,detail:""};
    price=t.price;detail=t.detail;zonaNombre=zona?ZN[zona]:"";
    if(recargo&&manual==null&&t.price!=null){rec=r2(kg*RECARGO_KG);recLbl=num(kg)+" kg × 0,05 €"}
  }
  const porte=manual!=null?r2(manual):(price||0);
  const cpv=parseFloat($("#pComb").value);const cp=isNaN(cpv)?0:cpv;
  const comb=r2((porte+supl+rec)*cp/100);
  const base=r2(porte+supl+rec+comb);
  const iv=currentIVA();const iva=r2(base*iv.pct/100);const total=r2(base+iva);
  $("#mBultos").textContent=num(nb);$("#mPeso").textContent=num(peso,peso%1?1:0)+" kg";$("#mVol").textContent=num(vol,3)+" m³";$("#mPvkg").textContent=num(pvkg)+" kg";$("#mKg").textContent=num(kg)+" kg";
  $("#tTarifa").textContent=tarifaNombre;
  $("#tZona").innerHTML=zona?`<span class="zone">${esc(zonaNombre)}</span>`:"—";
  $("#tKgLbl").textContent=modo==="PALLETS"?"Pallets":"Kg facturables";
  $("#tKg").textContent=modo==="PALLETS"?num(nPal)+" pallets":num(kg)+" kg";
  $("#tPorteLbl").innerHTML=manual!=null?"Porte (precio manual)":"Porte según tarifa"+(detail?`<small>${esc(detail)}</small>`:"");
  $("#tPorte").textContent=(manual==null&&zona&&price==null)?"Buscar cotización":eur(porte);
  $("#tSupRow").hidden=!supl;$("#tSup").textContent=eur(supl);$("#tSupLbl").textContent=supl?bultos.filter(isNoEur).reduce((s,b)=>s+(b.cant||0),0)+" pallets mayores de 1,20 × 0,80":"";
  $("#tRecRow").hidden=!rec;$("#tRec").textContent=eur(rec);$("#tRecLbl").textContent=recLbl;
  $("#tCombPct").textContent=num(cp,2);
  $("#tComb").textContent=eur(comb);$("#tBase").textContent=eur(base);
  $("#tIvaPct").textContent=iv.pct;$("#tIvaWhy").textContent=iv.why;$("#tIva").textContent=eur(iva);$("#tTotal").textContent=eur(total);
  $("#tRoute").textContent=(o.pob||d.pob)?((o.pob||"?")+" → "+(d.pob||"?")):"Indica origen y destino";
  const al=$("#tAlert");al.textContent="";
  const add=m=>{const x=document.createElement("div");x.className="alert warn";x.textContent=m;al.append(x)};
  if(aviso)add(aviso);
  avisos.forEach(add);
  if(zona&&price==null&&manual==null)add("Buscar cotización: esta combinación no tiene precio en tarifa. Indica un precio manual para poder guardar.");
  if(!selCliente)add("Falta seleccionar el cliente.");
  if(modo==="PALLETS"?!nPal:!kg)add(modo==="PALLETS"?"Indica el número de pallets.":"Indica peso o medidas de la mercancía.");
  const ok=!!(selCliente&&(modo==="PALLETS"?nPal>0:kg>0)&&zona&&(price!=null||manual!=null));
  $("#btnGuardar").disabled=!ok;$("#btnGuardarPdf").disabled=!ok;
  return {serie,modo,nb,nPal,precioUd,vol:Math.round(vol*1000)/1000,peso,pvkg,kg,o,d,zona,zonaNombre,tarifaNombre,tarifaDetalle:detail,porte,manual:manual!=null,supl,recargo:rec,recLbl,combPct:cp,comb,base,ivaPct:iv.pct,iva,total};
}
function setCliente(c){
  selCliente=c||null;
  $("#pCliente").value=c?c.nombre:"";
  const envio=$("#pEmailEnvio");if(envio)envio.value=(c&&c.email)||"";
  const card=$("#clientCard");card.textContent="";card.className="";
  if(c){card.className="clientcard";card.innerHTML=`<div><span>CIF/NIF</span> ${esc(c.cif)}</div><div><span>Tel.</span> ${esc(c.tel)}</div><div style="grid-column:1/-1"><span>Dirección</span> ${esc(c.dir)}, ${esc(c.cp)} ${esc(c.pob)} (${esc(c.prov)}) · ${esc(paisNombre(c.pais))}</div><div class="mail"><span>Email</span> ${esc(c.email)}</div><div><span>IVA</span> <span class="iva-chip">${(c.pais||"ES")==="ES"?"21 %":"0 %"}</span></div>`}
  calc();
}
function resetForm(keepDeleg){
  editing=null;$("#formTitle").textContent="Nuevo presupuesto";$("#btnCancelEdit").hidden=true;$("#pDeleg").disabled=false;
  $("#pFecha").value=today();
  if(!keepDeleg){const s=ls("ald_serie");$("#pDeleg").value=DELEG[s]?s:"MER"}
  placeSet("o",DELEG[serieSel()].origen);placeSet("d",{pais:"ES"});
  bultos=[{tipo:"Palet",cant:1,l:1.2,a:0.8,h:1.2}];drawBultos();
  $("#pPeso").value="";$("#pMerc").value="";$("#pManual").value="";$("#pIvaMode").value="auto";$("#pEstado").value="Pendiente";$("#pObs").value="";
  $("#pModo").value="TG";motivoRech="";prevEstado="Pendiente";
  $("#pComb").value=SETTINGS.combustible;
  setCliente(null);previewNumber();
}
function previewNumber(){
  if(editing){const p=PRES.find(x=>x.id===editing);$("#pNum").value=p?p.codigo:"";$("#tNum").textContent=p?p.codigo:"—";return}
  const serie=serieSel(),anio=parseInt(($("#pFecha").value||today()).slice(0,4));
  const n=Math.max(0,...PRES.filter(p=>p.anio===anio&&p.serie===serie).map(p=>p.numero||0))+1;
  $("#pNum").value=numCode(serie,n,anio)+" (provisional)";$("#tNum").textContent=numCode(serie,n,anio);
}
function loadIntoForm(p,asCopy){
  editing=asCopy?null:p.id;
  $("#formTitle").textContent=asCopy?"Nuevo presupuesto (copia de "+p.codigo+")":"Editando presupuesto "+p.codigo;
  $("#btnCancelEdit").hidden=asCopy;
  $("#pDeleg").value=p.serie;$("#pDeleg").disabled=!asCopy;
  $("#pFecha").value=asCopy?today():p.fecha;
  placeSet("o",p.origen);placeSet("d",p.destino);
  bultos=(p.bultos||[]).map(b=>Object.assign({},b));if(!bultos.length)bultos=[{tipo:"Palet",cant:1,l:0,a:0,h:0}];
  if(p.peso&&!bultos.some(b=>b.kg)){const c0=bultos[0].cant||1;bultos[0].kg=r2(p.peso/c0)} /* presupuestos antiguos: peso total pasa a la 1ª línea */
  drawBultos();
  $("#pPeso").value=p.peso||"";$("#pMerc").value=p.mercancia||"";$("#pManual").value=p.manual?p.porte:"";
  $("#pIvaMode").value=p.ivaMode||"auto";$("#pEstado").value=asCopy?"Pendiente":(p.estado||"Pendiente");$("#pObs").value=p.observaciones||"";
  $("#pModo").value=p.modo||"TG";motivoRech=asCopy?"":(p.motivoRechazo||"");prevEstado=$("#pEstado").value;
  $("#pComb").value=p.combPct;
  setCliente(CLIENTES.find(x=>x.id===p.clienteId)||Object.assign({id:p.clienteId},p.cliente));
  if(p.emailEnvio!=null&&$("#pEmailEnvio"))$("#pEmailEnvio").value=p.emailEnvio;
  previewNumber();location.hash="nuevo";
}
let saving=false;
async function savePres(withPdf){
  if(saving)return;const r=calc();if($("#btnGuardar").disabled)return;
  if(withPdf&&!L($("#pEmailEnvio").value).includes("@")){toast("Indica el email donde enviar el presupuesto");return}
  saving=true;$("#btnGuardar").disabled=true;$("#btnGuardarPdf").disabled=true;
  try{
    const fecha=$("#pFecha").value||today(),anio=parseInt(fecha.slice(0,4)),serie=r.serie;
    let id,numero,prev=null;
    if(editing){prev=PRES.find(x=>x.id===editing);id=editing;numero=prev.numero;
      if(prev.anio!==anio){toast("No se puede cambiar el año de un presupuesto ya numerado");return}}
    else{numero=await Store.nextNumber(serie+"-"+anio,PRES.filter(p=>p.anio===anio&&p.serie===serie).map(p=>p.numero||0));id=serie+"-"+anio+"-"+String(numero).padStart(5,"0")}
    const c=selCliente;
    const estado=$("#pEstado").value;
    const doc={serie,numero,anio,codigo:numCode(serie,numero,anio),fecha,delegacion:delegNombre(serie),estado,motivoRechazo:estado==="Rechazado"?motivoRech:"",
      modo:r.modo,numPallets:r.nPal,precioPallet:r.precioUd,suplNoEur:r.supl,recargoDetalle:r.recLbl,
      clienteId:c.id||null,cliente:{nombre:U(c.nombre),cif:U(c.cif),dir:U(c.dir),cp:U(c.cp),pob:U(c.pob),prov:U(c.prov),pais:c.pais||"ES",tel:U(c.tel),email:L(c.email)},
      bultos:bultos.map(b=>({tipo:b.tipo,cant:b.cant||0,l:b.l||0,a:b.a||0,h:b.h||0,kg:b.kg||0})),numBultos:r.nb,peso:r.peso,volumen:r.vol,pvkg:r.pvkg,kgFact:r.kg,
      mercancia:U($("#pMerc").value),origen:r.o,destino:r.d,zona:r.zona,zonaNombre:r.zonaNombre,tarifa:r.tarifaNombre,tarifaDetalle:r.tarifaDetalle,
      porte:r.porte,manual:r.manual,recargo:r.recargo,combPct:r.combPct,combustible:r.comb,base:r.base,ivaMode:$("#pIvaMode").value,ivaPct:r.ivaPct,iva:r.iva,total:r.total,
      observaciones:U($("#pObs").value),
      emailEnvio:L($("#pEmailEnvio").value),
      enviadoEn:prev&&prev.enviadoEn||null,enviadoA:prev&&prev.enviadoA||"",
      creadoPor:prev?prev.creadoPor:(Me.id||null),creadoPorNombre:prev?(prev.creadoPorNombre||""):(Me.id?"":Me.manual),
      creadoEn:prev?prev.creadoEn:new Date().toISOString(),modificadoEn:new Date().toISOString(),modificadoPor:Me.id||null};
    await Store.set("presupuestos",id,doc);
    ls("ald_serie",serie);
    toast("Presupuesto "+doc.codigo+" guardado");
    const saved=Object.assign({id},doc);
    if(withPdf){
      const ok=await downloadPdf(saved,null,{enviar:true,descargar:true});
      if(ok){doc.enviadoEn=new Date().toISOString();doc.enviadoA=doc.emailEnvio;await Store.set("presupuestos",id,doc)}
    }
    resetForm(true);location.hash="presupuestos";
  }catch(e){toast("No se pudo guardar: "+(e.message||e.code||e))}
  finally{saving=false;calc()}
}

/* ===================== CLIENTES ===================== */
function clientModal(c,onSaved){
  c=c||{};
  const root=$("#modalRoot");
  root.innerHTML=`<div class="modal" role="dialog" aria-modal="true" aria-labelledby="mcT"><div class="box">
    <div class="mh"><h3 id="mcT">${c.id?"Editar cliente":"Nuevo cliente"}</h3><button class="btn ghost" type="button" data-x aria-label="Cerrar">✕</button></div>
    <form class="mb" id="fCli" autocomplete="off">
      <div class="row"><div class="f" style="grid-column:span 2"><label for="cNom">Nombre / empresa *</label><input id="cNom" required></div><div class="f"><label for="cCif">CIF / NIF *</label><input id="cCif" required></div></div>
      <div class="row"><div class="f"><label for="cDir">Dirección</label><input id="cDir"></div></div>
      <div class="row"><div class="f"><label for="cPais">País</label><select id="cPais"></select></div>
        <div class="f"><label for="cCP">Código postal</label><input id="cCP" placeholder="CP"><div class="ac" hidden></div></div></div>
      <div class="row"><div class="f"><label for="cPob">Población</label><input id="cPob" placeholder="Escribe la población"><div class="ac" hidden></div></div><div class="f"><label for="cProv">Provincia / región</label><input id="cProv"></div></div>
      <div class="row"><div class="f"><label for="cTel">Teléfono de contacto</label><input id="cTel" type="tel"></div><div class="f"><label for="cMail">Email</label><input id="cMail" type="email"></div></div>
      <p class="hint" id="cIvaHint" style="margin:10px 0 0"></p>
      <div class="alert warn" id="cErr" hidden></div>
    </form>
    <div class="mf"><button class="btn" type="button" data-x>Cancelar</button><button class="btn primary" type="button" id="cSave">Guardar cliente</button></div>
  </div></div>`;
  fillPaises($("#cPais"),c.pais||"ES");
  const f={nombre:"#cNom",cif:"#cCif",dir:"#cDir",cp:"#cCP",pob:"#cPob",prov:"#cProv",tel:"#cTel",email:"#cMail"};
  for(const k in f)$(f[k]).value=c[k]||"";
  const hint=()=>{$("#cIvaHint").textContent=$("#cPais").value==="ES"?"Cliente de España: se aplicará IVA 21 %.":"Cliente fuera de España: se aplicará IVA 0 %."};hint();
  $("#cPais").addEventListener("change",hint);
  $("#cCif").addEventListener("change",()=>{const v=U($("#cCif").value);const m=v.match(/^([A-Z]{2})\d/);if(m&&PAIS_NOM[m[1]]&&m[1]!=="ES"){$("#cPais").value=m[1];hint()}});
  wirePlace("c",hint);
  const close=()=>{root.innerHTML=""};
  root.querySelectorAll("[data-x]").forEach(b=>b.addEventListener("click",close));
  $("#cNom").focus();
  $("#cSave").addEventListener("click",async()=>{
    const d={};for(const k in f)d[k]=k==="email"?L($(f[k]).value):U($(f[k]).value);
    d.pais=$("#cPais").value;
    const err=$("#cErr");
    if(!d.nombre||!d.cif){err.hidden=false;err.textContent="Nombre y CIF/NIF son obligatorios.";return}
    const dup=CLIENTES.find(x=>norm(x.cif)===norm(d.cif)&&x.id!==c.id);
    if(dup){err.hidden=false;err.textContent="Ya existe un cliente con ese CIF: "+dup.nombre+".";return}
    const id=c.id||("c"+Date.now().toString(36)+Math.random().toString(36).slice(2,6));
    const doc=Object.assign({},d,{creadoEn:c.creadoEn||new Date().toISOString(),creadoPor:c.creadoPor||Me.id||null});
    try{await Store.set("clientes",id,doc);close();toast("Cliente guardado");if(onSaved)onSaved(Object.assign({id},doc))}
    catch(e){err.hidden=false;err.textContent="No se pudo guardar: "+(e.message||e.code)}
  });
}
function drawClientes(){
  const q=norm($("#cTxt").value);
  const list=CLIENTES.filter(c=>!q||norm([c.nombre,c.cif,c.pob,c.prov,c.email,c.tel].join(" ")).includes(q)).sort((a,b)=>(a.nombre||"").localeCompare(b.nombre||"","es"));
  const w=$("#cliWrap");
  if(!CLIENTES.length){w.innerHTML=`<div class="empty-state"><b>Todavía no hay clientes</b>Crea el primero con «+ Nuevo cliente». Quedará disponible para todo el equipo.</div>`;return}
  const count={};PRES.forEach(p=>{if(p.clienteId)count[p.clienteId]=(count[p.clienteId]||0)+1});
  w.innerHTML=`<table class="data"><thead><tr><th>Cliente</th><th>CIF/NIF</th><th>Dirección</th><th>Población</th><th>Provincia</th><th>País</th><th>Teléfono</th><th>Email</th><th>IVA</th><th class="r">Presup.</th><th></th></tr></thead><tbody>${
    list.map(c=>`<tr><td class="wrapcell"><b>${esc(c.nombre)}</b></td><td>${esc(c.cif)}</td><td class="wrapcell">${esc(c.dir)}</td><td>${esc(c.cp)} ${esc(c.pob)}</td><td>${esc(c.prov)}</td><td>${esc(paisNombre(c.pais))}</td><td>${esc(c.tel)}</td><td>${esc(c.email)}</td><td>${(c.pais||"ES")==="ES"?"21 %":"0 %"}</td><td class="r">${count[c.id]||0}</td>
    <td><div class="actions"><button class="btn small" data-new="${esc(c.id)}">Presupuestar</button><button class="btn small ghost" data-edit="${esc(c.id)}">Editar</button></div></td></tr>`).join("")}</tbody></table>`;
  w.querySelectorAll("[data-edit]").forEach(b=>b.addEventListener("click",()=>clientModal(CLIENTES.find(c=>c.id===b.dataset.edit))));
  w.querySelectorAll("[data-new]").forEach(b=>b.addEventListener("click",()=>{resetForm(true);setCliente(CLIENTES.find(c=>c.id===b.dataset.new));location.hash="nuevo"}));
}

/* ===================== PARRILLA ===================== */
function filtered(){
  const q=norm($("#qTxt").value),d1=$("#qDesde").value,d2=$("#qHasta").value,dl=$("#qDeleg").value,st=$("#qEstado").value;
  return PRES.filter(p=>(!d1||p.fecha>=d1)&&(!d2||p.fecha<=d2)&&(!dl||p.serie===dl)&&(!st||p.estado===st)&&
    (!q||norm([p.codigo,p.cliente&&p.cliente.nombre,p.cliente&&p.cliente.cif,p.origen&&p.origen.pob,p.destino&&p.destino.pob,p.mercancia].join(" ")).includes(q)))
    .sort((a,b)=>(b.fecha||"").localeCompare(a.fecha||"")||(b.creadoEn||"").localeCompare(a.creadoEn||""));
}
async function drawGrid(){
  const list=filtered(),w=$("#gridWrap");
  const sum=list.reduce((s,p)=>{s.base+=p.base||0;s.total+=p.total||0;s.kg+=p.kgFact||0;if(p.estado==="Aceptado")s.ok++;return s},{base:0,total:0,kg:0,ok:0});
  $("#sumBox").innerHTML=`<div class="metric"><span>Presupuestos</span><b>${num(list.length)}</b></div><div class="metric"><span>Aceptados</span><b>${num(sum.ok)}${list.length?` <small style="font-size:12px;color:var(--muted)">${num(sum.ok/list.length*100)} %</small>`:""}</b></div><div class="metric"><span>Kg facturables</span><b>${num(sum.kg)}</b></div><div class="metric key"><span>Base imponible</span><b>${eur(sum.base)}</b></div><div class="metric"><span>Total con IVA</span><b>${eur(sum.total)}</b></div>`;
  if(!PRES.length){w.innerHTML=`<div class="empty-state"><b>Aún no hay presupuestos guardados</b>Crea el primero en «Nuevo presupuesto». Aquí aparecerán todos con su número, cliente, recorrido e importe.</div>`;return}
  if(!list.length){w.innerHTML=`<div class="empty-state"><b>Ningún presupuesto coincide</b>Cambia el rango de fechas o los filtros.</div>`;return}
  const names=await userNames(list.map(p=>p.creadoPor));
  w.innerHTML=`<table class="data compact"><thead><tr><th>Nº</th><th>Fecha</th><th>Cliente</th><th>Recorrido</th><th class="r">Bultos</th><th class="r">Peso</th><th class="r">PVKG</th><th class="r">Kg / pal.</th><th class="r">Porte</th><th class="r">Comb.</th><th class="r">IVA</th><th class="r">Total</th><th>Estado</th><th>Motivo</th><th>Usuario</th><th></th></tr></thead><tbody>${
    list.map(p=>`<tr><td><span class="num">${esc(p.codigo)}</span>${p.enviadoEn?`<span class="pill Enviado" title="${esc(textoEnvio(p))}">Enviado</span>`:""}${p.proforma?`<span class="pfc" title="Factura proforma">${esc(p.proforma.codigo)}</span>`:""}</td><td>${fmtDate(p.fecha)}</td>
    <td class="wrapcell cli"><b>${esc(p.cliente.nombre)}</b><br><span class="hint">${esc(p.cliente.cif)}</span></td>
    <td class="wrapcell rec">${esc(p.origen.pob)}${p.origen.pais!=="ES"?" <span class=\"hint\">"+esc(p.origen.pais)+"</span>":""} → ${esc(p.destino.pob)}${p.destino.pais!=="ES"?" <span class=\"hint\">"+esc(p.destino.pais)+"</span>":""}</td>
    <td class="r">${num(p.numBultos)}</td><td class="r">${num(p.peso)}</td><td class="r">${num(p.pvkg)}</td><td class="r"><b>${p.modo==="PALLETS"?num(p.numPallets)+" pal.":num(p.kgFact)}</b></td>
    <td class="r">${eur((p.porte||0)+(p.suplNoEur||0)+(p.recargo||0))}</td><td class="r">${eur(p.combustible)}</td><td class="r">${eur(p.iva)}</td><td class="r tot">${eur(p.total)}</td>
    <td><button class="pill ${esc(p.estado)}" data-st="${esc(p.id)}" title="Cambiar estado">${esc(p.estado)}</button></td>
    <td class="wrapcell mot">${p.estado==="Rechazado"?`<button data-mot="${esc(p.id)}" title="Cambiar motivo">${esc(p.motivoRechazo||"Indicar motivo")}</button>`:""}</td>
    <td class="wrapcell">${esc(names[p.creadoPor]||p.creadoPorNombre||"—")}</td>
    <td><div class="acts"><button class="btn small" data-pdf="${esc(p.id)}" title="PDF del presupuesto">PDF</button><button class="btn small" data-mail="${esc(p.id)}" title="${p.enviadoEn?"Volver a enviar el PDF por email":"Enviar el PDF por email"}">${p.enviadoEn?"Reenviar":"Enviar"}</button><button class="btn small gold" data-pf="${esc(p.id)}" title="${p.proforma?"Descargar factura proforma "+esc(p.proforma.codigo):"Crear factura proforma"}">Proforma</button><button class="btn small ghost danger" data-del="${esc(p.id)}" aria-label="Eliminar">✕</button><button class="btn small ghost" data-ed="${esc(p.id)}">Editar</button><button class="btn small ghost" data-cp="${esc(p.id)}">Duplicar</button></div></td></tr>`).join("")
  }</tbody><tfoot><tr><td colspan="7">${num(list.length)} presupuestos</td><td class="r">${num(sum.kg)}</td><td colspan="3"></td><td class="r">${eur(sum.total)}</td><td colspan="4"></td></tr></tfoot></table>`;
  const byId=id=>PRES.find(p=>p.id===id);
  w.querySelectorAll("[data-pdf]").forEach(b=>b.addEventListener("click",()=>downloadPdf(byId(b.dataset.pdf))));
  w.querySelectorAll("[data-mail]").forEach(b=>b.addEventListener("click",()=>enviarDesdeLista(byId(b.dataset.mail))));
  w.querySelectorAll("[data-pf]").forEach(b=>b.addEventListener("click",()=>proformaFor(byId(b.dataset.pf))));
  w.querySelectorAll("[data-ed]").forEach(b=>b.addEventListener("click",()=>loadIntoForm(byId(b.dataset.ed),false)));
  w.querySelectorAll("[data-cp]").forEach(b=>b.addEventListener("click",()=>loadIntoForm(byId(b.dataset.cp),true)));
  w.querySelectorAll("[data-st]").forEach(b=>b.addEventListener("click",async()=>{const p=byId(b.dataset.st);const order=["Pendiente","Aceptado","Rechazado"];const d=Object.assign({},p);delete d.id;d.estado=order[(order.indexOf(p.estado)+1)%3];
    const save=async()=>{try{await Store.set("presupuestos",p.id,d)}catch(e){toast("No se pudo cambiar el estado")}};
    if(d.estado==="Rechazado")rejectModal(p.codigo,p.motivoRechazo,m=>{d.motivoRechazo=m;save()});else{d.motivoRechazo="";save()}}));
  w.querySelectorAll("[data-mot]").forEach(b=>b.addEventListener("click",()=>{const p=byId(b.dataset.mot);rejectModal(p.codigo,p.motivoRechazo,async m=>{const d=Object.assign({},p);delete d.id;d.motivoRechazo=m;try{await Store.set("presupuestos",p.id,d)}catch(e){toast("No se pudo guardar el motivo")}})}));
  w.querySelectorAll("[data-del]").forEach(b=>b.addEventListener("click",()=>confirmModal("¿Eliminar el presupuesto "+byId(b.dataset.del).codigo+"?","Se borrará para todo el equipo. El número no se reutiliza.","Eliminar",async()=>{await Store.del("presupuestos",b.dataset.del);toast("Presupuesto eliminado")})));
}
function rejectModal(codigo,current,onOk,onCancel){
  const root=$("#modalRoot");
  const cur=current||"";const base=MOTIVOS.find(m=>cur===m||cur.startsWith(m+":"))||"";
  root.innerHTML=`<div class="modal" role="dialog" aria-modal="true" aria-labelledby="rjT"><div class="box narrow"><div class="mh"><h3 id="rjT">Motivo del rechazo</h3></div>
    <div class="mb"><p class="hint" style="margin:0 0 10px">Presupuesto ${esc(codigo)}. El motivo queda registrado en la parrilla y en el Excel.</p>
    <div style="display:flex;flex-direction:column;gap:6px">${MOTIVOS.map((m,i)=>`<label style="display:flex;gap:8px;align-items:center;font-weight:600;font-size:13px;cursor:pointer"><input type="radio" name="rjM" value="${esc(m)}" style="width:auto" ${m===base?"checked":""}> ${esc(m)}</label>`).join("")}</div>
    <div class="f" style="margin-top:10px"><label for="rjTxt">Detalle (obligatorio en OTROS)</label><input id="rjTxt"></div>
    <div class="alert warn" id="rjErr" hidden></div></div>
    <div class="mf"><button class="btn" type="button" data-x>Cancelar</button><button class="btn primary" type="button" id="rjOk">Marcar como rechazado</button></div></div></div>`;
  if(cur.includes(": "))$("#rjTxt").value=cur.split(": ").slice(1).join(": ");
  root.querySelector("[data-x]").addEventListener("click",()=>{root.innerHTML="";onCancel&&onCancel()});
  $("#rjOk").addEventListener("click",()=>{
    const sel=root.querySelector("input[name=rjM]:checked");const txt=U($("#rjTxt").value);const err=$("#rjErr");
    if(!sel){err.hidden=false;err.textContent="Elige un motivo.";return}
    if(sel.value==="OTROS"&&!txt){err.hidden=false;err.textContent="Escribe el detalle del motivo.";return}
    root.innerHTML="";onOk(sel.value+(txt?": "+txt:""));
  });
}
function confirmModal(title,text,okLabel,onOk){
  const root=$("#modalRoot");
  root.innerHTML=`<div class="modal" role="dialog" aria-modal="true"><div class="box narrow"><div class="mh"><h3></h3></div><div class="mb"><p style="margin:0"></p></div><div class="mf"><button class="btn" data-x type="button">Cancelar</button><button class="btn primary" id="okB" type="button"></button></div></div></div>`;
  root.querySelector("h3").textContent=title;root.querySelector("p").textContent=text;$("#okB").textContent=okLabel;
  root.querySelector("[data-x]").addEventListener("click",()=>root.innerHTML="");
  $("#okB").addEventListener("click",async()=>{root.innerHTML="";try{await onOk()}catch(e){toast("No se pudo completar: "+(e.message||e.code))}});
}

/* ===================== DESCARGAS ===================== */
async function saveFile(filename,blob){
  try{const dl=window.claude&&window.claude.use?await window.claude.use("downloads"):null;
    if(dl){await dl.save({filename,data:blob});return}
  }catch(e){if(e&&e.code==="declined")return;if(e&&e.code&&e.code!=="unavailable"&&e.code!=="not_granted"){toast("No se pudo descargar: "+e.message);return}}
  try{const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=filename;document.body.append(a);a.click();a.remove()}catch(e){toast("La descarga no está disponible en esta vista")}
}
let logoData=null;
async function getLogo(){if(logoData)return logoData;try{if(window.LOGO_URI){logoData=window.LOGO_URI;return logoData}const b=await (await fetch("/static/logo.png")).blob();logoData=await new Promise(r=>{const fr=new FileReader();fr.onload=()=>r(fr.result);fr.readAsDataURL(b)})}catch(e){logoData=null}return logoData}

/* ===================== PDF (una hoja) ===================== */
const PDFMAP={"Ł":"L","ł":"l","Đ":"D","đ":"d","ı":"i","Ş":"S","ş":"s","Ș":"S","ș":"s","Ț":"T","ț":"t","Ő":"Ö","ő":"ö","Ű":"Ü","ű":"ü","€":"€","–":"-","—":"-","→":">"};
const T=s=>String(s==null?"":s).normalize("NFC").replace(/[^\x00-\xFF]/g,ch=>{if(PDFMAP[ch])return PDFMAP[ch];const b=ch.normalize("NFD").replace(/\p{M}/gu,"");return /^[\x00-\xFF]+$/.test(b)?b:"?"});
function drawPdf(doc,p,logo,usuario,opts){
  const W=210,M=15,GOLD=[227,155,18],INK=[22,24,29],GREY=[95,100,110],ASPH=[29,32,38],LIGHT=[246,246,248],RED=[194,31,31],SOFT=[252,241,220];
  const G=opts.gap||0,pf=opts.pf||null;
  const intl=[p.origen&&p.origen.pais,p.destino&&p.destino.pais].some(c=>c&&c!=="ES"&&c!=="PT");
  const tx=(s,x,y,o)=>doc.text(T(s),x,y,o);
  const split=(s,w)=>doc.splitTextToSize(T(s),w);
  const font=(st,sz,col)=>{doc.setFont("helvetica",st);doc.setFontSize(sz);doc.setTextColor(...col)};
  // Cabecera
  if(logo)doc.addImage(logo,"JPEG",M,10,50,50*235/811);
  font("bold",17,INK);tx(pf?"FACTURA PROFORMA":"PRESUPUESTO",W-M,16,{align:"right"});
  const code=pf?pf.codigo:p.codigo;
  font("bold",10.5,INK);const cw=doc.getTextWidth(T(code));tx(code,W-M,22,{align:"right"});font("normal",8.5,GREY);tx("Nº",W-M-cw-1.5,22,{align:"right"});
  font("normal",7.8,GREY);
  if(pf){tx("Fecha: "+fmtDate(pf.fecha)+"  ·  Ref. presupuesto: "+p.codigo,W-M,26.5,{align:"right"})}
  else tx("Fecha: "+fmtDate(p.fecha)+"  ·  Validez: 15 días",W-M,26.5,{align:"right"});
  tx("Delegación: "+p.delegacion,W-M,30.2,{align:"right"});
  doc.setDrawColor(...GOLD);doc.setLineWidth(.9);doc.line(M,33.5,W-M,33.5);doc.setDrawColor(...INK);doc.setLineWidth(.3);doc.line(M,34.6,W-M,34.6);
  // Emisor / cliente
  let y=40.5;
  const block=(x,w,title,lines)=>{font("bold",6.5,GOLD);tx(title,x,y);let yy=y+4.3;
    lines.forEach((l,i)=>{if(!l)return;font(i===0?"bold":"normal",i===0?9.2:7.6,i===0?INK:GREY);const t=split(l,w);doc.text(t,x,yy);yy+=t.length*(i===0?4:3.3)});return yy};
  const y1=block(M,78,"EMISOR",[EMPRESA.nombre,EMPRESA.dir,EMPRESA.cpPob,"CIF: "+EMPRESA.cif]);
  const c=p.cliente;
  doc.setFillColor(...LIGHT);doc.roundedRect(104,y-4,W-M-104+2,25.5,1.5,1.5,"F");
  const y2=block(108,W-M-112,"CLIENTE",[c.nombre,"CIF/NIF: "+c.cif,c.dir,[c.cp,c.pob].filter(Boolean).join(" ")+(c.prov?" ("+c.prov+")":"")+(c.pais&&c.pais!=="ES"?" · "+U(paisNombre(c.pais)):""),[c.tel?"TEL. "+c.tel:"",c.email].filter(Boolean).join("  ·  ")]);
  y=Math.max(y1,y2,y+21.5)+3+G;
  const band=t=>{doc.setFillColor(...ASPH);doc.rect(M,y,W-2*M,5.8,"F");font("bold",7.8,[255,255,255]);tx(t,M+2.5,y+4);y+=5.8};
  band("DATOS DEL SERVICIO");
  const half=(W-2*M-10)/2;
  doc.setDrawColor(220,223,228);doc.setLineWidth(.25);doc.rect(M,y,half,13.5);doc.rect(M+half+10,y,half,13.5);
  const place=(x,lab,pl)=>{font("bold",6.2,GREY);tx(lab,x+2.5,y+3.8);font("bold",9.8,INK);tx(split(pl.pob||"",half-5)[0]||"",x+2.5,y+8.3);font("normal",7.4,GREY);tx((pl.cp||"")+"  "+(pl.prov||"")+(pl.pais&&pl.pais!=="ES"?" · "+U(paisNombre(pl.pais)):""),x+2.5,y+11.8)};
  place(M,"ORIGEN",p.origen);place(M+half+10,"DESTINO",p.destino);
  if(intl){font("bold",6.4,RED);tx("CONSULTAR TRÁNSITO INTERNACIONAL",W-M-2.5,y+3.8,{align:"right"})}
  font("bold",13,GOLD);tx(">",M+half+5,y+8.8,{align:"center"});
  y+=16;
  doc.autoTable({startY:y,margin:{left:M,right:M},theme:"plain",
    head:[["Tipo","Cantidad","Largo (m)","Ancho (m)","Alto (m)","Peso ud. (kg)","Peso (kg)","Volumen (m³)"]],
    body:(p.bultos||[]).map(b=>[U(b.tipo)+(p.modo==="PALLETS"?(isNoEur(b)?" USA":" EUR"):""),num(b.cant),num(b.l,2),num(b.a,2),num(b.h,2),b.kg?num(b.kg,b.kg%1?1:0):"-",b.kg?num(b.cant*b.kg,(b.cant*b.kg)%1?1:0):"-",num(b.cant*b.l*b.a*b.h,3)]),
    styles:{fontSize:7.6,cellPadding:{top:1.1,bottom:1.1,left:2,right:2},textColor:INK,halign:"center"},headStyles:{fillColor:[252,241,220],textColor:[110,72,6],fontStyle:"bold",fontSize:6.8,halign:"center"},
    alternateRowStyles:{fillColor:LIGHT}});
  y=doc.lastAutoTable.finalY+2.5;
  const pal=p.modo==="PALLETS";
  const mets=[[pal?"PALLETS":"BULTOS",num(pal?p.numPallets:p.numBultos)],["PESO REAL",num(p.peso)+" kg"],["VOLUMEN",num(p.volumen,3)+" m³"],["PVKG (m³×250)",num(p.pvkg)+" kg"],pal?["ENVÍO","PALETIZADO"]:["KG FACTURABLES",num(p.kgFact)+" kg"]];
  const mw=(W-2*M-4*2.5)/5;
  mets.forEach((m,i)=>{const x=M+i*(mw+2.5),key=i===4,cx=x+mw/2;doc.setFillColor(...(key?[252,241,220]:LIGHT));doc.rect(x,y,mw,9.5,"F");if(key){doc.setFillColor(...GOLD);doc.rect(x,y,.9,9.5,"F")}
    font("bold",5.8,GREY);tx(m[0],cx,y+3.5,{align:"center"});font("bold",8.8,INK);tx(m[1],cx,y+7.8,{align:"center"})});
  y+=12;
  if(p.mercancia){font("normal",7.4,GREY);const t=split("MERCANCÍA: "+p.mercancia,W-2*M);doc.text(t,M,y);y+=t.length*3.2+1.5}
  y+=1+G;band("IMPORTE DEL SERVICIO");
  const rows=[["PORTE "+p.origen.pob+" - "+p.destino.pob,eur(p.porte)]];
  if(p.suplNoEur)rows.push(["Suplemento pallets USA",eur(p.suplNoEur)]);
  if(p.recargo)rows.push(["Recargo entrega Badajoz/Cáceres ("+(p.recargoDetalle||(num(p.kgFact)+" kg × 0,05 €"))+")",eur(p.recargo)]);
  rows.push(["Recargo combustible ("+num(p.combPct,2)+" %)",eur(p.combustible)]);
  rows.push([{content:"Base imponible",styles:{fontStyle:"bold"}},{content:eur(p.base),styles:{fontStyle:"bold"}}]);
  rows.push(["IVA "+p.ivaPct+" %",eur(p.iva)]);
  doc.autoTable({startY:y,margin:{left:M,right:M},theme:"plain",body:rows.map(r=>r.map(x=>typeof x==="string"?T(x):Object.assign({},x,{content:T(x.content)}))),
    styles:{fontSize:8.2,cellPadding:{top:1.6,bottom:1.6,left:2.5,right:2.5},textColor:INK},columnStyles:{1:{halign:"right",cellWidth:34}},
    didDrawCell:d=>{if(d.section==="body"){doc.setDrawColor(225,227,231);doc.setLineWidth(.15);doc.line(d.cell.x,d.cell.y+d.cell.height,d.cell.x+d.cell.width,d.cell.y+d.cell.height)}}});
  y=doc.lastAutoTable.finalY;
  doc.setFillColor(...GOLD);doc.rect(M,y,W-2*M,9,"F");font("bold",9,[26,18,5]);tx("TOTAL A PAGAR",M+2.5,y+6);doc.setFontSize(12.5);tx(eur(p.total),W-M-2.5,y+6.3,{align:"right"});
  y+=12.5;
  if(p.observaciones){font("bold",7.4,INK);tx("OBSERVACIONES",M,y);y+=3.4;font("normal",7.4,GREY);const t=split(p.observaciones,W-2*M);doc.text(t,M,y);y+=t.length*3.2+2.5}
  // Mensaje comercial
  y+=G;
  {const bx=M,bw2=W-2*M;font("normal",7.6,GREY);
   const msg=split(pf?"Le adjuntamos la factura proforma de su servicio. En cuanto recibamos el pago pondremos en marcha el envío y le mantendremos informado. Quedamos a su entera disposición para cualquier consulta. Será un placer ocuparnos de su mercancía.":"Esperamos que este presupuesto sea de su agrado. Lo hemos preparado a la medida de su envío y quedamos a su entera disposición para resolver cualquier duda o ajustar lo que necesite. Será un placer ocuparnos de su mercancía.",bw2-10);
   const h=9.5+msg.length*3.3+(usuario?4.2:0);
   doc.setFillColor(...SOFT);doc.roundedRect(bx,y,bw2,h,1.5,1.5,"F");doc.setFillColor(...GOLD);doc.rect(bx,y,1.2,h,"F");
   font("bold",10,INK);tx("Gracias por confiar en Alditraex",bx+5,y+5.6);
   font("normal",7.6,[70,74,82]);doc.text(msg,bx+5,y+9.8);
   if(usuario){font("italic",7.4,GREY);tx("Atentamente, "+usuario+" · Alditraex "+(DELEG[p.serie]?DELEG[p.serie].nombre:p.delegacion||""),bx+5,y+9.8+msg.length*3.3+1.2)}
   y+=h+3;}
  // Compromiso de servicio
  if(opts.strip!==false){
    const tiles=[intl?["Consultar","Tránsito internacional: plazo según país de destino"]:["24-72 h","Plazo de entrega tipo, según el servicio contratado"],["97 %","De nuestros envíos se entregan en plazo"],["ESP · PT · EUR","Cobertura peninsular, Baleares, Canarias y Europa"],["Trato directo","Atención personalizada desde su delegación"]];
    const tw=(W-2*M-3*2.5)/4,th=13;
    tiles.forEach((t,i)=>{const x=M+i*(tw+2.5);doc.setFillColor(...ASPH);doc.roundedRect(x,y,tw,th,1.2,1.2,"F");
      font("bold",i===3||i===2||(intl&&i===0)?10:12,GOLD);tx(t[0],x+tw/2,y+5.6,{align:"center"});
      font("normal",6,[205,209,216]);const l=split(t[1],tw-5);doc.text(l,x+tw/2,y+8.9,{align:"center"})});
    y+=th+3;
  }
  // Pago y factura
  y+=G;
  const bw=(W-2*M-5)/2,bh=22;
  doc.setFillColor(...ASPH);doc.roundedRect(M,y,bw,bh,1.5,1.5,"F");
  font("bold",6.5,GOLD);tx("FORMA DE PAGO · TRANSFERENCIA",M+3.5,y+4.6);
  font("bold",10.5,[255,255,255]);tx(EMPRESA.iban,M+3.5,y+10);
  font("normal",6.4,[205,209,216]);doc.text(split(pf?"Realice el ingreso indicando en el concepto el Nº "+pf.codigo+" y envíenos copia de la transferencia para poner en marcha el servicio.":"Si está de acuerdo con la cotización, realice el ingreso indicando el Nº "+p.codigo+" y adjunte copia de la transferencia a este email para poner en marcha el servicio.",bw-7),M+3.5,y+13.6);
  const x2=M+bw+5;doc.setDrawColor(...GOLD);doc.setLineWidth(.5);doc.roundedRect(x2,y,bw,bh,1.5,1.5,"S");
  if(pf){font("bold",6.5,GOLD);tx("DOCUMENTO PROFORMA",x2+3.5,y+4.6);
    font("normal",7,INK);doc.text(split("Este documento no tiene validez fiscal como factura. La factura definitiva se emitirá una vez realizado el servicio. Consultas:",bw-7),x2+3.5,y+8.6);
    font("bold",9.5,INK);tx(EMPRESA.admin,x2+3.5,y+18.4)}
  else{font("bold",6.5,GOLD);tx("¿NECESITA FACTURA?",x2+3.5,y+4.6);
  font("normal",7.6,INK);tx("Para solicitar la factura en firme escriba a",x2+3.5,y+9);
  font("bold",9.5,INK);tx(EMPRESA.admin,x2+3.5,y+13.2);
  font("normal",7,GREY);tx("indicando el Nº de presupuesto: "+p.codigo,x2+3.5,y+17)}
  y+=bh+5+G;
  // Condiciones (letra pequeña)
  const cond=[pf?"PROFORMA EMITIDA SEGÚN EL PRESUPUESTO "+p.codigo+". VALIDEZ: 15 DÍAS.":"VALIDEZ DEL PRESUPUESTO: 15 DÍAS DESDE SU COMUNICACIÓN.",
    intl?"PLAZOS DE ENTREGA: CONSULTAR TRÁNSITO INTERNACIONAL. El plazo depende del país de origen y destino; el servicio de Alditraex no es un servicio de entrega garantizada y los plazos son orientativos, sin que se garantice una fecha u hora concreta de entrega.":"PLAZOS DE ENTREGA: el servicio de Alditraex no es un servicio de entrega garantizada. Nuestro plazo de entrega tipo es de 24 a 72 h según el tipo de servicio contratado, y lo cumplimos en el 97 % de las ocasiones; los plazos son orientativos y no se garantiza una fecha u hora concreta de entrega.",
    "La mercancía debe estar perfectamente embalada y paletizada para ser transportada en nuestra red.",
    "Esta mercancía transportada no está cubierta por nuestro seguro. Cualquier avería, daño o pérdida que surja en estas tipologías o similares, en caso de aceptación del servicio, no será admitida como reclamación por parte de Alditraex.",
    "No entramos en fincas: nuestras entregas y recogidas son puerta a puerta.",
    "Si el bulto, una vez recibido en nuestro almacén, difiere de las medidas y pesos indicados en la petición del servicio, primarán las medidas y pesos tomados en nuestras instalaciones para el precio del servicio a pagar."];
  font("bold",6.8,INK);tx(pf?"CONDICIONES DEL SERVICIO":"CONDICIONES DEL PRESUPUESTO",M,y);doc.setDrawColor(...GOLD);doc.setLineWidth(.4);doc.line(M,y+1.3,M+22,y+1.3);y+=4.3;
  cond.forEach((t,i)=>{font(i===0?"bold":"normal",6.1,[70,74,82]);const lines=split(t,W-2*M-4);doc.setFillColor(...(i===3?RED:GOLD));doc.rect(M,y-1.7,1.1,1.1,"F");doc.text(lines,M+3.2,y);y+=lines.length*2.55+0.6});
  const priv="Política de privacidad. Sus datos personales serán usados para nuestra relación y poder prestarle nuestros servicios. Dichos datos son necesarios para poder relacionarnos con usted, lo que nos permite el uso de su información dentro de la legalidad. Asimismo, podrán tener conocimiento de su información aquellas entidades que necesiten tener acceso a la misma para que podamos prestarle nuestros servicios. Conservaremos sus datos durante nuestra relación y mientras nos obliguen las leyes aplicables. En cualquier momento puede dirigirse a nosotros para saber qué información tenemos sobre usted, rectificarla si fuese incorrecta y eliminarla una vez finalizada nuestra relación. También tiene derecho a solicitar el traspaso de su información a otra entidad (portabilidad). Para solicitar alguno de estos derechos, deberá realizar una solicitud escrita a nuestra dirección, junto con una fotocopia de su DNI: C/ Cádiz, 15, Pol. Ind. El Prado, CP 06800, Mérida (Badajoz). En caso de que entienda que sus derechos han sido desatendidos, puede formular una reclamación en la Agencia Española de Protección de Datos (www.aepd.es).";
  font("normal",5.1,[135,140,148]);const pl=split(priv,W-2*M);y+=1.8+G;
  if(y+pl.length*2.05>284){doc.addPage();y=16}
  doc.text(pl,M,y);const endY=(doc.getNumberOfPages()-1)*1000+y+pl.length*2.05;
  const pages=doc.getNumberOfPages();
  for(let i=1;i<=pages;i++){doc.setPage(i);doc.setDrawColor(...GOLD);doc.setLineWidth(.4);doc.line(M,287.5,W-M,287.5);font("normal",6.3,GREY);
    tx(EMPRESA.nombre+" · "+EMPRESA.dir+" · "+EMPRESA.cpPob+" · CIF "+EMPRESA.cif,M,291.5);
    tx((pf?"Proforma "+pf.codigo+" · Presupuesto ":"Presupuesto ")+p.codigo+(usuario?" · Atendido por "+usuario:"")+(pages>1?" · Pág. "+i+"/"+pages:""),W-M,291.5,{align:"right"})}
  return endY;
}
function pedirEmailEnvio(p,actual,onOk){
  const root=$("#modalRoot");
  root.innerHTML=`<div class="modal" role="dialog" aria-modal="true" aria-labelledby="emT"><div class="box narrow"><div class="mh"><h3 id="emT">Enviar presupuesto</h3><button class="btn ghost" type="button" data-x aria-label="Cerrar">✕</button></div>
    <div class="mb"><p class="hint" style="margin:0 0 10px">Presupuesto ${esc(p.codigo)}. El PDF se envía a este correo.</p>
    <div class="f"><label for="emMail">Email donde enviar presupuesto</label><input id="emMail" type="email" autocomplete="off"></div>
    <div class="alert warn" id="emErr" hidden></div></div>
    <div class="mf"><button class="btn" type="button" data-x>Cancelar</button><button class="btn primary" type="button" id="emOk">Enviar</button></div></div></div>`;
  $("#emMail").value=actual||"";$("#emMail").focus();
  const close=()=>{root.innerHTML=""};
  root.querySelectorAll("[data-x]").forEach(b=>b.addEventListener("click",close));
  $("#emOk").addEventListener("click",()=>{
    const mail=L($("#emMail").value);
    if(!mail.includes("@")){$("#emErr").hidden=false;$("#emErr").textContent="Indica un email válido.";return}
    close();onOk(mail);
  });
}
function textoEnvio(p){
  const d=new Date(p.enviadoEn);
  const cuando=isNaN(d)?fmtDate(String(p.enviadoEn||"").slice(0,10)):d.toLocaleString("es-ES",{day:"2-digit",month:"2-digit",year:"numeric",hour:"2-digit",minute:"2-digit"});
  return "Enviado a "+(p.enviadoA||"")+" el "+cuando;
}
async function guardarEnvio(p){
  const d=Object.assign({},p);delete d.id;
  d.enviadoEn=new Date().toISOString();d.enviadoA=p.emailEnvio||"";
  await Store.set("presupuestos",p.id,d);
}
async function enviarDesdeLista(p){
  if(!p)return;
  const mail=L(p.emailEnvio||"");
  const lanzar=async doc=>{
    try{if(await downloadPdf(doc,null,{enviar:true,descargar:false}))await guardarEnvio(doc)}
    catch(e){toast("No se pudo enviar el email")}
  };
  if(mail.includes("@")){await lanzar(p);return}
  pedirEmailEnvio(p,(p.cliente&&p.cliente.email)||"",async mail2=>{
    const d=Object.assign({id:p.id},p);d.emailEnvio=mail2;
    const guardado=Object.assign({},d);delete guardado.id;
    try{await Store.set("presupuestos",p.id,guardado);await lanzar(d)}
    catch(e){toast("No se pudo enviar el email")}
  });
}
async function downloadPdf(p,pf,opts){
  if(opts===true)opts={enviar:true};
  opts=opts||{};
  const enviar=!!opts.enviar,descargar=opts.descargar!==false;
  if(!window.jspdf){toast("No se pudo cargar el generador de PDF");return}
  const {jsPDF}=window.jspdf;
  const logo=await getLogo();
  const names=await userNames([p.creadoPor]);const usuario=names[p.creadoPor]||p.creadoPorNombre||"";
  // Dos pasadas: se mide el contenido y el hueco libre se reparte entre secciones para llenar la hoja A4
  const LIMIT=284,SLOTS=6;
  let dibujo={gap:0,strip:true,pf:pf||null};
  let end=drawPdf(new jsPDF({unit:"mm",format:"a4"}),p,logo,usuario,dibujo);
  if(end>LIMIT){dibujo.strip=false;end=drawPdf(new jsPDF({unit:"mm",format:"a4"}),p,logo,usuario,dibujo)}
  if(end<LIMIT)dibujo.gap=Math.min(7,(LIMIT-end-0.5)/SLOTS);
  const doc=new jsPDF({unit:"mm",format:"a4"});
  drawPdf(doc,p,logo,usuario,dibujo);
  const fname=(pf?"Proforma_"+pf.codigo.replace("/","-"):"Presupuesto_"+p.codigo.replace("/","-"))+"_"+(p.cliente.nombre||"").replace(/[^\p{L}\p{N}]+/gu,"_").slice(0,40)+".pdf";
  const blob=doc.output("blob");
  if(descargar)await saveFile(fname,blob);
  let enviado=false;
  if(enviar&&!pf&&p.emailEnvio){
    try{
      const fd=new FormData();
      fd.append("email",p.emailEnvio);fd.append("codigo",p.codigo||"");fd.append("serie",p.serie||"");fd.append("archivo",blob,fname);
      const res=await fetch("/api/presupuestos2/enviar",{method:"POST",body:fd});
      const data=await res.json();
      enviado=!!data.ok;
      toast(data.ok?(data.aviso||("Presupuesto enviado a "+p.emailEnvio+(data.copia&&data.copia!==p.emailEnvio?" (copia a "+data.copia+")":""))):(data.error||"No se pudo enviar el email"));
    }catch(e){toast("No se pudo enviar el email")}
  }
  return enviado;
}

/* ===================== FACTURA PROFORMA ===================== */
/* Numeración propia: PF-n/aa, correlativa por año para toda la empresa. Se asigna una sola vez por presupuesto. */
async function proformaFor(p){
  if(!p)return;
  if(p.proforma&&p.proforma.codigo){await downloadPdf(p,p.proforma);return}
  confirmModal("¿Crear factura proforma para "+p.codigo+"?","Se le asignará el siguiente número de proforma (PF) y quedará registrado en este presupuesto. Después podrás volver a descargarla con el mismo número.","Crear proforma",async()=>{
    try{
      const anio=new Date().getFullYear();
      const usados=PRES.filter(x=>x.proforma&&x.proforma.anio===anio).map(x=>x.proforma.numero||0);
      const n=await Store.nextNumber("PF-"+anio,usados);
      const pf={numero:n,anio,codigo:numCode("PF",n,anio),fecha:today(),creadoPor:Me.id||"",creadoPorNombre:Me.name||Me.manual||""};
      const d=Object.assign({},p);delete d.id;d.proforma=pf;
      await Store.set("presupuestos",p.id,d);
      toast("Proforma "+pf.codigo+" creada");
      await downloadPdf(Object.assign({id:p.id},d),pf);
    }catch(e){toast("No se pudo crear la proforma: "+e.message)}
  });
}

/* ===================== EXCEL ===================== */
async function exportExcel(){
  if(!window.ExcelJS){toast("No se pudo cargar el generador de Excel");return}
  const list=filtered().slice().reverse();
  if(!list.length){toast("No hay presupuestos en el rango elegido");return}
  const names=await userNames(list.map(p=>p.creadoPor));
  const wb=new ExcelJS.Workbook();wb.creator="Tarificador Alditraex";
  const ws=wb.addWorksheet("Presupuestos",{views:[{state:"frozen",ySplit:4}],pageSetup:{orientation:"landscape",fitToPage:true,fitToWidth:1,fitToHeight:0}});
  const cols=[["Nº",12],["Fecha",11],["Delegación",14],["Estado",11],["Motivo rechazo",26],["Cliente",32],["CIF/NIF",14],["Dirección cliente",30],["CP cliente",9],["Población cliente",20],["Provincia cliente",16],["País cliente",12],["Teléfono",14],["Email",28],
    ["País origen",11],["CP origen",9],["Origen",20],["Prov. origen",15],["País destino",11],["CP destino",9],["Destino",20],["Prov. destino",15],["Mercancía",28],["Bultos",8],["Medidas (cant × L×A×H m)",30],["Peso real kg",11],["Volumen m³",11],["PVKG kg",10],["Kg facturables",12],
    ["Tarifa",20],["Zona",18],["Nº pallets",9],["Precio pallet €",11],["Porte €",11],["Supl. no EUR +8% €",12],["Recargo Badajoz/Cáceres €",14],["% Comb.",8],["Combustible €",12],["Base imponible €",14],["% IVA",7],["IVA €",11],["Total €",12],["Usuario",20],["Observaciones",36]];
  const CI=Object.fromEntries(cols.map((c,i)=>[c[0],i+1]));
  ws.columns=cols.map(c=>({width:c[1]}));
  const d1=$("#qDesde").value,d2=$("#qHasta").value;
  ws.mergeCells(1,1,1,10);ws.getCell(1,1).value="ALDITRAEX · PRESUPUESTOS";ws.getCell(1,1).font={size:16,bold:true,color:{argb:"FF1D2026"}};
  ws.mergeCells(2,1,2,10);ws.getCell(2,1).value="Periodo: "+(d1?fmtDate(d1):"inicio")+" – "+(d2?fmtDate(d2):"hoy")+"   ·   Generado el "+fmtDate(today())+"   ·   "+list.length+" presupuestos";ws.getCell(2,1).font={size:10,color:{argb:"FF5B626E"}};
  ws.getRow(3).height=4;for(let i=1;i<=cols.length;i++)ws.getCell(3,i).fill={type:"pattern",pattern:"solid",fgColor:{argb:"FFE39B12"}};
  const hr=ws.getRow(4);cols.forEach((c,i)=>{const cell=hr.getCell(i+1);cell.value=c[0].toUpperCase();cell.font={bold:true,color:{argb:"FFFFFFFF"},size:9};cell.fill={type:"pattern",pattern:"solid",fgColor:{argb:"FF1D2026"}};cell.alignment={vertical:"middle",horizontal:"center",wrapText:true}});hr.height=30;
  list.forEach((p,i)=>{
    const c=p.cliente;
    const row=ws.addRow([p.codigo,new Date(p.fecha+"T12:00:00"),U(p.delegacion),U(p.estado),p.motivoRechazo||"",c.nombre,c.cif,c.dir,c.cp,c.pob,c.prov,U(paisNombre(c.pais)),c.tel,c.email,
      U(paisNombre(p.origen.pais)),p.origen.cp,p.origen.pob,p.origen.prov,U(paisNombre(p.destino.pais)),p.destino.cp,p.destino.pob,p.destino.prov,p.mercancia,p.numBultos,(p.bultos||[]).map(b=>b.cant+"× "+b.l+"×"+b.a+"×"+b.h).join(" | "),
      p.peso,p.volumen,p.pvkg,p.kgFact,U(p.tarifa),U(p.zonaNombre),p.modo==="PALLETS"?p.numPallets:null,p.modo==="PALLETS"?p.precioPallet:null,p.porte,p.suplNoEur||0,p.recargo||0,(p.combPct||0)/100,p.combustible,p.base,(p.ivaPct||0)/100,p.iva,p.total,U(names[p.creadoPor]||p.creadoPorNombre||""),p.observaciones]);
    row.eachCell(cell=>{cell.font={size:10};cell.border={bottom:{style:"thin",color:{argb:"FFDCDFE4"}}};if(i%2)cell.fill={type:"pattern",pattern:"solid",fgColor:{argb:"FFF7F8FA"}}});
    row.getCell(2).numFmt="dd/mm/yyyy";
    ["Peso real kg","PVKG kg","Kg facturables","Bultos","Nº pallets"].forEach(k=>row.getCell(CI[k]).numFmt="#,##0");row.getCell(CI["Volumen m³"]).numFmt="#,##0.000";
    ["Precio pallet €","Porte €","Supl. no EUR +8% €","Recargo Badajoz/Cáceres €","Combustible €","Base imponible €","IVA €","Total €"].forEach(k=>row.getCell(CI[k]).numFmt='#,##0.00 "€"');
    if(p.motivoRechazo)row.getCell(CI["Motivo rechazo"]).font={size:10,color:{argb:"FFB42318"}};
    ["% Comb.","% IVA"].forEach(k=>row.getCell(CI[k]).numFmt="0.00%");
    row.getCell(CI["Total €"]).font={size:10,bold:true};row.getCell(1).font={size:10,bold:true};
    row.getCell(4).font={size:10,bold:true,color:{argb:p.estado==="Aceptado"?"FF1E7A46":p.estado==="Rechazado"?"FFB42318":"FF9A5B00"}};
  });
  const last=ws.rowCount;const tr=ws.addRow([]);tr.getCell(1).value="TOTALES";
  const sumCol=(name,fmt)=>{const k=CI[name],Lc=ws.getColumn(k).letter;tr.getCell(k).value={formula:`SUM(${Lc}5:${Lc}${last})`};tr.getCell(k).numFmt=fmt};
  ["Bultos","Peso real kg","Kg facturables","Nº pallets"].forEach(n=>sumCol(n,"#,##0"));["Porte €","Supl. no EUR +8% €","Recargo Badajoz/Cáceres €","Combustible €","Base imponible €","IVA €","Total €"].forEach(n=>sumCol(n,'#,##0.00 "€"'));
  tr.eachCell({includeEmpty:true},cell=>{cell.font={bold:true,size:10.5};cell.fill={type:"pattern",pattern:"solid",fgColor:{argb:"FFFCF1DC"}};cell.border={top:{style:"medium",color:{argb:"FF1D2026"}}}});
  ws.autoFilter={from:{row:4,column:1},to:{row:last,column:cols.length}};
  const buf=await wb.xlsx.writeBuffer();
  await saveFile("Presupuestos_Alditraex_"+(d1||"inicio")+"_a_"+(d2||today())+".xlsx",new Blob([buf],{type:"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}));
}

/* ===================== TARIFA ===================== */
let rateShown="MER";
function drawRate(){
  document.querySelectorAll("[data-rt]").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.rt===rateShown)));
  $("#setComb").value=SETTINGS.combustible;
  const pc=v=>v==null?"Cotiz.":v+" €";
  if(rateShown==="PAL"){
    const names=Object.keys(TP3);
    $("#rateWrap").innerHTML=`<h2 style="margin-bottom:8px">TP3 2026 · Pallets EUR 1,20 × 0,80 (hasta 2,30 m, 451-1.000 kg)</h2><table class="rate"><thead><tr><th>Provincia</th>${TP3_COLS.map(c=>`<th>${c} pal.</th>`).join("")}</tr></thead><tbody>${names.map(n=>`<tr><td>${esc(n.toUpperCase())}</td>${TP3[n].map(v=>`<td>${pc(v)}</td>`).join("")}</tr>`).join("")}<tr><td>ISLAS MENORES</td>${TP3_COLS.map(()=>"<td>Cotiz.</td>").join("")}</tr></tbody></table>`;
    $("#zoneList").innerHTML=`<div><b>Medida mayor que EUR</b>+8 % sobre el precio del pallet</div><div><b>Destino Badajoz/Cáceres</b>+17 € por pallet si el origen está fuera</div><div><b>Más de 10 pallets</b>Cotización</div>`;return}
  if(rateShown==="PALPT"){
    $("#rateWrap").innerHTML=`<h2 style="margin-bottom:8px">TP3 Pallets Portugal (solo delegación Mérida)</h2><table class="rate"><thead><tr><th>C.P.</th><th>Zona</th>${TP3PT_COLS.map(c=>`<th>${c} pal.</th>`).join("")}</tr></thead><tbody>${TP3PT.map(r=>`<tr><td>${r[0]===r[1]?r[0]:r[0]+"-"+r[1]}</td><td style="text-align:left">${esc(r[2].toUpperCase())}</td>${r[3].map(v=>`<td>${pc(v)}</td>`).join("")}</tr>`).join("")}<tr><td>90-99</td><td style="text-align:left">MADEIRA / AZORES</td>${TP3PT_COLS.map(()=>"<td>Cotiz.</td>").join("")}</tr></tbody></table>`;
    $("#zoneList").innerHTML=`<div><b>Zona por CP</b>Primeros dígitos del código postal portugués</div><div><b>Navalmoral</b>Sin tarifa pallets Portugal: buscar cotización</div>`;return}
  const TF=TARIFAS[rateShown],Z=["REGIONAL","CORTO","MEDIO","LARGO","PORTUGAL","MALLORCA","BALEARES"];
  const f=v=>v==null?"Cotiz.":v.toLocaleString("es-ES",{minimumFractionDigits:2})+" €";
  const fk=v=>v==null?"Cotiz.":v.toLocaleString("es-ES",{minimumFractionDigits:4})+" €/kg";
  let h=`<table class="rate"><thead><tr><th>Kg / vol</th>${Z.map(z=>`<th>${ZN[z]}</th>`).join("")}</tr></thead><tbody>`;
  TIERS.forEach((t,i)=>{h+=`<tr><td>${num(t)}</td>${Z.map(z=>`<td>${f(TF.R[z].p[i])}</td>`).join("")}</tr>`});
  ["2.000","3.000","10.000"].forEach((t,i)=>{h+=`<tr class="perkg"><td>${t}</td>${Z.map(z=>`<td>${fk(TF.R[z].k[i])}</td>`).join("")}</tr>`});
  $("#rateWrap").innerHTML=`<h2 style="margin-bottom:8px">${esc(TF.nombre)}</h2>`+h+"</tbody></table>";
  const cap=s=>s.toUpperCase();
  $("#zoneList").innerHTML=`<div><b>Regional</b>BADAJOZ, CÁCERES</div><div><b>1-Corto</b>${TF.zonas.CORTO.map(cap).join(", ")}</div><div><b>2-Medio</b>${TF.zonas.MEDIO.map(cap).join(", ")}</div><div><b>3-Largo</b>RESTO DE PROVINCIAS PENINSULARES</div><div><b>Mallorca / Resto Baleares</b>MENORCA (077xx), IBIZA Y FORMENTERA (078xx)</div><div><b>Cotización</b>CANARIAS, CEUTA, MELILLA Y RESTO DE EUROPA</div>`;
  $("#setComb").value=SETTINGS.combustible;
}

/* ===================== NAVEGACIÓN ===================== */
const VIEWS=["nuevo","presupuestos","clientes","tarifa"];
function route(){
  const v=VIEWS.includes(location.hash.slice(1))?location.hash.slice(1):"nuevo";
  VIEWS.forEach(x=>{$("#v-"+x).hidden=x!==v});
  document.querySelectorAll("#tabs a").forEach(a=>{if(a.dataset.v===v)a.setAttribute("aria-current","page");else a.removeAttribute("aria-current")});
  if(v==="presupuestos")drawGrid();if(v==="clientes")drawClientes();if(v==="tarifa")drawRate();
  window.scrollTo(0,0);
}

/* ===================== ARRANQUE ===================== */
function wire(){
  fillPaises($("#oPais"),"ES");fillPaises($("#dPais"),"ES");
  wirePlace("o",calc);wirePlace("d",calc);
  $("#btnAddBulto").addEventListener("click",()=>{bultos.push({tipo:"Palet",cant:1,l:1.2,a:0.8,h:1,kg:0});drawBultos();calc()});
  ["#pPeso","#pManual","#pComb","#oCP","#oPob","#oProv","#dCP","#dPob","#dProv"].forEach(s=>$(s).addEventListener("input",calc));
  ["#pIvaMode","#pModo"].forEach(s=>$(s).addEventListener("change",calc));
  $("#pEstado").addEventListener("change",()=>{const v=$("#pEstado").value;
    if(v==="Rechazado")rejectModal(editing?(PRES.find(x=>x.id===editing)||{}).codigo||"":$("#tNum").textContent,motivoRech,m=>{motivoRech=m;prevEstado=v;toast("Motivo: "+m)},()=>{$("#pEstado").value=prevEstado});
    else{motivoRech="";prevEstado=v}});
  $("#btnCombMes").addEventListener("click",async()=>{const v=parseFloat($("#pComb").value);if(isNaN(v)){toast("Indica un porcentaje válido");return}SETTINGS.combustible=v;try{await Store.set("ajustes","general",{combustible:v});toast("Combustible del mes fijado en "+num(v,2)+" %")}catch(e){toast("No se pudo guardar el ajuste")}});
  $("#pFecha").addEventListener("change",previewNumber);
  $("#pDeleg").addEventListener("change",()=>{const cur=placeGet("o");if(!cur.cp||Object.values(DELEG).some(d=>d.origen.cp===cur.cp))placeSet("o",DELEG[serieSel()].origen);ls("ald_serie",serieSel());previewNumber();calc()});
  attachAC($("#pCliente"),$("#acCliente"),async q=>{q=norm(q);return CLIENTES.filter(c=>!q||norm([c.nombre,c.cif,c.pob].join(" ")).includes(q)).sort((a,b)=>(a.nombre||"").localeCompare(b.nombre||"","es")).slice(0,12).concat([{_new:true}])},
    c=>c._new?`<span style="color:var(--gold-ink);font-weight:600">+ Crear cliente nuevo…</span>`:`<span><b>${esc(c.nombre)}</b></span><span class="pr">${esc(c.cif)} · ${esc(c.pob)}</span>`,
    c=>{if(c._new)clientModal({nombre:U($("#pCliente").value)},setCliente);else setCliente(c)});
  $("#pCliente").dataset.openEmpty="1";
  $("#pCliente").addEventListener("input",()=>{if(selCliente&&U($("#pCliente").value)!==U(selCliente.nombre)){selCliente=null;$("#clientCard").textContent="";$("#clientCard").className="";calc()}});
  $("#btnNuevoCliente").addEventListener("click",()=>clientModal({},setCliente));
  $("#btnNuevoCliente2").addEventListener("click",()=>clientModal({}));
  $("#btnGuardar").addEventListener("click",()=>savePres(false));
  $("#btnGuardarPdf").addEventListener("click",()=>savePres(true));
  $("#btnReset").addEventListener("click",()=>resetForm(true));
  $("#btnCancelEdit").addEventListener("click",()=>{resetForm(true);location.hash="presupuestos"});
  ["#qTxt","#qDesde","#qHasta","#qDeleg","#qEstado"].forEach(s=>$(s).addEventListener("input",drawGrid));
  $("#cTxt").addEventListener("input",drawClientes);
  $("#btnExcel").addEventListener("click",exportExcel);
  $("#btnBackup").addEventListener("click",()=>{const data={app:"Tarificador Alditraex",fecha:new Date().toISOString()};["clientes","presupuestos","contadores","ajustes"].forEach(c=>data[c]=Store._local(c));
    saveFile("Copia_Tarificador_Alditraex_"+today()+".json",new Blob([JSON.stringify(data)],{type:"application/json"}))});
  $("#fRestore").addEventListener("change",async e=>{const f=e.target.files[0];if(!f)return;
    try{const data=JSON.parse(await f.text());if(data.app!=="Tarificador Alditraex")throw new Error("no es una copia del Tarificador");
      let n=0;["clientes","presupuestos","ajustes"].forEach(c=>{const o=Store._local(c);Object.assign(o,data[c]||{});n+=Object.keys(data[c]||{}).length;Store._saveLocal(c,o);Store._emit(c)});
      const ct=Store._local("contadores");Object.entries(data.contadores||{}).forEach(([k,v])=>{if(!ct[k]||(v.ultimo||0)>(ct[k].ultimo||0))ct[k]=v});Store._saveLocal("contadores",ct);
      toast("Copia restaurada: "+n+" registros");}catch(err){toast("No se pudo restaurar: "+err.message)}e.target.value=""});
  document.querySelectorAll("[data-rt]").forEach(b=>b.addEventListener("click",()=>{rateShown=b.dataset.rt;drawRate()}));
  $("#btnSetComb").addEventListener("click",async()=>{const v=parseFloat($("#setComb").value);if(isNaN(v)){toast("Indica un porcentaje válido");return}SETTINGS.combustible=v;try{await Store.set("ajustes","general",{combustible:v});toast("Combustible por defecto: "+num(v,2)+" %");if(!editing)$("#pComb").value=v;calc()}catch(e){toast("No se pudo guardar el ajuste")}});
  $("#fPres").addEventListener("submit",e=>e.preventDefault());
  window.addEventListener("hashchange",route);
  const d=new Date();$("#qDesde").value=d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-01";
}
(async function start(){
  wire();resetForm(false);route();loadCountry("ES");
  await Promise.all([Store.init(),initUser()]);
  $("#bkBox").hidden=Store.mode!=="local";
  Store.listen("clientes",docs=>{CLIENTES=docs;if(!$("#v-clientes").hidden)drawClientes()});
  Store.listen("presupuestos",docs=>{PRES=docs;previewNumber();if(!$("#v-presupuestos").hidden)drawGrid();if(!$("#v-clientes").hidden)drawClientes()});
  Store.listen("ajustes",docs=>{const g=docs.find(x=>x.id==="general");if(g&&typeof g.combustible==="number"){const old=SETTINGS.combustible;SETTINGS.combustible=g.combustible;if(!editing&&String($("#pComb").value)===String(old)){$("#pComb").value=g.combustible;calc()}if(!$("#v-tarifa").hidden)$("#setComb").value=g.combustible}});
})();
