(function(){
  const year=document.querySelector('[data-year]'); if(year) year.textContent=new Date().getFullYear();
  const gate=document.querySelector('#age-gate'); const accept=document.querySelector('#age-accept'); const check=document.querySelector('#age-confirm'); const gateMsg=document.querySelector('#age-msg');
  function unlock(){ if(gate){gate.hidden=true; sessionStorage.setItem('fedpromptly-age-ok','yes');} }
  if(gate && sessionStorage.getItem('fedpromptly-age-ok')==='yes') unlock();
  if(accept) accept.addEventListener('click',()=>{ if(!check.checked){gateMsg.textContent='Please confirm you are 18 or older to continue.'; return;} unlock(); });
  const tabButtons=document.querySelectorAll('[data-tab]');
  tabButtons.forEach(btn=>btn.addEventListener('click',()=>{tabButtons.forEach(x=>x.classList.remove('active')); document.querySelectorAll('[data-panel]').forEach(x=>x.hidden=true); btn.classList.add('active'); const p=document.querySelector('[data-panel="'+btn.dataset.tab+'"]'); if(p)p.hidden=false;}));
})();
