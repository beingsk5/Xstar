<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1920,height=1080">
<title>Xstar Sports MAIN — 1920×1080</title>
<link rel="stylesheet" href="fonts/xstar-fonts.css">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#04060f;
  --glass:rgba(12,16,35,0.72);
  --glass2:rgba(18,24,50,0.65);
  --glass-border:rgba(255,255,255,0.07);
  --glass-border-bright:rgba(255,255,255,0.13);
  --gold:#f6bc1a;--gold2:#ffe680;--goldd:#c8920a;
  --red:#e8192c;--red2:#ff4d5e;
  --cyan:#00d4c8;--cyan2:#4dfffb;
  --blue:#3a7cff;--blue2:#7aaaff;
  --orange:#ff7c00;--purple:#a06cff;
  --white:#eef2ff;--muted:#4e5878;--dim:#1e2540;
  --F:'Oswald',sans-serif;
  --FC:'Barlow Condensed',sans-serif;
  --FD:'Rajdhani',sans-serif;
}
html,body{width:1920px;height:1080px;overflow:hidden;background:var(--bg);color:var(--white);cursor:none}

/* ══ ANIMATED BACKGROUND ══ */
.bg-mesh{
  position:fixed;inset:0;z-index:0;
  background:
    radial-gradient(ellipse 120% 80% at 50% -10%,rgba(58,124,255,.14),transparent 55%),
    radial-gradient(ellipse 60% 60% at 95% 45%,rgba(246,188,26,.09),transparent 50%),
    radial-gradient(ellipse 50% 70% at 5% 95%,rgba(0,212,200,.07),transparent 50%),
    radial-gradient(ellipse 80% 50% at 50% 120%,rgba(160,108,255,.06),transparent 50%),
    var(--bg)
}
.bg-grid{
  position:fixed;inset:0;z-index:0;
  background-image:
    linear-gradient(rgba(58,124,255,.03) 1px,transparent 1px),
    linear-gradient(90deg,rgba(58,124,255,.03) 1px,transparent 1px);
  background-size:80px 80px;
  animation:bgscroll 40s linear infinite
}
@keyframes bgscroll{to{background-position:80px 80px}}
.bg-vignette{position:fixed;inset:0;z-index:1;background:radial-gradient(ellipse 140% 140% at 50% 50%,transparent 30%,rgba(4,6,15,.8) 100%);pointer-events:none}
.bg-scan{position:fixed;inset:0;z-index:1;pointer-events:none;background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,0,0,.012) 3px,rgba(0,0,0,.012) 4px)}

/* ══ GLASS MIXIN ══ */
.glass{
  background:var(--glass);
  backdrop-filter:blur(18px) saturate(1.4);
  -webkit-backdrop-filter:blur(18px) saturate(1.4);
  border:1px solid var(--glass-border);
}
.glass-bright{
  background:var(--glass2);
  backdrop-filter:blur(22px) saturate(1.6);
  -webkit-backdrop-filter:blur(22px) saturate(1.6);
  border:1px solid var(--glass-border-bright);
}

/* ══ LAYOUT ══ */
#wrap{position:relative;z-index:10;width:1920px;height:1080px;display:grid;grid-template-rows:68px 1fr 82px}

/* ══ TOP BAR ══ */
#topbar{
  display:flex;align-items:center;gap:0;
  background:linear-gradient(90deg,rgba(6,9,22,.97),rgba(10,14,30,.94));
  border-bottom:1px solid rgba(255,255,255,.06);
  position:relative;overflow:hidden;padding:0 20px 0 0;
  box-shadow:0 4px 30px rgba(0,0,0,.4)
}
#topbar::after{
  content:'';position:absolute;bottom:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--goldd),var(--gold),var(--blue),var(--cyan),var(--gold),var(--goldd));
  background-size:400%;animation:goldflow 7s linear infinite
}
@keyframes goldflow{to{background-position:400%}}

/* Brand */
.ch-brand{
  display:flex;align-items:center;gap:12px;
  background:linear-gradient(90deg,rgba(246,188,26,.12),transparent);
  border-right:1px solid rgba(255,255,255,.06);
  padding:0 24px 0 20px;height:100%;flex-shrink:0
}
.ch-icon{
  width:42px;height:42px;border-radius:10px;
  background:linear-gradient(135deg,var(--gold),#c87000);
  display:flex;align-items:center;justify-content:center;
  font-family:var(--F);font-size:18px;font-weight:900;color:#000;letter-spacing:-1px;
  box-shadow:0 0 22px rgba(246,188,26,.5),0 3px 12px rgba(0,0,0,.6)
}
.ch-name{font-family:var(--F);font-size:23px;font-weight:700;letter-spacing:2px;text-transform:uppercase;line-height:1.1}
.ch-name .x{color:var(--gold)}
.ch-tagline{font-family:var(--FC);font-size:11px;font-weight:600;color:var(--muted);letter-spacing:3px;text-transform:uppercase}

/* Live badge */
.live-pill{
  display:flex;align-items:center;gap:6px;
  background:var(--red);color:#fff;
  font-family:var(--F);font-size:13px;font-weight:700;letter-spacing:2.5px;
  padding:5px 13px 5px 10px;border-radius:5px;margin-left:16px;flex-shrink:0;
  box-shadow:0 0 20px rgba(232,25,44,.55);
  animation:livepulse 2.2s ease infinite
}
@keyframes livepulse{0%,100%{box-shadow:0 0 16px rgba(232,25,44,.5)}50%{box-shadow:0 0 32px rgba(232,25,44,.9)}}
.live-dot{width:7px;height:7px;background:#fff;border-radius:50%;flex-shrink:0;animation:dot 1.2s ease infinite}
@keyframes dot{0%,100%{opacity:1}50%{opacity:.2}}

/* Top bar center */
.topbar-center{flex:1;display:flex;align-items:center;justify-content:center;gap:14px;padding:0 16px}
.t-series{font-family:var(--F);font-size:13px;font-weight:500;color:var(--muted);letter-spacing:2px;text-transform:uppercase}
.t-dot{color:rgba(255,255,255,.15);font-size:14px}
.t-match{font-family:var(--F);font-size:17px;font-weight:600;color:var(--gold)}
.t-format{
  font-family:var(--F);font-size:13px;font-weight:700;letter-spacing:2.5px;
  border:1px solid rgba(246,188,26,.4);color:var(--gold);
  padding:3px 9px;border-radius:4px;
  background:rgba(246,188,26,.08)
}
.t-venue{font-family:var(--FC);font-size:13px;color:var(--muted);display:flex;align-items:center;gap:4px}
.topbar-right{display:flex;align-items:center;gap:12px}
.tb-clock{
  font-family:var(--FD);font-size:22px;font-weight:700;letter-spacing:3px;
  background:rgba(255,255,255,.04);padding:5px 14px;border-radius:5px;
  border:1px solid rgba(255,255,255,.07)
}

/* ══ MAIN ══ */
#main{display:grid;grid-template-columns:358px 1fr 320px;overflow:hidden;gap:0}

/* ══ LEFT PANEL ══ */
#left{
  background:linear-gradient(180deg,rgba(10,13,28,.97),rgba(6,9,20,.96));
  border-right:1px solid rgba(255,255,255,.05);
  display:flex;flex-direction:column;padding:16px 14px;gap:10px;
  position:relative;overflow:hidden
}
#left::before{
  content:'';position:absolute;top:0;left:0;width:3px;height:100%;
  background:linear-gradient(180deg,var(--gold),var(--blue),var(--cyan),transparent)
}

.l-label{
  font-family:var(--F);font-size:12px;font-weight:600;color:var(--muted);
  letter-spacing:2.5px;text-transform:uppercase;
  padding-bottom:10px;border-bottom:1px solid rgba(255,255,255,.05)
}

/* Glass team cards */
.team-card{
  border-radius:10px;padding:10px 12px;
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.07);
  position:relative;overflow:hidden;
  transition:all .5s cubic-bezier(.4,0,.2,1)
}
.team-card::before{
  content:'';position:absolute;inset:0;border-radius:10px;
  background:linear-gradient(135deg,rgba(255,255,255,.04),transparent);
  pointer-events:none
}
.team-card.batting{
  background:rgba(246,188,26,.07);
  border-color:rgba(246,188,26,.3);
  box-shadow:0 0 24px rgba(246,188,26,.1),inset 0 0 30px rgba(246,188,26,.04)
}
.team-card.batting::after{
  content:'BAT';position:absolute;top:7px;right:10px;
  font-family:var(--F);font-size:9px;font-weight:700;color:var(--gold);letter-spacing:2px
}
.tc-row{display:flex;align-items:center;gap:9px}
.tc-flag{
  width:40px;height:28px;border-radius:5px;
  background:rgba(255,255,255,.05);
  display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;
  border:1px solid rgba(255,255,255,.08)
}
.tc-name{font-family:var(--F);font-size:24px;font-weight:700;color:var(--white);flex:1}
.tc-score{font-family:var(--FD);font-size:30px;font-weight:700;color:var(--gold);text-align:right;line-height:1}
.tc-overs{font-size:12px;color:var(--muted);text-align:right;margin-top:1px}

/* Target banner */
.target-banner{
  display:none;
  border-radius:9px;padding:9px 12px;text-align:center;
  background:rgba(0,212,200,.08);
  border:1px solid rgba(0,212,200,.25);
  box-shadow:0 0 20px rgba(0,212,200,.08)
}
.target-banner.show{display:block}
.tb-lbl{font-size:11px;font-weight:700;color:var(--cyan);letter-spacing:2px;text-transform:uppercase;margin-bottom:2px}
.tb-val{font-family:var(--FD);font-size:30px;font-weight:700;color:var(--cyan);line-height:1}
.tb-sub{font-size:12px;color:var(--white);margin-top:2px}

/* Status badge */
.status-badge{
  display:flex;align-items:center;justify-content:center;gap:7px;
  padding:6px 12px;border-radius:20px;
  font-family:var(--F);font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase
}
.status-badge.live{background:rgba(232,25,44,.12);color:var(--red2);border:1px solid rgba(232,25,44,.25)}
.status-badge.break{background:rgba(246,188,26,.1);color:var(--gold);border:1px solid rgba(246,188,26,.25)}
.status-badge.complete{background:rgba(0,212,200,.1);color:var(--cyan);border:1px solid rgba(0,212,200,.25)}
.status-badge.interrupt{background:rgba(255,124,0,.1);color:var(--orange);border:1px solid rgba(255,124,0,.25)}

/* Stats 2×2 glass boxes */
.stats2{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.sbox{
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.07);
  border-radius:8px;padding:8px 10px;text-align:center;
  backdrop-filter:blur(8px)
}
.sbox-l{font-size:10px;font-weight:700;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-bottom:2px}
.sbox-v{font-family:var(--FD);font-size:21px;font-weight:700;color:var(--white);line-height:1}
.sbox-v.g{color:var(--cyan)}.sbox-v.r{color:var(--red2)}.sbox-v.y{color:var(--gold)}

/* Phase strip */
.mps-strip{
  display:flex;align-items:center;justify-content:space-between;
  padding:5px 10px;
  background:rgba(0,212,200,.05);
  border:1px solid rgba(0,212,200,.12);
  border-radius:7px;flex-shrink:0
}
.mps-inn{font-family:var(--F);font-size:12px;font-weight:700;color:var(--cyan);letter-spacing:1.5px;text-transform:uppercase}
.mps-ov{font-family:var(--FD);font-size:13px;font-weight:600;color:var(--white)}

/* Phase pill */
.phase-pill{
  font-family:var(--F);font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;
  padding:3px 9px;border-radius:4px;display:none
}
.phase-pill.POWERPLAY{background:rgba(246,188,26,.18);color:var(--gold);border:1px solid rgba(246,188,26,.3)}
.phase-pill.MIDDLE{background:rgba(58,124,255,.14);color:var(--blue2);border:1px solid rgba(58,124,255,.25)}
.phase-pill.DEATH{background:rgba(232,25,44,.14);color:var(--red2);border:1px solid rgba(232,25,44,.25)}

/* Win probability */
.wp-lbl{font-size:11px;font-weight:700;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-bottom:5px}
.wp-bar{height:18px;background:rgba(255,255,255,.04);border-radius:5px;overflow:hidden;border:1px solid rgba(255,255,255,.07);display:flex}
.wp-t1{height:100%;background:linear-gradient(90deg,var(--blue),#5599ff);display:flex;align-items:center;padding:0 6px;font-family:var(--F);font-size:11px;font-weight:700;transition:width 1.6s cubic-bezier(.4,0,.2,1);min-width:26px}
.wp-t2{flex:1;height:100%;background:linear-gradient(90deg,var(--orange),var(--red));display:flex;align-items:center;justify-content:flex-end;padding:0 6px;font-family:var(--F);font-size:11px;font-weight:700;min-width:26px}
.wp-lbls{display:flex;justify-content:space-between;margin-top:3px;font-size:11px;color:var(--muted)}
.wp-t1.tied,.wp-t2.tied{background:linear-gradient(90deg,#4e5878,#6a7090)!important}
.wp-tied-label{display:none;text-align:center;font-family:var(--F);font-size:11px;font-weight:700;color:var(--muted);letter-spacing:3px;text-transform:uppercase;margin-top:3px;animation:blink 1.5s ease infinite}
.wp-tied-label.show{display:block}

/* Partnership live */
.pship-live{
  display:none;
  background:rgba(0,212,200,.06);border:1px solid rgba(0,212,200,.18);border-radius:7px;
  padding:7px 10px;align-items:center;justify-content:space-between
}
.pship-live.show{display:flex}
.pl-lbl{font-size:11px;color:var(--cyan);font-weight:700;letter-spacing:2px;text-transform:uppercase}
.pl-val{font-family:var(--FD);font-size:16px;font-weight:700;color:var(--cyan)}

.toss-strip{
  font-size:12px;color:var(--white);
  background:rgba(246,188,26,.05);border:1px solid rgba(246,188,26,.12);
  border-radius:5px;padding:5px 9px;line-height:1.4
}
.toss-strip b{color:var(--gold)}

/* ══ CENTER ══ */
#center{display:flex;flex-direction:column;overflow:hidden;background:rgba(4,6,15,.45)}

/* Panel bar */
.panel-bar{
  display:flex;align-items:stretch;
  background:rgba(8,11,24,.92);
  border-bottom:1px solid rgba(255,255,255,.05);
  flex-shrink:0;height:50px;position:relative
}
.panel-progress{position:absolute;bottom:0;left:0;height:2px;background:var(--gold);width:0%;z-index:10}
.panel-progress.go{transition:width var(--dur,15s) linear}
.pp{
  flex:1;display:flex;align-items:center;justify-content:center;gap:6px;
  font-family:var(--F);font-size:14px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;
  color:var(--muted);border-right:1px solid rgba(255,255,255,.05);position:relative;user-select:none
}
.pp:last-of-type{border-right:none}
.pp.on{color:var(--gold);background:rgba(246,188,26,.05)}
.pp.on::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--gold)}
.pp-num{
  width:20px;height:20px;border-radius:50%;
  background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.09);
  display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;
  transition:all .3s
}
.pp.on .pp-num{background:var(--gold);border-color:var(--gold);color:#000}
.panel-next{
  flex-shrink:0;display:flex;align-items:center;gap:6px;padding:0 14px;
  border-left:1px solid rgba(255,255,255,.05);
  font-family:var(--F);font-size:12px;font-weight:600;color:var(--muted);letter-spacing:1.5px;white-space:nowrap
}
.panel-next span{color:var(--white)}

/* Panes */
.pane{display:none;flex:1;overflow:hidden;flex-direction:column}
.pane.on{display:flex}
.scrollable{flex:1;overflow-y:auto;scrollbar-width:thin;scrollbar-color:rgba(255,255,255,.08) transparent}
.scrollable::-webkit-scrollbar{width:3px}
.scrollable::-webkit-scrollbar-thumb{background:rgba(255,255,255,.08);border-radius:2px}

/* Scorecard */
.sc-hdr{
  display:grid;padding:9px 18px;
  background:rgba(255,255,255,.03);border-bottom:1px solid rgba(255,255,255,.05);
  font-size:11px;font-weight:700;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase;
  position:sticky;top:0;z-index:5
}
.sc-hdr.bat{grid-template-columns:1fr 58px 62px 50px 50px 66px}
.sc-hdr.bowl{grid-template-columns:1fr 58px 58px 58px 64px 50px}
.sc-row{display:grid;padding:13px 18px;min-height:58px;border-bottom:1px solid rgba(255,255,255,.04);align-items:center;transition:background .15s}
.sc-row:hover{background:rgba(255,255,255,.02)}
.sc-row.bat{grid-template-columns:1fr 58px 62px 50px 50px 66px}
.sc-row.bowl{grid-template-columns:1fr 58px 58px 58px 64px 50px}
.sc-row.extras{grid-template-columns:1fr auto;background:rgba(246,188,26,.03);border-top:1px solid rgba(255,255,255,.05);padding:9px 18px}
.sc-n{font-size:16px;font-weight:700;color:var(--white)}
.sc-n.no{color:var(--cyan)}.sc-nd{font-size:12px;color:var(--muted);margin-top:2px}
.sc-v{font-family:var(--FD);font-size:18px;font-weight:700;color:var(--white);text-align:center}
.sc-v.big{font-size:21px}.sc-v.W{color:var(--red2)}.sc-v.g{color:var(--cyan)}.sc-v.y{color:var(--gold)}

/* Innings selector */
.sc-inn-selector{
  display:flex;align-items:center;gap:0;
  background:rgba(255,255,255,.03);border-bottom:1px solid rgba(255,255,255,.05);
  flex-shrink:0;padding:5px 13px
}
.sc-inn-btn{
  font-family:var(--F);font-size:13px;font-weight:600;letter-spacing:1.5px;
  text-transform:uppercase;padding:6px 16px;border-radius:4px;cursor:default;
  color:var(--muted);transition:all .2s
}
.sc-inn-btn.active{background:var(--gold);color:#000}
.sc-inn-btn:not(.active){border:1px solid rgba(255,255,255,.07)}

/* Partnerships */
.pr-row{display:flex;align-items:center;gap:9px;padding:8px 14px;border-bottom:1px solid rgba(255,255,255,.04)}
.pr-names{font-size:14px;font-weight:600;color:var(--white);width:210px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex-shrink:0}
.pr-bg{flex:1;height:10px;background:rgba(255,255,255,.05);border-radius:3px;overflow:hidden;border:1px solid rgba(255,255,255,.07)}
.pr-bar{height:100%;background:linear-gradient(90deg,var(--blue),var(--cyan));border-radius:3px;transition:width .7s}
.pr-stat{font-family:var(--FD);font-size:16px;font-weight:700;color:var(--gold);width:72px;text-align:right;flex-shrink:0}
.fow-wrap{padding:10px 14px;display:flex;flex-wrap:wrap;gap:6px}
.fow-chip{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:8px;padding:7px 10px}
.fow-wkt{font-family:var(--FD);font-size:19px;font-weight:700;color:var(--red2);line-height:1}
.fow-bat{font-size:13px;color:var(--white);margin-top:2px}
.fow-ov{font-size:12px;color:var(--muted)}

/* ── COMMENTARY — glass panel ── */
.comm-zone{
  flex-shrink:0;
  border-top:2px solid rgba(246,188,26,.5);
  display:flex;flex-direction:column;
  height:308px;
  background:rgba(6,9,20,.85)
}
.comm-hdr{
  display:flex;align-items:center;justify-content:space-between;
  padding:10px 18px;
  background:rgba(255,255,255,.03);border-bottom:1px solid rgba(255,255,255,.05);
  flex-shrink:0
}
.comm-hdr-left{display:flex;align-items:center;gap:8px}
.comm-ch-icon{
  width:22px;height:22px;border-radius:5px;
  background:linear-gradient(135deg,var(--gold),#c87000);
  display:flex;align-items:center;justify-content:center;
  font-family:var(--F);font-size:10px;font-weight:900;color:#000
}
.comm-title{font-family:var(--F);font-size:15px;font-weight:700;color:var(--white);letter-spacing:1.5px;text-transform:uppercase}
.innings-pill{display:flex;align-items:center;gap:5px;padding:4px 12px;border-radius:10px;font-family:var(--F);font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase}
.innings-pill.first{background:rgba(58,124,255,.12);color:var(--blue2);border:1px solid rgba(58,124,255,.25)}
.innings-pill.second{background:rgba(0,212,200,.1);color:var(--cyan);border:1px solid rgba(0,212,200,.25)}
.innings-pill.super{background:rgba(246,188,26,.18);color:var(--gold);border:1px solid rgba(246,188,26,.4);animation:superpulse 1.5s ease infinite}
@keyframes superpulse{0%,100%{box-shadow:0 0 0 rgba(246,188,26,0)}50%{box-shadow:0 0 10px rgba(246,188,26,.4)}}
.innings-pip{width:5px;height:5px;border-radius:50%;background:currentColor}
.comm-list{overflow:hidden}
.ci{
  display:flex;gap:11px;padding:7px 18px;
  border-bottom:1px solid rgba(255,255,255,.04);
  animation:ciIn .3s ease;max-height:44px;overflow:hidden
}
@keyframes ciIn{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:none}}
.ci.EV_FOUR{background:rgba(246,188,26,.04);border-left:3px solid var(--gold)}
.ci.EV_SIX{background:rgba(58,124,255,.05);border-left:3px solid var(--blue)}
.ci.EV_WICKET,.ci.EV_OUT{background:rgba(232,25,44,.05);border-left:3px solid var(--red)}
.ci.EV_NOBALL{background:rgba(0,212,200,.04);border-left:3px solid var(--cyan)}
.ci.EV_REVIEW{background:rgba(255,124,0,.04);border-left:3px solid var(--orange)}
.ci-over{font-family:var(--FD);font-size:15px;font-weight:700;color:var(--gold);width:40px;flex-shrink:0;padding-top:1px}
.ci-txt{font-size:14px;color:var(--white);line-height:1.4;flex:1}
.ci-bdg{display:inline-flex;align-items:center;padding:2px 6px;border-radius:3px;font-family:var(--F);font-size:11px;font-weight:700;letter-spacing:1px;margin-left:5px}
.ci-bdg.FOUR{background:rgba(246,188,26,.18);color:var(--gold)}
.ci-bdg.SIX{background:rgba(58,124,255,.18);color:var(--blue2)}
.ci-bdg.WICKET,.ci-bdg.OUT{background:rgba(232,25,44,.18);color:var(--red2)}
.ci-bdg.NOBALL{background:rgba(0,212,200,.15);color:var(--cyan)}
.ci-bdg.WIDE{background:rgba(255,255,255,.06);color:var(--muted)}
.ci-bdg.REVIEW{background:rgba(255,124,0,.18);color:var(--orange)}

/* ══ RIGHT PANEL ══ */
#right{
  background:linear-gradient(180deg,rgba(10,13,28,.97),rgba(6,9,20,.96));
  border-left:1px solid rgba(255,255,255,.05);
  display:flex;flex-direction:column;padding:14px 12px;gap:9px;overflow:hidden
}
.r-title{font-family:var(--F);font-size:12px;font-weight:700;color:var(--muted);letter-spacing:3px;text-transform:uppercase;padding-bottom:9px;border-bottom:1px solid rgba(255,255,255,.05)}

/* Glass player cards */
.bat-card{
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.08);
  border-radius:9px;padding:10px 11px;position:relative;overflow:hidden
}
.bat-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px}
.bat-card.striker::before{background:linear-gradient(90deg,var(--gold),transparent)}
.bat-card.ns::before{background:linear-gradient(90deg,var(--blue),transparent)}
.bat-card.striker{
  background:rgba(246,188,26,.06);
  border-color:rgba(246,188,26,.2);
  box-shadow:0 0 18px rgba(246,188,26,.07)
}
.bc-lbl{font-size:10px;font-weight:700;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-bottom:3px}
.bc-name{font-family:var(--F);font-size:16px;font-weight:700;color:var(--white);line-height:1;margin-bottom:5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bc-stats{display:flex;gap:8px}
.bs{text-align:center}
.bs-v{font-family:var(--FD);font-size:17px;font-weight:700;line-height:1}
.bs-v.main{font-size:20px;color:var(--gold)}.bs-v.g{color:var(--cyan)}.bs-v.b{color:var(--blue2)}
.bs-l{font-size:10px;color:var(--muted);letter-spacing:1px;text-transform:uppercase}

.bowl-card{
  background:rgba(232,25,44,.05);
  border:1px solid rgba(232,25,44,.15);
  border-radius:9px;padding:10px 11px;position:relative;overflow:hidden
}
.bowl-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--red),transparent)}

/* Balls track */
.balls-lbl{font-size:10px;font-weight:700;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-bottom:5px}
.balls-track{display:flex;gap:5px;flex-wrap:wrap}
.ball{
  width:30px;height:30px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-family:var(--FD);font-size:13px;font-weight:700;border:2px solid
}
.ball.dot{background:rgba(78,88,120,.12);border-color:rgba(255,255,255,.09);color:var(--muted)}
.ball.run{background:rgba(238,242,255,.06);border-color:rgba(255,255,255,.13);color:var(--white)}
.ball.four{background:rgba(246,188,26,.18);border-color:var(--gold);color:var(--gold)}
.ball.six{background:rgba(58,124,255,.18);border-color:var(--blue);color:var(--blue2)}
.ball.wkt{background:rgba(232,25,44,.18);border-color:var(--red);color:var(--red2)}
.ball.wd{background:rgba(0,212,200,.12);border-color:var(--cyan);color:var(--cyan)}
.ball.nb{background:rgba(255,124,0,.15);border-color:var(--orange);color:var(--orange)}
.ball.fh{background:rgba(160,108,255,.18);border-color:#a06cff;color:#c8a0ff}

.fh-ring{
  display:none;align-items:center;justify-content:center;gap:5px;
  padding:5px 10px;border-radius:16px;
  background:rgba(160,108,255,.1);border:1px solid rgba(160,108,255,.35);
  font-family:var(--F);font-size:10px;font-weight:700;letter-spacing:2px;color:#c8a0ff;
  text-transform:uppercase;animation:fhpulse 1.5s ease infinite
}
.fh-ring.show{display:flex}
@keyframes fhpulse{0%,100%{box-shadow:0 0 0 rgba(160,108,255,0)}50%{box-shadow:0 0 12px rgba(160,108,255,.4)}}

.lw-box{background:rgba(232,25,44,.06);border:1px solid rgba(232,25,44,.18);border-radius:7px;padding:7px 10px}
.lw-lbl{font-size:10px;font-weight:700;color:var(--red2);letter-spacing:2px;text-transform:uppercase;margin-bottom:3px}
.lw-txt{font-size:13px;color:var(--white);line-height:1.4}

/* ══ GLASS TICKER ══ */
#ticker{
  display:flex;align-items:center;
  background:rgba(5,7,18,.95);
  border-top:1px solid rgba(255,255,255,.05);
  overflow:hidden;position:relative
}
#ticker::before{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--gold),var(--blue),var(--cyan),var(--gold));
  background-size:400%;animation:goldflow 7s linear infinite
}
.tk-ch{
  flex-shrink:0;display:flex;align-items:center;gap:7px;padding:0 14px;height:100%;
  background:linear-gradient(90deg,rgba(246,188,26,.12),rgba(246,188,26,.04));
  border-right:1px solid rgba(246,188,26,.18)
}
.tk-ch-name{font-family:var(--F);font-size:14px;font-weight:700;letter-spacing:2px;color:var(--gold);text-transform:uppercase}
.tk-live{
  flex-shrink:0;background:var(--red);color:#fff;
  font-family:var(--F);font-size:12px;font-weight:700;letter-spacing:2px;
  padding:0 14px;height:100%;display:flex;align-items:center;
  clip-path:polygon(0 0,calc(100% - 8px) 0,100% 50%,calc(100% - 8px) 100%,0 100%)
}
.tk-sw{flex:1;overflow:hidden;height:100%;display:flex;align-items:center;padding:0 8px}
.tk-sc{
  display:flex;gap:40px;align-items:center;
  animation:ticker 42s linear infinite;
  white-space:nowrap;font-family:var(--FD);font-size:16px;font-weight:600;color:var(--white)
}
@keyframes ticker{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.tk-sep{color:var(--gold)}.tk-hi{color:var(--gold);font-weight:700}
.tk-time{
  flex-shrink:0;background:rgba(255,255,255,.04);padding:0 14px;height:100%;
  border-left:1px solid rgba(255,255,255,.06);
  display:flex;align-items:center;
  font-family:var(--FD);font-size:16px;font-weight:700;letter-spacing:2px
}

/* Channel watermark */
.ch-watermark{
  position:fixed;bottom:92px;right:16px;z-index:50;
  display:flex;align-items:center;gap:6px;
  opacity:.5;pointer-events:none
}
.cw-name{font-family:var(--F);font-size:13px;font-weight:700;letter-spacing:2px;color:var(--gold);text-transform:uppercase}

/* ═══ SPECIAL SCREENS — all glass style ═══ */

/* Standby */
#standby{
  position:fixed;inset:0;z-index:200;
  background:radial-gradient(ellipse 130% 130% at 50% 50%,#080b1e,#03040d);
  display:none;flex-direction:column;align-items:center;justify-content:center;gap:18px
}
#standby.show{display:flex}
.sb-logo{font-family:var(--F);font-size:54px;font-weight:700;letter-spacing:5px}
.sb-logo .x{color:var(--gold)}
.sb-msg{font-family:var(--F);font-size:15px;color:var(--muted);letter-spacing:3px;animation:blink 2s ease infinite}
@keyframes blink{0%,100%{opacity:.3}50%{opacity:1}}
.sb-prog{width:260px;height:2px;background:rgba(255,255,255,.06);border-radius:1px;overflow:hidden}
.sb-fill{height:100%;background:linear-gradient(90deg,var(--gold),var(--blue),var(--cyan));animation:sbsc 2.8s ease infinite}
@keyframes sbsc{0%{width:0;margin-left:0}50%{width:100%;margin-left:0}100%{width:0;margin-left:100%}}

/* Skeleton */
#skeleton{position:fixed;inset:0;z-index:180;background:radial-gradient(ellipse 130% 130% at 50% 50%,#080b1e,#03040d);display:none;flex-direction:column;align-items:center;justify-content:center;gap:24px}
#skeleton.show{display:flex}
.sk-logo{font-family:var(--F);font-size:42px;font-weight:700;letter-spacing:4px;opacity:.6}
.sk-logo .x{color:var(--gold)}
.sk-msg{font-family:var(--F);font-size:12px;color:var(--muted);letter-spacing:3px;text-transform:uppercase}
.sk-blocks{display:flex;flex-direction:column;gap:10px;width:320px}
.sk-block{height:16px;border-radius:4px;background:linear-gradient(90deg,rgba(255,255,255,.04) 25%,rgba(255,255,255,.1) 50%,rgba(255,255,255,.04) 75%);background-size:200% 100%;animation:shimmer 1.8s ease infinite}
.sk-block.w60{width:60%}.sk-block.w80{width:80%}.sk-block.w40{width:40%}
@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}

/* Countdown */
#countdown{position:fixed;inset:0;z-index:178;background:radial-gradient(ellipse 130% 130% at 50% 50%,#0c0f1e,#06080f);display:none;flex-direction:column;align-items:center;justify-content:center;gap:16px}
#countdown.show{display:flex}
.cd-eyebrow{font-family:var(--F);font-size:12px;letter-spacing:5px;color:var(--muted);text-transform:uppercase}
.cd-match{font-family:var(--F);font-size:30px;font-weight:700;color:var(--white);letter-spacing:2px}
.cd-lbl{font-family:var(--F);font-size:17px;font-weight:600;color:var(--muted);letter-spacing:3px;text-transform:uppercase}
.cd-clock{font-family:var(--FD);font-size:78px;font-weight:700;color:var(--gold);letter-spacing:4px;animation:glowpulse 1s ease infinite}
@keyframes glowpulse{0%,100%{text-shadow:0 0 30px rgba(246,188,26,.3)}50%{text-shadow:0 0 60px rgba(246,188,26,.7)}}

/* Break */
#break-screen{position:fixed;inset:0;z-index:176;background:radial-gradient(ellipse 130% 130% at 50% 50%,#0c0f1e,#06080f);display:none;flex-direction:column;align-items:center;justify-content:center;gap:20px}
#break-screen.show{display:flex}
.bs-eyebrow{font-family:var(--F);font-size:12px;letter-spacing:5px;color:var(--muted);text-transform:uppercase}
.bs-title{font-family:var(--F);font-size:70px;font-weight:700;letter-spacing:5px;color:var(--white);animation:glowpulse 2.8s ease infinite;text-align:center}
.bs-title .x{color:var(--gold)}
.bs-score{font-family:var(--FD);font-size:90px;font-weight:700;color:var(--gold);line-height:1}
.bs-status{font-family:var(--F);font-size:16px;color:var(--muted);letter-spacing:3px;text-transform:uppercase}
.bs-line{width:180px;height:2px;background:linear-gradient(90deg,transparent,var(--gold),transparent)}

/* Interruption */
#interrupt-screen{position:fixed;inset:0;z-index:174;background:radial-gradient(ellipse 130% 130% at 50% 50%,#0c0f1e,#06080f);display:none;flex-direction:column;align-items:center;justify-content:center;gap:18px}
#interrupt-screen.show{display:flex}
.is-icon{font-size:96px;animation:bob 2s ease infinite}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
.is-type{font-family:var(--F);font-size:52px;font-weight:700;letter-spacing:4px;color:var(--orange);text-transform:uppercase;text-align:center}
.is-score{font-family:var(--FD);font-size:64px;font-weight:700;color:var(--gold);line-height:1}
.is-status{font-family:var(--FC);font-size:22px;color:var(--white);text-align:center;max-width:900px;line-height:1.4}
.is-resume{font-family:var(--F);font-size:13px;color:var(--muted);letter-spacing:3px;text-transform:uppercase;animation:blink 2s ease infinite}

/* Complete */
#complete-screen{position:fixed;inset:0;z-index:172;background:radial-gradient(ellipse 130% 130% at 50% 50%,#0c0f1e,#06080f);display:none;flex-direction:column;align-items:center;justify-content:center;gap:18px}
#complete-screen.show{display:flex}
.mc-ch{font-family:var(--F);font-size:13px;letter-spacing:4px;color:var(--muted);text-transform:uppercase}
.mc-title{font-family:var(--F);font-size:60px;font-weight:700;letter-spacing:4px;color:var(--cyan);text-shadow:0 0 50px rgba(0,212,200,.5)}
.mc-score{font-family:var(--FD);font-size:80px;font-weight:700;color:var(--gold);line-height:1}
.mc-result{font-family:var(--F);font-size:26px;font-weight:600;color:var(--white);text-align:center;max-width:900px;line-height:1.4}

/* DLS overlay */
.dls-overlay{position:fixed;inset:0;z-index:320;pointer-events:none;display:flex;align-items:center;justify-content:center;opacity:0;transform:scale(.85)}
.dls-overlay.show{animation:evIn .25s cubic-bezier(.22,1,.36,1) forwards,evOut .45s ease 5.1s forwards}
.dls-card{background:rgba(0,50,45,.85);backdrop-filter:blur(20px);border:2px solid var(--cyan);border-radius:16px;padding:30px 60px;text-align:center;box-shadow:0 0 80px rgba(0,212,200,.45),0 40px 100px rgba(0,0,0,.8)}
.dls-eyebrow{font-family:var(--F);font-size:13px;color:var(--muted);letter-spacing:4px;text-transform:uppercase;margin-bottom:8px}
.dls-title{font-family:var(--F);font-size:42px;font-weight:700;color:var(--cyan);letter-spacing:3px;text-shadow:0 0 40px rgba(0,212,200,.7)}
.dls-target{font-family:var(--FD);font-size:100px;font-weight:700;color:var(--gold);line-height:1;margin:8px 0}
.dls-sub{font-family:var(--FC);font-size:20px;color:var(--white);margin-top:4px}

/* ═══ EVENT OVERLAYS — glass style ═══ */
.ev{position:fixed;inset:0;z-index:300;pointer-events:none;display:flex;align-items:center;justify-content:center;opacity:0;transform:scale(.82)}
.ev.show{animation:evIn .22s cubic-bezier(.22,1,.36,1) forwards,evOut .45s ease 3.1s forwards}
@keyframes evIn{to{opacity:1;transform:scale(1)}}
@keyframes evOut{to{opacity:0;transform:scale(1.04)}}

.ev-card{border-radius:18px;padding:32px 68px;text-align:center;position:relative;overflow:hidden;backdrop-filter:blur(24px)}
.ev-t{font-family:var(--F);font-weight:700;line-height:.9}
.ev-s{font-family:var(--F);font-weight:600;letter-spacing:4px;text-transform:uppercase;margin-top:7px}
.ev-d{font-family:var(--FC);font-size:17px;margin-top:7px;opacity:.75;line-height:1.4}

.ev-wicket .ev-card{background:rgba(18,4,16,.85);border:2px solid var(--red);box-shadow:0 0 80px rgba(232,25,44,.5),0 40px 100px rgba(0,0,0,.8)}
.ev-wicket .ev-t{font-size:124px;color:var(--red2);text-shadow:0 0 50px rgba(232,25,44,.8)}
.ev-wicket .ev-s{font-size:26px;color:var(--white)}

.ev-four .ev-card{background:rgba(20,15,0,.85);border:2px solid var(--gold);box-shadow:0 0 80px rgba(246,188,26,.45),0 40px 100px rgba(0,0,0,.8)}
.ev-four .ev-t{font-size:154px;color:var(--gold);text-shadow:0 0 60px rgba(246,188,26,.8)}
.ev-four .ev-s{font-size:26px;color:var(--gold2)}

.ev-six .ev-card{background:rgba(0,12,30,.85);border:2px solid var(--blue);box-shadow:0 0 80px rgba(58,124,255,.5),0 40px 100px rgba(0,0,0,.8)}
.ev-six .ev-t{font-size:154px;color:var(--blue2);text-shadow:0 0 60px rgba(58,124,255,.8)}
.ev-six .ev-s{font-size:26px;color:#a8ccff}

.ev-lbw .ev-card{background:rgba(18,0,16,.85);border:2px solid #e040fb;box-shadow:0 0 80px rgba(224,64,251,.45),0 40px 100px rgba(0,0,0,.8)}
.ev-lbw .ev-t{font-size:106px;color:#e040fb;text-shadow:0 0 50px rgba(224,64,251,.7);letter-spacing:8px}
.ev-lbw .ev-s{font-size:22px;color:var(--white)}

.ev-caught .ev-card{background:rgba(20,8,0,.85);border:2px solid var(--orange);box-shadow:0 0 80px rgba(255,124,0,.45),0 40px 100px rgba(0,0,0,.8)}
.ev-caught .ev-t{font-size:92px;color:var(--orange);text-shadow:0 0 50px rgba(255,124,0,.7);letter-spacing:3px}
.ev-caught .ev-s{font-size:22px;color:var(--white)}

.ev-runout .ev-card{background:rgba(0,16,14,.85);border:2px solid var(--cyan);box-shadow:0 0 80px rgba(0,212,200,.45),0 40px 100px rgba(0,0,0,.8)}
.ev-runout .ev-t{font-size:82px;color:var(--cyan);text-shadow:0 0 50px rgba(0,212,200,.7);letter-spacing:4px}
.ev-runout .ev-s{font-size:22px;color:var(--white)}

.ev-stumped .ev-card{background:rgba(8,12,22,.85);border:2px solid var(--blue2);box-shadow:0 0 80px rgba(122,170,255,.4),0 40px 100px rgba(0,0,0,.8)}
.ev-stumped .ev-t{font-size:82px;color:var(--blue2);text-shadow:0 0 50px rgba(122,170,255,.7)}
.ev-stumped .ev-s{font-size:22px;color:var(--white)}

.ev-review .ev-card{background:rgba(16,14,0,.85);border:2px solid #f5e542;box-shadow:0 0 80px rgba(245,229,66,.4),0 40px 100px rgba(0,0,0,.8)}
.ev-review .ev-t{font-size:68px;color:#f5e542;text-shadow:0 0 45px rgba(245,229,66,.7);letter-spacing:4px}
.ev-review .ev-s{font-size:20px;color:var(--white)}

.ev-noball .ev-card{background:rgba(0,16,14,.85);border:2px solid var(--cyan);box-shadow:0 0 80px rgba(0,212,200,.45),0 40px 100px rgba(0,0,0,.8)}
.ev-noball .ev-t{font-size:96px;color:var(--cyan);text-shadow:0 0 50px rgba(0,212,200,.7);letter-spacing:5px}
.ev-noball .ev-s{font-size:22px;color:var(--white)}

.ev-freehit .ev-card{background:rgba(8,0,20,.85);border:2px solid #a06cff;box-shadow:0 0 80px rgba(160,108,255,.5),0 40px 100px rgba(0,0,0,.8)}
.ev-freehit .ev-t{font-size:72px;color:#c8a0ff;text-shadow:0 0 50px rgba(160,108,255,.8);letter-spacing:3px}
.ev-freehit .ev-s{font-size:22px;color:var(--white)}

.ev-milestone .ev-card{background:rgba(20,14,0,.85);border:2px solid var(--gold);box-shadow:0 0 80px rgba(246,188,26,.5),0 40px 100px rgba(0,0,0,.8)}
.ev-milestone .ev-t{font-size:96px;color:var(--gold);text-shadow:0 0 60px rgba(246,188,26,.9)}
.ev-milestone .ev-s{font-size:26px;color:var(--gold2)}
.ev-milestone .ev-d{font-size:18px;color:rgba(255,255,255,.7)}

.ev-over .ev-card{background:rgba(8,11,22,.85);border:2px solid rgba(255,255,255,.12);box-shadow:0 0 50px rgba(58,124,255,.3),0 40px 80px rgba(0,0,0,.8)}
.ev-over .ev-t{font-size:50px;color:var(--white);letter-spacing:4px}
.ev-over .ev-s{font-size:20px;color:var(--muted)}
.ev-over .ev-d{font-size:26px;color:var(--gold);margin-top:10px}

/* Particles */
#particles{position:fixed;inset:0;z-index:290;pointer-events:none;overflow:hidden}
.pt{position:absolute;opacity:0}
.pt.go{animation:ptfall var(--dur,1.6s) ease-out forwards}
@keyframes ptfall{0%{opacity:1;transform:translate(0,0) scale(1)}100%{opacity:0;transform:translate(var(--tx),var(--ty)) scale(0)}}

/* Score flash */
@keyframes scoreFlash{0%{color:var(--gold)}30%{color:#fff;text-shadow:0 0 30px rgba(246,188,26,.9),0 0 60px rgba(246,188,26,.5);transform:scale(1.08)}100%{color:var(--gold);transform:scale(1)}}
.tc-score.score-flash{animation:scoreFlash .6s ease forwards}

/* Stale badge */
.stale-badge{
  display:none;position:fixed;top:74px;right:14px;z-index:80;
  background:rgba(255,124,0,.85);backdrop-filter:blur(8px);color:#fff;
  font-family:var(--F);font-size:11px;font-weight:700;letter-spacing:1.5px;
  padding:4px 10px;border-radius:4px;text-transform:uppercase;
  animation:blink 2s ease infinite
}
.stale-badge.show{display:block}

/* Just Joined card */
.just-joined{
  position:fixed;bottom:92px;left:50%;transform:translateX(-50%);
  z-index:160;pointer-events:none;
  background:rgba(10,14,30,.92);backdrop-filter:blur(20px);
  border:1px solid rgba(255,255,255,.1);border-radius:14px;
  padding:16px 28px;min-width:700px;max-width:960px;
  display:none;align-items:center;gap:24px;
  box-shadow:0 20px 60px rgba(0,0,0,.8)
}
.just-joined.show{display:flex;animation:jjIn .35s cubic-bezier(.22,1,.36,1) forwards}
.just-joined::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--gold),var(--blue),var(--cyan));border-radius:14px 14px 0 0}
@keyframes jjIn{from{opacity:0;transform:translateX(-50%) translateY(20px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}
.jj-tag{font-family:var(--F);font-size:12px;font-weight:700;letter-spacing:2.5px;color:var(--gold);text-transform:uppercase;white-space:nowrap;background:rgba(246,188,26,.09);border:1px solid rgba(246,188,26,.25);padding:4px 9px;border-radius:4px}
.jj-section{display:flex;flex-direction:column;gap:2px}
.jj-lbl{font-size:11px;font-weight:700;color:var(--muted);letter-spacing:2px;text-transform:uppercase}
.jj-val{font-family:var(--FD);font-size:19px;font-weight:700;color:var(--white);line-height:1}
.jj-sep{width:1px;height:38px;background:rgba(255,255,255,.07);flex-shrink:0}

/* Super over badge */
#super-over-badge{display:none;align-items:center;gap:8px;padding:0 16px;border-right:1px solid rgba(255,255,255,.06);background:rgba(246,188,26,.08);flex-shrink:0}
</style>
</head>
<body>
<div class="bg-mesh"></div><div class="bg-grid"></div><div class="bg-vignette"></div><div class="bg-scan"></div>
<div class="ch-watermark"><div class="cw-name">XSTAR SPORTS</div></div>
<div id="particles"></div>

<!-- Special screens -->
<div id="standby">
  <div class="sb-logo"><span class="x">X</span>STAR SPORTS</div>
  <div class="sb-msg">Waiting for match to begin…</div>
  <div class="sb-prog"><div class="sb-fill"></div></div>
</div>
<div id="skeleton">
  <div class="sk-logo"><span class="x">X</span>STAR SPORTS</div>
  <div class="sk-msg">Connecting to live data…</div>
  <div class="sk-blocks">
    <div class="sk-block w80"></div><div class="sk-block w60"></div>
    <div class="sk-block w80"></div><div class="sk-block w40"></div>
  </div>
</div>
<div id="countdown">
  <div class="cd-eyebrow">XSTAR SPORTS · Match Starting Soon</div>
  <div class="cd-match" id="cd-match">—</div>
  <div class="cd-lbl">First Ball In</div>
  <div class="cd-clock">SOON</div>
  <div style="font-size:13px;color:var(--white)" id="cd-toss"></div>
</div>
<div id="break-screen">
  <div class="bs-eyebrow">XSTAR SPORTS · Cricket Live</div>
  <div class="bs-title">INNINGS <span class="x">BREAK</span></div>
  <div class="bs-line"></div>
  <div style="font-family:var(--F);font-size:22px;color:var(--white);letter-spacing:2px" id="bs-match">—</div>
  <div class="bs-score" id="bs-score">—</div>
  <div class="bs-status" id="bs-status">—</div>
</div>
<div id="interrupt-screen">
  <div class="is-icon" id="is-icon">🌧️</div>
  <div class="is-type" id="is-type">RAIN STOPPED PLAY</div>
  <div class="is-score" id="is-score">—</div>
  <div class="is-status" id="is-status">Players are off the field</div>
  <div class="is-resume">Stream continues — updates when play resumes</div>
</div>
<div id="complete-screen">
  <div class="mc-ch">XSTAR SPORTS</div>
  <div class="mc-title">MATCH RESULT</div>
  <div class="mc-score" id="mc-score">—</div>
  <div class="mc-result" id="mc-result">—</div>
</div>
<div class="dls-overlay" id="dls-overlay">
  <div class="dls-card">
    <div class="dls-eyebrow">🏏 Duckworth-Lewis-Stern Method</div>
    <div class="dls-title">TARGET REVISED</div>
    <div class="dls-target" id="dls-target-val">—</div>
    <div class="dls-sub" id="dls-target-sub">—</div>
  </div>
</div>

<!-- Event overlays -->
<div class="ev ev-wicket"  id="ev-wicket"><div class="ev-card"><div class="ev-t">OUT!</div><div class="ev-s" id="ev-wt">WICKET</div><div class="ev-d" id="ev-wd"></div></div></div>
<div class="ev ev-four"    id="ev-four"><div class="ev-card"><div class="ev-t">4</div><div class="ev-s">BOUNDARY</div></div></div>
<div class="ev ev-six"     id="ev-six"><div class="ev-card"><div class="ev-t">6</div><div class="ev-s">MAXIMUM!</div></div></div>
<div class="ev ev-lbw"     id="ev-lbw"><div class="ev-card"><div class="ev-t">LBW</div><div class="ev-s">Leg Before Wicket</div></div></div>
<div class="ev ev-caught"  id="ev-caught"><div class="ev-card"><div class="ev-t">CAUGHT!</div><div class="ev-s" id="ev-cd">—</div></div></div>
<div class="ev ev-runout"  id="ev-runout"><div class="ev-card"><div class="ev-t">RUN OUT!</div><div class="ev-s">Direct Hit</div></div></div>
<div class="ev ev-stumped" id="ev-stumped"><div class="ev-card"><div class="ev-t">STUMPED!</div><div class="ev-s">Behind the Stumps</div></div></div>
<div class="ev ev-review"  id="ev-review"><div class="ev-card"><div class="ev-t">⚖ REVIEW</div><div class="ev-s">DRS Check</div><div class="ev-d" id="ev-rd">Checking with technology…</div></div></div>
<div class="ev ev-noball"  id="ev-noball"><div class="ev-card"><div class="ev-t">NO BALL</div><div class="ev-s">Free Hit Next Ball!</div></div></div>
<div class="ev ev-freehit" id="ev-freehit"><div class="ev-card"><div class="ev-t">⚡ FREE HIT</div><div class="ev-s">Batter Cannot Be Out!</div></div></div>
<div class="ev ev-milestone" id="ev-ms"><div class="ev-card"><div class="ev-t" id="ev-msn">50</div><div class="ev-s" id="ev-mss">HALF CENTURY</div><div class="ev-d" id="ev-msd"></div></div></div>
<div class="ev ev-over"    id="ev-over"><div class="ev-card"><div class="ev-t">END OF OVER</div><div class="ev-s" id="ev-ovn">—</div><div class="ev-d" id="ev-ovr">— runs</div></div></div>

<div class="stale-badge" id="stale-badge">⚠ Data Delayed</div>
<div class="just-joined" id="just-joined">
  <div class="jj-tag">Just Joined?</div>
  <div class="jj-sep"></div>
  <div class="jj-section"><div class="jj-lbl">Match</div><div class="jj-val" id="jj-match">—</div></div>
  <div class="jj-sep"></div>
  <div class="jj-section"><div class="jj-lbl">Score</div><div class="jj-val" id="jj-score" style="color:var(--gold)">—</div></div>
  <div class="jj-sep"></div>
  <div class="jj-section"><div class="jj-lbl">Top Scorer</div><div class="jj-val" id="jj-bat" style="color:var(--cyan)">—</div></div>
  <div class="jj-sep"></div>
  <div class="jj-section"><div class="jj-lbl">Best Bowler</div><div class="jj-val" id="jj-bowl" style="color:var(--red2)">—</div></div>
  <div class="jj-sep"></div>
  <div class="jj-section"><div class="jj-lbl">Situation</div><div class="jj-val" id="jj-status" style="font-size:14px;color:var(--white)">—</div></div>
</div>

<!-- Main layout -->
<div id="wrap">
  <header id="topbar">
    <div class="ch-brand">
      <div class="ch-icon">XS</div>
      <div>
        <div class="ch-name"><span class="x">X</span>STAR SPORTS</div>
        <div class="ch-tagline">Cricket · Live</div>
      </div>
    </div>
    <div class="live-pill"><div class="live-dot"></div>LIVE</div>
    <div class="topbar-center">
      <span class="t-series" id="h-series">—</span>
      <span class="t-dot">·</span>
      <span class="t-match" id="h-desc">—</span>
      <span class="t-dot">·</span>
      <span class="t-format" id="h-format">ODI</span>
      <span class="t-dot">·</span>
      <span class="t-venue">📍 <span id="h-venue">—</span></span>
    </div>
    <div class="topbar-right">
      <div class="tb-clock" id="clock">00:00:00</div>
    </div>
  </header>

  <div id="main">
    <!-- LEFT -->
    <div id="left">
      <div class="l-label" id="l-label">Cricket · Live</div>

      <div class="mps-strip" id="match-phase-strip">
        <span class="mps-inn" id="mps-innings">—</span>
        <span class="mps-ov" id="mps-overs">—</span>
      </div>

      <div class="team-card" id="tc1">
        <div class="tc-row">
          <div class="tc-flag" id="tc1-flag">🏏</div>
          <div class="tc-name" id="tc1-name">—</div>
          <div>
            <div class="tc-score" id="tc1-score">—</div>
            <div class="tc-overs" id="tc1-ov"></div>
          </div>
        </div>
      </div>

      <div class="team-card" id="tc2">
        <div class="tc-row">
          <div class="tc-flag" id="tc2-flag">🏏</div>
          <div class="tc-name" id="tc2-name">—</div>
          <div>
            <div class="tc-score" id="tc2-score">—</div>
            <div class="tc-overs" id="tc2-ov"></div>
          </div>
        </div>
      </div>

      <div class="target-banner" id="target-banner">
        <div class="tb-lbl">Target</div>
        <div class="tb-val" id="target-val">—</div>
        <div class="tb-sub" id="target-sub">—</div>
      </div>

      <div class="status-badge live" id="state-badge">
        <div class="live-dot"></div><span id="state-txt">Live</span>
      </div>

      <div style="display:flex;align-items:center;justify-content:space-between;gap:8px">
        <div class="stats2" style="flex:1">
          <div class="sbox"><div class="sbox-l">CRR</div><div class="sbox-v g" id="s-crr">—</div></div>
          <div class="sbox"><div class="sbox-l">RRR</div><div class="sbox-v r" id="s-rrr">—</div></div>
          <div class="sbox"><div class="sbox-l">Overs</div><div class="sbox-v" id="s-ov">—</div></div>
          <div class="sbox"><div class="sbox-l">Last Over</div><div class="sbox-v y" id="s-lov">—</div></div>
        </div>
        <div class="phase-pill" id="phase-pill"></div>
      </div>

      <div class="wp-section">
        <div class="wp-lbl">Win Probability</div>
        <div class="wp-bar">
          <div class="wp-t1" id="wp1" style="width:50%">50%</div>
          <div class="wp-t2" id="wp2">50%</div>
        </div>
        <div class="wp-lbls"><span id="wp1l">—</span><span id="wp2l">—</span></div>
        <div class="wp-tied-label" id="wp-tied">MATCH TIED</div>
      </div>

      <div class="pship-live" id="pship-live">
        <div><div class="pl-lbl">Partnership</div><div style="font-size:11px;color:var(--white);margin-top:1px" id="pship-names">—</div></div>
        <div class="pl-val" id="pship-val">—</div>
      </div>

      <div class="toss-strip"><b>🪙 Toss:</b> <span id="toss-txt">—</span></div>
    </div>

    <!-- CENTER -->
    <div id="center">
      <div class="panel-bar">
        <div id="super-over-badge">
          <span style="font-size:17px">⚡</span>
          <span style="font-family:var(--F);font-size:13px;font-weight:700;color:var(--gold);letter-spacing:2px">SUPER OVER</span>
        </div>
        <div class="panel-progress" id="panel-progress"></div>
        <div class="pp on" id="pp-batting"><div class="pp-num">1</div>Batting</div>
        <div class="pp"    id="pp-bowling"><div class="pp-num">2</div>Bowling</div>
        <div class="pp"    id="pp-partnerships"><div class="pp-num">3</div>Partnerships</div>
        <div class="pp"    id="pp-fow"><div class="pp-num">4</div>Fall of Wickets</div>
        <div class="panel-next" id="panel-next">NEXT <span id="panel-next-lbl">Bowling</span></div>
      </div>

      <div class="pane on" id="pane-batting">
        <div class="sc-inn-selector" id="inn-selector" style="display:none">
          <div class="sc-inn-btn active" id="inn-btn-1" onclick="selectInnings(1)">1st Innings</div>
          <div style="width:8px"></div>
          <div class="sc-inn-btn" id="inn-btn-2" onclick="selectInnings(2)">2nd Innings</div>
        </div>
        <div class="sc-hdr bat"><div>BATTER</div><div style="text-align:center">R</div><div style="text-align:center">B</div><div style="text-align:center">4s</div><div style="text-align:center">6s</div><div style="text-align:center">SR</div></div>
        <div class="scrollable" id="bat-rows"></div>
      </div>
      <div class="pane" id="pane-bowling">
        <div class="sc-hdr bowl"><div>BOWLER</div><div style="text-align:center">O</div><div style="text-align:center">R</div><div style="text-align:center">W</div><div style="text-align:center">ECO</div><div style="text-align:center">M</div></div>
        <div class="scrollable" id="bowl-rows"></div>
      </div>
      <div class="pane" id="pane-partnerships">
        <div class="sc-hdr" style="grid-template-columns:1fr"><div>PARTNERSHIPS</div></div>
        <div class="scrollable" id="pship-rows"></div>
      </div>
      <div class="pane" id="pane-fow">
        <div class="sc-hdr" style="grid-template-columns:1fr"><div>FALL OF WICKETS</div></div>
        <div class="scrollable fow-wrap" id="fow-rows"></div>
      </div>

      <div class="comm-zone">
        <div class="comm-hdr">
          <div class="comm-hdr-left">
            <div class="comm-ch-icon">XS</div>
            <div class="comm-title">Live Commentary</div>
          </div>
          <div class="innings-pill first" id="innings-pill">
            <div class="innings-pip"></div>
            <span id="innings-pill-txt">1st Innings</span>
          </div>
        </div>
        <div class="comm-list" id="comm-list"></div>
      </div>
    </div>

    <!-- RIGHT -->
    <div id="right">
      <div class="r-title">🔴 Live · This Over</div>
      <div class="bat-card striker">
        <div class="bc-lbl">On Strike ★</div>
        <div class="bc-name" id="b1n">—</div>
        <div class="bc-stats">
          <div class="bs"><div class="bs-v main" id="b1r">—</div><div class="bs-l">R</div></div>
          <div class="bs"><div class="bs-v"       id="b1b">—</div><div class="bs-l">B</div></div>
          <div class="bs"><div class="bs-v g"     id="b1sr">—</div><div class="bs-l">SR</div></div>
          <div class="bs"><div class="bs-v y"     id="b1f">—</div><div class="bs-l">4s</div></div>
          <div class="bs"><div class="bs-v b"     id="b1s">—</div><div class="bs-l">6s</div></div>
        </div>
      </div>
      <div class="bat-card ns">
        <div class="bc-lbl">Non-Striker</div>
        <div class="bc-name" id="b2n">—</div>
        <div class="bc-stats">
          <div class="bs"><div class="bs-v main" id="b2r">—</div><div class="bs-l">R</div></div>
          <div class="bs"><div class="bs-v"       id="b2b">—</div><div class="bs-l">B</div></div>
          <div class="bs"><div class="bs-v g"     id="b2sr">—</div><div class="bs-l">SR</div></div>
        </div>
      </div>
      <div class="bowl-card">
        <div class="bc-lbl" style="color:var(--red2)">Current Bowler</div>
        <div class="bc-name" id="bown">—</div>
        <div class="bc-stats">
          <div class="bs"><div class="bs-v" style="color:var(--red2)" id="boww">—</div><div class="bs-l">W</div></div>
          <div class="bs"><div class="bs-v" id="bowr">—</div><div class="bs-l">R</div></div>
          <div class="bs"><div class="bs-v" id="bowo">—</div><div class="bs-l">OV</div></div>
          <div class="bs"><div class="bs-v g" id="bowe">—</div><div class="bs-l">ECO</div></div>
        </div>
      </div>
      <div class="fh-ring" id="fh-ring">⚡ FREE HIT</div>
      <div>
        <div class="balls-lbl">This Over</div>
        <div class="balls-track" id="balls-track"></div>
      </div>
      <div class="lw-box">
        <div class="lw-lbl">Last Wicket</div>
        <div class="lw-txt" id="lw-txt">—</div>
      </div>
    </div>
  </div>

  <footer id="ticker">
    <div class="tk-ch"><div class="tk-ch-name">XSTAR</div></div>
    <div class="tk-live">LIVE</div>
    <div class="tk-sw"><div class="tk-sc" id="tk-sc">Xstar Sports Live</div></div>
    <div class="tk-time" id="tk-time">00:00</div>
  </footer>
</div>

<script>
// ════════════════════════════════════════════════════
//  XSTAR SPORTS — MAIN OVERLAY v5
//  FIX: iPage/isSuperOver defined before use (was causing empty UI)
//  FIX: All data fields render correctly
//  1920×1080 · Glassmorphism UI
// ════════════════════════════════════════════════════
const DATA_URL = './stream_data_main.json';
const POLL_MS  = 4500;
const TAB_MS   = 15000;
const TABS     = ['batting','bowling','partnerships','fow'];
const TAB_LBLS = ['Batting','Bowling','Partnerships','Fall of Wickets'];

let tabIdx = 0, tabTimer = null;
let lastCommSig = '', prevBat1Runs = 0, prevFH = false, lastOverNum = '';
let dataLoaded = false;
let selectedInnings = 0;

const $ = id => document.getElementById(id);
const T = (id,v) => { const e=$(id); if(e) e.textContent=(v===null||v===undefined||v==='')?'—':String(v); };

// Flags
const FLAGS={india:'🇮🇳',ind:'🇮🇳',pak:'🇵🇰',pakistan:'🇵🇰',ban:'🇧🇩',bangladesh:'🇧🇩',
  aus:'🇦🇺',australia:'🇦🇺',eng:'🏴󠁧󠁢󠁥󠁮󠁧󠁿',england:'🏴󠁧󠁢󠁥󠁮󠁧󠁿','new zealand':'🇳🇿',nz:'🇳🇿',
  'south africa':'🇿🇦',sa:'🇿🇦','west indies':'🏝️',wi:'🏝️','sri lanka':'🇱🇰',sl:'🇱🇰',
  afghanistan:'🇦🇫',afg:'🇦🇫',zimbabwe:'🇿🇼',zim:'🇿🇼',ireland:'🇮🇪',ire:'🇮🇪',
  lahore:'🦁',karachi:'🐊',mumbai:'🔵',chennai:'🦁',kolkata:'💜',delhi:'🔵',
  hyderabad:'🟠',punjab:'🔴',rajasthan:'🩷',bangalore:'🔴'};
function flag(n=''){const k=(n||'').toLowerCase();for(const[a,f]of Object.entries(FLAGS))if(k.includes(a))return f;return'🏏';}

// Interruption config
const INTERRUPTIONS={
  rain:{icon:'🌧️',label:'RAIN STOPPED PLAY',color:'#4895ef'},
  bad_light:{icon:'🌑',label:'BAD LIGHT',color:'#505878'},
  lunch:{icon:'🍽️',label:'LUNCH BREAK',color:'#f6bc1a'},
  tea:{icon:'☕',label:'TEA BREAK',color:'#f6bc1a'},
  drinks:{icon:'💧',label:'DRINKS BREAK',color:'#00d4c8'},
  injury:{icon:'🏥',label:'INJURY — PLAY PAUSED',color:'#ff4d5e'},
  abandoned:{icon:'❌',label:'MATCH ABANDONED',color:'#ff4d5e'},
  cancelled:{icon:'❌',label:'MATCH CANCELLED',color:'#ff4d5e'},
  delayed:{icon:'⏰',label:'MATCH DELAYED',color:'#f6bc1a'},
  dls:{icon:'📊',label:'DLS METHOD APPLIED',color:'#00d4c8'},
  suspended:{icon:'⏸️',label:'PLAY SUSPENDED',color:'#ff7c00'},
};

// Clock
function tick(){const t=new Date().toLocaleTimeString('en-GB',{hour12:false});T('clock',t);T('tk-time',t.slice(0,5));}
setInterval(tick,1000);tick();

// Panel rotation
function switchPanel(name){
  tabIdx=TABS.indexOf(name);if(tabIdx<0)tabIdx=0;
  TABS.forEach((t,i)=>{const p=$('pp-'+t);if(p)p.classList.toggle('on',i===tabIdx);});
  document.querySelectorAll('.pane').forEach(p=>p.classList.remove('on'));
  const pane=$('pane-'+name);if(pane)pane.classList.add('on');
  const nextIdx=(tabIdx+1)%TABS.length;
  T('panel-next-lbl',TAB_LBLS[nextIdx]);
  const bar=$('panel-progress');
  if(bar){bar.classList.remove('go');bar.style.width='0%';bar.style.setProperty('--dur',TAB_MS+'ms');
    setTimeout(()=>{bar.classList.add('go');bar.style.width='100%';},40);}
}
function startPanels(){clearInterval(tabTimer);switchPanel(TABS[tabIdx]);tabTimer=setInterval(()=>{tabIdx=(tabIdx+1)%TABS.length;switchPanel(TABS[tabIdx]);},TAB_MS);}
startPanels();

// Ball parser
function parseBalls(s){if(!s)return[];return(s+'').trim().split(/\s+/).map(b=>{
  if(b==='W'||b.toUpperCase()==='W')return{l:'W',c:'wkt'};
  if(b==='4')return{l:'4',c:'four'};if(b==='6')return{l:'6',c:'six'};
  if(b==='0'||b==='.')return{l:'•',c:'dot'};
  if(/^wd$/i.test(b))return{l:'Wd',c:'wd'};if(/^nb$/i.test(b))return{l:'NB',c:'nb'};
  if(/^fh$/i.test(b))return{l:'FH',c:'fh'};return{l:b,c:'run'};});}

// Events
function fireEv(id,dur=3600){const e=$(id);if(!e)return;e.classList.remove('show');void e.offsetWidth;e.classList.add('show');setTimeout(()=>e.classList.remove('show'),dur+200);}
function spark(type){
  const c={wicket:['#e8192c','#ff4d5e'],four:['#f6bc1a','#ffe680'],six:['#3a7cff','#7aaaff','#00d4c8'],
    lbw:['#e040fb'],caught:['#ff7c00'],runout:['#00d4c8'],noball:['#00d4c8'],
    review:['#f5e542'],freehit:['#a06cff','#c8a0ff'],milestone:['#f6bc1a','#ffe680','#fff','#fff']}[type]||['#fff'];
  const w=$('particles'),n=type==='milestone'?35:18;
  for(let i=0;i<n;i++){const p=document.createElement('div');p.className='pt';
    const sz=4+Math.random()*9;
    p.style.cssText=`left:${10+Math.random()*80}%;top:${10+Math.random()*80}%;width:${sz}px;height:${sz}px;background:${c[Math.floor(Math.random()*c.length)]};border-radius:${Math.random()>.5?'50%':'3px'};--tx:${(Math.random()-.5)*400}px;--ty:${(Math.random()-.5)*400}px;--dur:${1.2+Math.random()*.8}s;animation-delay:${Math.random()*.3}s`;
    p.classList.add('go');w.appendChild(p);setTimeout(()=>p.remove(),2500);}
}

function detectEvents(d,comm){
  if(!comm?.length)return;
  const c=comm[0],sig=`${c.over}|${c.text}`;
  if(sig===lastCommSig)return;lastCommSig=sig;
  const txt=(c.text||'').toLowerCase(),ev=(c.event||'').toUpperCase();
  if(ev==='SIX'||txt.includes(' six')||txt.includes('maximum')){fireEv('ev-six');spark('six');return;}
  if(ev==='FOUR'||(txt.includes('boundary')||(txt.includes('four')&&!txt.includes('forty')))){fireEv('ev-four');spark('four');return;}
  if(ev==='WICKET'||ev.includes('OUT')||txt.includes(' out ')||txt.includes('takes the wicket')){
    let id='ev-wicket';
    if(txt.includes('lbw')){id='ev-lbw';spark('lbw');}
    else if(txt.includes('caught')||txt.includes(' c ')){id='ev-caught';T('ev-cd',(c.text||'').slice(0,80));spark('caught');}
    else if(txt.includes('run out')){id='ev-runout';spark('runout');}
    else if(txt.includes('stumped')){id='ev-stumped';spark('runout');}
    else{T('ev-wt',txt.includes('bowled')?'BOWLED':txt.includes('lbw')?'LBW':'WICKET');T('ev-wd',(c.text||'').slice(0,80));spark('wicket');}
    fireEv(id);return;
  }
  if(txt.includes('no ball')||ev==='NOBALL'){fireEv('ev-noball');spark('noball');return;}
  if(txt.includes('review')||txt.includes('drs')||ev==='REVIEW'){T('ev-rd',(c.text||'').slice(0,60));fireEv('ev-review');spark('review');return;}
  if(d.is_free_hit&&!prevFH){fireEv('ev-freehit');spark('freehit');}
  prevFH=!!d.is_free_hit;
}

function detectMilestones(bats){
  if(!bats?.length)return;
  const r1=parseInt(bats[0]?.runs||0);
  if(prevBat1Runs<50&&r1>=50&&r1<60){T('ev-msn','50');T('ev-mss','HALF CENTURY 🏏');T('ev-msd',bats[0].batName||'');fireEv('ev-ms',4500);spark('milestone');}
  if(prevBat1Runs<100&&r1>=100&&r1<110){T('ev-msn','100');T('ev-mss','CENTURY! 🎉');T('ev-msd',bats[0].batName||'');fireEv('ev-ms',5000);spark('milestone');}
  prevBat1Runs=r1;
}

function detectOverComplete(d){
  const ov=d.live_overs||d.overs||'';if(!ov)return;
  const decimal=parseFloat(ov),fraction=Math.round((decimal%1)*10),overNum=Math.floor(decimal);
  if(fraction===0&&String(overNum)!==lastOverNum&&overNum>0){
    lastOverNum=String(overNum);T('ev-ovn',`Over ${overNum}`);
    const bl=parseBalls(d.last_ball||'');
    const r=bl.reduce((a,b)=>{const v=parseInt(b.l);return a+(isNaN(v)?0:v);},0);
    T('ev-ovr',`${r} run${r!==1?'s':''} this over`);fireEv('ev-over',3200);
  }
}

function fmtExtras(ex){
  if(!ex)return'0';
  const p=[ex.wides&&ex.wides+'w',ex.noBalls&&ex.noBalls+'nb',ex.byes&&ex.byes+'b',ex.legByes&&ex.legByes+'lb'].filter(Boolean);
  return p.length?p.join(', '):'0';
}

function selectInnings(num){
  selectedInnings=num;
  [$('inn-btn-1'),$('inn-btn-2')].forEach((b,i)=>{if(b)b.classList.toggle('active',i+1===num);});
  if(window._lastData)renderScorecard(window._lastData);
}

function renderScorecard(d){
  const sc=(d.scorecard?.innings)||[];
  if(!sc.length)return;
  const sel=$('inn-selector');
  if(sel)sel.style.display=sc.length>=2?'flex':'none';
  const idx=selectedInnings>0?selectedInnings-1:sc.length-1;
  const inn=sc[Math.min(idx,sc.length-1)];
  if(!inn)return;

  // FIX: Compute iPage and isSuperOver BEFORE any usage
  const iPage=d.innings_page||d.innings_num||1;
  const isSuperOver=(iPage>=3)||((d.status||'').toLowerCase().includes('super over'));

  if(inn.batsmen?.length){
    $('bat-rows').innerHTML=inn.batsmen.map(b=>{
      const no=!b.is_out&&(!b.out_desc||b.out_desc==='batting');
      return`<div class="sc-row bat"><div><div class="sc-n ${no?'no':''}">${b.name}</div><div class="sc-nd">${b.out_desc||'batting'}</div></div><div class="sc-v big ${no?'y':''}">${b.runs}</div><div class="sc-v">${b.balls}</div><div class="sc-v y">${b.fours}</div><div class="sc-v" style="color:var(--blue2)">${b.sixes}</div><div class="sc-v g">${b.strike_rate}</div></div>`;
    }).join('')+`<div class="sc-row extras"><div class="sc-n" style="color:var(--muted);font-size:10px">Extras: ${fmtExtras(inn.extras)}</div><div class="sc-v big y">${inn.runs}/${inn.wickets} (${inn.overs})</div></div>`;
  }
  if(inn.bowlers?.length){
    $('bowl-rows').innerHTML=inn.bowlers.map(b=>
      `<div class="sc-row bowl"><div><div class="sc-n">${b.name}</div></div><div class="sc-v">${b.overs}</div><div class="sc-v">${b.runs}</div><div class="sc-v W">${b.wickets}</div><div class="sc-v g">${b.economy}</div><div class="sc-v">${b.maidens||0}</div></div>`
    ).join('')+`<div style="display:grid;grid-template-columns:1fr repeat(5,58px);padding:12px 18px;background:rgba(0,212,200,.07);border-top:2px solid var(--cyan)"><div style="font-family:var(--F);font-size:13px;font-weight:700;color:var(--cyan);letter-spacing:1.5px">TOTAL: ${inn.runs}/${inn.wickets}</div><div style="font-family:var(--FD);font-size:15px;color:var(--muted);text-align:center">${inn.overs}</div><div style="font-family:var(--FD);font-size:15px;color:var(--white);text-align:center">${inn.runs}</div><div style="font-family:var(--FD);font-size:15px;color:var(--red2);text-align:center">${inn.wickets}</div><div style="font-family:var(--FD);font-size:15px;color:var(--cyan);text-align:center">${inn.run_rate||'—'}</div><div></div></div>`;
  }
  if(inn.partnerships?.length){
    const mx=Math.max(...inn.partnerships.map(p=>+(p.runs||0)),1);
    $('pship-rows').innerHTML=inn.partnerships.map(p=>
      `<div class="pr-row"><div class="pr-names">${p.bat1} &amp; ${p.bat2}</div><div class="pr-bg"><div class="pr-bar" style="width:${Math.round(+(p.runs||0)/mx*100)}%"></div></div><div class="pr-stat">${p.runs} <span style="font-size:10px;color:var(--muted)">(${p.balls}b)</span></div></div>`
    ).join('');
  }
  if(inn.fall_of_wickets?.length){
    $('fow-rows').innerHTML=inn.fall_of_wickets.map((w,i)=>
      `<div class="fow-chip"><div class="fow-wkt">${i+1}-${w.runs}</div><div class="fow-bat">${w.batter}</div><div class="fow-ov">${w.overs} ov</div></div>`
    ).join('');
  }
}

// DLS announcement
let lastDlsTarget='';
function checkDLS(d){
  const dlsTgt=d.live_dls_target||d.dls_target||'';
  const announced=d.dls_announcement===true;
  if(dlsTgt&&dlsTgt!==lastDlsTarget&&announced){
    lastDlsTarget=dlsTgt;T('dls-target-val',dlsTgt);T('dls-target-sub',`Target revised by DLS — ${d.status||''}`);
    const el=$('dls-overlay');if(el){el.classList.remove('show');void el.offsetWidth;el.classList.add('show');setTimeout(()=>el.classList.remove('show'),5500);}
  }
}

// Just Joined
let jjTimer=null;
function showJustJoined(d){
  const sc=(d.scorecard?.innings)||[];const inn=sc[sc.length-1];
  T('jj-match',d.title||`${d.team1} vs ${d.team2}`);T('jj-score',d.live_score||d.score||'—');
  const batters=[...(inn?.batsmen||[])].sort((a,b)=>(b.runs||0)-(a.runs||0));const topBat=batters[0];
  T('jj-bat',topBat?`${topBat.name} ${topBat.runs}*(${topBat.balls}b)`:'—');
  const bowlers=[...(inn?.bowlers||[])].sort((a,b)=>(b.wickets||0)-(a.wickets||0));const topBowl=bowlers[0];
  T('jj-bowl',topBowl?`${topBowl.name} ${topBowl.wickets}/${topBowl.runs}`:'—');
  T('jj-status',d.status||d.state||'—');
  const jj=$('just-joined');jj.classList.add('show');setTimeout(()=>jj.classList.remove('show'),8000);
}
function startJustJoined(d){if(jjTimer)clearInterval(jjTimer);jjTimer=setInterval(()=>showJustJoined(d),300000);}

// Stale detection
function checkStale(d){
  if(d.last_updated){const age=(Date.now()-new Date(d.last_updated).getTime())/1000;$('stale-badge').classList.toggle('show',age>90);}
}

// ── MAIN RENDER ────────────────────────────────────────────────────────
function render(d){
  if(!d)return;
  window._lastData=d;

  const state=(d.state||'').toLowerCase();
  const status=(d.status||'').toLowerCase();
  const interruption=d.interruption||'';

  // FIX: Compute iPage and isSuperOver FIRST — used throughout render
  const iPage=d.innings_page||d.innings_num||1;
  const isSuperOver=(iPage>=3)||((d.status||'').toLowerCase().includes('super over'));

  const isWaiting   = state==='waiting'||!d.team1;
  const isPreview   = (state==='preview'||state.includes('preview'))&&!interruption;
  const isBreak     = state.includes('break')||status.includes('innings break');
  const isComplete  = (d.stream_complete===true||state.includes('complete')||state.includes('result'))&&!isSuperOver;
  const isInterrupt = !!interruption&&!isBreak&&!isComplete;

  // Skeleton
  const hasSomeData=d.team1||d.score||d.status;
  $('skeleton').classList.toggle('show',!dataLoaded&&!hasSomeData);
  if(hasSomeData)dataLoaded=true;

  $('standby').classList.toggle('show',     isWaiting);
  $('countdown').classList.toggle('show',   !isWaiting&&isPreview);
  $('break-screen').classList.toggle('show',!isWaiting&&isBreak&&!isInterrupt);
  $('interrupt-screen').classList.toggle('show',!isWaiting&&isInterrupt);
  $('complete-screen').classList.toggle('show', !isWaiting&&isComplete&&!isBreak);

  if(isPreview){T('cd-match',d.title||`${d.team1} vs ${d.team2}`);T('cd-toss',d.toss||'');}
  if(isBreak){T('bs-match',d.title||`${d.team1} vs ${d.team2}`);T('bs-score',d.live_score||d.score||'—');T('bs-status',d.status||'Innings Break');}
  if(isInterrupt){
    const cfg=INTERRUPTIONS[interruption]||{icon:'⏸️',label:'PLAY PAUSED',color:'#ff7c00'};
    T('is-icon',cfg.icon);T('is-type',cfg.label);
    T('is-score',d.live_score||d.score||'—');
    T('is-status',(d.status||'Play suspended')+(d.resumption?` — Expected: ${d.resumption}`:''));
    const isEl=$('is-type');if(isEl)isEl.style.color=cfg.color||'var(--orange)';
  }
  if(isComplete){
    T('mc-result',d.status||'Match Complete');
    const sc=(d.scorecard?.innings)||[];const li=sc[sc.length-1];
    T('mc-score',li?`${li.runs}/${li.wickets}`:'—');
  }

  // Header
  T('h-series',d.series||'Xstar Sports');
  T('h-desc',d.match_desc||d.title||'');
  T('h-format',d.match_format||'');
  T('h-venue',(d.venue||'').split('•')[0].trim()||'—');
  T('l-label',`${(d.match_format||'Cricket').toUpperCase()} · ${d.series||'Live'}`);

  // Match phase strip — FIX: iPage and isSuperOver defined above
  const innLabels=['','1ST INNINGS','2ND INNINGS','SUPER OVER','SUPER OVER 2'];
  const innLabel=isSuperOver?'⚡ SUPER OVER':(innLabels[iPage]||`INN ${iPage}`);
  T('mps-innings',innLabel);
  const ovsStr=d.live_overs||d.overs||'';
  const fmtUpper=(d.match_format||'').toUpperCase();
  const maxOv=fmtUpper.includes('T20')?20:fmtUpper.includes('T10')?10:fmtUpper.includes('ODI')?50:0;
  T('mps-overs',ovsStr?(maxOv?`${ovsStr} / ${maxOv} OV`:`${ovsStr} OV`):'');

  // Teams
  const sc=(d.scorecard?.innings)||[];
  $('tc1-flag').textContent=flag(d.team1);T('tc1-name',d.team1);
  $('tc2-flag').textContent=flag(d.team2);T('tc2-name',d.team2);
  if(sc[0]){T('tc1-score',`${sc[0].runs}/${sc[0].wickets}`);T('tc1-ov',`(${sc[0].overs} ov)`);}
  else if(d.live_score){T('tc1-score',d.live_score);T('tc1-ov',d.live_overs?`(${d.live_overs} ov)`:'')}
  else{T('tc1-score','—');T('tc1-ov','');}
  if(sc[1]){T('tc2-score',`${sc[1].runs}/${sc[1].wickets}`);T('tc2-ov',`(${sc[1].overs} ov)`);}
  else{T('tc2-score','—');T('tc2-ov','');}
  $('tc1').classList.toggle('batting',sc.length===1);
  $('tc2').classList.toggle('batting',sc.length===2);

  // Target
  const tgt=d.live_target||d.target||'';
  const tb=$('target-banner');
  if(tgt&&sc.length>=2){
    tb.classList.add('show');T('target-val',tgt);
    const remaining=parseInt(tgt)-(sc[1]?.runs||0);
    const balls=Math.round((20-parseFloat(sc[1]?.overs||0))*6);
    T('target-sub',remaining>0?`Need ${remaining} from ~${balls} balls`:'Target reached!');
  }else{tb.classList.remove('show');}

  // State badge
  const badge=$('state-badge');
  badge.className='status-badge '+(isInterrupt?'interrupt':isBreak?'break':isComplete?'complete':'live');
  T('state-txt',d.status||d.state||'Live');

  // Stats
  T('s-crr',d.live_crr||d.run_rate||'—');
  const rrrVal=parseFloat(d.live_rrr||d.req_rate||0),crrVal=parseFloat(d.live_crr||d.run_rate||0);
  T('s-rrr',d.live_rrr||d.req_rate||'—');
  const rrrEl=$('s-rrr');
  if(rrrEl&&rrrVal>0&&crrVal>0){
    if(rrrVal>crrVal+1.5)rrrEl.style.color='var(--red2)';
    else if(rrrVal<crrVal-1.5)rrrEl.style.color='var(--cyan)';
    else rrrEl.style.color='var(--gold)';
  }
  T('s-ov',d.live_overs||d.overs||'—');
  const bl2=parseBalls(d.last_ball||'');
  T('s-lov',bl2.length?String(bl2.reduce((a,b)=>{const v=parseInt(b.l);return a+(isNaN(v)?0:v);},0)):'—');

  // Phase pill
  const phase=d.over_phase||'';const pp=$('phase-pill');
  if(phase&&pp){pp.style.display='block';pp.textContent=phase;pp.className='phase-pill '+phase;}
  else if(pp){pp.style.display='none';}

  // Win probability
  const wp=d.win_prob||{};
  const _wp1=parseFloat(wp.team1||wp[Object.keys(wp)[0]]||0);
  if(_wp1>0&&_wp1<=1){
    const v1=Math.round(_wp1*100),v2=100-v1,isTied=(v1===50&&v2===50);
    requestAnimationFrame(()=>{
      $('wp1').style.width=v1+'%';$('wp1').textContent=v1+'%';$('wp2').textContent=v2+'%';
      ['wp1','wp2'].forEach(id=>{const el=$(id);if(el)el.classList.toggle('tied',isTied);});
      const tl=$('wp-tied');if(tl)tl.classList.toggle('show',isTied);
    });
    T('wp1l',d.team1);T('wp2l',d.team2);
  }
  T('toss-txt',d.toss||'—');

  // Partnership
  const pr=d.partnership_runs,pb=d.partnership_balls;
  const plive=$('pship-live');
  if(pr!==undefined&&pr!==''){
    plive.classList.add('show');T('pship-val',`${pr}${pb?` (${pb}b)`:''}`);
    const bnames=(d.live_batsmen||[]).map(b=>b.batName||b.name||'').filter(Boolean).join(' & ');
    T('pship-names',bnames||'Current partnership');
  }else{plive.classList.remove('show');}

  $('fh-ring').classList.toggle('show',!!d.is_free_hit);

  // Commentary
  const comm=(d.live_commentary||d.commentary||[]).slice(0,6);
  detectEvents(d,comm);

  // Innings pill — FIX: iPage/isSuperOver defined at top of render
  const pill=$('innings-pill');
  if(pill){
    if(isSuperOver){pill.className='innings-pill super';T('innings-pill-txt','⚡ SUPER OVER');}
    else{pill.className='innings-pill '+(iPage>=2?'second':'first');T('innings-pill-txt',iPage>=2?'2nd Innings':'1st Innings');}
  }
  const sob=$('super-over-badge');if(sob)sob.style.display=isSuperOver?'flex':'none';

  $('comm-list').innerHTML=comm.map(c=>{
    const ev=(c.event||'').toUpperCase();const txt=c.text||c||'';
    const cls=ev.includes('WICKET')||ev.includes('OUT')?'EV_WICKET':ev==='FOUR'?'EV_FOUR':ev==='SIX'?'EV_SIX':ev==='NOBALL'?'EV_NOBALL':ev==='REVIEW'?'EV_REVIEW':'';
    const badge=ev?`<span class="ci-bdg ${ev}">${ev}</span>`:'';
    return`<div class="ci ${cls}"><div class="ci-over">${c.over||''}</div><div class="ci-txt">${txt}${badge}</div></div>`;
  }).join('');

  // Scorecard
  renderScorecard(d);

  // Live batsmen
  const bats=d.live_batsmen||[];
  const b1=bats.find(b=>b.isStriker!==false)||bats[0];
  const b2=bats.find(b=>b.isStriker===false)||bats[1];
  if(b1){T('b1n',b1.batName||b1.name||'—');T('b1r',b1.runs);T('b1b',b1.balls);T('b1sr',b1.strikeRate);T('b1f',b1.fours);T('b1s',b1.sixes);}
  if(b2){T('b2n',b2.batName||b2.name||'—');T('b2r',b2.runs);T('b2b',b2.balls);T('b2sr',b2.strikeRate);}
  detectMilestones(bats);

  // Bowler
  const bw=d.current_bowler||{};
  T('bown',bw.bowlName||'—');T('boww',bw.wickets);T('bowr',bw.runs);T('bowo',bw.overs);T('bowe',bw.economy);

  // Balls
  $('balls-track').innerHTML=parseBalls(d.last_ball||d.recent_overs||'').map(b=>`<div class="ball ${b.c}">${b.l}</div>`).join('');
  detectOverComplete(d);
  T('lw-txt',d.last_wicket||'—');

  // Ticker
  const items=[`${d.team1||'—'} vs ${d.team2||'—'}`,d.series||'',
    `Score: <span class="tk-hi">${d.live_score||d.score||'—'} (${d.live_overs||d.overs||'—'} ov)</span>`,
    d.live_crr?`CRR: <span class="tk-hi">${d.live_crr}</span>`:'',
    d.live_rrr?`RRR: <span class="tk-hi">${d.live_rrr}</span>`:'',
    tgt?`Target: <span class="tk-hi">${tgt}</span>`:'',
    d.status||'',d.toss||'',d.venue||''].filter(Boolean);
  $('tk-sc').innerHTML=[...items,...items].map(i=>`<span>${i}</span><span class="tk-sep"> ◆ </span>`).join('');

  checkStale(d);checkDLS(d);startJustJoined(d);
}

// Poll with cache-bust
async function poll(){
  try{const r=await fetch(DATA_URL+'?t='+Date.now(),{cache:'no-store'});if(!r.ok)return;render(await r.json());}
  catch(e){console.warn('poll:',e);}
}
poll();setInterval(poll,POLL_MS);
</script>
</body>
</html>
