(() => {
  'use strict';
  const root = document.documentElement, journey = document.querySelector('.journey');
  const stage = document.querySelector('.stage'), optics = document.querySelector('.optics');
  const copy = document.querySelector('.hero-copy'), core = document.querySelector('.core');
  const cards = [...document.querySelectorAll('.study')], emerging=document.querySelector('.emerging');
  let cardsVisible=false;
  // Original optical geometry is an immutable SVG asset; no startup DOM construction.
  const media=matchMedia('(prefers-reduced-motion: reduce)');
  const staticMode=new URLSearchParams(location.search).has('static');
  let frame=0, start=0, distance=1, mobile=false, enabled=false,lastProgress=-1;
  const clamp=x=>Math.min(1,Math.max(0,x));
  const smooth=x=>{x=clamp(x);return x*x*(3-2*x)};
  function render(p) {
    if(p===lastProgress)return;lastProgress=p;
    const show=p>.25;
    if(show!==cardsVisible){emerging.style.display=show?'block':'none';cardsVisible=show}
    optics.style.transform=`translate3d(${-p*(mobile?0:16)}%,${-p*13}%,0) rotate(${p*24}deg) scale(${1+p*1.7})`;
    optics.style.opacity=String(1-smooth((p-.3)/.4));
    optics.style.willChange=p>0&&p<.7?'transform, opacity':'auto';
    core.style.opacity=String(1-smooth(p/.35));
    copy.style.transform=`translate3d(0,${-p*110}px,0)`;
    copy.style.opacity=String(1-smooth(p/.4));
    copy.inert=p>.4;
    cards.forEach((card,i)=>{
      const q=smooth((p-.25-i*.06)/.6);
      const x=mobile?(i-1)*88:(i-1)*112;
      card.style.transform=`translate3d(calc(-50% + ${x*q}%),${(1-q)*55+i*10}px,${(q-1)*520}px) rotateY(${(1-q)*(i-1)*35}deg) rotateZ(${(i-1)*(1-q)*-12}deg)`;
      card.style.opacity=String(clamp(q*3));card.inert=q<.6;
      card.querySelector('span:last-child').style.visibility=mobile&&i!==1?'hidden':'visible';
      card.style.zIndex=String(3-Math.abs(i-1));
    });
    stage.dataset.progress=p.toFixed(3);
  }
  function update(){frame=0;if(enabled)render(clamp((scrollY-start)/distance))}
  function schedule(){if(!frame&&enabled)frame=requestAnimationFrame(update)}
  function measure(){if(!enabled)return;lastProgress=-1;start=journey.getBoundingClientRect().top+scrollY;distance=Math.max(1,journey.offsetHeight-stage.offsetHeight);mobile=innerWidth<=700;update()}
  const geometry=typeof ResizeObserver==='function'?new ResizeObserver(measure):null;
  function configure(){enabled=!media.matches&&!staticMode;root.classList.toggle('motion',enabled);if(enabled){if(geometry){geometry.observe(journey);geometry.observe(stage)}else measure()}else {cancelAnimationFrame(frame);frame=0;emerging.removeAttribute('style');cardsVisible=false;[optics,copy,core,...cards].forEach(e=>{e.removeAttribute('style');e.inert=false})}}
  addEventListener('scroll',schedule,{passive:true});if(!geometry)addEventListener('resize',measure);
  media.addEventListener('change',configure);configure();
  addEventListener('pagehide',()=>{cancelAnimationFrame(frame);frame=0;geometry?.disconnect();removeEventListener('scroll',schedule);removeEventListener('resize',measure);media.removeEventListener('change',configure)});
  addEventListener('pageshow',e=>{if(e.persisted){addEventListener('scroll',schedule,{passive:true});if(!geometry)addEventListener('resize',measure);media.addEventListener('change',configure);configure()}});
})();
