'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),root=path.resolve(__dirname,'..');
const data=JSON.parse(fs.readFileSync(path.join(root,'data/etat_solde_net_2013_2025.json'),'utf8'));
const html=fs.readFileSync(path.join(root,'etat.html'),'utf8');

test('Official state budget balance covers every year 2013–2025',()=>{
 assert.deepEqual(data.years.map(y=>y.year),Array.from({length:13},(_,i)=>2013+i));
 assert.equal(data.years[0].solde_eur,-74867970256);
 assert.equal(data.years.at(-1).solde_eur,-124205673502);
});
test('Official net budget balance, cash receipts and adjustments reconcile within EUR rounding',()=>{
 for(const y of data.years){
  assert.ok(Number.isSafeInteger(y.solde_eur));
  assert.ok(Math.abs(y.recettes_bg_nettes_eur-y.recettes_fiscales_nettes_eur-y.recettes_non_fiscales_eur)<=2);
  const sum=y.recettes_bg_nettes_eur-y.depenses_bg_nettes_eur-y.prelevements_recettes_eur+
   y.solde_comptes_speciaux_eur+y.solde_budgets_annexes_eur+y.fonds_concours_eur;
  assert.ok(Math.abs(sum-y.solde_eur)<=4, String(y.year));
 }
});
test('Budget balance chart and reconciliation are accessible and scoped',()=>{
 for(const fragment of ['id="balance-chart"','id="balance-summary"','id="balance-rows"',
  'id="balance-year"','role="status"','aria-live="polite"','2013–2025',
  'DGFiP','PLRG','recettes_fiscales_nettes_eur']){
  assert.ok(html.includes(fragment),fragment);
 }
 assert.doesNotMatch(html,/scrollIntoView|scrollTo\(/);
});
