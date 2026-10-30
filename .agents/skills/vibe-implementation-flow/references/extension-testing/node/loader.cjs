const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const output=process.env.VIBE_EXTENSION_DOCTOR_OUTPUT;
const exists=Boolean(output&&fs.existsSync(output));
const regular=exists&&fs.lstatSync(output).isFile()&&!fs.lstatSync(output).isSymbolicLink();
const raw=regular?fs.readFileSync(output):null;
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
exports.snapshot={state:regular?'generated':exists?'unavailable':'absent',exists,sha256:raw===null?null:hash(raw),path_binding_sha256:output?hash(path.resolve(output)):null,loader_origin:__filename,before_helper_import:true};
console.log('LOADER-START '+JSON.stringify(exports.snapshot));
