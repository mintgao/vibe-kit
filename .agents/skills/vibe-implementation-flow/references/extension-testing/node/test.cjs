const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const {spawnSync} = require('node:child_process');
const {observe} = require('./adapter.cjs');
const receipt = require('../receipt.json');
const clone = x => JSON.parse(JSON.stringify(x));
const value = observe(receipt, ['receipt','default']);
console.log('EXTENSION-ENTRY '+JSON.stringify({...value, dispatcher:process.argv.slice(2)}));
assert.deepEqual(value.findings,[]);
assert.ok(value.origin.endsWith('/bin/vibe'));
assert.equal(value.helper_origin,require.resolve('./new-helper.cjs'));
assert.equal(value.helper_function,'check');
assert.deepEqual(value.arguments,['receipt','default']);
for (const version of [true,2.5]) { const x=clone(receipt); x.schema_version=version; assert.ok(observe(x,[]).findings.includes('$')); }
for (const key of Object.keys(receipt)) { const x=clone(receipt); delete x[key]; assert.ok(observe(x,[]).findings.includes('$')); }
let x=clone(receipt); x.extra=true; assert.ok(observe(x,[]).findings.includes('$'));
x=clone(receipt); x.checks.shift(); x.summary.unconfigured--;
assert.deepEqual(x.summary, Object.fromEntries(
  Object.keys(receipt.summary).map(name =>
    [name, x.checks.filter(check => check.outcome === name).length])));
let findings=observe(x,[]).findings;
assert.ok(findings.includes('$.checks'));
assert.ok(findings.includes('$.summary'));

x=clone(receipt); x.summary.passed=1;
findings=observe(x,[]).findings;
assert.ok(findings.includes('$.summary'));
assert.ok(!findings.includes('$.checks'));

x=clone(receipt); x.cli_invoked=false;
findings=observe(x,[]).findings;
assert.ok(findings.includes('$'));
assert.ok(!findings.includes('$.summary'));
for (const [mutate,p] of [
 [x=>x.selection.coverage='partial','$.selection'],[x=>x.cli_invoked=false,'$'],
 [x=>x.checks[0].provenance.kind='agent','$.checks[0].provenance'],
 [x=>x.checks[0].outcome='Pass','$.checks[0]'],[x=>x.checks.reverse(),'$.checks'],
 [x=>x.default_order.pop(),'$.default_order']]) {x=clone(receipt);mutate(x);assert.ok(observe(x,[]).findings.includes(p));}
x=clone(receipt);x.default_order.reverse();x.checks.reverse();assert.deepEqual(observe(x,[]).findings,[]);
x=clone(receipt);x.selection={mode:'only',requested:['test'],coverage:'partial'};x.checks=[x.checks[2]];x.summary.unconfigured=1;assert.deepEqual(observe(x,[]).findings,[]);assert.notEqual(x.selection.coverage,'all-configured');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const frozen=hash(fs.readFileSync(path.join(__dirname,'../receipt.json')));
const root=fs.mkdtempSync(path.join(os.tmpdir(),'extension-node-'));
const p=path.join(root,'doctor.json');
function integrity(index) {
 const names=fs.readdirSync(root).sort();if(JSON.stringify(names)!==JSON.stringify(Object.keys(index).sort()))return false;
 return names.every(n=>{const s=fs.lstatSync(path.join(root,n));return s.isFile()&&!s.isSymbolicLink()&&hash(fs.readFileSync(path.join(root,n)))===index[n][0]&&(s.mode&0o777)===index[n][1];});
}
try {
 const good=[],bad=[];let index={};
 for(const body of [null,'{bad','{"status":"Fail"}','{"status":"Pass"}']) {
  if(fs.existsSync(p))fs.unlinkSync(p);index={};
  if(body!==null){fs.writeFileSync(p,body,{mode:0o600});index['doctor.json']=[hash(body),0o600];}
  good.push(integrity(index));let decoded={};try{if(body!==null)decoded=JSON.parse(fs.readFileSync(p,'utf8'));}catch{}
  bad.push(integrity(index)&&decoded.status==='Pass');
 }
 assert.deepEqual(good,[true,true,true,true]);assert.equal(new Set(bad).size,2);
 fs.writeFileSync(p,'changed');assert.equal(integrity(index),false);
 fs.writeFileSync(p,'{"status":"Pass"}');fs.chmodSync(p,0o700);assert.equal(integrity(index),false);
 fs.chmodSync(p,0o600);fs.writeFileSync(path.join(root,'undeclared'),'x');assert.equal(integrity(index),false);fs.unlinkSync(path.join(root,'undeclared'));
 fs.unlinkSync(p);assert.equal(integrity(index),false);
 {
  const p=process.env.VIBE_EXTENSION_DOCTOR_OUTPUT||path.join(root,'doctor.json');
  const observed=value.loader_start;
  assert.equal(observed.state,process.env.EXTENSION_DOCTOR==='generated'?'generated':'absent');
  assert.equal(observed.before_helper_import,true);
  assert.equal(fs.existsSync(p),process.env.EXTENSION_DOCTOR==='generated');
  if(fs.existsSync(p)){
   assert.equal(observed.sha256,hash(fs.readFileSync(p)));
   assert.equal(JSON.parse(fs.readFileSync(p,'utf8')).command,'doctor');
  }else assert.equal(observed.sha256,null);
  console.log('DOCTOR-LIFECYCLE '+JSON.stringify({state:observed.state,loader:'node-package-script',observed_at:'before-helper-import',sha256:observed.sha256}));
 }
 assert.equal(hash(fs.readFileSync(path.join(__dirname,'../receipt.json'))),frozen);
} finally {fs.rmSync(root,{recursive:true});}
if(!process.argv.includes('--focused')){require('./direct.cjs');require('./historical.cjs');}
