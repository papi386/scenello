// Prepare exact reading fonts in bounded idle slices; never alter the scene or its timing.
(() => {
 'use strict';
 if(!window.requestIdleCallback||!document.fonts)return;
 let frame=0,idle=0,disposed=false,index=0,attempts=0,started=0,canvas=null,context=null;
 const nodes=[],seen=new Set();
 function stop(){
  disposed=true;cancelAnimationFrame(frame);cancelIdleCallback(idle);frame=idle=0;
  nodes.length=0;seen.clear();if(canvas)canvas.width=canvas.height=0;canvas=context=null;
  removeEventListener('pagehide',stop);removeEventListener('visibilitychange',visibility);
 }
 function visibility(){if(document.hidden)stop()}
 function prepare(deadline){
  idle=0;
  if(disposed||document.hidden||!document.documentElement.classList.contains('motion')||++attempts>60||performance.now()-started>1500){stop();return}
  if(deadline.timeRemaining()>=8){
   const begin=performance.now();
   while(index<nodes.length&&performance.now()-begin<2){
    const node=nodes[index++],style=getComputedStyle(node);
    const font=`${style.fontStyle} ${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
    const key=font+' '+style.letterSpacing;
    if(seen.has(key))continue;
    seen.add(key);context.font=font;context.letterSpacing=style.letterSpacing;
    context.measureText(node.textContent);break;
   }
  }
  if(index<nodes.length)idle=requestIdleCallback(prepare);else stop();
 }
 frame=requestAnimationFrame(()=>{frame=requestAnimationFrame(()=>{
  frame=0;if(disposed||document.hidden||!document.documentElement.classList.contains('motion'))return;
  document.fonts.ready.then(()=>{
   if(disposed)return;
   nodes.push(...document.querySelectorAll('.study>span:last-child,.study b,#catalogue h2,#catalogue h3,#catalogue p,#catalogue summary,#catalogue button,#research h2,#research h3,#research p,#research summary'));
   canvas=document.createElement('canvas');canvas.width=canvas.height=1;context=canvas.getContext('2d');
   if(!context){stop();return}started=performance.now();idle=requestIdleCallback(prepare);
  });
 })});
 addEventListener('pagehide',stop);addEventListener('visibilitychange',visibility);
})();
