const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const page=fs.readFileSync(path.join(root,'tva-justice.html'),'utf8');
const index=fs.readFileSync(path.join(root,'index.html'),'utf8');
const receipts=fs.readFileSync(path.join(root,'recettes.html'),'utf8');
const lines=fs.readFileSync(path.join(root,'data/tva_choc_deciles_insee_2019.csv'),'utf8').trim().split(/\r?\n/);
const fields=lines[0].split(',');
const rows=lines.slice(1).map(line=>Object.fromEntries(line.split(',').map((v,i)=>[fields[i],Number(v)])));

test('transcription has exactly 10 deciles and original figure-2 values',()=>{
  assert.equal(rows.length,10);
  assert.deepEqual(rows.map(x=>x.decile),Array.from({length:10},(_,i)=>i+1));
  assert.deepEqual(rows.map(x=>x.indirect_tax_pp),[-2.8,-1.9,-1.7,-1.6,-1.5,-1.4,-1.3,-1.3,-1.3,-1]);
  assert.deepEqual(rows.map(x=>x.net_living_standard_pct),[-1.4,-.7,-.6,-.6,-.6,-.5,-.5,-.5,-.6,-.5]);
});

test('simulation is explicitly distinct from observed 2025 tax receipts',()=>{
  assert.match(page,/Simulation publiée en 2019/);
  assert.match(page,/Référence 2016/);
  assert.match(page,/Ce ne sont pas les taxes payées en 2025/);
  assert.match(page,/Prélèvements indirects/);
  assert.match(page,/Effet total après trois ans/);
  assert.match(page,/3713290/);
  assert.match(index,/href="\/tva-justice.html"/);
  assert.match(receipts,/href="\/tva-justice.html"/);
});

test('page avoids injection through string templating and has a chart error state',()=>{
  assert.match(page,/document\.createElement\('button'\)/);
  assert.match(page,/textContent=/);
  assert.match(page,/Erreur de chargement/);
  assert.match(page,/type="radio" name="metric"/);
});
