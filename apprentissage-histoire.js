'use strict';
/* Headcounts, Depp / SIFA, Insee T04 T1. NOT Dares contract starts or stock. */
(() => {
  const csvPath = '/data/apprentissage_sifa_effectifs_1982_2024.csv';
  const svg = document.getElementById('sifa-history-chart');
  const status = document.getElementById('sifa-history-status');
  const tableBody = document.getElementById('sifa-history-rows');
  const number = new Intl.NumberFormat('fr-FR');
  const keys = [
    ['cap_mention', 'CAP / mention', '#3674ae'],
    ['bep_certification', 'BEP / certification', '#70a7a1'],
    ['bac_pro', 'Bac pro', '#b78a64'],
    ['bac_plus_2', 'Bac+2', '#a890bd'],
    ['bac_plus_3_or_more', 'Bac+3 ou plus', '#416c54']
  ];
  const ns = 'http://www.w3.org/2000/svg';
  let values = [];
  function child(parent, type, attrs = {}, content) {
    const node = document.createElementNS(ns, type);
    for (const [k,v] of Object.entries(attrs)) node.setAttribute(k, String(v));
    if (content !== undefined) node.textContent = String(content);
    parent.append(node);
    return node;
  }
  function select(name) {
    return document.querySelector('input[name="' + name + '"]:checked').value;
  }
  function plot() {
    if (!values.length) return;
    const begin = Number(select('history-range'));
    const mode = select('history-mode');
    const rows = values.filter(d => d.year >= begin);
    const x0=84, x1=956, y0=24, y1=280, max=1200000;
    const x = year => x0 + (year-begin)/(2024-begin)*(x1-x0);
    const y = val => y1-(val/max)*(y1-y0);
    svg.replaceChildren();
    child(svg,'title',{id:'sifa-svg-title'},
      mode==='total' ? 'Évolution des effectifs d’apprentis au 31 décembre' :
      'Évolution des effectifs d’apprentis ventilés par niveau de diplôme');
    child(svg,'desc',{id:'sifa-svg-desc'},
      'Source Insee, Depp enquête SIFA. Données de '+begin+' à 2024. France hors Mayotte jusqu’en 2010, France incluant Mayotte depuis 2011. Tableau détaillé disponible après le graphique.');
    for (const n of [0,300000,600000,900000,1200000]) {
      child(svg,'line',{x1:x0,y1:y(n),x2:x1,y2:y(n),stroke:'#d8e0eb','stroke-width':1});
      child(svg,'text',{x:x0-9,y:y(n)+5,'text-anchor':'end',fill:'#475a72','font-size':15},number.format(n));
    }
    const ticks=begin===1995?[1995,2000,2005,2010,2015,2020,2024]:[1982,1990,2000,2010,2020,2024];
    for (const yr of ticks) {
      child(svg,'line',{x1:x(yr),y1:y1,x2:x(yr),y2:y1+6,stroke:'#708095'});
      child(svg,'text',{x:x(yr),y:310,'text-anchor':'middle',fill:'#475a72','font-size':15},yr);
    }
    const x2018=x(2018);
    child(svg,'line',{x1:x2018,y1:y0,x2:x2018,y2:y1,stroke:'#98683c','stroke-dasharray':'5 5','stroke-width':1.6});
    child(svg,'text',{x:x2018+7,y:y0+12,fill:'#885a34','font-size':14},'2018');
    if (mode==='total') {
      const pts=rows.map((r,i)=>[x(r.year),y(r.total)]);
      const fill='M'+pts[0][0]+','+y(0)+' L'+pts.map(p=>p.join(',')).join(' L')+' L'+pts[pts.length-1][0]+','+y(0)+' Z';
      child(svg,'path',{d:fill,fill:'#dce9f5'});
      child(svg,'path',{d:'M'+pts.map(p=>p.join(',')).join(' L'),fill:'none',stroke:'#28679d','stroke-width':4,'stroke-linejoin':'round'});
      child(svg,'circle',{cx:x(2024),cy:y(rows[rows.length-1].total),r:5,fill:'#28679d'});
    } else {
      let lower=rows.map(()=>0);
      for(const [key,,color] of keys) {
        const upper=rows.map((r,i)=>lower[i]+r[key]);
        const forward=rows.map((r,i)=>[x(r.year),y(upper[i])]);
        const backwards=rows.map((r,i)=>[x(r.year),y(lower[i])]).reverse();
        child(svg,'path',{
          d:'M'+forward.concat(backwards).map(p=>p.join(',')).join(' L')+' Z',
          fill:color,'fill-opacity':'0.92',stroke:'#f5f8fd','stroke-width':'0.7'
        });
        lower=upper;
      }
    }
    const first=rows[0],last=rows[rows.length-1], old=values.find(v=>v.year===1995);
    const start=begin===1995 ? old : first;
    status.textContent = mode==='total'
      ? 'Au 31 décembre '+begin+' : '+number.format(start.total)+' apprentis en formation ; fin 2024 : '+
          number.format(last.total)+' (environ '+(last.total/start.total).toFixed(1).replace('.',',')+' fois plus).'
      : 'En 1995 : '+number.format(old.cap_mention)+' apprentis en CAP ou mention et '+
          number.format(old.bac_plus_3_or_more)+' en bac+3 ou plus. Fin 2024 : '+
          number.format(last.cap_mention)+' en CAP ou mention et '+
          number.format(last.bac_plus_3_or_more)+' en bac+3 ou plus.';
    document.getElementById('sifa-legend').hidden = mode !== 'diplomas';
  }
  function rowsFromCSV(text) {
    const lines=text.trim().split(/\r?\n/).map(r=>r.split(','));
    const columns=['year','cap_mention','bep_certification','bac_pro','bac_plus_2',
      'bac_plus_3_or_more','total','territory','source_id'];
    if (lines[0].join('|') !== columns.join('|')) throw new Error('En-têtes CSV inattendus');
    const rows=lines.slice(1).map(fields=>{
      const d=Object.fromEntries(fields.map((v,i)=>[columns[i],v]));
      for(const key of columns.slice(0,7)) {
        if (!/^\d+$/.test(d[key])) throw new Error('Nombre SIFA invalide');
        d[key]=Number(d[key]);
      }
      return d;
    });
    if(rows.length!==43 || rows[0].year!==1982 || rows.at(-1).year!==2024)throw Error('Années SIFA manquantes');
    for(let i=0;i<rows.length;i++) {
      const r=rows[i];
      if(r.year!==1982+i || keys.reduce((sum,[key])=>sum+r[key],0)!==r.total ||
        r.source_id!=='insee_bilan_formation_emploi_2025_t04_sifa_t1' ||
        r.territory!==(r.year<=2010?'france_excluding_mayotte':'france_including_mayotte'))
        throw Error('Observation SIFA incohérente : '+r.year);
    }
    return rows;
  }
  function renderTable() {
    tableBody.replaceChildren();
    for (const r of values) {
      const row=document.createElement('tr');
      const parts=[r.year,r.total,r.cap_mention,r.bep_certification,r.bac_pro,
        r.bac_plus_2,r.bac_plus_3_or_more];
      for(let i=0;i<parts.length;i++){
        const cell=document.createElement(i===0?'th':'td');
        if(i===0)cell.scope='row';
        cell.textContent=i===0 ? String(r.year) : number.format(parts[i]);
        row.append(cell);
      }
      tableBody.append(row);
    }
  }
  for(const input of document.querySelectorAll('input[name="history-mode"], input[name="history-range"]'))
    input.addEventListener('change', plot);
  fetch(csvPath).then(response=>{
    if(!response.ok)throw new Error('HTTP '+response.status);
    return response.text();
  }).then(text=>{
    values=rowsFromCSV(text);
    renderTable();plot();
  }).catch(()=>{
    status.textContent="Série Insee temporairement indisponible. Les chiffres clés ci-dessus et les autres sections restent consultables.";
  });
})();
