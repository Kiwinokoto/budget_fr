const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'interets.html'),'utf8');
const home=fs.readFileSync(path.join(root,'index.html'),'utf8');
const data=fs.readFileSync(path.join(root,'data/interets_apu_1959_2025_bn_eur.csv'),'utf8').trim().split(/\r?\n/);
test('public interest chart 1959-2025 and source documentation',()=>{
 assert.equal(data.length,68);
 assert.equal(data[0],'year,interest_d41_bn_eur,interest_ex_fisim_bn_eur,total_expenditure_bn_eur');
 assert.match(data.at(-1),/^2025,65\.7209,64\.6519,1714\.1117$/);
 assert.match(html,/D41G/);
 assert.match(html,/SIFIM/);
 assert.match(html,/8988845/);
 assert.match(home,/href="\/interets.html"/);
});
test('interest chart cannot confuse debt stock with annual flows',()=>{
 assert.match(html,/stocks? de fin d'année|stock de fin d'année/);
 assert.match(html,/flux annuel/);
 assert.match(html,/ne sont <strong>pas deux charges additionnables<\/strong>/);
 assert.match(html,/écart|hors correction SIFIM/);
});
test('chart offers explicit units, years and recoverable error state',()=>{
 assert.match(html,/Milliards d'euros courants/);
 assert.match(html,/Part des dépenses publiques/);
 assert.match(html,/1959/);
 assert.match(html,/2025/);
 assert.match(html,/matchMedia/);
 assert.match(html,/Impossible de charger le graphique/);
});
