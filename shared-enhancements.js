/* shared-enhancements.js — cursor glow, card tilt, click sparks, touch support */
(function(){
  'use strict';
  var html = document.documentElement;
  var params = new URLSearchParams(location.search);
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  var plain = html.classList.contains('plain') || params.get('plain') === '1';

  function fxOn(key){
    // Default-on when no FX system is present (e.g. on sub-pages without the panel).
    return !window.BSC_FX || window.BSC_FX.get(key);
  }

  function accentColor(){
    return getComputedStyle(html).getPropertyValue('--accent').trim() || '#86a6ff';
  }

  /* ── cursor glow (desktop only) ──────────────────────────────── */
  if(!reduced && !plain && window.matchMedia('(pointer:fine)').matches){
    var glow = document.getElementById('cursor-glow');
    if(!glow){
      glow = document.createElement('div');
      glow.id = 'cursor-glow';
      glow.setAttribute('aria-hidden','true');
      document.body.appendChild(glow);
    }
    if(!document.getElementById('bsc-glow-style')){
      var st = document.createElement('style');
      st.id = 'bsc-glow-style';
      st.textContent = [
        '#cursor-glow{',
          'position:fixed;pointer-events:none;',
          'width:320px;height:320px;border-radius:50%;',
          'background:radial-gradient(circle,color-mix(in srgb,var(--accent) 16%,transparent) 0%,transparent 65%);',
          'transform:translate(-50%,-50%);',
          'z-index:2;',
          'transition:left .1s linear,top .1s linear,opacity .4s ease,background .3s ease;',
          'mix-blend-mode:screen;opacity:0;will-change:left,top;',
        '}',
        'html[data-theme="light"] #cursor-glow{display:none}',
      ].join('');
      document.head.appendChild(st);
    }
    var glowActive = false;
    document.addEventListener('mousemove',function(e){
      if(!fxOn('spotlight')){
        if(glowActive){ glowActive = false; glow.style.opacity = '0'; }
        return;
      }
      glow.style.left = e.clientX+'px';
      glow.style.top  = e.clientY+'px';
      if(!glowActive){ glowActive=true; glow.style.opacity='1'; }
    },{passive:true});
    document.addEventListener('mouseleave',function(){ glowActive=false; glow.style.opacity='0'; });
    // Hide immediately when the user toggles spotlight off via the FX panel
    window.addEventListener('bsc-fx-change', function(ev){
      if(ev.detail && ev.detail.key === 'spotlight' && !ev.detail.value){
        glowActive = false;
        glow.style.opacity = '0';
      }
    });
  }

  /* ── card 3D tilt ────────────────────────────────────────────── */
  if(!reduced){
    var hasFinePointer = window.matchMedia('(pointer:fine)').matches;
    var hasCoarsePointer = window.matchMedia('(pointer:coarse)').matches;

    document.querySelectorAll('.card').forEach(function(card){
      if(hasFinePointer){
        card.addEventListener('mousemove',function(e){
          if(!fxOn('tilt')) return;
          var r = card.getBoundingClientRect();
          var x = (e.clientX - r.left) / r.width  - 0.5;
          var y = (e.clientY - r.top)  / r.height - 0.5;
          card.style.willChange  = 'transform';
          card.style.transform   = 'perspective(700px) rotateX('+(-y*7)+'deg) rotateY('+(x*7)+'deg) translateZ(6px)';
          card.style.boxShadow   = 'var(--shadow-hover,var(--shadow))';
          card.style.transition  = 'transform .12s ease,box-shadow .18s ease';
        });
        card.addEventListener('mouseleave',function(){
          card.style.transform  = '';
          card.style.boxShadow  = '';
          card.style.willChange = '';
        });
      }
      if(hasCoarsePointer){
        card.addEventListener('touchmove',function(e){
          if(!fxOn('tilt')) return;
          var t = e.touches[0];
          var r = card.getBoundingClientRect();
          var x = (t.clientX - r.left) / r.width  - 0.5;
          var y = (t.clientY - r.top)  / r.height - 0.5;
          card.style.willChange  = 'transform';
          card.style.transform   = 'perspective(700px) rotateX('+(-y*4)+'deg) rotateY('+(x*4)+'deg)';
          card.style.transition  = 'none';
        },{passive:true});
        card.addEventListener('touchend',function(){
          card.style.transform   = '';
          card.style.willChange  = '';
          card.style.transition  = 'transform .28s ease';
        });
      }
    });
    // Snap all cards back when tilt is turned off mid-hover
    window.addEventListener('bsc-fx-change', function(ev){
      if(ev.detail && ev.detail.key === 'tilt' && !ev.detail.value){
        document.querySelectorAll('.card').forEach(function(card){
          card.style.transform = '';
          card.style.boxShadow = '';
          card.style.willChange = '';
        });
      }
    });
  }

  /* ── click / tap sparks ──────────────────────────────────────── */
  if(!reduced && !plain){
    function spawnSparks(cx,cy){
      var count = 10;
      var color = accentColor();
      for(var i=0;i<count;i++){
        (function(idx){
          var angle = (Math.PI*2*idx/count)+(Math.random()-0.5)*0.9;
          var speed = 48+Math.random()*72;
          var vx = Math.cos(angle)*speed;
          var vy = Math.sin(angle)*speed-28;
          var size = 3+Math.random()*3;
          var s = document.createElement('div');
          s.setAttribute('aria-hidden','true');
          s.style.cssText = [
            'position:fixed','pointer-events:none','z-index:9999',
            'width:'+size+'px','height:'+size+'px',
            'border-radius:50%','background:'+color,
            'left:'+cx+'px','top:'+cy+'px','opacity:1'
          ].join(';');
          document.body.appendChild(s);
          var start=null, dur=520+Math.random()*280;
          (function frame(ts){
            if(!start) start=ts;
            var p=(ts-start)/dur;
            if(p>=1){s.remove();return;}
            s.style.left=(cx+vx*p)+'px';
            s.style.top =(cy+vy*p+145*p*p)+'px';
            s.style.opacity=Math.max(0,1-p*p);
            requestAnimationFrame(frame);
          })(performance.now());
        })(i);
      }
    }

    document.addEventListener('click',function(e){
      if(!fxOn('sparks')) return;
      if(e.target.closest('a,button,input,select,textarea,summary,label')) return;
      spawnSparks(e.clientX,e.clientY);
    });

    document.addEventListener('touchend',function(e){
      if(!fxOn('sparks')) return;
      if(e.target.closest('a,button,input,select,textarea,summary,label')) return;
      var t = e.changedTouches[0];
      spawnSparks(t.clientX,t.clientY);
    },{passive:true});
  }

})();
