const loader=require('./loader.cjs');
exports.observe=(receipt,args)=>{
 const resolved=require.resolve(process.env.EXTENSION_ORIGIN==='old'?'./historical-helper.cjs':'./new-helper.cjs');
 const loaded=require(resolved);
 const actual=process.env.EXTENSION_ARGUMENT?['WRONG']:args;
 const value=loaded.check(receipt,...actual);
 value.helper_origin=require.cache[resolved].filename;value.helper_function=loaded.check.name;value.loader_start=loader.snapshot;
 return value;
};
