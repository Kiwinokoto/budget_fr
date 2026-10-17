const test=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const doc=fs.readFileSync(path.join(root,'apprentissage-contexte.html'),'utf8');
const js=fs.readFileSync(path.join(root,'jeunes-contexte.js'),'utf8');
const cols=['age_group','sex','study_only','study_and_work','work_only','unemployed','other_inactive','source_id'];
const content=fs.readFileSync(path.join(root,'data/jeunes_situations_2024_insee.csv'),'utf8').trim().split(/\r?\n/);
const header=content.shift().split(',');
const rows=content.map(x=>Object.fromEntries(x.split(',').map((value,i)=>[header[i],value])));
test('Insee EEC 2024 source categories exclusive, six profiles only',()=>{
 assert.deepEqual(header,cols);assert.equal(rows.length,6);
 for(const row of rows){
  assert.ok(['women','men'].includes(row.sex));
  assert.ok(['18-20','21-24','25-29'].includes(row.age_group));
  assert.equal(row.source_id,'insee_fps2025_figure2_eec2024');
  assert.ok(Math.abs(cols.slice(2,7).reduce((sum,k)=>sum+Number(row[k]),0)-100)<0.11);
 }
 assert.deepEqual([rows[0].study_only,rows[0].study_and_work,rows[0].work_only,rows[0].unemployed,rows[0].other_inactive],
 ['58.0','17.4','11.0','5.2','8.3']);
});
test('2024 demographic numerator never misused as apprenticeship cohort denominator',()=>{
 const values=fs.readFileSync(path.join(root,'data/jeunes_population_2024_par_age.csv'),'utf8').trim().split(/\r?\n/);
 assert.equal(values.length,16);
 const totals=values.slice(1).map(v=>v.split(',')).filter(v=>Number(v[1])>=18&&Number(v[1])<=25);
 assert.equal(totals.length,8);
 assert.equal(totals.reduce((sum,v)=>sum+Number(v[2]),0),6375226);
 assert.match(doc,/6 375 226/);assert.match(doc,/1 049 965/);assert.match(doc,/3 012 800/);
 assert.match(doc,/pas le dénominateur exact/);
 assert.match(doc,/ne se soustraient pas et ne s’additionnent pas/);
});
test('real donut selectable group and gender, accessible source table',()=>{
 for(const age of ['18-20','21-24','25-29'])assert.match(doc,new RegExp('name="age-group" value="'+age+'"'));
 for(const sex of ['women','men'])assert.match(doc,new RegExp('name="sex" value="'+sex+'"'));
 assert.match(doc,/id="youth-donut" role="img" aria-label=/);
 assert.match(doc,/id="youth-data-rows"/);
 assert.match(js,/fetch\(src\)/);assert.match(js,/setAttribute\('aria-label'/);
 assert.match(js,/renderTable\(\);paint\(\)/);
 assert.match(js,/total=categories\.reduce/);
 assert.doesNotMatch(js,/innerHTML\s*=/);
 assert.match(doc,/href="\/apprentissage.html"/);
 assert.match(fs.readFileSync(path.join(root,'apprentissage.html'),'utf8'),/href="\/apprentissage-contexte.html"/);
 assert.match(doc,/JEUNES_CONTEXTE_SOURCES\.md/);
});
