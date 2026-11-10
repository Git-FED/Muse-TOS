(() => {
  const canvas = document.querySelector('#signal-field');
  const ctx = canvas.getContext('2d');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let w, h, dpr, t = 0, particles = [];
  const colors = ['#62e8ff', '#8f7cff', '#d46dff', '#5ef0c6'];
  const resize = () => { dpr = Math.min(devicePixelRatio || 1, 2); w = innerWidth; h = innerHeight; canvas.width=w*dpr; canvas.height=h*dpr; canvas.style.width=w+'px'; canvas.style.height=h+'px'; ctx.setTransform(dpr,0,0,dpr,0,0); particles = Array.from({length:Math.min(170, Math.floor(w*h/8500))}, (_,i)=>({ x:Math.random()*w, y:Math.random()*h, z:Math.random(), r:Math.random()*1.5+.3, c:colors[i%colors.length], vx:(Math.random()-.5)*.16, vy:(Math.random()-.5)*.16 })); };
  const glow = (x,y,r,color,alpha) => { const g=ctx.createRadialGradient(x,y,0,x,y,r); g.addColorStop(0,color+alpha); g.addColorStop(1,color+'00'); ctx.fillStyle=g; ctx.fillRect(x-r,y-r,r*2,r*2); };
  function frame() {
    t += reduce ? .001 : .006; ctx.clearRect(0,0,w,h);
    // Slow aurora interference: several drifting light wells create a non-repeating field.
    for(let i=0;i<5;i++){ const x=w*(.12+i*.2)+Math.sin(t*(.7+i*.13)+i*2.3)*w*.16; const y=h*(.18+i*.17)+Math.cos(t*(.6+i*.11)+i)*h*.13; glow(x,y,Math.max(w,h)*.34,colors[i%colors.length], i===2?'24':'18'); }
    ctx.save(); ctx.globalAlpha=.17; ctx.strokeStyle='#8391ff'; ctx.lineWidth=1;
    const gap=52, drift=(t*18)%gap; for(let x=-h;x<w+h;x+=gap) { ctx.beginPath(); ctx.moveTo(x+drift,0); ctx.lineTo(x-h+drift,h); ctx.stroke(); } for(let y=-h;y<h*2;y+=gap){ ctx.beginPath(); ctx.moveTo(0,y+drift*.6); ctx.lineTo(w,y-w*.08+drift*.6); ctx.stroke(); } ctx.restore();
    for(const p of particles){ p.x+=p.vx*(reduce?0:1); p.y+=p.vy*(reduce?0:1); if(p.x<0)p.x=w; if(p.x>w)p.x=0; if(p.y<0)p.y=h; if(p.y>h)p.y=0; ctx.beginPath(); ctx.fillStyle=p.c; ctx.globalAlpha=.18+p.z*.55; ctx.arc(p.x,p.y,p.r+p.z*1.3,0,Math.PI*2); ctx.fill(); }
    ctx.globalAlpha=1; if(!reduce) requestAnimationFrame(frame);
  }
  resize(); addEventListener('resize',resize); frame();
  const clock=document.querySelector('#clock'); const tick=()=>clock.textContent=new Date().toLocaleTimeString('en-US',{hour12:false}); tick(); setInterval(tick,1000);
})();
