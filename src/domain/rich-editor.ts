import {normalizeRichTextRuns} from './rich-text.js';
import type {InlineMark,RichTextRun} from './rich-text.js';

/** Extract supported marks from the browser editor; store no raw markup. */
export function runsFromEditable(editor:HTMLElement):RichTextRun[]{
 const collected:RichTextRun[]=[];
 const add=(s:string,marks:InlineMark[])=>{if(s)collected.push({text:s,marks:[...marks]});};
 const newline=()=>collected.length>0&&collected[collected.length-1]?.text.endsWith('\n');
 const visit=(node:Node,inherited:InlineMark[])=>{
  if(node.nodeType===Node.TEXT_NODE){add(node.textContent??'',inherited);return;}
  if(!(node instanceof HTMLElement))return;
  const tag=node.tagName.toLowerCase();
  if(tag==='br'){add('\n',inherited);return;}
  if((tag==='div'||tag==='p')&&collected.length&&!newline())add('\n',[]);
  const marks=[...inherited];
  const mark=(name:InlineMark)=>{if(!marks.includes(name))marks.push(name);};
  if(tag==='strong'||tag==='b')mark('bold');
  if(tag==='em'||tag==='i')mark('italic');
  if(tag==='u')mark('underline');
  if(tag==='s'||tag==='strike'||tag==='del')mark('strike');
  if(tag==='span'){
   if(/^(bold|[6-9]00)$/.test(node.style.fontWeight))mark('bold');
   if(node.style.fontStyle==='italic')mark('italic');
   if(node.style.textDecorationLine.includes('underline'))mark('underline');
   if(node.style.textDecorationLine.includes('line-through'))mark('strike');
  }
  for(const child of node.childNodes)visit(child,marks);
 };
 for(const child of editor.childNodes)visit(child,[]);
 return normalizeRichTextRuns(collected);
}
