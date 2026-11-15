(function(){
  var d=document,b=d.body;
  window.addEventListener('load',function(){b.classList.add('loaded')});
  // header + mobile bar
  var h=d.querySelector('.header'),mb=d.querySelector('.mbar');
  function onS(){var y=window.scrollY;if(h)h.classList.toggle('scrolled',y>20);if(mb)mb.classList.toggle('show',y>320)}
  window.addEventListener('scroll',onS,{passive:true});onS();
  // burger
  var bg=d.querySelector('.burger');
  if(bg){bg.addEventListener('click',function(){var o=b.classList.toggle('menu-open');bg.setAttribute('aria-expanded',o)});
    d.querySelectorAll('.mobile-menu a').forEach(function(a){a.addEventListener('click',function(){b.classList.remove('menu-open')})});}
  // reveal
  var els=d.querySelectorAll('.rv');
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});els.forEach(function(e){io.observe(e)})}else els.forEach(function(e){e.classList.add('in')});
  // segmented tabs (rent / buy)
  d.querySelectorAll('.seg').forEach(function(seg){
    var pill=seg.querySelector('.pill'),btns=seg.querySelectorAll('button'),tgt=d.querySelector(seg.dataset.target);
    function set(btn){btns.forEach(function(x){x.classList.toggle('on',x===btn);x.setAttribute('aria-selected',x===btn)});
      if(pill){pill.style.width=btn.offsetWidth+'px';pill.style.transform='translateX('+(btn.offsetLeft-5)+'px)'}
      if(tgt){tgt.classList.remove('mode-rent','mode-buy');tgt.classList.add('mode-'+btn.dataset.mode)}}
    btns.forEach(function(x){x.addEventListener('click',function(){set(x)})});
    var first=seg.querySelector('button.on')||btns[0];set(first);
    window.addEventListener('resize',function(){set(seg.querySelector('button.on'))});
    if(d.fonts&&d.fonts.ready)d.fonts.ready.then(function(){set(seg.querySelector('button.on'))});
  });
  // gallery
  var gm=d.querySelector('.gallery-main[data-imgs]');
  if(gm){
    var imgs=JSON.parse(gm.dataset.imgs),i=0,main=gm.querySelector('img'),cnt=gm.querySelector('.gal-count'),th=d.querySelectorAll('.thumbs button');
    var lb=d.querySelector('.lb'),lbi=lb&&lb.querySelector('img');
    function show(n){i=(n+imgs.length)%imgs.length;main.src=imgs[i];if(cnt)cnt.textContent=(i+1)+' / '+imgs.length;th.forEach(function(t,k){t.classList.toggle('on',k===i)});if(lbi)lbi.src=imgs[i]}
    th.forEach(function(t,k){t.addEventListener('click',function(){show(k)})});
    d.querySelectorAll('[data-gal]').forEach(function(x){x.addEventListener('click',function(e){e.stopPropagation();show(i+(+x.dataset.gal))})});
    gm.addEventListener('click',function(){if(lb){lb.classList.add('open');lbi.src=imgs[i]}});
    if(lb){lb.addEventListener('click',function(e){if(e.target===lb||e.target.closest('.lb-close'))lb.classList.remove('open')});
      d.addEventListener('keydown',function(e){if(!lb.classList.contains('open'))return;if(e.key==='Escape')lb.classList.remove('open');if(e.key==='ArrowRight')show(i+1);if(e.key==='ArrowLeft')show(i-1)})}
    var sx=null;gm.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});
    gm.addEventListener('touchend',function(e){if(sx===null)return;var dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>40){show(i+(dx<0?1:-1))}sx=null});
  }
  // 2GIS map (lazy), points are listed in window.VOLT_POINTS
  var mapEl=d.getElementById('map');
  if(mapEl&&window.VOLT_POINTS){
    var pts=window.VOLT_POINTS,map=null,markers=[],cur=0,started=false;
    var tabs=d.querySelector('.loc-tabs');
    function fill(k){var p=pts[k];cur=k;
      d.querySelectorAll('[data-loc]').forEach(function(el){var f=el.dataset.loc;if(f==='addr')el.textContent=p.addr;if(f==='route')el.href=p.route;if(f==='open')el.href=p.open;if(f==='name')el.textContent=p.name});
      if(tabs)tabs.querySelectorAll('button').forEach(function(x,j){x.classList.toggle('on',j===k)});
      if(map){map.setView([p.lat,p.lon],16);markers[k]&&markers[k].openPopup()}}
    if(tabs){if(pts.length<2)tabs.style.display='none';pts.forEach(function(p,k){var bt=d.createElement('button');bt.type='button';bt.textContent=p.name;bt.addEventListener('click',function(){fill(k)});tabs.appendChild(bt)})}
    fill(0);
    function init(){if(started)return;started=true;
      var l=d.createElement('link');l.rel='stylesheet';l.href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';d.head.appendChild(l);
      var s=d.createElement('script');s.src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';s.onload=function(){
      var p=pts[cur];map=L.map('map',{center:[p.lat,p.lon],zoom:16,scrollWheelZoom:false,attributionControl:true});map.attributionControl.setPrefix(false);
      L.tileLayer('https://tile{s}.maps.2gis.com/tiles?x={x}&y={y}&z={z}&v=1',{subdomains:'0123',maxZoom:18,attribution:'&copy; <a href="https://2gis.ru" target="_blank" rel="noopener">2ГИС</a>'}).addTo(map);
      var icon=L.divIcon({className:'vpin',html:'<span></span>',iconSize:[44,54],iconAnchor:[22,52],popupAnchor:[0,-48]});
      pts.forEach(function(q,k){markers[k]=L.marker([q.lat,q.lon],{icon:icon}).addTo(map).bindPopup('<b>VOLT ONE</b><br>'+q.addr)});
      markers[cur].openPopup();var ph=d.querySelector('.map-ph');if(ph)ph.remove();};d.head.appendChild(s)}
    if('IntersectionObserver' in window){var mo=new IntersectionObserver(function(es){if(es[0].isIntersecting){init();mo.disconnect()}},{rootMargin:'600px'});mo.observe(mapEl)}else init();
  }

  // parts filter + lightbox
  var pg=d.getElementById('pgrid');
  if(pg){
    var tiles=[].slice.call(pg.querySelectorAll('.ptile')),btns=d.querySelectorAll('.pcat');
    btns.forEach(function(b){b.addEventListener('click',function(){var c=b.dataset.cat;btns.forEach(function(x){x.classList.toggle('on',x===b)});
      tiles.forEach(function(t){var on=c==='all'||(' '+t.dataset.cats+' ').indexOf(' '+c+' ')>-1;t.hidden=!on;if(on){t.style.animation='none';t.offsetWidth;t.style.animation=''}});
      var pc=b.parentNode;if(pc.scrollWidth>pc.clientWidth){pc.scrollTo({left:b.offsetLeft-(pc.clientWidth-b.offsetWidth)/2,behavior:'smooth'})}})});
    var plb=d.getElementById('plb'),pli=plb.querySelector('img'),cur=0;
    function vis(){return tiles.filter(function(t){return !t.hidden})}
    function pshow(n){var v=vis();cur=(n+v.length)%v.length;var b=v[cur].querySelector('.ptile-img');pli.src=b.dataset.full;pli.alt=v[cur].querySelector('h3').textContent}
    tiles.forEach(function(t){t.querySelector('.ptile-img').addEventListener('click',function(){pshow(vis().indexOf(t));plb.classList.add('open')})});
    plb.querySelectorAll('[data-plb]').forEach(function(x){x.addEventListener('click',function(e){e.stopPropagation();pshow(cur+(+x.dataset.plb))})});
    plb.addEventListener('click',function(e){if(e.target===plb||e.target.closest('.lb-close'))plb.classList.remove('open')});
    d.addEventListener('keydown',function(e){if(!plb.classList.contains('open'))return;if(e.key==='Escape')plb.classList.remove('open');if(e.key==='ArrowRight')pshow(cur+1);if(e.key==='ArrowLeft')pshow(cur-1)});
    var px=null;plb.addEventListener('touchstart',function(e){px=e.touches[0].clientX},{passive:true});
    plb.addEventListener('touchend',function(e){if(px===null)return;var dx=e.changedTouches[0].clientX-px;if(Math.abs(dx)>40)pshow(cur+(dx<0?1:-1));px=null});
  }
})();
