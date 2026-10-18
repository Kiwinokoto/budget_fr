'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'fonctions.html'),'utf8');
const details=JSON.parse(fs.readFileSync(path.join(root,'data/cofog_subfunctions_1995_2024.json'),'utf8'));
test('COFOG level 2 is navigable, year-sensitive and accessible',()=>{
 assert.match(html,/id="sub-breakdown" role="list"/);
 assert.match(html,/className='sub-row';line.setAttribute\('role','listitem'\)/);
 assert.match(html,/const base=current\[selected\],index=Number\(range.value\)-1995/);
 assert.match(html,/subRefresh\(\)/);
 assert.match(html,/sous-fonctions COFOG/);
 assert.match(html,/Détail indisponible/);
 assert.match(html,/id="cofog-trace"/);
 assert.match(html,/bénéficiaire final/);
 assert.match(html,/role="status" aria-live="polite"/);
 assert.doesNotMatch(html,/scrollIntoView|scrollTo\(/);
});
test('COFOG details have ten groups and the same thirty years',()=>{
 assert.deepEqual(details.years,Array.from({length:30},(_,i)=>1995+i));
 assert.equal(details.categories.length,10);
 assert.equal(details.categories.reduce((n,c)=>n+c.children.length,0),69);
 const social=details.categories.find(c=>c.code==='gf10');
 const pension=social.children.find(c=>c.code==='gf1002');
 assert.equal(pension.values[29],391.954);
 assert.match(pension.label,/Vieillesse/);
});
