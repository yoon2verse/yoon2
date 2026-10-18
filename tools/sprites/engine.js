/* ---------- pixel sprites: layered char grids (see SP) ---------- */
const SW=32,SH=63;
const COUPLE_PAL={O:'#141216',k:'#a0604f',S:'#ffe2cc',s:'#f2bfa0',B:'#f7a1a8',M:'#b5555f',E:'#141216',I:'#4e4a56',W:'#ffffff',
  H:'#222025',h:'#4a4850',j:'#76747e',T:'#28282d',t:'#4a4a52',C:'#ffffff',c:'#dcd8ea',D:'#ffffff',d:'#e7e3f1',e:'#c9c2dc',
  v:'#d6d1e6',V:'rgba(250,249,255,.75)',G:'#6f9d55',g:'#a6c97a',R:'#fff6f0',r:'#f3d9de',P:'#ffffff',p:'#cfc8e0',F:'#0e0d10'};
const SKIN=['#ffe2cc','#f6d2b2','#dcaa82'];
const HAIR=['#222025','#4a3226','#7a4f33','#b98a55','#6e6a78','#8c5a6e'];
const TOPS=['#ffffff','#2d2d35','#c8414b','#4a7bd1','#7fae6b','#f2b6c3','#e9c46a','#6d4c8e','#b8d4ea','#d8c3a6'];
const BOTS=['#2f3b57','#2d2d35','#8a6e52','#e8e2d6','#5b6b48','#f2b6c3','#ffffff'];
const STYLES={m:[['part','가르마'],['comma','쉼표머리'],['short','짧은머리']],f:[['long','긴머리'],['bob','단발'],['bun','올림머리']]};
const TOPTYPES={m:[['shirt','셔츠'],['knit','니트'],['suit','정장']],f:[['blouse','블라우스'],['knit','니트'],['jacket','재킷']]};
const LEGS=[['pants','바지'],['skirt','치마']];
const shade=(hex,k)=>{const n=parseInt(hex.slice(1),16),f=v=>Math.max(0,Math.min(255,Math.round(k<0?v*(1+k):v+(255-v)*k)));
  return '#'+((1<<24)|(f(n>>16)<<16)|(f(n>>8&255)<<8)|f(n&255)).toString(16).slice(1)};
const lum=hex=>{const n=parseInt(hex.slice(1),16);return .3*(n>>16)+.59*(n>>8&255)+.11*(n&255)};

/* older saved looks (before the new sprites) still render */
function normLook(L){
  L=L||{};
  const base=L.base||(L.style==='long'||L.style==='bun'?'f':'m');
  const ok=STYLES[base].some(s=>s[0]===L.style);
  const style=ok?L.style:(base==='f'?'long':(L.style==='short'||L.style==='cap'?'short':'part'));
  const t2=TOPTYPES[base].some(s=>s[0]===L.top2)?L.top2:TOPTYPES[base][0][0];
  return{base,style,hair:L.hair||HAIR[0],top2:t2,top:L.top||TOPS[0],legs:L.legs||(base==='f'?'skirt':'pants'),
    bottom:L.bottom||BOTS[0],skin:L.skin||SKIN[0]};
}
function guestPal(L){
  const sk=L.skin,hr=L.hair,tp=L.top,bt=L.bottom,light=lum(tp)>200;
  return{...COUPLE_PAL,S:sk,s:shade(sk,-.07),k:shade(sk,-.42),H:hr,h:shade(hr,.2),j:shade(hr,.38),
    T:tp,t:light?shade(tp,-.06):shade(tp,.2),d:shade(tp,light?-.18:-.25),u:light?'#ffffff':shade(tp,.42),
    C:'#ffffff',X:lum(tp)<90?'#a52a39':'#2f3b57',W:light?'#d8d4e4':'#ffffff',P:bt,p:lum(bt)>200?shade(bt,-.06):shade(bt,.18)};
}
function guestGrid(L){
  const B=SP[L.base],g=Array.from({length:SH},()=>Array(SW).fill('.'));
  const lay=(rows,y0,mode)=>rows.forEach((r,dy)=>{const y=y0+dy;if(y<0||y>=SH)return;
    for(let x=0;x<SW;x++){const c=r[x];if(c==='.')continue;const d=g[y][x];
      if(mode==='hair'&&c==='O'&&d!=='.'&&d!=='k')continue;
      if(mode==='head'&&c==='k'&&d==='S'){g[y][x]='s';continue}
      g[y][x]=c}});
  const top=B.top[L.top2],bot=B.bottom[L.legs],hair=B.hair[L.style];
  if(L.base==='m'){lay(B.head,0);lay(hair,0,'hair');lay(top,B.topY);lay(bot,B.bottomY)}
  else{lay(top,B.topY);lay(bot,B.bottomY);lay(B.head,0,'head');lay(hair,0,'hair')}
  return g.map(r=>r.join(''));
}
function gridCanvas(rows,pal){
  const c=document.createElement('canvas');c.width=rows[0].length;c.height=rows.length;const g=c.getContext('2d');
  rows.forEach((r,y)=>{for(let x=0;x<r.length;x++){const ch=r[x];if(ch==='.')continue;g.fillStyle=pal[ch]||'#f0f';g.fillRect(x,y,1,1)}});
  return c;
}
const spriteCache=new Map();
function spriteOf(who){
  // who: 'groom' | 'bride' | look object
  const key=typeof who==='string'?who:JSON.stringify(who);
  let s=spriteCache.get(key);if(s)return s;
  if(who==='groom')s={cv:gridCanvas(SP.groom,COUPLE_PAL),leg:53,kind:'legs'};
  else if(who==='bride')s={cv:gridCanvas(SP.bride,COUPLE_PAL),leg:56,kind:'gown',axis:19};
  else{const L=normLook(who);s={cv:gridCanvas(guestGrid(L),guestPal(L)),leg:L.legs==='skirt'?57:53,kind:'legs'}}
  s.w=s.cv.width;s.h=s.cv.height;s.axis=s.axis||16;spriteCache.set(key,s);return s;
}
/* frame 0/2 stand, 1 = left foot up + bob, 3 = right foot up + bob (gown: hem sways instead) */
function drawSprite(g,s,x,y,frame){
  const cv=s.cv,w=s.w,h=s.h,L=s.leg;
  if(!(frame&1)){g.drawImage(cv,x,y);return}
  g.drawImage(cv,0,0,w,L,x,y-1,w,L);
  if(s.kind==='gown'){const dx=frame===1?-1:1;g.drawImage(cv,0,L-1,w,h-L+1,x+dx,y+L-1,w,h-L+1);return}
  const m=s.axis,lift=frame===1;
  g.drawImage(cv,0,L-1,m,h-L+1,x,y+L-1-(lift?2:0),m,h-L+1);
  g.drawImage(cv,m,L-1,w-m,h-L+1,x+m,y+L-1-(lift?0:2),w-m,h-L+1);
}
