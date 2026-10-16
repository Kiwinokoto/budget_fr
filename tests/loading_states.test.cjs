const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname,'..');
for (const name of ['recettes.html','tva-incidence.html']) {
  const html = fs.readFileSync(path.join(root,name),'utf8');
  test(name + ' explicitly distinguishes loading, loaded, and failed-data states',()=>{
    assert.match(html,/<body class="loading-data">/);
    assert.match(html,/id="load-status" role="status" aria-live="polite">Chargement des données…/);
    assert.match(html,/body\.loading-data [^{]*\{display:none\}/);
    assert.match(html,/document\.body\.classList\.remove\('loading-data'\)/);
    assert.match(html,/document\.getElementById\('load-status'\)\.hidden=true/);
    assert.match(html,/status\.textContent='Impossible de charger les données : '/);
    assert.match(html,/retry\.textContent='Réessayer'/);
    assert.match(html,/window\.location\.reload\(\)/);
  });
}
