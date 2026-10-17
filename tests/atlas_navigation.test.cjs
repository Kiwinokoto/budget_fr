const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const pages=['index.html','fonctions.html','recettes.html','solde-primaire.html','interets.html','dette.html','tva-justice.html','tva-incidence.html','aides-entreprises.html'];
test('shared navigation has a unique active page across all chapters',()=>{
 for(const file of pages){
  const html=fs.readFileSync(path.join(root,file),'utf8');
  assert.match(html,/<link rel="stylesheet" href="\/atlas-nav.css">/,file);
  assert.match(html,/<nav class="atlas-nav" aria-label="Sections de l’atlas">/,file);
  assert.equal((html.match(/aria-current="page"/g)||[]).length,1,file);
  assert.equal((html.match(/class="atlas-nav"/g)||[]).length,1,file);
  for(const page of pages)assert.ok(html.includes('href="/'+(page==='index.html'?'':page)+'"'),file+' -> '+page);
 }
});
test('navigation stays local, keyboard-ready, responsive and uses no external scripts',()=>{
 const css=fs.readFileSync(path.join(root,'atlas-nav.css'),'utf8');
 assert.match(css,/overflow-x:auto/);
 assert.match(css,/focus-visible/);
 assert.match(css,/aria-current=page/);
 assert.match(css,/min-width:0/);
 assert.doesNotMatch(css,/https?:\/\//);
});
test('COFOG explorer keeps chart and list together without automatic scrolling',()=>{
 const html=fs.readFileSync(path.join(root,'fonctions.html'),'utf8');
 assert.match(html,/class="explorer"/);
 assert.match(html,/\.explorer\{display:grid;grid-template-columns:/);
 assert.match(html,/\.trend-panel\{position:sticky;top:68px\}/);
 assert.match(html,/\.trend-panel\{position:static\}/);
 assert.match(html,/id="chart-summary".*aria-live="polite"/);
 assert.match(html,/button\.dataset\.category=key/);
 assert.match(html,/breakdown\.querySelectorAll\('\.func'\)/);
 assert.doesNotMatch(html,/scrollIntoView|scrollTo\(/);
});
test('home displays charts before the exploratory cards',()=>{
 const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
 assert.ok(html.indexOf('id="chart"')<html.indexOf('class="explore-atlas"'));
 assert.ok(html.indexOf('id="debt-chart"')<html.indexOf('class="explore-atlas"'));
 assert.equal((html.match(/class="atlas-card"/g)||[]).length,8);
});
