const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

const root = path.join(__dirname, '..');
const axes = [
 {page:'index.html', start:1960, end:2025,
  desktop:[1960,1965,1970,1975,1980,1985,1990,1995,2000,2005,2010,2015,2020,2025],
  mobile:[1960,1970,1980,1990,2000,2010,2025]},
 {page:'fonctions.html', start:1995, end:2024,
  desktop:[1995,2000,2005,2010,2015,2020,2024],
  mobile:[1995,2005,2015,2024]},
 {page:'recettes.html', start:1995, end:2025,
  desktop:[1995,2000,2005,2010,2015,2020,2025],
  mobile:[1995,2005,2015,2025]}
];
for(const item of axes) {
 test(item.page+' : ticks + terminal year + selected year', () => {
  const html=fs.readFileSync(path.join(root,item.page),'utf8');
  const fn=html.match(/function yearTicks\(start,end,compact\)\{[\s\S]*?\n\}/);
  assert.ok(fn, 'yearTicks function exists');
  const yearTicks=vm.runInNewContext('('+fn[0]+')');
  assert.deepEqual(Array.from(yearTicks(item.start,item.end,false)), item.desktop);
  assert.deepEqual(Array.from(yearTicks(item.start,item.end,true)), item.mobile);
  assert.match(html, /stroke-dasharray['"]?\s*:\s*['"]3 7['"]|stroke-dasharray="3 7"/);
  assert.match(html,/compactQuery\.addEventListener\('change'/);
 });
}
