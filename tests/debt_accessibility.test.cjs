const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const file=path.resolve(__dirname,'../dette.html');
const html=fs.readFileSync(file,'utf8');

test('both debt SVGs provide descriptions and a keyboard-scrollable readable viewport',()=>{
 assert.match(html,/<svg id="history"[^>]*aria-describedby="history-description history-note"/);
 assert.match(html,/<svg id="stock-history"[^>]*aria-describedby="stock-description"/);
 assert.match(html,/\.chart-scroll svg\{min-width:900px;width:100%\}/);
 assert.match(html,/class="chart-scroll" role="region"[^>]*tabindex="0"/);
 assert.match(html,/id="history-description"/);
 assert.match(html,/id="stock-description"/);
 assert.match(html,/défiler le graphique horizontalement/);
 assert.match(html,/mode==='share'\?'% de l’encours':'Md€'/);
});

test('annual accessible table includes every official year and all distinct categories',()=>{
 assert.match(html,/<details id="annual-details"/);
 assert.match(html,/<table class="annual-table" id="annual-table">/);
 assert.match(html,/<caption id="annual-caption">/);
 assert.match(html,/<tbody id="annual-body"><\/tbody>/);
 for(const label of [
   'Année','Dépôts (Md€)','Titres courts (Md€)','Titres longs (Md€)',
   'Crédits courts (Md€)','Crédits longs (Md€)','Reste non attribué',
   'Dette brute (Md€)','Dette nette (Md€)'
 ])assert.ok(html.includes(label),label);
 assert.match(html,/for\(let y=YEAR_START;y<=YEAR_END;y\+\+\)/);
 assert.match(html,/head\.scope='row'/);
 assert.match(html,/values\.values\.includes\(null\)\?'Non calculable'/);
 assert.match(html,/value===null\?'Non renseigné'/);
 assert.match(html,/renderAnnual\(year,sector\)/);
});

test('selection status and retry focus are recoverable',()=>{
 assert.match(html,/id="selection-status"[^>]*role="status" aria-live="polite"/);
 assert.match(html,/function announceSelection\(\)/);
 assert.match(html,/yearInput\.addEventListener\('change',announceSelection\)/);
 assert.match(html,/sectorInput\.addEventListener\('change',\(\)=>\{render\(\);announceSelection\(\);\}\)/);
 assert.match(html,/async function load\(returnFocus=false\)/);
 assert.match(html,/sectorInput\.focus\(\)/);
 assert.match(html,/retry\.addEventListener\('click',\(\)=>load\(true\)\)/);
 assert.doesNotMatch(html,/\.innerHTML\s*=/);
});

test('main landmark encompasses the explorer and has separately labeled navigation',()=>{
 assert.match(html,/<nav class="atlas-nav" aria-label="Sections de l’atlas">/);
 assert.match(html,/<main id="main-content">/);
 assert.match(html,/<\/main>\s*<script>/);
 assert.equal((html.match(/<main\b/g)||[]).length,1);
});

test('instrument legend has explicit group role for its accessible name',()=>{
 assert.match(html,/<div class="legend" role="group" aria-label="Légende des instruments">/);
});
