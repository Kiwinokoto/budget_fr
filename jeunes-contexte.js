'use strict';
(() => {
  const categories = [
    ['study_only','En études initiales sans emploi','#487aab'],
    ['study_and_work','Études et emploi','#84afa3'],
    ['work_only','En emploi hors études','#d5a46e'],
    ['unemployed','Au chômage','#b77e83'],
    ['other_inactive','Autres inactifs hors études','#b4bac7']
  ];
  const src = '/data/jeunes_situations_2024_insee.csv';
  const names={women:'Femmes',men:'Hommes'};
  const csvHeaders=['age_group','sex',...categories.map(x=>x[0]),'source_id'];
  const formatter=new Intl.NumberFormat('fr-FR',{minimumFractionDigits:1,maximumFractionDigits:1});
  let rows=[];
  function csvRows(text){
    const lines=text.trim().split(/\r?\n/).map(s=>s.split(','));
    if(lines.shift().join('|')!==csvHeaders.join('|'))throw Error('Unexpected youth situations CSV headers');
    const data=lines.map(c=>Object.fromEntries(c.map((v,i)=>[csvHeaders[i],v])));
    if(data.length!==6)throw Error('Expected six Insee groups');
    for(const row of data){
      if(!['women','men'].includes(row.sex) || !['18-20','21-24','25-29'].includes(row.age_group))throw Error('Unknown cohort');
      if(row.source_id!=='insee_fps2025_figure2_eec2024')throw Error('Unknown source');
      for(const [key] of categories){
        if(!/^\d+\.\d$/.test(row[key]))throw Error('Uncertain percentage '+key);
        row[key]=Number(row[key]);
      }
      const total=categories.reduce((s,[key])=>s+row[key],0);
      if(Math.abs(total-100)>0.11)throw Error('Shares do not sum to 100: '+row.age_group+' '+row.sex);
    }
    return data;
  }
  function label(){
    const age=document.querySelector('input[name="age-group"]:checked')?.value;
    const sex=document.querySelector('input[name="sex"]:checked')?.value;
    return {age,sex};
  }
  function paint(){
    const {age,sex}=label();
    const row=rows.find(r=>r.age_group===age && r.sex===sex);
    if(!row)return;
    const total=categories.reduce((s,[key])=>s+row[key],0);
    const title=names[sex]+', '+age.replace('-','–')+' ans';
    document.getElementById('donut-title').textContent=title;
    let cumulative=0;
    const gradients=[];
    const phrases=[];
    const legend=document.getElementById('youth-legend');
    legend.replaceChildren();
    for(const [key,name,color] of categories){
      const percent=row[key];
      const start=100*cumulative/total;
      cumulative+=percent;
      const end=100*cumulative/total;
      gradients.push(color+' '+start+'% '+end+'%');
      phrases.push(name+' : '+formatter.format(percent)+' %');
      const li=document.createElement('li');
      const icon=document.createElement('i');icon.style.background=color;
      const span=document.createElement('span');span.textContent=name;
      const strong=document.createElement('b');strong.textContent=formatter.format(percent)+' %';
      li.append(icon,span,strong);legend.append(li);
    }
    const donut=document.getElementById('youth-donut');
    donut.style.background='conic-gradient('+gradients.join(',')+')';
    donut.setAttribute('aria-label','Répartition '+title+' : '+phrases.join(' ; ')+'.');
    document.getElementById('donut-note').textContent='Population '+title+' : parts publiées par l’Insee, arrondies à 0,1 point. Total publié : '+formatter.format(total)+' %. Couleurs normalisées à 100 % pour dessiner le cercle.';
  }
  function renderTable(){
    const body=document.getElementById('youth-data-rows');
    body.replaceChildren();
    for(const r of rows){
      const tr=document.createElement('tr');
      const cells=[r.age_group.replace('-','–')+' ans',names[r.sex],...categories.map(([key])=>formatter.format(r[key]))];
      for(let i=0;i<cells.length;i++){
        const el=document.createElement(i===0?'th':'td');
        if(i===0)el.scope='row';
        el.textContent=cells[i];tr.append(el);
      }
      body.append(tr);
    }
  }
  document.querySelectorAll('input[name="age-group"],input[name="sex"]').forEach(el=>
    el.addEventListener('change',()=>{if(el.checked)paint()}));
  fetch(src).then(r=>{if(!r.ok)throw Error('HTTP '+r.status);return r.text()}).then(text=>{
    rows=csvRows(text);renderTable();paint();
  }).catch(()=>{
    document.getElementById('donut-note').textContent='Données interactives temporairement indisponibles : veuillez consulter le tableau à la source Insee indiquée ci-dessous.';
  });
})();
