import test from 'node:test';
import assert from 'node:assert/strict';
import {
  migrateLegacyRichText, projectRichBlocksToLegacy,
  splitRichParagraph, joinRichParagraphs,
  insertHorizontalRule, removeHorizontalRule,
  isRichBlockDocument
} from '../dist/domain/rich-blocks.js';
import { normalizeRichTextRuns } from '../dist/domain/rich-text.js';

const baseline = migrateLegacyRichText({body:'AlphaBeta'}).value;

test('every UTF-16 cursor boundary can split and reunite plain paragraphs losslessly',()=>{
 for(let offset=0;offset<='AlphaBeta'.length;offset++){
  const split=splitRichParagraph(baseline,0,offset);
  assert.equal(split.ok,true);
  assert.equal(split.value.blocks.length,2);
  const joined=joinRichParagraphs(split.value,0);
  assert.equal(joined.ok,true);
  assert.deepEqual(joined.value,baseline);
  assert.deepEqual(projectRichBlocksToLegacy(joined.value),
   {ok:true,value:{body:'AlphaBeta'}});
 }
});

test('split and join preserve mixed font, link, subscript and adjacent runs exactly',()=>{
 const a='H2O e documento com link externo';
 const runs=[
  {text:'H',marks:['bold'],color:'#123abc'},
  {text:'2',marks:['subscript']},
  {text:'O e ',marks:[]},
  {text:'documento',marks:['italic'],href:'https://example.com/'},
  {text:' com link externo',marks:['underline']}
 ];
 const from=migrateLegacyRichText({body:a,bodyRuns:runs});
 assert.equal(from.ok,true);
 const original=structuredClone(from.value);
 for(const at of [0,1,2,3,4,7,8,13,a.length]){
  const split=splitRichParagraph(from.value,0,at);
  assert.equal(split.ok,true,'failed at offset '+at);
  assert.equal(isRichBlockDocument(split.value),true);
  assert.equal(split.value.blocks.map(b=>b.text??'').join(''),a);
  const restored=joinRichParagraphs(split.value,0);
  assert.equal(restored.ok,true);
  const result=projectRichBlocksToLegacy(restored.value);
  assert.equal(result.ok,true);
  assert.equal(result.value.body,a);
  assert.deepEqual(normalizeRichTextRuns(result.value.bodyRuns),normalizeRichTextRuns(runs));
  assert.deepEqual(from.value,original);
 }
});

test('split never corrupts Unicode surrogate pairs and supports grapheme-safe boundaries',()=>{
 const source=migrateLegacyRichText({body:'A🌙B'}).value;
 assert.deepEqual(splitRichParagraph(source,0,2),
  {ok:false,reason:'invalid-position'});
 const split=splitRichParagraph(source,0,3);
 assert.equal(split.ok,true);
 const joined=joinRichParagraphs(split.value,0);
 assert.equal(joined.ok,true);
 assert.equal(projectRichBlocksToLegacy(joined.value).value.body,'A🌙B');
});

test('rules are structural barriers; Backspace may not merge across one',()=>{
 const start=migrateLegacyRichText({body:'Antes\nDepois'}).value;
 const withRule=insertHorizontalRule(start,0).value;
 assert.deepEqual(joinRichParagraphs(withRule,0),
  {ok:false,reason:'invalid-position'});
 assert.deepEqual(joinRichParagraphs(withRule,1),
  {ok:false,reason:'invalid-position'});
 const split=splitRichParagraph(withRule,0,2);
 assert.equal(split.ok,true);
 assert.equal(split.value.blocks[2].type,'horizontalRule');
 const remove=removeHorizontalRule(split.value,2);
 assert.equal(remove.ok,true);
 const join=joinRichParagraphs(remove.value,0);
 assert.equal(join.ok,true);
 assert.deepEqual(projectRichBlocksToLegacy(join.value),
  {ok:true,value:{body:'Antes\nDepois'}});
});

test('all mutations are immutable including nested marks and layout',()=>{
 const layout={align:'justify',left:16,right:32,lineHeight:2};
 const source=migrateLegacyRichText({body:'AB',bodyRuns:[
  {text:'A',marks:['bold'],color:'#aabbcc'},
  {text:'B',marks:['italic']}
 ],bodyLayout:layout}).value;
 const split=splitRichParagraph(source,0,1).value;
 split.blocks[0].text='X';
 split.blocks[1].runs[0].marks.push('underline');
 split.layout.left=0;
 assert.equal(source.blocks[0].text,'AB');
 assert.deepEqual(source.blocks[0].runs[1].marks,['italic']);
 assert.equal(source.layout.left,16);
 const join=joinRichParagraphs(source,0);
 assert.deepEqual(join,{ok:false,reason:'invalid-position'});
});

test('reject invalid offsets, invalid documents and 1024-block overflow without modification',()=>{
 for(const offset of [-1,0.5,Number.NaN,999,Infinity]){
  assert.deepEqual(splitRichParagraph(baseline,0,offset),
   {ok:false,reason:'invalid-position'});
 }
 for(const index of [-1,0.5,1,999]){
  assert.deepEqual(joinRichParagraphs(baseline,index),
   {ok:false,reason:'invalid-position'});
 }
 const maximum=migrateLegacyRichText({body:'x\n'.repeat(1023)}).value;
 const snapshot=structuredClone(maximum);
 assert.deepEqual(splitRichParagraph(maximum,0,1),
  {ok:false,reason:'limit-exceeded'});
 assert.deepEqual(maximum,snapshot);
 assert.deepEqual(splitRichParagraph({version:2,blocks:[]},0,0),
  {ok:false,reason:'invalid-document'});
 assert.deepEqual(joinRichParagraphs({version:1,blocks:[{type:'table'}]},0),
  {ok:false,reason:'invalid-document'});
});


test('split refuses combining accents, skin tones, joined emoji and flags as partial graphemes',()=>{
 const examples=[
  {body:'e\u0301x',rejected:[1],accepted:[0,2,3]},
  {body:'👩🏽‍💻x',rejected:[2,3,4,5,6],accepted:[0,7,8]},
  {body:'🇧🇷!',rejected:[1,2,3],accepted:[0,4,5]},
  {body:'a\u0308\u0301z',rejected:[1,2],accepted:[0,3,4]}
 ];
 for(const {body,rejected,accepted} of examples){
  const from=migrateLegacyRichText({body});
  assert.equal(from.ok,true,body);
  for(const offset of rejected){
   assert.deepEqual(splitRichParagraph(from.value,0,offset),
    {ok:false,reason:'invalid-position'},body+' offset '+offset);
  }
  for(const offset of accepted){
   const split=splitRichParagraph(from.value,0,offset);
   assert.equal(split.ok,true,body+' offset '+offset);
   const joined=joinRichParagraphs(split.value,0);
   assert.deepEqual(joined,{ok:true,value:from.value});
  }
 }
});

test('split also rejects a grapheme boundary hidden inside different formatting runs',()=>{
 const body='e\u0301 pronto';
 const rich=migrateLegacyRichText({body,bodyRuns:[
  {text:'e',marks:['bold']},
  {text:'\u0301 pronto',marks:['italic'],href:'https://example.com/'}
 ]});
 assert.equal(rich.ok,true);
 const unchanged=structuredClone(rich.value);
 assert.deepEqual(splitRichParagraph(rich.value,0,1),
  {ok:false,reason:'invalid-position'});
 const okay=splitRichParagraph(rich.value,0,2);
 assert.equal(okay.ok,true);
 assert.equal(projectRichBlocksToLegacy(joinRichParagraphs(okay.value,0).value).value.body,body);
 assert.deepEqual(rich.value,unchanged);
});

test('unavailable grapheme segmenter fails closed without affecting empty/end splits',()=>{
 const from=migrateLegacyRichText({body:'Abc'}).value;
 const descriptor=Object.getOwnPropertyDescriptor(Intl,'Segmenter');
 assert.equal(typeof Intl.Segmenter,'function');
 try{
  Object.defineProperty(Intl,'Segmenter',{configurable:true,writable:true,value:undefined});
  assert.deepEqual(splitRichParagraph(from,0,1),
   {ok:false,reason:'invalid-position'});
  assert.equal(splitRichParagraph(from,0,0).ok,true);
  assert.equal(splitRichParagraph(from,0,3).ok,true);
 }finally{
  if(descriptor)Object.defineProperty(Intl,'Segmenter',descriptor);
 }
});
