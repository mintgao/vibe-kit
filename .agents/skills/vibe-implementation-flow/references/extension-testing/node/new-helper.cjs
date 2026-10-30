const {spawnSync}=require('node:child_process');
const path=require('node:path');
exports.check=function check(receipt,...args) {
 const result=spawnSync(process.env.PYTHON||'python3',['-B',path.join(__dirname,'../bridge.py'),...args],{input:JSON.stringify(receipt),encoding:'utf8'});
 if(result.status!==0)throw Error('production validator bridge unavailable');
 return JSON.parse(result.stdout);
};
