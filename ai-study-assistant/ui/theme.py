# Global CSS in the green theme palette (animations, cards, buttons, quiz options) injected into the Streamlit page.
import streamlit as st
GLOBAL_CSS = """
<style>
:root{--primary:#4A7023;--bg:#F4F9F1;--card:#FFFFFF;--text:#2D5016;--leaf:#6B9B37;--lime:#A8D672;--mint:#DCEFD0;--soft:#EEF6E8;--amber:#F2B544;--coral:#D96C4F;--shadow:0 10px 30px rgba(45,80,22,.12);--shadow-lg:0 18px 40px rgba(45,80,22,.18);}
@keyframes saFadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
@keyframes saFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes saPulse{0%{box-shadow:0 0 0 0 rgba(74,112,35,.45)}70%{box-shadow:0 0 0 12px rgba(74,112,35,0)}100%{box-shadow:0 0 0 0 rgba(74,112,35,0)}}
@keyframes saGradient{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
@keyframes saPop{0%{transform:scale(.7);opacity:0}70%{transform:scale(1.05);opacity:1}100%{transform:scale(1)}}
@keyframes saGrow{from{width:0}to{width:56px}}
@keyframes saShake{0%,100%{transform:translateX(0)}25%{transform:translateX(-3px)}75%{transform:translateX(3px)}}
@keyframes saWiggle{0%,100%{transform:rotate(0)}25%{transform:rotate(-8deg)}75%{transform:rotate(8deg)}}
@keyframes saSpin{to{transform:rotate(360deg)}}
.stApp{background:radial-gradient(circle at 8% 0%,#E1F0D3 0,transparent 38%),radial-gradient(circle at 92% 18%,#EAF5E0 0,transparent 32%),radial-gradient(circle at 50% 100%,#E6F2DC 0,transparent 40%),var(--bg);}
.block-container{padding-top:3.2rem;}
[data-testid="stHeading"] h1,[data-testid="stHeading"] h2,[data-testid="stHeading"] h3{color:var(--text);letter-spacing:-.01em;}
[data-testid="stHeading"] h2{animation:saFadeUp .5s ease both;}
[data-testid="stHeading"] h2::after{content:"";display:block;height:4px;width:56px;margin-top:.35rem;border-radius:4px;background:linear-gradient(90deg,var(--primary),var(--lime));animation:saGrow .7s ease both;}
button[data-testid^="stBaseButton"]{border-radius:999px!important;font-weight:700!important;transition:transform .18s ease,box-shadow .2s ease,background-position .6s ease!important;}
button[data-testid^="stBaseButton"]:hover{transform:translateY(-2px) scale(1.02);box-shadow:var(--shadow);}
button[data-testid^="stBaseButton"]:active{transform:translateY(0) scale(.98);}
button[data-testid^="stBaseButton-primary"]{background:linear-gradient(120deg,#4A7023,#6B9B37,#4A7023)!important;background-size:220% 100%!important;border:none!important;color:#fff!important;}
button[data-testid^="stBaseButton-primary"]:hover{background-position:100% 0!important;}
[data-testid="stForm"]{background:var(--card);border:1px solid var(--mint)!important;border-radius:22px!important;box-shadow:var(--shadow);animation:saFadeUp .55s ease both;}
[data-testid="stTextInput"] input{border-radius:14px!important;font-size:1.05rem;}
[data-testid="stTextInput"] div[data-baseweb="input"]{border-radius:14px!important;transition:box-shadow .2s ease;}
[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within{box-shadow:0 0 0 4px rgba(168,214,114,.45);}
[class*="st-key-qcard"]{background:var(--card);border-radius:18px;padding:1rem 1.1rem .6rem;border-left:6px solid var(--lime);box-shadow:0 6px 18px rgba(45,80,22,.08);animation:saFadeUp .5s ease both;transition:transform .2s ease,box-shadow .2s ease;}
[class*="st-key-qcard"]:hover{transform:translateY(-3px);box-shadow:var(--shadow-lg);border-left-color:var(--primary);}
[class*="st-key-qcard"] [data-testid="stElementContainer"]:has([data-testid="stRadio"]),[data-testid="stRadio"]{width:100%!important;}
[data-testid="stRadio"] [role="radiogroup"]{gap:.4rem;width:100%;}
[data-testid="stRadioOption"],[data-testid="stRadio"] label[data-baseweb="radio"]{background:var(--soft);border:2px solid transparent;border-radius:14px;padding:.55rem .85rem;margin:0;width:100%;box-sizing:border-box;transition:all .18s ease;cursor:pointer;}
[data-testid="stRadioOption"]:hover,[data-testid="stRadio"] label[data-baseweb="radio"]:hover{border-color:var(--lime);transform:translateX(5px);}
[data-testid="stRadioOption"]:has(input:checked),[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked){background:var(--mint);border-color:var(--primary);animation:saPop .3s ease;}
[data-testid="stExpander"] details{border-radius:18px!important;border:1px solid var(--mint)!important;background:var(--card);box-shadow:0 4px 14px rgba(45,80,22,.06);}
[data-testid="stAlert"]{border-radius:16px;animation:saPop .45s ease both;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#FFFFFF 0%,#EEF6E8 100%);border-right:1px solid var(--mint);}
[data-testid="stIFrame"],iframe{border-radius:22px;}
[data-testid="stTabs"] button[role="tab"]{border-radius:12px 12px 0 0;font-weight:600;}
.sa-hero{animation:saFadeUp .6s ease both;}
.sa-badge{display:inline-block;padding:.3rem .8rem;border-radius:999px;background:var(--mint);color:var(--primary);font-weight:700;font-size:.78rem;letter-spacing:.04em;}
.sa-title{font-size:clamp(2.1rem,6vw,3.2rem);font-weight:900;line-height:1.05;margin:.6rem 0 .4rem;background:linear-gradient(90deg,#2D5016,#4A7023,#6B9B37,#A8D672,#4A7023);background-size:300% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;animation:saGradient 6s ease infinite;}
.sa-sub{color:var(--text);opacity:.85;font-size:1.02rem;margin:0 0 .9rem;}
.sa-chips{display:flex;flex-wrap:wrap;gap:.5rem;}
.sa-chip{display:inline-flex;align-items:center;gap:.35rem;padding:.35rem .75rem;border-radius:999px;background:var(--card);border:1px solid var(--mint);color:var(--text);font-weight:600;font-size:.88rem;box-shadow:0 3px 10px rgba(45,80,22,.06);animation:saPop .45s ease both;}
.sa-chip.good{background:#E4F3D6;border-color:var(--lime);}
.sa-chip.warn{background:#FDF1D8;border-color:var(--amber);}
.sa-float{display:inline-block;animation:saFloat 3s ease-in-out infinite;}
.sa-stepper{display:flex;gap:.4rem;align-items:center;flex-wrap:wrap;background:var(--card);border:1px solid var(--mint);border-radius:999px;padding:.45rem .6rem;box-shadow:var(--shadow);animation:saFadeUp .5s ease both;}
.sa-step{display:flex;align-items:center;gap:.35rem;padding:.35rem .7rem;border-radius:999px;font-weight:700;font-size:.85rem;color:#8AA37A;transition:all .3s ease;}
.sa-step .dot{width:1.7rem;height:1.7rem;border-radius:50%;display:grid;place-items:center;background:var(--soft);font-size:.8rem;}
.sa-step.done{color:var(--primary);}
.sa-step.done .dot{background:var(--mint);}
.sa-step.active{background:linear-gradient(120deg,#4A7023,#6B9B37);color:#fff;animation:saPulse 1.8s infinite;}
.sa-step.active .dot{background:rgba(255,255,255,.25);}
.sa-arrow{color:#B7CFA5;font-weight:900;}
.sa-card{background:var(--card);border:1px solid var(--mint);border-radius:20px;padding:1.05rem 1.15rem;box-shadow:var(--shadow);animation:saFadeUp .55s ease both;transition:transform .25s ease,box-shadow .25s ease;}
.sa-card:hover{transform:perspective(700px) rotateX(3deg) translateY(-4px);box-shadow:var(--shadow-lg);}
.sa-card h4{margin:0 0 .45rem;color:var(--primary);font-size:1.02rem;display:flex;align-items:center;gap:.45rem;}
.sa-card p{margin:0;color:var(--text);line-height:1.6;}
.sa-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:.9rem;margin:.4rem 0 1rem;}
.sa-grid>*:nth-child(1){animation-delay:.05s}.sa-grid>*:nth-child(2){animation-delay:.15s}.sa-grid>*:nth-child(3){animation-delay:.25s}.sa-grid>*:nth-child(4){animation-delay:.35s}
.sa-analogy{background:linear-gradient(135deg,#EAF5DF,#FFFFFF);border:2px dashed var(--lime);}
.sa-simpler{border-left:6px solid var(--amber);}
.sa-topic{display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap;}
.sa-topic .name{font-size:1.5rem;font-weight:900;color:var(--text);}
.sa-flip-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem;margin:.4rem 0 1rem;}
.sa-flip{perspective:1000px;height:230px;outline:none;cursor:pointer;animation:saFadeUp .55s ease both;}
.sa-flip-inner{position:relative;width:100%;height:100%;transition:transform .8s cubic-bezier(.2,.8,.2,1);transform-style:preserve-3d;}
.sa-flip:hover .sa-flip-inner,.sa-flip:focus .sa-flip-inner,.sa-flip:focus-within .sa-flip-inner{transform:rotateY(180deg);}
.sa-face{position:absolute;inset:0;border-radius:22px;padding:1.1rem;backface-visibility:hidden;-webkit-backface-visibility:hidden;box-shadow:var(--shadow);display:flex;flex-direction:column;}
.sa-front{background:linear-gradient(145deg,#4A7023,#6B9B37 60%,#A8D672);color:#fff;justify-content:center;align-items:center;text-align:center;}
.sa-front .num{font-size:3rem;font-weight:900;letter-spacing:-.02em;opacity:.9;animation:saFloat 3s ease-in-out infinite;}
.sa-front .ttl{font-weight:800;font-size:1.08rem;margin-top:.5rem;}
.sa-front .hint{font-size:.75rem;opacity:.85;margin-top:.6rem;}
.sa-back{background:var(--card);border:2px solid var(--lime);color:var(--text);transform:rotateY(180deg);overflow-y:auto;line-height:1.55;font-size:.93rem;}
.sa-back b{color:var(--primary);margin-bottom:.35rem;}
.sa-quiz-intro{display:flex;align-items:center;gap:.9rem;background:linear-gradient(120deg,#FFFFFF,#EEF6E8);border:1px solid var(--mint);border-radius:18px;padding:.8rem 1rem;margin-bottom:.8rem;animation:saFadeUp .5s ease both;}
.sa-quiz-intro .big{width:2.8rem;height:2.8rem;flex:none;border-radius:50%;display:grid;place-items:center;background:linear-gradient(135deg,#4A7023,#6B9B37);color:#fff;font-size:1.3rem;font-weight:900;animation:saPulse 2.4s infinite;}
.sa-tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:.7rem;margin:.6rem 0;}
.sa-tile{background:var(--card);border:1px solid var(--mint);border-radius:18px;padding:.8rem;text-align:center;box-shadow:var(--shadow);animation:saPop .5s ease both;}
.sa-tile .num{font-size:1.9rem;font-weight:900;color:var(--primary);}
.sa-tile .lbl{font-size:.8rem;font-weight:700;opacity:.75;text-transform:uppercase;letter-spacing:.05em;}
.sa-tile.bad .num{color:var(--coral);}
.sa-banner{border-radius:18px;padding:.9rem 1.1rem;font-weight:700;margin:.5rem 0;animation:saPop .5s ease both;}
.sa-banner.pass{background:linear-gradient(120deg,#DDF0CB,#F4FBEE);border:2px solid var(--lime);}
.sa-banner.retry{background:linear-gradient(120deg,#FDF0D4,#FFFBF2);border:2px solid var(--amber);}
.sa-banner.stop{background:linear-gradient(120deg,#F8E0D8,#FFF7F4);border:2px solid var(--coral);}
.sa-label{font-weight:800;color:var(--primary);margin:.7rem 0 .35rem;font-size:.9rem;}
.sa-result{border-radius:16px;padding:.75rem .95rem;margin:.5rem 0;background:var(--card);border:1px solid var(--mint);border-left:6px solid var(--lime);animation:saFadeUp .45s ease both;}
.sa-result.wrong{border-left-color:var(--coral);}
.sa-result .q{font-weight:800;margin-bottom:.3rem;}
.sa-result .icon{display:inline-block;margin-right:.45rem;padding:.08rem .55rem;border-radius:999px;font-size:.72rem;font-weight:800;letter-spacing:.03em;text-transform:uppercase;vertical-align:.1rem;background:var(--mint);color:var(--primary);}
.sa-result.wrong .icon{background:#F8E0D8;color:#A84A30;}
.sa-result.wrong .icon{animation:saShake .5s ease 2;}
.sa-result .ans{font-size:.92rem;line-height:1.55;}
.sa-result .why{font-size:.86rem;opacity:.8;margin-top:.3rem;}
.sa-next{position:relative;border-radius:24px;padding:3px;overflow:hidden;animation:saPop .55s ease both;}
.sa-next::before{content:"";position:absolute;inset:-60%;background:conic-gradient(from 0deg,#4A7023,#A8D672,#F2B544,#6B9B37,#4A7023);animation:saSpin 6s linear infinite;}
.sa-next-inner{position:relative;background:var(--card);border-radius:21px;padding:1.1rem 1.2rem;}
.sa-next .kicker{font-size:.78rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--leaf);}
.sa-next .topic{font-size:1.6rem;font-weight:900;color:var(--text);margin:.2rem 0 .5rem;}
.sa-side-head{background:linear-gradient(135deg,#4A7023,#6B9B37);color:#fff;border-radius:18px;padding:1rem;box-shadow:var(--shadow);}
.sa-side-head .t{font-weight:900;font-size:1.15rem;}
.sa-side-row{display:flex;justify-content:space-between;gap:.5rem;padding:.4rem 0;border-bottom:1px dashed var(--mint);font-size:.9rem;}
.sa-side-row span:last-child{font-weight:700;text-align:right;}
.sa-side-head .sa-side-row{border-bottom-color:rgba(255,255,255,.25);}
@media (max-width:640px){.block-container{padding-top:4.2rem;}.sa-tiles{grid-template-columns:repeat(3,minmax(0,1fr));}.sa-stepper{border-radius:18px;}.sa-arrow{display:none;}}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;}}
</style>
"""
# Inject the global CSS into the page once per rerun.
def inject_styles() -> None:
    st.html(GLOBAL_CSS)
