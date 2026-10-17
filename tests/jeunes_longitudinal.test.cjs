const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'apprentissage-contexte.html'),'utf8');
const js=fs.readFileSync(path.join(root,'jeunes-histoire.js'),'utf8');
const rows=name=>fs.readFileSync(path.join(root,'data',name),'utf8').trim().split(/\r?\n/).map(x=>x.split(','));
test('séries Insee non interpolées, unités et années',()=>{
 const s=rows('jeunes_scolarisation_1986_2023_insee.csv');
 const w=rows('jeunes_cumul_emploi_etudes_2003_2023_insee.csv');
 assert.equal(s.length,39);assert.equal(w.length,22);
 assert.deepEqual(s[0],['year','age_18_pct','age_21_pct','age_25_pct','age_29_pct','source_id']);
 assert.deepEqual(w[0],['year','age_15_29_pct','age_15_19_pct','age_20_24_pct','source_id']);
 assert.equal(s[1][0],'1986');assert.equal(s.at(-1)[0],'2023');
 assert.equal(w[1][0],'2003');assert.equal(w.at(-1)[0],'2023');
 assert.equal(w.at(-1)[1],'22.3');assert.equal(s.at(-1)[2],'50.9');
});
test('deux panneaux interactifs, tableaux accessibles et distinctions méthodologiques',()=>{
 for(const id of ['school','workstudy']){
  for(const suffix of ['age','chart','data','summary'])assert.match(html,new RegExp('id="'+id+'-'+suffix+'"'));
 }
 assert.match(html,/population du même âge/);assert.match(html,/en études initiales/);
 assert.match(html,/comparabilité limitée/);assert.match(html,/démontrer une hausse de l’accès aux études/);
 assert.match(js,/fetch\(conf\.url\)/);assert.match(js,/selection\.value/);
 assert.match(js,/chart\.setAttribute\('aria-label'/);assert.match(js,/chart\.replaceChildren\(\)/);
 assert.match(js,/conf\.breaks/);assert.doesNotMatch(js,/innerHTML\s*=/);
});
