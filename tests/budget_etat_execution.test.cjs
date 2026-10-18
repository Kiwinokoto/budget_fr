'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'etat.html'),'utf8');
const data=JSON.parse(fs.readFileSync(path.join(root,'data/etat_execution_2023_2025.json'),'utf8'));
test('Etat execution has coherent years, selective drilldowns and cautions',()=>{
 assert.deepEqual(data.years.map(y=>y.year),[2023,2024,2025]);
 assert.match(html,/id="missions"/);
 assert.match(html,/id="programs"/);
 assert.match(html,/id="revenues"/);
 assert.match(html,/id="revenue-sections"/);
 assert.match(html,/source_reconciliation_gap_eur/);
 assert.match(html,/Les recettes brutes ne mesurent pas/);
 assert.match(html,/CP consommés/);
 assert.doesNotMatch(html,/scrollIntoView|scrollTo\(/);
});
test('state budget is not silently identified with S13',()=>{
 assert.match(html,/et non des comptes consolidés/);
 assert.match(html,/comptabilité nationale des administrations publiques/);
 for(const y of data.years){
  assert.equal(y.missions.length,33);
  assert.ok(y.missions.find(m=>m.name==='Remboursements et dégrèvements'));
  assert.ok(y.revenues.find(r=>r.name==='Recettes fiscales'));
 }
});
