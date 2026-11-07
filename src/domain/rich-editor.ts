import { normalizeRichTextRuns, RICH_FONTS, RICH_SIZES } from './rich-text.js';
import type { InlineMark, RichFont, RichTextRun } from './rich-text.js';

/** Convert browser colors to a six-digit hex; do not persist arbitrary CSS. */
function safeColor(value:string):string|undefined{
 const raw=value.trim();
 if(/^#[0-9a-fA-F]{6}$/.test(raw))return raw.toLowerCase();
 if(/^#[0-9a-fA-F]{3}$/.test(raw))return '#'+[...raw.slice(1)].map(ch=>ch+ch).join('').toLowerCase();
 const match=/^rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})(?:\s*,\s*1(?:\.0+)?)?\s*\)$/i.exec(raw);
 if(!match)return undefined;
 const numbers=match.slice(1,4).map(Number);
 if(numbers.some(n=>n>255))return undefined;
 return '#'+numbers.map(n=>n.toString(16).padStart(2,'0')).join('');
}
function safeFont(value:string):RichFont|undefined{
 const first=value.split(',')[0]?.trim().replace(/^['"]|['"]$/g,'').toLowerCase();
 return RICH_FONTS.includes(first as RichFont)?first as RichFont:undefined;
}
type Style=Omit<RichTextRun,'text'>;
/** Extract only supported marks and styles from native contenteditable nodes. */
export function runsFromEditable(editor:HTMLElement):RichTextRun[]{
 const result:RichTextRun[]=[];
 const append=(text:string,s:Style)=>{
  if(text)result.push({text,marks:[...s.marks],
   ...(s.font?{font:s.font}:{}),...(s.size?{size:s.size}:{}),
   ...(s.color?{color:s.color}:{}),...(s.highlight?{highlight:s.highlight}:{})});
 };
 const newline=()=>Boolean(result[result.length-1]?.text.endsWith('\n'));
 const visit=(node:Node,parent:Style)=>{
  if(node.nodeType===Node.TEXT_NODE){append(node.textContent??'',parent);return;}
  if(!(node instanceof HTMLElement))return;
  const tag=node.tagName.toLowerCase();
  if(tag==='br'){append('\n',parent);return;}
  if((tag==='div'||tag==='p')&&result.length&&!newline())append('\n',{marks:[]});
  const style:Style={...parent,marks:[...parent.marks]};
  const mark=(m:InlineMark)=>{if(!style.marks.includes(m))style.marks.push(m);};
  if(tag==='strong'||tag==='b')mark('bold');
  if(tag==='em'||tag==='i')mark('italic');
  if(tag==='u')mark('underline');
  if(tag==='s'||tag==='strike'||tag==='del')mark('strike');
  if(tag==='font'){
   const face=safeFont(node.getAttribute('face')??'');
   if(face)style.font=face;
   const scale:Record<string,number>={'2':12,'3':16,'4':18,'5':24,'6':30};
   const size=scale[node.getAttribute('size')??''];
   if(size)style.size=size;
   const color=safeColor(node.getAttribute('color')??'');
   if(color)style.color=color;
  }
  if(tag==='span'||tag==='font'){
   if(/^(bold|[6-9]00)$/.test(node.style.fontWeight))mark('bold');
   if(node.style.fontStyle==='italic')mark('italic');
   if(node.style.textDecorationLine.includes('underline'))mark('underline');
   if(node.style.textDecorationLine.includes('line-through'))mark('strike');
   const face=safeFont(node.style.fontFamily);
   if(face)style.font=face;
   const size=Number.parseFloat(node.style.fontSize);
   if(node.style.fontSize.endsWith('px')&&RICH_SIZES.includes(size as typeof RICH_SIZES[number]))style.size=size;
   const color=safeColor(node.style.color);
   if(color)style.color=color;
   const bg=safeColor(node.style.backgroundColor);
   if(bg)style.highlight=bg;
  }
  for(const child of node.childNodes)visit(child,style);
 };
 for(const child of editor.childNodes)visit(child,{marks:[]});
 return normalizeRichTextRuns(result);
}
