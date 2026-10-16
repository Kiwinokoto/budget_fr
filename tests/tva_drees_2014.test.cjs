const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'tva-incidence.html'),'utf8');
const lines=fs.readFileSync(path.join(root,'data/tva_part_deciles_ines_2014.csv'),'utf8').trim().split(/\r?\n/);
const values=lines.slice(1).map(s=>Number(s.split(',')[1]));
test('Drees 2014 source values: 10 deciles, exact TVA shares and sum 100 percent',()=>{
 assert.equal(lines[0],'decile,vat_share_pct');
 assert.deepEqual(values,[4.3,6.3,7.2,8,8.9,9.8,11,12,14,18.5]);
 assert.equal(values.reduce((s,n)=>s+n,0),100);
});
test('2014 VAT chart does not mislabel source data as annual receipts or effort',()=>{
 assert.match(html,/head-ines/);
 assert.match(html,/Ines 2014/);
 assert.match(html,/Budget de famille 2011/);
 assert.match(html,/ni une mesure en 2025/);
 assert.match(html,/aux recettes nationales 1995–2025/);
 assert.match(html,/\/data\/tva_part_deciles_ines_2014.csv/);
 assert.match(html,/ines\.reduce\(\(sum,r\)=>sum\+r\.vat_share_pct,0\)-100/);
});
