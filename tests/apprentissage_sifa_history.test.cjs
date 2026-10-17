const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const csv=fs.readFileSync(path.join(root,'data/apprentissage_sifa_effectifs_1982_2024.csv'),'utf8').trim().split(/\r?\n/);
const head=csv.shift().split(',');
const rows=csv.map(line=>Object.fromEntries(line.split(',').map((v,i)=>[head[i],v])));
const doc=fs.readFileSync(path.join(root,'apprentissage.html'),'utf8');
const script=fs.readFileSync(path.join(root,'apprentissage-histoire.js'),'utf8');
test('SIFA series has 43 years with consistent counts, fields and geography',()=>{
 assert.equal(rows.length,43);
 assert.deepEqual(head, ['year','cap_mention','bep_certification','bac_pro','bac_plus_2','bac_plus_3_or_more','total','territory','source_id']);
 for(let i=0;i<rows.length;i++){
  const row=rows[i];
  assert.equal(Number(row.year),1982+i);
  assert.equal(Number(row.total),
    ['cap_mention','bep_certification','bac_pro','bac_plus_2','bac_plus_3_or_more']
      .reduce((sum,col)=>sum+Number(row[col]),0));
  assert.equal(row.territory,i<29?'france_excluding_mayotte':'france_including_mayotte');
 }
});
test('historic CAP vs bac+3 growth is derived from the same SIFA table',()=>{
 const r=Object.fromEntries(rows.map(v=>[v.year,v]));
 assert.deepEqual([r['1995'].total,r['1995'].cap_mention,r['1995'].bac_plus_3_or_more],
  ['293512','194485','4777']);
 assert.deepEqual([r['2024'].total,r['2024'].cap_mention,r['2024'].bac_plus_3_or_more],
  ['1049965','191029','421000']);
 assert.equal(r['2018'].total,'448127');
});
test('HTML contains keyboard-usable series chart, per-diploma mode and full accessible table',()=>{
 assert.match(doc,/type="radio" name="history-mode" value="total" checked/);
 assert.match(doc,/type="radio" name="history-mode" value="diplomas"/);
 assert.match(doc,/type="radio" name="history-range" value="1995" checked/);
 assert.match(doc,/type="radio" name="history-range" value="1982"/);
 assert.match(doc,/id="sifa-history-rows"/);
 assert.match(doc,/role="status" aria-live="polite"/);
 assert.match(doc,/role="region" aria-label="Graphique historique défilable horizontalement sur petit écran"/);
 assert.match(doc,/class="history-legend" id="sifa-legend" hidden/);
 assert.match(doc,/\.history-legend\[hidden\]\{display:none\}/);
 assert.match(doc,/apprentissage-histoire\.js/);
 assert.match(doc,/France hors Mayotte jusqu'en 2010/);
 assert.match(doc,/non une preuve de causalité/);
});
test('source is openly documented and distinct from Dares and financing',()=>{
 const method=fs.readFileSync(path.join(root,'APPRENTISSAGE_SOURCES.md'),'utf8');
 assert.match(method,/93432bd9c0f7e950502544df2de2604b9ec2730e873693b8387b53b2b6800a0d/);
 assert.match(method,/SIFA/);
 assert.match(method,/Mayotte/);
 assert.match(method,/Dares/);
 assert.match(script,/fetch\(csvPath\)/);
 assert.match(script,/if\(!response\.ok\)/);
 assert.match(script,/rows\.length!==43/);
 assert.match(script,/svg\.replaceChildren\(\)/);
 assert.doesNotMatch(script,/innerHTML\s*=/);
});
