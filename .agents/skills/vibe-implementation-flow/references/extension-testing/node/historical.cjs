require('node:assert/strict').deepEqual({legacy:1},{legacy:1});
const assert=require('node:assert/strict');const value=require('./historical-helper.cjs').check(require('../receipt.json'),'legacy');assert.deepEqual(value.arguments,['legacy']);assert.deepEqual(value.findings,[]);
