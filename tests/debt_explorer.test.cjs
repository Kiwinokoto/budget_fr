const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const page=fs.readFileSync(path.join(root,'dette.html'),'utf8');
const index=fs.readFileSync(path.join(root,'index.html'),'utf8');
function csv(name){
 const lines=fs.readFileSync(path.join(root,'data',name),'utf8').trim().split(/\r?\n/);
 const header=lines.shift().split(',');
 const rows=lines.map(line=>Object.fromEntries(line.split(',').map((cell,i)=>[header[i],cell])));
 return {header,rows};
}
const instruments=csv('dette_maastricht_instruments_1995_2025_bn_eur.csv');
const net=csv('dette_nette_apu_1995_2025.csv');
const bridge=csv('dette_passifs_maastricht_1995_2025.csv');
const flow=csv('dette_deficit_variation_2009_2025.csv');
test('source coverage and 2025 anchors match pinned Insee tables',()=>{
 assert.equal(instruments.rows.length,186);
 assert.equal(net.rows.length,186);
 assert.equal(bridge.rows.length,186);
 assert.equal(flow.rows.length,17);
 const lookup=(data,year,sector)=>data.rows.find(r=>r.year===String(year)&&(!sector||r.sector===sector));
 assert.equal(lookup(instruments,2025,'S13').maastricht_bn_eur,'3460.1');
 assert.equal(lookup(net,2025,'S13').net_debt_bn_eur,'3242.7');
 assert.equal(lookup(flow,2025).debt_change_bn_eur,'154.0');
 assert.equal(lookup(instruments,2025,'S1314').deposits_bn_eur,'');
 assert.equal(lookup(bridge,2025,'S1314').maastricht_bn_eur,'293.1');
});
test('new page supports year 1995-2025, sector navigation, stock instruments and source links',()=>{
 assert.match(page,/<html lang="fr">/);
 assert.match(page,/id="year" type="range" min="1995" max="2025"/);
 for(const s of ['S13','S13111','S13112','S1313','S1314','S1311'])assert.match(page,new RegExp('value="'+s+'"'));
 for(const key of ['deposits_bn_eur','short_securities_bn_eur','long_securities_bn_eur','short_loans_bn_eur','long_loans_bn_eur','maastricht_bn_eur','net_debt_bn_eur','valuation_breakdown_gap_bn_eur'])assert.ok(page.includes(key),key);
 assert.match(page,/insee\.fr\/fr\/statistiques\/8988843/);
 assert.match(index,/href="\/dette.html"/);
});
test('separates gross / net / cash flow and identifies known anomalies explicitly',()=>{
 assert.match(page,/dette brute/);
 assert.match(page,/dette nette/);
 assert.match(page,/stocks?|encours/i);
 assert.match(page,/flux annuels|variation annuelle/i);
 assert.match(page,/2014–2021/);
 assert.match(page,/293,1 Md€/);
 assert.match(page,/292,6 Md€/);
 assert.match(page,/−0,6 Md€/);
 assert.match(page,/2009/);
 assert.match(page,/échéance|durée initiale/i);
});
test('loading/error/retry, data schema verification, accessible chart and responsive layout',()=>{
 assert.match(page,/Chargement des données…/);
 assert.match(page,/aria-live="polite"/);
 assert.match(page,/Réessayer/);
 assert.match(page,/if\(responses\.some\(r=>!r\.ok\)\)/);
 assert.match(page,/if\(heads\.join\(','\)!==expectedHeaders\.join\(','\)/);
 assert.match(page,/document\.createElementNS\(svgNS,tag\)/);
 assert.match(page,/window\.matchMedia\('\(max-width: 660px\)'\)/);
 assert.match(page,/<svg id="history".*role="img"/);
 assert.doesNotMatch(page, /\.innerHTML\s*=/);
 const script=page.match(/<script>([\s\S]+?)<\/script>/);
 assert.ok(script,'inline application JS');
 new vm.Script(script[1],{filename:'dette.html'});
});
test('individual financial instrument components never double-count parent securities row',()=>{
 const f=+instruments.rows.find(r=>r.year==='2025'&&r.sector==='S13').maastricht_bn_eur;
 const r=instruments.rows.find(r=>r.year==='2025'&&r.sector==='S13');
 const v=+(r.deposits_bn_eur)+(+r.short_securities_bn_eur)+(+r.long_securities_bn_eur)+(+r.short_loans_bn_eur)+(+r.long_loans_bn_eur);
 assert.ok(Math.abs(f-v)<0.31);
 assert.ok(page.includes("securities_bn_eur"));
 assert.ok(Math.abs(+r.short_securities_bn_eur+(+r.long_securities_bn_eur)-(+r.securities_bn_eur))<1e-8);
});
