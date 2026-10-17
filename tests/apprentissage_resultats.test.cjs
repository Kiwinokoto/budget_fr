'use strict';
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'apprentissage-resultats.html'),'utf8');
const csv=fs.readFileSync(path.join(root,'data/apprentissage_parcours_2024_inserjeunes.csv'),'utf8').trim().split(/\r?\n/);
test('two different denominators cannot form a synthetic 100-person distribution',()=>{
 assert.equal(csv.length,5);
 assert.match(csv[1],/continue_studies,apprenticeship,39,final_year_enrolled/);
 assert.match(csv[2],/continue_studies,school_pathway,54,final_year_enrolled/);
 assert.match(csv[3],/salaried_employment_6m,apprenticeship,62,non_continuing_leavers/);
 assert.match(csv[4],/salaried_employment_6m,school_pathway,41,non_continuing_leavers/);
 assert.match(html,/ne peut pas les additionner/);
});
test('sourced comparative graphs and accessibility',()=>{
 for(const [title,pct] of [['Apprentissage',39],['Voie scolaire',54]]){
  assert.match(html,new RegExp(title)); assert.match(html,new RegExp('width:'+pct+'%'));
 }
 assert.match(html,/width:62%/);assert.match(html,/width:41%/);
 assert.match(html,/role="region" tabindex="0"/);
 assert.match(html,/href="\/APPRENTISSAGE_RESULTATS_SOURCES.md"/);
 assert.match(html,/20.?24/);
 assert.match(fs.readFileSync(path.join(root,'apprentissage.html'),'utf8'),/href="\/apprentissage-resultats.html"/);
});
