const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'apprentissage.html'),'utf8');
const sources=fs.readFileSync(path.join(root,'APPRENTISSAGE_SOURCES.md'),'utf8');
const navPages=['index.html','fonctions.html','recettes.html','solde-primaire.html','interets.html','dette.html','tva-justice.html','tva-incidence.html','aides-entreprises.html','apprentissage.html'];
function loadCSV(name){
 const lines=fs.readFileSync(path.join(root,'data',name),'utf8').trim().split(/\r?\n/);
 const cols=lines.shift().split(',');
 return lines.map(line=>Object.fromEntries(line.split(',').map((value,i)=>[cols[i],value])));
}
test('Dares published 2024 and provisional 2025 indicator pairs retain versions',()=>{
 const rows=loadCSV('apprentissage_dares_2024_2025_indicateurs.csv');
 assert.equal(rows.length,2);
 assert.deepEqual(rows.map(x=>[x.year,x.started_contracts,x.contracts_in_progress_dec31]),[
  ['2024','889400','1048800'],['2025','846700','1017500']]);
 assert.equal(rows[1].status,'first_estimate');
 assert.ok(rows.every(x=>x.sector_scope==='public_private'));
 for(const x of rows){
  for(const val of [x.started_contracts,x.contracts_in_progress_dec31])
   assert.ok(html.replace(/\s/g,'').includes(Number(val).toLocaleString('fr-FR').replace(/\s/g,'')),val);
 }
 assert.match(sources,/2025.*première estimation|2025.*Premières estimations/);
});
test('France compétences funding is from different field, not summed with Dares',()=>{
 const rows=loadCSV('apprentissage_financement_2024_france_competences.csv');
 assert.equal(rows.length,1);
 const d=rows[0];
 assert.deepEqual([d.year,d.commitments_bn_eur,d.unit_cost_eur,d.employer_aid_per_contract_eur],
  ['2024','15.6','17404','5983']);
 assert.equal(Number(d.pedagogical_share_pct)+Number(d.employer_aid_share_pct)+Number(d.other_share_rounded_pct),100);
 assert.match(html,/15,6 Md€/);
 assert.match(html,/17 404/);
 assert.match(html,/5 983/);
 assert.match(html,/52 %/);
 assert.match(html,/34 %/);
 assert.match(sources,/ne pas|Ne pas/);
});
test('count switch has keyboard radio semantics and updates accessible chart text',()=>{
 assert.match(html,/<fieldset><legend><strong>Indicateur<\/strong><\/legend>/);
 assert.match(html,/type="radio" name="count-mode" value="starts" checked/);
 assert.match(html,/type="radio" name="count-mode" value="stock"/);
 assert.match(html,/role="status" aria-live="polite"/);
 assert.match(html,/document\.getElementById\('mode-summary'\)\.textContent/);
 assert.match(html,/renderMode\(input.value\)/);
 assert.doesNotMatch(html,/innerHTML\s*=/);
});
test('history is sourced and context separates the apprenticeship from modern contracts',()=>{
 for(const year of ['1919','1925','1928','1971','1987','2018','2020'])
  assert.ok(html.includes('<time datetime="'+year+'">'+year+'</time>'),year);
 assert.match(html,/n’est pas.*date de naissance|pas sa date de naissance/);
 assert.match(html,/France compétences/);
 assert.match(html,/Dares/);
 assert.match(html,/APPRENTISSAGE_SOURCES\.md/);
});
test('ten chapters including APPRENTISSAGE have one current nav link and home card',()=>{
 for(const file of navPages){
  const h=fs.readFileSync(path.join(root,file),'utf8');
  assert.ok(h.includes('href="/apprentissage.html"'),file);
  assert.equal((h.match(/aria-current="page"/g)||[]).length,1,file);
  assert.equal((h.match(/class="atlas-nav"/g)||[]).length,1,file);
 }
 assert.ok(fs.readFileSync(path.join(root,'index.html'),'utf8').includes('class="atlas-card" href="/apprentissage.html"'));
});
