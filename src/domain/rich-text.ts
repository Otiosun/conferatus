/** Plain text remains authoritative; optional inline styling is whitelisted. */
export const INLINE_MARKS=['bold','italic','underline','strike'] as const;
export type InlineMark=typeof INLINE_MARKS[number];
export const RICH_FONTS=['aptos','arial','georgia'] as const;
export type RichFont=typeof RICH_FONTS[number];
export const RICH_SIZES=[12,16,18,24,30] as const;
export type RichTextRun={
 text:string;marks:InlineMark[];font?:RichFont;size?:number;color?:string;highlight?:string
};
const isHex=(x:unknown):x is string=>typeof x==='string'&&/^#[0-9a-fA-F]{6}$/.test(x);
const marksOrdered=(ms:readonly InlineMark[])=>INLINE_MARKS.filter(m=>ms.includes(m));
const sameStyle=(a:RichTextRun,b:RichTextRun)=>
 a.marks.join('|')===b.marks.join('|')&&a.font===b.font&&a.size===b.size&&
 a.color===b.color&&a.highlight===b.highlight;
export function normalizeRichTextRuns(items:readonly RichTextRun[]):RichTextRun[]{
 const result:RichTextRun[]=[];
 for(const run of items){
  if(!run.text)continue;
  const item:RichTextRun={text:run.text,marks:marksOrdered(run.marks),
   ...(run.font&&RICH_FONTS.includes(run.font)?{font:run.font}:{}),
   ...(run.size!==undefined&&RICH_SIZES.includes(run.size as typeof RICH_SIZES[number])?{size:run.size}:{}),
   ...(isHex(run.color)?{color:run.color.toLowerCase()}:{}),
   ...(isHex(run.highlight)?{highlight:run.highlight.toLowerCase()}:{})};
  const prev=result[result.length-1];
  if(prev&&sameStyle(prev,item))prev.text+=item.text;
  else result.push(item);
 }
 return result;
}
/** Session records and imported archives are untrusted, including nested properties. */
export function isRichTextRuns(value:unknown,body:string):value is RichTextRun[]{
 if(!Array.isArray(value)||value.length>2048||body.length>200000)return false;
 const keys=new Set(['text','marks','font','size','color','highlight']);let text='';
 for(const entry of value){
  if(!entry||typeof entry!=='object'||Array.isArray(entry))return false;
  const run=entry as Record<string,unknown>;
  if(Object.keys(run).some(key=>!keys.has(key))||
     typeof run.text!=='string'||!run.text||!Array.isArray(run.marks)||
     run.marks.length>4||
     !run.marks.every(m=>typeof m==='string'&&INLINE_MARKS.includes(m as InlineMark))||
     new Set(run.marks).size!==run.marks.length)return false;
  if(run.font!==undefined&&(typeof run.font!=='string'||!RICH_FONTS.includes(run.font as RichFont)))return false;
  if(run.size!==undefined&&(typeof run.size!=='number'||!RICH_SIZES.includes(run.size as typeof RICH_SIZES[number])))return false;
  if(run.color!==undefined&&!isHex(run.color))return false;
  if(run.highlight!==undefined&&!isHex(run.highlight))return false;
  text+=run.text;
  if(text.length>body.length)return false;
 }
 return text===body;
}
const safeText=(s:string)=>s.replace(/[&<>"']/g,c=>({
 '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
})[c]??c);
const tags:Record<InlineMark,string>={bold:'strong',italic:'em',underline:'u',strike:'s'};
const families:Record<RichFont,string>={
 aptos:"Aptos, 'Segoe UI', sans-serif",arial:'Arial, sans-serif',georgia:'Georgia, serif'
};
/** Output contains only escaped text, known tags and valid CSS property values. */
export function renderRichText(body:string,runs?:unknown):string{
 if(!isRichTextRuns(runs,body))return safeText(body);
 return runs.map(run=>{
  let html=safeText(run.text);
  for(const m of marksOrdered(run.marks)){const tag=tags[m];html='<'+tag+'>'+html+'</'+tag+'>';}
  const style:string[]=[];
  if(run.font)style.push('font-family:'+families[run.font]);
  if(run.size)style.push('font-size:'+run.size+'px');
  if(run.color)style.push('color:'+run.color.toLowerCase());
  if(run.highlight)style.push('background-color:'+run.highlight.toLowerCase());
  return style.length?'<span style="'+style.join(';')+'">'+html+'</span>':html;
 }).join('');
}
