const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const page=fs.readFileSync(path.join(root,'solde-primaire.html'),'utf8');
const index=fs.readFileSync(path.join(root,'index.html'),'utf8');
const lines=fs.readFileSync(path.join(root,'data/solde_primaire_apu_1959_2025_bn_eur.csv'),'utf8').trim().split(/\r?\n/);
test('primary explorer has 67 annual rows, separate interest definitions and correct 2025',()=>{
 assert.equal(lines.length,68);
 assert.equal(lines[0],'year,balance_b9_bn_eur,interest_d41_bn_eur,interest_d41g_bn_eur,primary_d41_bn_eur,primary_d41g_bn_eur,total_expenditure_bn_eur');
 assert.equal(lines.at(-1),'2025,-151.5920,65.7209,64.6519,-85.8711,-86.9401,1714.1117');
 assert.match(page,/name="interest-mode" value="d41" checked/);
 assert.match(page,/name="interest-mode" value="d41g"/);
 assert.match(page,/primary_d41g_bn_eur/);
 assert.match(page,/Ce calcul réintègre les <strong>intérêts payés<\/strong>/);
});
test('primary explorer explicitly distinguishes annual balance and debt concepts and units',()=>{
 assert.match(page,/Milliards d'euros courants/);
 assert.match(page,/% des dépenses publiques/);
 assert.match(page,/pas sur le PIB/);
 assert.match(page,/y1:Y\(0\),y2:Y\(0\),stroke:'#a6b5d3'/);
 assert.match(page,/un solde primaire structurel/);
 assert.match(page,/2025 est provisoire/);
 assert.match(index,/href="\/solde-primaire.html"/);
});
test('primary explorer handles missing data without confusing the loading state',()=>{
 assert.match(page,/Chargement des données…/);
 assert.match(page,/aria-live="polite"/);
 assert.match(page,/r\.total_expenditure_bn_eur<=0/);
 assert.match(page,/Réessayer/);
 assert.match(page,/body\.classList\.remove\('loading-data'\)/);
});
