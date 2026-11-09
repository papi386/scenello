(() => {
 'use strict';
 const root=document.documentElement,sequence=document.querySelector('.sequence'),stage=document.querySelector('.stage');
 const fan=document.querySelector('.fan'),copy=document.querySelector('.statement'),cards=[...document.querySelectorAll('.sample')];
 const media=matchMedia('(prefers-reduced-motion: reduce)');
 const staticMode=new URLSearchParams(location.search).has('static');
 let frame=0,start=0,distance=1,mobile=false,enabled=false,lastProgress=-1;
 const clamp=x=>Math.min(1,Math.max(0,x));
 const smooth=x=>{x=clamp(x);return x*x*(3-2*x)};
 function render(p){
   if(p===lastProgress)return;lastProgress=p;
   const turn=smooth(p/.75),spread=smooth((p-.3)/.7);
   fan.style.transform=`translate3d(${spread*(mobile?0:8)}%,0,0) rotate3d(.3,.8,.15,${-turn*42}deg)`;
   cards.forEach((card,i)=>{
    const theta=(i-1)*(13+spread*(mobile?9:24));
    card.style.transform=`translate3d(${(i-1)*(13+spread*(mobile?23:55))}%,${-spread*(i===1?20:0)}px,${spread*(i===1?110:-50)}px) rotate(${theta}deg) rotateY(${spread*(i-1)*-12}deg)`;
    card.style.zIndex=String(i===1?3:2);
   });
   copy.style.transform=`translate3d(0,${-p*50}px,0)`;
   // Text remains legible; the scene never needs to gate the catalogue.
   stage.dataset.progress=p.toFixed(3);
 }
 function update(){frame=0;if(enabled)render(clamp((scrollY-start)/distance))}
 function schedule(){if(enabled&&!frame)frame=requestAnimationFrame(update)}
 function measure(){if(!enabled)return;lastProgress=-1;start=sequence.getBoundingClientRect().top+scrollY;distance=Math.max(1,sequence.offsetHeight-stage.offsetHeight);mobile=innerWidth<=800;update()}

 // Read geometry after native layout; do not force a first-paint layout inside script evaluation.
 const geometry='ResizeObserver' in window?new ResizeObserver(measure):null;
 function configure(){enabled=!media.matches&&!staticMode;root.classList.toggle('motion',enabled);if(enabled){if(geometry){geometry.observe(sequence);geometry.observe(stage)}else measure()}else{cancelAnimationFrame(frame);frame=0;[fan,copy,...cards].forEach(e=>e.removeAttribute('style'));cards.forEach((c,i)=>c.style.setProperty('--n',i))}}
 document.querySelector('.filters').hidden=false;
 document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{
   const filter=button.dataset.filter;
   document.querySelectorAll('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
   let count=0;document.querySelectorAll('article[data-kind]').forEach(a=>{a.hidden=filter!=='all'&&a.dataset.kind!==filter;if(!a.hidden)count++});
   document.querySelector('#result-count').textContent=`${count} materials shown`;
 }));
 // A direct sample link always reveals its destination, even after filtering.
 function revealHash(){let id;try{id=decodeURIComponent(location.hash.slice(1))}catch{return;}const target=document.getElementById(id);if(target?.matches('article')){document.querySelector('[data-filter="all"]').click();target.scrollIntoView()}}
 addEventListener('hashchange',revealHash);
 addEventListener('scroll',schedule,{passive:true});if(!geometry)addEventListener('resize',measure);media.addEventListener('change',configure);configure();revealHash();
 addEventListener('pagehide',()=>{cancelAnimationFrame(frame);frame=0;geometry?.disconnect();removeEventListener('scroll',schedule);removeEventListener('resize',measure);removeEventListener('hashchange',revealHash);media.removeEventListener('change',configure)});
 addEventListener('pageshow',e=>{if(e.persisted){addEventListener('scroll',schedule,{passive:true});if(!geometry)addEventListener('resize',measure);addEventListener('hashchange',revealHash);media.addEventListener('change',configure);configure()}});
})();
