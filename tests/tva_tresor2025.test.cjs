const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const home=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(home,'tva-incidence.html'),'utf8');
const method=fs.readFileSync(path.join(home,'METHODOLOGY.md'),'utf8');
const sources=fs.readFileSync(path.join(home,'DATA_SOURCES.md'),'utf8');

test('Treasury 2025 scenario shows only documented Q1, Q5 and mean effects',()=>{
  assert.match(html,/septembre 2025/);
  assert.match(html,/−0,7 %/);
  assert.match(html,/−0,4 %/);
  assert.match(html,/−0,5 %/);
  assert.match(html,/<strong>12 %<\/strong>/);
  assert.match(html,/<strong>31 %<\/strong>/);
  assert.match(html,/Q2 à Q4 ne sont pas retranscrits/);
  assert.doesNotMatch(html,/<strong>Q2<\/strong>|<strong>Q3<\/strong>|<strong>Q4<\/strong>/);
});

test('Treasury scenario is separated from 2001 estimated VAT and 2020–2023 product taxes',()=>{
  assert.match(html,/hausse uniforme de <strong>1 point/);
  assert.match(html,/comptes nationaux 2021–2022/);
  assert.match(html,/répercutée dans les prix/);
  assert.match(html,/revalorisations ultérieures/);
  assert.match(html,/href="https:\/\/www.tresor.economie.gouv.fr\/Articles\/2025\/09\/25\/analyse-de-la-composition-des-recettes-de-tva"/);
  assert.match(html,/id="head-vat"/);
  assert.match(html,/id="head-products"/);
  assert.match(method,/quintiles/);
  assert.match(sources,/recettes marginales supplémentaires/);
});
