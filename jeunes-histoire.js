'use strict';
(() => {
  const NS='http://www.w3.org/2000/svg';
  const formatter=new Intl.NumberFormat('fr-FR',{minimumFractionDigits:1,maximumFractionDigits:1});
  const configs=[
    {
      id:'school', url:'/data/jeunes_scolarisation_1986_2023_insee.csv',
      first:1986, last:2023, count:38, source:'insee_fps2025_f7_fig1',
      groups:{age_18_pct:'18 ans',age_21_pct:'21 ans',age_25_pct:'25 ans',age_29_pct:'29 ans'},
      breaks:[1999,2018], color:'#2a689b'
    },
    {
      id:'workstudy', url:'/data/jeunes_cumul_emploi_etudes_2003_2023_insee.csv',
      first:2003, last:2023, count:21, source:'insee_bfe2025_f5_fig1',
      groups:{age_15_29_pct:'15–29 ans',age_15_19_pct:'15–19 ans',age_20_24_pct:'20–24 ans'},
      breaks:[2014,2021], color:'#1b7e73'
    }
  ];
  function svgNode(tag,attrs={},text=null){
    const el=document.createElementNS(NS,tag);
    for(const [key,value] of Object.entries(attrs))el.setAttribute(key,String(value));
    if(text!==null)el.textContent=text;
    return el;
  }
  function loadCsv(text,conf){
    const lines=text.trim().split(/\r?\n/).map(row=>row.split(','));
    const headers=['year',...Object.keys(conf.groups),'source_id'];
    if(lines.shift().join('|')!==headers.join('|'))throw Error('Invalid headers');
    if(lines.length!==conf.count)throw Error('Invalid year count');
    return lines.map((values,i)=>{
      if(values.length!==headers.length)throw Error('Invalid column count');
      const row=Object.fromEntries(headers.map((key,j)=>[key,values[j]]));
      const year=Number(row.year);
      if(year!==conf.first+i||row.source_id!==conf.source)throw Error('Year or source mismatch');
      for(const key of Object.keys(conf.groups)){
        if(!/^\d+\.\d$/.test(row[key]))throw Error('Uncertain percent');
        row[key]=Number(row[key]);
        if(row[key]<0||row[key]>100)throw Error('Out of range');
      }
      return row;
    });
  }
  function draw(conf,rows){
    const selection=document.getElementById(conf.id+'-age');
    const key=selection.value;
    if(!Object.hasOwn(conf.groups,key))return;
    const group=conf.groups[key], values=rows.map(x=>x[key]);
    const max=Math.max(10,Math.ceil(Math.max(...values)/10)*10);
    const x=year=>55+(year-conf.first)*675/(conf.last-conf.first);
    const y=val=>239-val*202/max;
    const chart=document.getElementById(conf.id+'-chart');
    chart.replaceChildren();
    const title=conf.id==='school'?'Taux de scolarisation':'Cumul études et emploi';
    chart.append(
      svgNode('title',{},title+' — '+group+' — '+conf.first+' à '+conf.last),
      svgNode('desc',{},'Taux annuel en pourcentage. Source Insee et Depp ; tableaux accessibles sous le graphique. Les ruptures de champ et de questionnaire sont signalées en pointillés.')
    );
    for(let i=0;i<=4;i++){
      const pct=max*i/4, yy=y(pct);
      chart.append(svgNode('line',{x1:55,y1:yy,x2:730,y2:yy,stroke:'#d7e0e7','stroke-width':1}));
      chart.append(svgNode('text',{x:45,y:yy+4,'text-anchor':'end',fill:'#526479','font-size':12},formatter.format(pct)));
    }
    for(const br of conf.breaks){
      const xx=x(br);
      chart.append(svgNode('line',{x1:xx,y1:28,x2:xx,y2:240,stroke:'#9a6472','stroke-dasharray':'4 5','stroke-width':1.5}));
    }
    const ticks=new Set([conf.first,conf.last]);
    for(let yr=conf.first;yr<=conf.last;yr++)if(yr%5===0)ticks.add(yr);
    for(const yr of [...ticks].sort((a,b)=>a-b)){
      chart.append(svgNode('text',{x:x(yr),y:260,'text-anchor':'middle',fill:'#526479','font-size':12},String(yr)));
    }
    const points=rows.map((r,i)=>(i===0?'M':'L')+x(Number(r.year)).toFixed(2)+' '+y(r[key]).toFixed(2)).join(' ');
    chart.append(svgNode('path',{d:points,stroke:conf.color,'stroke-width':3,fill:'none','stroke-linejoin':'round','stroke-linecap':'round'}));
    for(const r of [rows[0],rows.at(-1)]){
      chart.append(svgNode('circle',{cx:x(Number(r.year)),cy:y(r[key]),r:4,fill:conf.color,stroke:'#fff','stroke-width':2}));
    }
    chart.setAttribute('aria-label',title+' '+group+' : '+conf.first+', '+formatter.format(values[0])+' % ; '+conf.last+', '+formatter.format(values.at(-1))+' %. Ruptures de série décrites sous le graphique.');
    document.getElementById(conf.id+'-summary').textContent=group+' : '+formatter.format(values[0])+' % en '+conf.first+' ; '+formatter.format(values.at(-1))+' % en '+conf.last+' (variation descriptive de '+formatter.format(values.at(-1)-values[0])+' points).';
    const body=document.getElementById(conf.id+'-data');
    body.replaceChildren();
    for(const r of rows){
      const tr=document.createElement('tr');
      const th=document.createElement('th');th.scope='row';th.textContent=String(r.year);
      const td=document.createElement('td');td.textContent=formatter.format(r[key])+' %';
      tr.append(th,td);body.append(tr);
    }
  }
  for(const conf of configs){
    const sel=document.getElementById(conf.id+'-age');
    const summary=document.getElementById(conf.id+'-summary');
    sel.disabled=true;
    fetch(conf.url).then(response=>{
      if(!response.ok)throw Error('HTTP '+response.status);
      return response.text();
    }).then(text=>{
      const rows=loadCsv(text,conf);
      sel.disabled=false;
      sel.addEventListener('change',()=>draw(conf,rows));
      draw(conf,rows);
    }).catch(()=>{
      summary.textContent='Série indisponible pour le moment. Consulter le tableau officiel Insee lié ci-dessous.';
    });
  }
})();
