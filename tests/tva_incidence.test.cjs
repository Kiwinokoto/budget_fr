const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const home=path.resolve(__dirname,'..');
const page=fs.readFileSync(path.join(home,'tva-incidence.html'),'utf8');
const vat=fs.readFileSync(path.join(home,'data/tva_effort_bdf_2001.csv'),'utf8').trim().split(/\r?\n/);
const products=fs.readFileSync(path.join(home,'data/taxes_produits_cnd_2020_2023.csv'),'utf8').trim().split(/\r?\n/);
test('2001 VAT estimates are separate income, consumption and euros',()=>{
 assert.equal(vat.length,11);
 assert.match(vat[0],/vat_pct_gross_disposable_income/);
 assert.match(vat[0],/vat_pct_consumption/);
 assert.match(vat[1],/^1,1308,11\.52,10\.5$/);
 assert.match(vat[10],/^10,3588,5\.92,11\.6$/);
 for(const key of ['vat_pct_gross_disposable_income','vat_pct_consumption','vat_eur_per_household'])
  assert.match(page,new RegExp('value="'+key+'"'));
});
test('2020–2023 distributed product taxes are never called VAT alone',()=>{
 assert.equal(products.length,81);
 assert.match(products[0],/^year,vingtile,product_taxes_bn_eur$/);
 assert.match(products[80],/^2023,20,33\.3$/);
 assert.match(page,/TVA, TICPE, accises, DMTO/);
 assert.match(page,/Ce n'est pas une ventilation de la TVA seule/);
 assert.match(page,/Aucune valeur « TVA 2023 par décile »/);
});
test('page has navigational links and an explicit error state',()=>{
 assert.match(page,/href="\/tva-justice.html"/);
 assert.match(page,/href="\/recettes.html"/);
 assert.match(page,/Erreur de chargement|Impossible de charger les données/);
 assert.match(page,/document\.createElement\('button'\)/);
});
