(function(){
  var root=document.documentElement;
  var calm=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Menu */
  var burger=document.querySelector('.burger'), menu=document.getElementById('menu');
  function setMenu(o){var was=root.classList.contains('open');root.classList.toggle('open',o);[].forEach.call(document.querySelectorAll('main,footer'),function(el){if(o)el.setAttribute('inert','');else el.removeAttribute('inert')});if(o&&!was&&innerWidth<=1100){var f1=kbOpen?menu.querySelector('a'):menu;if(f1)setTimeout(function(){f1.focus({preventScroll:true})},50)}if(!o&&was&&menu.contains(document.activeElement))burger.focus();burger.setAttribute('aria-expanded',o);burger.setAttribute('aria-label',o?'Close menu':'Open menu');document.body.style.overflow=o?'hidden':''}
  /* Tap opens focus the menu itself (no focus ring on the first link); keyboard opens focus the first link */
  var kbOpen=false;menu.setAttribute('tabindex','-1');
  burger.addEventListener('click',function(e){kbOpen=e.detail===0;setMenu(!root.classList.contains('open'))});
  /* Picking a section: the other links fade, the page moves to the section behind the menu, then the menu ripples closed to reveal it */
  var leaving=false;
  menu.addEventListener('click',function(e){
    var a=e.target.closest('a');if(!a)return;
    var t=a.hash&&a.pathname===location.pathname&&document.getElementById(a.hash.slice(1));
    var animate=t&&root.classList.contains('open')&&innerWidth<=1100&&!matchMedia('(prefers-reduced-motion: reduce)').matches;
    if(!animate){setMenu(false);return}
    e.preventDefault();if(leaving)return;leaving=true;
    a.classList.add('picked');root.classList.add('menu-leaving');
    setTimeout(function(){
      t.scrollIntoView({behavior:'instant',block:'start'});
      if(history.pushState)history.pushState(null,'',a.hash);
      setMenu(false);
      setTimeout(function(){root.classList.remove('menu-leaving');a.classList.remove('picked');leaving=false},650);
    },260);
  });
  document.addEventListener('keydown',function(e){if(e.key==='Escape')setMenu(false)});
  window.addEventListener('resize',function(){if(innerWidth>1100)setMenu(false)});

  /* Hero: noise drifts down, one current runs upstream and parts it */
  var c=document.getElementById('flow');
  if(c){
  var x=c.getContext('2d'), W=0,H=0,D=Math.min(window.devicePixelRatio||1,2);
  var noise=[],up=[],mx=-9999,my=-9999,t=0,live=false,raf=0;
  function band(){return Math.max(46,W*.075)}
  function mid(y){return W*(W>860?.74:.66)+Math.sin(y*.0055+t*.0007)*W*.06+Math.sin(y*.013+1.7+t*.0004)*W*.022}
  function seed(){
    noise=[];up=[];
    var n=Math.min(280,Math.round(W*H/4600)),m=Math.min(110,Math.round(H/7)),i;
    for(i=0;i<n;i++)noise.push({x:Math.random()*W,y:Math.random()*H,v:.35+Math.random()*1.3,l:5+Math.random()*20,a:.07+Math.random()*.24,p:Math.random()*6.28});
    for(i=0;i<m;i++)up.push({y:Math.random()*H,o:(Math.random()*2-1)*Math.pow(Math.random(),.7),v:1.4+Math.random()*2.6,l:26+Math.random()*70,w:.7+Math.random()*1.7,b:Math.random()<.18});
  }
  function size(){
    var r=c.getBoundingClientRect();if(!r.width)return;
    W=r.width;H=r.height;c.width=Math.round(W*D);c.height=Math.round(H*D);x.setTransform(D,0,0,D,0,0);seed();if(!live)draw();
  }
  function draw(){
    x.clearRect(0,0,W,H);
    var b=band(),i,p,y,dx,dy,d;
    /* glow of the current */
    x.lineCap='round';x.lineJoin='round';
    [[b*2.6,.045],[b*1.5,.06],[b*.6,.08]].forEach(function(g){
      x.beginPath();for(y=-40;y<=H+40;y+=24){if(y===-40)x.moveTo(mid(y),y);else x.lineTo(mid(y),y)}
      x.strokeStyle='rgba(109,148,255,'+g[1]+')';x.lineWidth=g[0];x.stroke();
    });
    /* noise */
    x.lineWidth=1;
    for(i=0;i<noise.length;i++){
      p=noise[i];
      if(live){
        p.y+=p.v;p.x+=Math.sin(p.y*.012+p.p)*.35-.12;
        d=p.x-mid(p.y);if(Math.abs(d)<b*1.25)p.x+=(d<0?-1:1)*(1.6-Math.abs(d)/(b*1.25));
        dx=p.x-mx;dy=p.y-my;d=dx*dx+dy*dy;if(d<16900){d=Math.sqrt(d)||1;p.x+=dx/d*2.4;p.y+=dy/d*1.2}
        if(p.y-p.l>H){p.y=-4;p.x=Math.random()*W}
        if(p.x<-10)p.x=W+8;if(p.x>W+10)p.x=-8;
      }
      x.strokeStyle='rgba(153,185,255,'+p.a+')';
      x.beginPath();x.moveTo(p.x,p.y);x.lineTo(p.x+.12*p.l,p.y-p.l);x.stroke();
    }
    /* the current */
    for(i=0;i<up.length;i++){
      p=up[i];
      if(live){p.y-=p.v;if(p.y+p.l<0){p.y=H+p.l*Math.random()}}
      var x0=mid(p.y)+p.o*b,x1=mid(p.y+p.l)+p.o*b;
      var g=x.createLinearGradient(x0,p.y,x1,p.y+p.l);
      g.addColorStop(0,p.b?'rgba(255,255,255,.95)':'rgba(109,148,255,.95)');
      g.addColorStop(1,'rgba(109,148,255,0)');
      x.strokeStyle=g;x.lineWidth=p.w;
      x.beginPath();x.moveTo(x0,p.y);x.quadraticCurveTo(mid(p.y+p.l*.5)+p.o*b,p.y+p.l*.5,x1,p.y+p.l);x.stroke();
    }
  }
  function loop(){t+=16;draw();raf=requestAnimationFrame(loop)}
  function start(){if(live||calm||root.classList.contains('motion-paused'))return;live=true;raf=requestAnimationFrame(loop)}
  function stop(){live=false;cancelAnimationFrame(raf)}
  window.udFlow={start:start,stop:stop};
  size();
  var rz;window.addEventListener('resize',function(){clearTimeout(rz);rz=setTimeout(size,150)});
  var hero=document.querySelector('.hero');
  hero.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect();mx=e.clientX-r.left;my=e.clientY-r.top});
  hero.addEventListener('pointerleave',function(){mx=my=-9999});
  if('IntersectionObserver' in window){new IntersectionObserver(function(en){en[0].isIntersecting?start():stop()}).observe(hero)}else{start()}
  document.addEventListener('visibilitychange',function(){document.hidden?stop():start()});
  }

  /* Testimonial tabs */
  var tabs=[].slice.call(document.querySelectorAll('.tabs [role=tab]'));
  function pick(i,focus){
    tabs.forEach(function(tb,k){var on=k===i;tb.setAttribute('aria-selected',on);tb.tabIndex=on?0:-1;document.getElementById('voice-'+k).hidden=!on});
    if(focus)tabs[i].focus();
  }
  tabs.forEach(function(tb,i){
    tb.addEventListener('click',function(){pick(i)});
    tb.addEventListener('keydown',function(e){
      if(e.key==='ArrowRight'){e.preventDefault();pick((i+1)%tabs.length,true)}
      if(e.key==='ArrowLeft'){e.preventDefault();pick((i-1+tabs.length)%tabs.length,true)}
      if(e.key==='Home'){e.preventDefault();pick(0,true)}
      if(e.key==='End'){e.preventDefault();pick(tabs.length-1,true)}
    });
  });


  /* Client logo strip: auto-scrolls, and visitors can drag, swipe or trackpad-scroll it */
  var mq=document.getElementById('marquee'),strip=mq&&mq.parentElement;
  if(mq&&strip){
    if(!calm){[].slice.call(mq.children).forEach(function(a){var k=a.cloneNode(true);k.setAttribute('aria-hidden','true');k.tabIndex=-1;mq.appendChild(k)})}
    var looped=!calm,pos=0,hold=0,hover=false,dragging=false,startX=0,startPos=0,moved=0,lastT=0;
    function half(){return mq.scrollWidth/2}
    function wrap(){if(!looped)return;var h=half();if(h<=0)return;if(strip.scrollLeft>=h){strip.scrollLeft-=h;pos-=h}else if(strip.scrollLeft<1){strip.scrollLeft+=h;pos+=h}}
    function pauseFor(ms){hold=Math.max(hold,performance.now()+ms)}
    strip.addEventListener('scroll',function(){if(!dragging)wrap();if(Math.abs(strip.scrollLeft-pos)>1.5)pos=strip.scrollLeft},{passive:true});
    strip.addEventListener('mouseenter',function(){hover=true});
    strip.addEventListener('mouseleave',function(){hover=false;pauseFor(800)});
    strip.addEventListener('wheel',function(){pauseFor(2500)},{passive:true});
    strip.addEventListener('touchstart',function(){pauseFor(3000)},{passive:true});
    strip.addEventListener('focusin',function(){pauseFor(4000)});
    strip.addEventListener('pointerdown',function(e){
      if(e.pointerType!=='mouse'||e.button!==0)return;
      dragging=true;moved=0;startX=e.clientX;startPos=strip.scrollLeft;strip.classList.add('dragging');pauseFor(3000);
    });
    window.addEventListener('pointermove',function(e){
      if(!dragging)return;var dx=e.clientX-startX;moved=Math.max(moved,Math.abs(dx));strip.scrollLeft=startPos-dx;
      if(looped){var h=half();if(strip.scrollLeft>=h){startPos-=h;strip.scrollLeft-=h}else if(strip.scrollLeft<1){startPos+=h;strip.scrollLeft+=h}}
      pauseFor(3000);
    });
    function endDrag(){if(!dragging)return;dragging=false;pauseFor(2000);setTimeout(function(){strip.classList.remove('dragging')},0)}
    ['pointerup','pointercancel','mouseup','blur'].forEach(function(ev){window.addEventListener(ev,endDrag)});
    window.addEventListener('pointermove',function(e){if(dragging&&e.pointerType==='mouse'&&e.buttons===0)endDrag()});
    strip.addEventListener('click',function(e){if(moved>6){e.preventDefault();e.stopPropagation();moved=0}},true);
    strip.addEventListener('dragstart',function(e){e.preventDefault()});
    if(looped){
      var vis=true;
      if('IntersectionObserver' in window)new IntersectionObserver(function(en){vis=en[0].isIntersecting}).observe(strip);
      (function tick(t){
        var dt=lastT?Math.min(64,t-lastT):16;lastT=t;
        if(vis&&!hover&&!dragging&&t>hold&&!document.hidden&&!root.classList.contains('motion-paused')){
          pos+=dt*0.035;strip.scrollLeft=pos;if(strip.scrollLeft>=half()){pos-=half();strip.scrollLeft=pos}
        }
        requestAnimationFrame(tick);
      })(0);
      requestAnimationFrame(function(){pos=strip.scrollLeft=1});
    }
  }

  /* Contact form */
  var form=document.getElementById('contactForm'), status=document.getElementById('status');
  if(form)form.addEventListener('submit',function(e){
    e.preventDefault();
    var bad=null;
    [].forEach.call(form.querySelectorAll('[required]'),function(f){var ok=f.value.trim()!==''&&f.checkValidity();f.classList.toggle('bad',!ok);if(ok){f.removeAttribute('aria-invalid');f.removeAttribute('aria-describedby')}else{f.setAttribute('aria-invalid','true');f.setAttribute('aria-describedby','status')}if(!ok&&!bad)bad=f});
    if(bad){status.textContent='Add your email, phone and a message, then send again.';bad.focus();return}
    var endpoint=form.dataset.endpoint;
    if(!endpoint){status.textContent='This form isn’t connected to an inbox yet. Call +1 (860) 450-6983 or email info@getupstreamdigital.com.';return}
    status.textContent='Sending…';
    fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(new FormData(form)).toString()})
      .then(function(r){if(!r.ok)throw 0;form.reset();status.textContent='Message sent. We’ll be in touch shortly.'})
      .catch(function(){status.textContent='The message didn’t send. Call or email us instead.'});
  });

  /* ===== Revamp: header state, progress, reveals, spotlight, counters, process line ===== */
  var bar=document.querySelector('.bar');
  var prog=document.createElement('div');prog.className='progress';prog.setAttribute('aria-hidden','true');document.body.appendChild(prog);
  var lastY=window.scrollY,ticking=false;
  var flows=[].slice.call(document.querySelectorAll('.flow'));
  function onScroll(){
    var y=window.scrollY,max=document.documentElement.scrollHeight-innerHeight;
    prog.style.setProperty('--p',max>0?Math.min(1,y/max):0);
    if(bar){
      bar.classList.toggle('scrolled',y>24);
      var down=y>lastY+4,up=y<lastY-4;
      if(down&&y>420&&!root.classList.contains('open')&&!bar.contains(document.activeElement))bar.classList.add('hide');
      else if(up||y<=420)bar.classList.remove('hide');
    }
    lastY=y;
    if(!calm)flows.forEach(function(f){
      var r=f.getBoundingClientRect(),mark=innerHeight*.62;
      var vertical=innerWidth<=860;
      var lis=[].slice.call(f.children),fill;
      if(vertical){fill=(mark-r.top)/r.height}
      else{fill=(mark-r.top)/(Math.max(r.height,1)*.55)}
      fill=Math.max(0,Math.min(1,fill));
      f.style.setProperty('--fill',fill.toFixed(3));
      lis.forEach(function(li,i){
        var on=vertical?li.getBoundingClientRect().top<mark:fill>=i/Math.max(lis.length-1,1)-.001&&fill>0;
        li.classList.toggle('on',on);
      });
    });
    ticking=false;
  }
  window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(onScroll)}},{passive:true});
  window.addEventListener('resize',onScroll);
  if(bar)bar.addEventListener('focusin',function(){bar.classList.remove('hide')});

  /* Active nav link (homepage sections) */
  var navLinks=[].slice.call(document.querySelectorAll('.menu a[href^="#"]:not(.btn)'));
  if('IntersectionObserver' in window&&navLinks.length){
    var secObs=new IntersectionObserver(function(en){en.forEach(function(e){
      if(e.isIntersecting)navLinks.forEach(function(a){a.classList.toggle('active',a.getAttribute('href')==='#'+e.target.id)});
    })},{rootMargin:'-45% 0px -50% 0px'});
    navLinks.forEach(function(a){var t=document.querySelector(a.getAttribute('href'));if(t)secObs.observe(t)});
  }

  /* Spotlight that follows the pointer */
  var spotSel='.quad li,.work-card,.svc-card,.case-stats li,.cs-quote';
  [].forEach.call(document.querySelectorAll(spotSel),function(el){el.classList.add('spot')});
  if(window.matchMedia('(hover:hover)').matches){
    document.addEventListener('pointermove',function(e){
      var el=e.target.closest&&e.target.closest('.spot');if(!el)return;
      var r=el.getBoundingClientRect();el.style.setProperty('--mx',(e.clientX-r.left)+'px');el.style.setProperty('--my',(e.clientY-r.top)+'px');
    },{passive:true});
  }

  /* Count-up numbers */
  function countUp(el){
    var end=+el.dataset.count,t0=null,d=1400;
    function step(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/d),e=1-Math.pow(1-k,3);el.textContent=Math.round(end*e);if(k<1)requestAnimationFrame(step)}
    el.textContent='0';requestAnimationFrame(step);
  }

  /* Scroll reveal */
  if(!calm&&'IntersectionObserver' in window){
    root.classList.add('js-motion');
    var revealSel=['.kicker','.title','.results-head h2','.results-head p','.services-head p','.about-copy p','.flow li','.quad li','.figures li','.work-card','.tabs','.faq-item','.contact-copy p','.contact-copy .btn','.form','.foot-cta','.page-intro','.cs-client','.case-stats li','.cs-text section','.cs-aside','.cta-inner p','.cta-actions','.process-head','.clients-label','.svc-card','.svc-list li','.svc-aside-card','.svc-others','.page-cta','.legal-toc nav','.prose section'].join(',');
    var items=[].slice.call(document.querySelectorAll(revealSel)).filter(function(el){return !el.closest('.hero')});
    items=items.filter(function(el){return !items.some(function(o){return o!==el&&o.contains(el)})});
    var groups=new Map();
    items.forEach(function(el){var p=el.parentNode,n=groups.get(p)||0;el.style.setProperty('--i',Math.min(n,6));groups.set(p,n+1);el.classList.add('rv')});
    var rvObs=new IntersectionObserver(function(en){en.forEach(function(e){
      if(e.isIntersecting){e.target.classList.add('in');rvObs.unobserve(e.target)}
    })},{rootMargin:'0px 0px -8% 0px',threshold:.12});
    items.forEach(function(el){rvObs.observe(el)});
    var cObs=new IntersectionObserver(function(en){en.forEach(function(e){if(e.isIntersecting){countUp(e.target);cObs.unobserve(e.target)}})},{threshold:.6});
    [].forEach.call(document.querySelectorAll('[data-count]'),function(el){cObs.observe(el)});
  }
  onScroll();

  /* ===== Accessibility helpers ===== */
  /* Keep keyboard focus inside the open mobile menu */
  document.addEventListener('keydown',function(e){
    if(e.key!=='Tab'||!root.classList.contains('open'))return;
    var f=[].slice.call(document.querySelectorAll('.bar a,.bar button')).filter(function(el){return el.offsetParent!==null});
    if(!f.length)return;var first=f[0],last=f[f.length-1];
    if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}
    else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}
  });

  /* Tell screen reader users when a link opens a new tab */
  [].forEach.call(document.querySelectorAll('a[target="_blank"]'),function(a){
    if(a.querySelector('.visually-hidden'))return;
    var s=document.createElement('span');s.className='visually-hidden';s.textContent=' (opens in a new tab)';a.appendChild(s);
  });

  /* Pause / play for moving content (hero animation, logo strip) */
  var PAUSE_KEY='ud_motion_paused';
  function getPaused(){try{return localStorage.getItem(PAUSE_KEY)==='1'}catch(e){return false}}
  var ICON_PAUSE='<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3" y="2" width="3.5" height="12" rx="1" fill="currentColor"/><rect x="9.5" y="2" width="3.5" height="12" rx="1" fill="currentColor"/></svg>';
  var ICON_PLAY='<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 2.5v11l9-5.5z" fill="currentColor"/></svg>';
  var motionBtns=[];
  function setPaused(p,save){
    root.classList.toggle('motion-paused',p);
    motionBtns.forEach(function(b){b.setAttribute('aria-pressed',p?'true':'false');b.innerHTML=(p?ICON_PLAY:ICON_PAUSE)+'<span>'+(p?'Play animation':'Pause animation')+'</span>'});
    if(window.udFlow){p?window.udFlow.stop():window.udFlow.start()}
    if(save){try{localStorage.setItem(PAUSE_KEY,p?'1':'0')}catch(e){}}
  }
  if(!calm){
    var heroEl=document.querySelector('.hero');
    if(heroEl){
      var b=document.createElement('button');b.type='button';b.className='motion-toggle';
      b.addEventListener('click',function(){setPaused(!root.classList.contains('motion-paused'),true)});
      heroEl.appendChild(b);motionBtns.push(b);
    }
    setPaused(getPaused(),false);
  }

  /* ===== Cookie consent (Essential, Functional, Analytics, Marketing) ===== */
  var CC_KEY='ud_consent_v1';
  var CATS=[
    {id:'essential',name:'Essential',desc:'Required for the basic functions of the website, such as remembering your cookie choices. These are always on.',locked:true},
    {id:'functional',name:'Functional',desc:'Let the website remember information that changes how it looks or behaves.'},
    {id:'analytics',name:'Analytics',desc:'Help us understand how visitors use the website so we can measure and improve performance, for example with Google Analytics.'},
    {id:'marketing',name:'Marketing',desc:'Let us and our advertising partners, such as Google and Meta, measure ad performance and show more relevant ads.'}
  ];
  function readConsent(){try{return JSON.parse(localStorage.getItem(CC_KEY))}catch(e){return null}}
  function applyConsent(c){
    window.udConsent=c;
    if(typeof window.gtag==='function'){
      var g=function(v){return v?'granted':'denied'};
      window.gtag('consent','update',{functionality_storage:g(c.functional),personalization_storage:g(c.functional),analytics_storage:g(c.analytics),ad_storage:g(c.marketing),ad_user_data:g(c.marketing),ad_personalization:g(c.marketing)});
    }
    try{document.dispatchEvent(new CustomEvent('ud:consent',{detail:c}))}catch(e){}
  }
  function saveConsent(c){c.v=1;c.ts=new Date().toISOString();try{localStorage.setItem(CC_KEY,JSON.stringify(c))}catch(e){}applyConsent(c)}
  var SHIELD='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5 4.5 5.4v6.1c0 4.6 3.1 8.6 7.5 10 4.4-1.4 7.5-5.4 7.5-10V5.4z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="m8.6 12.2 2.4 2.4 4.6-4.8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var CLOSE='<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';

  var banner=document.createElement('section');
  banner.className='cc';banner.hidden=true;banner.setAttribute('role','region');banner.setAttribute('aria-labelledby','cc-title');
  banner.innerHTML='<div class="cc-head"><span class="cc-icon">'+SHIELD+'</span><h2 id="cc-title">We value your privacy</h2></div>'+
    '<p id="cc-desc">We use cookies and similar technologies to keep this site working, understand how it’s used, and improve our marketing. You can accept all, deny non-essential cookies, or choose what to allow. Change your choice anytime under Cookie settings at the bottom of any page. <a href="/privacy-policy/">Privacy Policy</a></p>'+
    '<div class="cc-actions"><button type="button" class="btn btn-ghost" data-cc="deny">Deny</button><button type="button" class="btn btn-solid" data-cc="accept">Accept all</button><button type="button" class="btn btn-quiet cc-more" data-cc="customize">Customize settings</button></div>';

  var backdrop=document.createElement('div');backdrop.className='cc-backdrop';backdrop.hidden=true;
  var rows=CATS.map(function(cat){
    var ctl=cat.locked?'<span class="cc-always">Always on</span>':
      '<label class="switch"><input type="checkbox" role="switch" id="cc-'+cat.id+'" data-cat="'+cat.id+'" aria-describedby="cc-'+cat.id+'-desc"><span class="track" aria-hidden="true"></span><span class="state" aria-hidden="true">Off</span><span class="visually-hidden">'+cat.name+'</span></label>';
    return '<div class="cc-cat"><h3 id="cc-'+cat.id+'-name">'+cat.name+'</h3>'+ctl+'<p id="cc-'+cat.id+'-desc">'+cat.desc+'</p></div>';
  }).join('');
  backdrop.innerHTML='<div class="cc-panel" role="dialog" aria-modal="true" aria-labelledby="cc-panel-title" aria-describedby="cc-panel-desc">'+
    '<div class="cc-panel-head"><div><h2 id="cc-panel-title">Cookie settings</h2><p id="cc-panel-desc">Choose which cookies and similar technologies we can use. Essential ones are always on because the site needs them to work. Learn more in our <a href="/privacy-policy/">Privacy Policy</a>.</p></div><button type="button" class="cc-close" data-cc="close" aria-label="Close cookie settings">'+CLOSE+'</button></div>'+
    '<div class="cc-body">'+rows+'</div>'+
    '<div class="cc-panel-foot"><button type="button" class="btn btn-ghost" data-cc="deny">Deny all</button><button type="button" class="btn btn-ghost" data-cc="save">Save settings</button><button type="button" class="btn btn-solid" data-cc="accept">Accept all</button></div></div>';
  var skip=document.querySelector('.skip');
  if(skip&&skip.nextSibling)document.body.insertBefore(banner,skip.nextSibling);else document.body.appendChild(banner);
  document.body.appendChild(backdrop);
  var panel=backdrop.querySelector('.cc-panel'),lastFocus=null;
  var switches=[].slice.call(backdrop.querySelectorAll('input[data-cat]'));
  function syncSwitch(i){var st=i.parentNode.querySelector('.state');if(st)st.textContent=i.checked?'On':'Off'}
  switches.forEach(function(i){i.addEventListener('change',function(){syncSwitch(i)})});
  function bgInert(on){[].forEach.call(document.body.children,function(el){if(el===backdrop||el.tagName==='SCRIPT')return;if(on)el.setAttribute('inert','');else el.removeAttribute('inert')})}
  function openPanel(){
    var c=readConsent()||{};
    switches.forEach(function(i){i.checked=!!c[i.dataset.cat];syncSwitch(i)});
    lastFocus=document.activeElement;backdrop.hidden=false;root.classList.add('cc-lock');bgInert(true);
    setTimeout(function(){(switches[0]||panel.querySelector('button')).focus()},30);
  }
  function closePanel(){
    backdrop.hidden=true;root.classList.remove('cc-lock');bgInert(false);
    if(!readConsent()){banner.hidden=false;var b=banner.querySelector('[data-cc="customize"]');if(b)b.focus()}
    else if(lastFocus&&document.contains(lastFocus)&&!banner.contains(lastFocus))lastFocus.focus();
  }
  function finish(c){
    var hadFocus=banner.contains(document.activeElement);
    saveConsent(c);banner.hidden=true;
    if(!backdrop.hidden){backdrop.hidden=true;root.classList.remove('cc-lock');bgInert(false);if(lastFocus&&document.contains(lastFocus)&&!banner.contains(lastFocus))lastFocus.focus();else hadFocus=true}
    if(hadFocus){var l=document.querySelector('.bar .logo');if(l)l.focus()}
  }
  function all(v){return{functional:v,analytics:v,marketing:v}}
  function onAction(e){
    var b=e.target.closest('[data-cc]');if(!b)return;var a=b.dataset.cc;
    if(a==='accept')finish(all(true));
    else if(a==='deny')finish(all(false));
    else if(a==='customize')openPanel();
    else if(a==='close')closePanel();
    else if(a==='save'){var c={};switches.forEach(function(i){c[i.dataset.cat]=i.checked});finish(c)}
  }
  banner.addEventListener('click',onAction);backdrop.addEventListener('click',function(e){if(e.target===backdrop){closePanel();return}onAction(e)});
  backdrop.addEventListener('keydown',function(e){
    if(e.key==='Escape'){e.preventDefault();closePanel();return}
    if(e.key!=='Tab')return;
    var f=[].slice.call(panel.querySelectorAll('a[href],button,input')).filter(function(el){return !el.disabled&&el.offsetParent!==null});
    var first=f[0],last=f[f.length-1];
    if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}
    else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}
  });
  /* Footer link to reopen settings on every page */
  var base=document.querySelector('.foot-base');
  if(base){var fb=document.createElement('button');fb.type='button';fb.className='linklike';fb.textContent='Cookie settings';fb.addEventListener('click',openPanel);
    var pp=base.querySelector('a');if(pp){var wrapL=document.createElement('span');wrapL.className='foot-legal';pp.parentNode.insertBefore(wrapL,pp);wrapL.appendChild(pp);wrapL.appendChild(document.createTextNode(' · '));wrapL.appendChild(fb)}else base.appendChild(fb)}
  var existing=readConsent();
  if(existing)applyConsent(existing);else banner.hidden=false;

  /* About: what businesses like yours usually need */
  var fit=document.getElementById('fit');
  if(fit){
    /* Typical starting points by business type. Highlighted tactics are always services Upstream offers. */
    var FIT_WORDS={meta:'Meta Ads',google:'Google Ads',linkedin:'LinkedIn Ads',web:'a website',seo:'SEO / AEO',gbp:'a Google Business Profile',reviews:'review generation',landing:'landing pages',locpages:'location pages',creative:'ad creative',content:'content'};
    var FITS=[
      {who:'A medical or dental practice',keys:['google','seo','gbp','reviews','web']},
      {who:'A law office',keys:['google','seo','gbp','web','content']},
      {who:'A B2B or industrial company',keys:['google','linkedin','seo','web','landing']},
      {who:'A real estate business',keys:['meta','google','gbp','landing','web','content']},
      {who:'A home improvement contractor',keys:['google','seo','gbp','web','reviews']},
      {who:'An online store',keys:['meta','google','gbp','creative','seo']},
      {who:'A retail or supply store',keys:['web','seo','gbp','locpages','google']},
      {who:'A fitness or wellness studio',keys:['meta','seo','gbp','web','creative']},
      {who:'A restaurant',keys:['meta','seo','gbp','content','creative']},
      {who:'A nonprofit or public office',keys:['web','seo','gbp','reviews']}
    ];
    function fitList(keys){var w=keys.map(function(k){return FIT_WORDS[k]});return w.length>1?w.slice(0,-1).join(', ')+' and '+w[w.length-1]:w[0]}
    FITS.forEach(function(f){f.text=f.who+' usually starts with '+fitList(f.keys)+'.'});
    var fitBtns=[].slice.call(fit.querySelectorAll('[data-fit]')),fitChips=[].slice.call(fit.querySelectorAll('.fit-cloud li'));
    var fitWhat=fit.querySelector('.fit-what');
    function showFit(i){
      var f=FITS[i];
      fitBtns.forEach(function(b,k){b.setAttribute('aria-pressed',k===i?'true':'false')});
      fitChips.forEach(function(li){li.classList.toggle('on',f.keys.indexOf(li.dataset.k)>-1)});
      fitWhat.textContent=f.text;
      fit.classList.add('filtered');
    }
    fitBtns.forEach(function(b,i){b.addEventListener('click',function(){showFit(i)})});
    if(!calm&&'IntersectionObserver' in window){
      /* One moment: show the whole kitchen sink, then let the noise fall away */
      fitChips.forEach(function(li){li.classList.toggle('on',FITS[0].keys.indexOf(li.dataset.k)>-1)});
      var fitObs=new IntersectionObserver(function(en){if(en[0].isIntersecting){fitObs.disconnect();setTimeout(function(){if(!fit.classList.contains('filtered'))showFit(0)},900)}},{threshold:.45});
      fitObs.observe(fit);
    }else{showFit(0)}
  }

  /* Services: tributaries flow into the selected service's panel */
  var sf=document.getElementById('svc-flow');
  if(sf){
    var sTabs=[].slice.call(sf.querySelectorAll('[role=tab]')),sPanels=[].slice.call(sf.querySelectorAll('[role=tabpanel]'));
    var svg=sf.querySelector('.svc-lines'),NS='http://www.w3.org/2000/svg',sCur=0,sPending=!calm&&('IntersectionObserver' in window);
    function sGeom(){
      if(!svg||svg.getBoundingClientRect().width===0)return null;
      var r=svg.getBoundingClientRect(),p=sPanels[sCur].getBoundingClientRect();
      var yc=Math.max(12,Math.min(r.height-12,p.top+p.height/2-r.top));
      return {w:r.width,h:r.height,yc:yc,ys:sTabs.map(function(t){var b=t.getBoundingClientRect();return b.top+b.height/2-r.top})};
    }
    function curve(y,g){var cx=g.w*.55;return 'M0,'+y.toFixed(1)+' C'+cx.toFixed(1)+','+y.toFixed(1)+' '+(g.w-cx).toFixed(1)+','+g.yc.toFixed(1)+' '+g.w.toFixed(1)+','+g.yc.toFixed(1)}
    function sDraw(pulse){
      var g=sGeom();if(!g)return;
      while(svg.firstChild)svg.removeChild(svg.firstChild);
      svg.setAttribute('viewBox','0 0 '+g.w+' '+g.h);
      var base=[];
      g.ys.forEach(function(y,i){if(i===sCur)return;var p=document.createElementNS(NS,'path');p.setAttribute('d',curve(y,g));svg.appendChild(p);base.push(p)});
      var d=curve(g.ys[sCur],g);
      ['glow','on'].forEach(function(cls){var p=document.createElementNS(NS,'path');p.setAttribute('d',d);p.setAttribute('class',cls);svg.appendChild(p);base.push(p)});
      if(sPending){base.forEach(function(p){var L=p.getTotalLength();p.style.strokeDasharray=L;p.style.strokeDashoffset=L});pulse=false}
      if(pulse&&!calm&&!root.classList.contains('motion-paused')){var q=document.createElementNS(NS,'path');q.setAttribute('d',d);q.setAttribute('class','pulse');svg.appendChild(q)}
      var dot=document.createElementNS(NS,'circle');dot.setAttribute('cx',g.w);dot.setAttribute('cy',g.yc);dot.setAttribute('r',4.5);svg.appendChild(dot);
      return base;
    }
    function sPick(i,focus,pulse){
      if(i===sCur&&!focus){return}
      /* On phones the details sit under each service: keep the tapped service where it was on screen */
      var stacked=innerWidth<=860,before=stacked?sTabs[i].getBoundingClientRect().top:0;
      sCur=i;
      sTabs.forEach(function(t,k){var on=k===i;t.setAttribute('aria-selected',on?'true':'false');t.tabIndex=on?0:-1;sPanels[k].hidden=!on});
      if(stacked){var shift=sTabs[i].getBoundingClientRect().top-before;if(Math.abs(shift)>1)window.scrollBy({top:shift,left:0,behavior:'instant'})}
      if(focus)sTabs[i].focus({preventScroll:stacked});
      sDraw(pulse!==false);
    }
    sTabs.forEach(function(t,i){
      t.addEventListener('click',function(){sPick(i,false)});
      t.addEventListener('keydown',function(e){
        var n=sTabs.length,k=null;
        if(e.key==='ArrowDown'||e.key==='ArrowRight')k=(i+1)%n;
        else if(e.key==='ArrowUp'||e.key==='ArrowLeft')k=(i-1+n)%n;
        else if(e.key==='Home')k=0;else if(e.key==='End')k=n-1;
        if(k!==null){e.preventDefault();sPick(k,true)}
      });
    });
    if(window.matchMedia('(hover:hover)').matches){
      var hoverT;
      sTabs.forEach(function(t,i){t.addEventListener('mouseenter',function(){clearTimeout(hoverT);hoverT=setTimeout(function(){sPick(i,false)},110)});t.addEventListener('mouseleave',function(){clearTimeout(hoverT)})});
    }
    var sRz;window.addEventListener('resize',function(){clearTimeout(sRz);sRz=setTimeout(function(){sDraw(false)},120)});
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){sDraw(false)});
    sDraw(false);
    /* One moment: the tributaries draw in the first time the section is seen */
    if(sPending){
      var sObs=new IntersectionObserver(function(en){if(!en[0].isIntersecting)return;sObs.disconnect();sPending=false;
        [].slice.call(svg.querySelectorAll('path')).forEach(function(p,k){p.style.transition='stroke-dashoffset 1.1s cubic-bezier(.2,.7,.2,1) '+(k*90)+'ms';requestAnimationFrame(function(){p.style.strokeDashoffset=0})});
        setTimeout(function(){sDraw(true)},1500);
      },{threshold:.35});
      sObs.observe(sf);
    }
  }

  /* FAQ: show the first five questions, the rest behind "Show more questions" */
  var faqList=document.getElementById('faq-list'),faqBtn=document.querySelector('.faq-toggle');
  if(faqList&&faqBtn){
    var faqItems=[].slice.call(faqList.querySelectorAll('.faq-item')),FAQ_SHOW=5;
    if(faqItems.length>FAQ_SHOW){
      faqItems.slice(FAQ_SHOW).forEach(function(it){it.classList.add('faq-extra')});
      faqList.classList.add('collapsed');faqBtn.hidden=false;
      faqBtn.addEventListener('click',function(){
        var open=faqList.classList.toggle('collapsed')===false;
        faqBtn.setAttribute('aria-expanded',open?'true':'false');
        faqBtn.querySelector('span').textContent=open?'Show fewer questions':'Show more questions';
        if(open){
          faqItems.slice(FAQ_SHOW).forEach(function(it){it.classList.remove('just-shown');void it.offsetWidth;it.classList.add('just-shown')});
          var first=faqItems[FAQ_SHOW].querySelector('summary');if(first)first.focus({preventScroll:true});
        }else{
          faqItems.slice(FAQ_SHOW).forEach(function(it){it.open=false});
        }
      });
    }
  }
})();
