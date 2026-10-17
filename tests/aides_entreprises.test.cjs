const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const doc=fs.readFileSync(path.join(root,'aides-entreprises.html'),'utf8');
const source=fs.readFileSync(path.join(root,'AIDES_ENTREPRISES_SOURCES.md'),'utf8');
const csv=fs.readFileSync(path.join(root,'data/aides_entreprises_senat_2023_estimations.csv'),'utf8').trim().split(/\r?\n/);
test('estimates are two separate Senate 2023 perimeter estimates, not a time series',()=>{
 const header=csv.shift().split(',');
 assert.deepEqual(header,['year','scope','amount_bn_eur','value_type','source_id']);
 const rows=csv.map(line=>Object.fromEntries(line.split(',').map((v,i)=>[header[i],v])));
 assert.deepEqual(rows.map(row=>[row.year,row.scope,row.amount_bn_eur]),[['2023','strict','108'],['2023','large','211']]);
 assert.ok(rows.every(r=>r.value_type==='estimation_plancher_ordre_de_grandeur'&&r.source_id==='senat_r24_808_1'));
 assert.match(doc,/number:108/);
 assert.match(doc,/number:211/);
 assert.match(doc,/ne s’additionnent pas/);
 assert.match(doc,/seules grandes entreprises|grandes entreprises.*seulement/);
 assert.match(doc,/Ce ne sont pas trois points successifs d’une même série/);
});
test('article links sources and communicates tax and financial caveats',()=>{
 assert.match(doc,/href="https:\/\/www\.senat\.fr\/rap\/r24-808-1\/r24-808-1_mono\.html"/);
 assert.match(doc,/href="https:\/\/www\.igf\.gouv\.fr\/rapports-de-mission\/revue-de-depenses-les-aides-aux-entreprises"/);
 assert.match(doc,/href="https:\/\/www\.strategie-plan\.gouv\.fr\/publications\/politiques-industrielles-france-evolutions-comparaisons-internationales"/);
 assert.match(doc,/64 Md€ en 2022/);
 assert.match(doc,/139 à 223 Md€/);
 assert.match(doc,/prêts et garanties/);
 assert.match(doc,/réellement dépensés|subvention dépensée/);
 assert.match(source,/risque de double compte|double compte/);
});
test('radio scope control has real live state and a textual alternative',()=>{
 assert.match(doc,/<fieldset class="choice"><legend>Choisir la définition à examiner<\/legend>/);
 assert.match(doc,/<input type="radio" name="scope" value="strict" checked>/);
 assert.match(doc,/<input type="radio" name="scope" value="large">/);
 assert.match(doc,/aria-live="polite"/);
 assert.match(doc,/renderScope\(input.value\)/);
 assert.match(doc,/setAttribute\('aria-label',scope.number\+'/);
 assert.doesNotMatch(doc,/innerHTML\s*=/);
 assert.match(doc,/<main>/);
});
test('project website links new chapter in all nine nav bars',()=>{
 for(const page of ['index.html','fonctions.html','recettes.html','solde-primaire.html','interets.html','dette.html','tva-justice.html','tva-incidence.html','aides-entreprises.html']){
  const html=fs.readFileSync(path.join(root,page),'utf8');
  assert.ok(html.includes('href="/aides-entreprises.html"'),page);
  assert.equal((html.match(/aria-current="page"/g)||[]).length,1,page);
 }
 assert.match(fs.readFileSync(path.join(root,'index.html'),'utf8'),/Pourquoi 108 ou 211 milliards en 2023/);
});
