"""Charts fuer / for no. 01 - Der Fall (des) Infantino / The Case (and Fall) of Infantino.
Erzeugt beide Sprachfassungen aus denselben Daten. Regeln: theme.py / DESIGN.md."""
import theme
from theme import FARBEN, SCHRIFT
import matplotlib.pyplot as plt

S, R, G, GH = FARBEN["schwarz"], FARBEN["rot"], FARBEN["grau"], FARBEN["grauhell"]

T = {
"de": dict(
  f1="gewichtete summe aus fünf kriterien, 0–100 · grau: referenzverbände außerhalb des fußballs",
  marke70="70-punkte-linie",
  krit=["K1 patronage","K2 kontrolle","K3 omertà","K4 konkurrenz","K5 fassade"],
  f2="gleiche kriterien, gleiche gewichte · fifa 85 · iba 78 · ioc 47",
  abh="ausschüttungsabhängige blöcke: 146 (69 %)", wert="wertschöpfungsblöcke: 65 (31 %)",
  mehr="mehrheit: 106", f3="die 211 kongressstimmen · ein verband, eine stimme",
  l4=["ausschüttungen\n2016–2018","ausschüttungen\nab 2019","gesamtbudget\n2027–2030"],
  mrd=lambda w:f"{w} mrd. $",
  anm4='+ 20 mio. $ \u201esoforthilfe\u201c je verband,\nnur bei zustimmung (aug. 2026)',
  f4="budget 2027–2030 (grau) enthält alle ausgaben, nicht nur ausschüttungen",
  f5="patronage-wert k1 (ausschüttungsabhängigkeit) · schwarz: unterschrieben · grau: nicht · rot: der ausreißer",
  pkt=["A recht & staaten","B verbändekoalition","C exit / sezession","D sponsoren & markt","E selbstreform"],
  pfeil="aug. 2026: 30 auf 50", xl="realisierbarkeit", yl="wirksamkeit (gewichtet)", sfx="de"),
"en": dict(
  f1="weighted sum of five criteria, 0–100 · grey: reference bodies outside football",
  marke70="70-point line",
  krit=["K1 patronage","K2 control","K3 omertà","K4 competition","K5 façade"],
  f2="same criteria, same weights · fifa 85 · iba 78 · ioc 47",
  abh="payout-dependent blocs: 146 (69 %)", wert="value-creating blocs: 65 (31 %)",
  mehr="majority: 106", f3="the 211 congress votes · one federation, one vote",
  l4=["payouts\n2016–2018","payouts\nfrom 2019 on","total budget\n2027–2030"],
  mrd=lambda w:f"${w} bn",
  anm4='+ $20 m \u201cemergency grant\u201d per federation,\nonly upon approval (aug. 2026)',
  f4="budget 2027–2030 (grey) includes all spending, not only payouts",
  f5="patronage score k1 (payout dependence) · black: signed the letter · grey: did not · red: the outlier",
  pkt=["A law & states","B federations' coalition","C exit / secession","D sponsors & market","E self-reform"],
  pfeil="aug. 2026: 30 to 50", xl="feasibility", yl="effectiveness (weighted)", sfx="en"),
}

def fig(h=3.0, left=0.16):
    f, ax = plt.subplots(figsize=(6.4, h))
    f.subplots_adjust(left=left, right=0.97, top=0.93, bottom=0.16)
    return f, ax

def fertig(f, ax, fussnote, out, x0=0.02):
    if fussnote: f.text(x0, 0.03, fussnote, color=G, fontsize=10, fontproperties=SCHRIFT[400])
    f.savefig(out, format="svg", transparent=True); plt.close(f)

def achse(ax):
    ax.set_xlim(0,104); ax.set_xticks([]); ax.tick_params(left=False)
    ax.spines.bottom.set_visible(False); ax.spines.left.set_visible(True)
    ax.spines.left.set_linewidth(2); ax.spines.left.set_color(S)

def build(t):
    # --- 1: Skala ---
    namen=["FIFA","AFC","IBA","CAF","CONMEBOL","CONCACAF","OFC","IOC","UEFA"]
    werte=[85,78,78,74,69,58,54,47,46]; farben=[R,S,GH,S,S,S,S,GH,S]; wf=[R,S,G,S,S,S,S,G,S]
    f,ax=fig(3.6); y=range(len(namen))[::-1]
    ax.barh(list(y),werte,height=0.62,color=farben,linewidth=0)
    ax.set_yticks(list(y)); ax.set_yticklabels(namen)
    for lab in ax.get_yticklabels(): lab.set_fontproperties(SCHRIFT[400]); lab.set_fontsize(10.5); lab.set_color(S)
    for yi,w,c in zip(y,werte,wf):
        ax.text(w+1.5,yi,str(w),va="center",fontsize=10.5,color=c,fontproperties=SCHRIFT[700 if c==R else 500])
    ax.axvline(70,color=R,lw=1,ls=(0,(3,3)))
    ax.text(71.5,len(namen)-0.35,t["marke70"],color=G,fontsize=10,fontproperties=SCHRIFT[400])
    achse(ax); fertig(f,ax,t["f1"],f"001-skala.{t['sfx']}.svg")

    # --- 2: Profil ---
    f,ax=fig(3.6)
    fifa,iba,ioc=[95,85,80,45,95],[90,90,85,95,30],[45,40,55,40,55]
    ypos=range(5)[::-1]
    for off,w,c in ((0.27,fifa,R),(0.0,iba,S),(-0.27,ioc,GH)):
        ax.barh([yy+off for yy in ypos],w,height=0.24,color=c,linewidth=0)
    ax.set_yticks(list(ypos)); ax.set_yticklabels(t["krit"])
    for lab in ax.get_yticklabels(): lab.set_fontproperties(SCHRIFT[400]); lab.set_fontsize(10.5); lab.set_color(S)
    for off,w,c in ((0.27,fifa,R),(0.0,iba,S),(-0.27,ioc,G)):
        for yy,v in zip(ypos,w):
            ax.text(v+1.5,yy+off,str(v),va="center",fontsize=9,color=c,fontproperties=SCHRIFT[500])
    for x,tx,c in ((72,"fifa",R),(80,"iba",S),(88,"ioc",G)):
        ax.text(x/100,1.03,tx,transform=ax.transAxes,color=c,fontsize=10.5,fontproperties=SCHRIFT[700])
    achse(ax); fertig(f,ax,t["f2"],f"001-profil.{t['sfx']}.svg")

    # --- 3: Stimmen ---
    f,ax=plt.subplots(figsize=(6.4,2.0)); f.subplots_adjust(left=0.02,right=0.98,top=0.80,bottom=0.30)
    bloecke=[("CAF",54,S),("AFC",46,S),("CONCACAF",35,S),("OFC",11,S),("UEFA",55,GH),("CONMEBOL",10,GH)]
    x=0
    for name,w,c in bloecke:
        ax.barh(0,w,left=x,height=0.6,color=c,linewidth=0)
        if w>=20:
            ax.text(x+w/2,0,f"{name}\n{w}",ha="center",va="center",color="#ffffff" if c==S else S,
                    fontsize=9.5,fontproperties=SCHRIFT[500],linespacing=1.3)
        else:
            ax.text(min(x+w/2,206),-0.62,f"{name} {w}",ha="center" if x+w/2<200 else "right",va="top",
                    color=G,fontsize=9,fontproperties=SCHRIFT[400])
        x+=w
    ax.axvline(106,color=R,lw=1.2,ls=(0,(3,3)))
    ax.text(106-2.5,-0.62,t["mehr"],color=R,fontsize=10,fontproperties=SCHRIFT[700],va="top",ha="right")
    ax.text(0,0.62,t["abh"],color=S,fontsize=10.5,fontproperties=SCHRIFT[500],va="bottom")
    ax.text(211,0.62,t["wert"],color=G,fontsize=10.5,fontproperties=SCHRIFT[400],va="bottom",ha="right")
    ax.set_xlim(0,211); ax.set_ylim(-1.1,1.3); ax.axis("off")
    fertig(f,ax,t["f3"],f"001-stimmen.{t['sfx']}.svg",x0=0.02)

    # --- 4: Kaufmechanik ---
    f,ax=fig(3.0,left=0.06)
    werte=[1,2,14]
    ax.bar(range(3),werte,width=0.55,color=[S,S,GH],linewidth=0)
    ax.set_xticks(range(3)); ax.set_xticklabels(t["l4"])
    for lab in ax.get_xticklabels(): lab.set_fontproperties(SCHRIFT[400]); lab.set_fontsize(10); lab.set_color(G)
    for i,(w,c) in enumerate(zip(werte,[S,S,G])):
        ax.text(i,w+0.35,t["mrd"](w),ha="center",fontsize=10.5,color=c,fontproperties=SCHRIFT[500])
    ax.set_ylim(0,16.5); ax.set_yticks([])
    ax.plot([2,2],[14.6,15.8],color=R,lw=1,ls=(0,(3,3)))
    ax.plot([0.9,2],[15.8,15.8],color=R,lw=1,ls=(0,(3,3)))
    ax.text(0.82,15.8,t["anm4"],ha="right",va="center",color=R,fontsize=10,fontproperties=SCHRIFT[500],linespacing=1.35)
    ax.tick_params(bottom=False)
    fertig(f,ax,t["f4"],f"001-kaufmechanik.{t['sfx']}.svg",x0=0.06)

    # --- 5: Aufstand ---
    namen=["CAF","AFC","CONMEBOL","CONCACAF","OFC","UEFA"]
    werte=[85,80,80,60,60,45]; farben=[GH,R,GH,S,GH,S]; wf=[G,R,G,S,G,S]
    f,ax=fig(3.0); y=range(len(namen))[::-1]
    ax.barh(list(y),werte,height=0.6,color=farben,linewidth=0)
    ax.set_yticks(list(y)); ax.set_yticklabels(namen)
    for lab in ax.get_yticklabels(): lab.set_fontproperties(SCHRIFT[400]); lab.set_fontsize(10.5); lab.set_color(S)
    for yi,w,c in zip(y,werte,wf):
        ax.text(w+1.5,yi,str(w),va="center",fontsize=10.5,color=c,fontproperties=SCHRIFT[700 if c==R else 500])
    achse(ax); fertig(f,ax,t["f5"],f"001-aufstand.{t['sfx']}.svg")

    # --- 6: Reform ---
    f,ax=fig(3.6,left=0.10)
    xy=[(35,67,S),(50,50,R),(20,56,S),(40,45,S),(90,24,S)]
    for (x,yv,c) in xy: ax.scatter(x,yv,s=210,color=c,zorder=3)
    ax.annotate("",xy=(50,50),xytext=(31,50),arrowprops=dict(arrowstyle="-|>",color=R,lw=1.2,ls=(0,(3,3))))
    ax.text(40,52.8,t["pfeil"],color=R,fontsize=9.5,ha="center",fontproperties=SCHRIFT[500])
    lagen=[(35,73,"center",S),(56,55,"left",R),(20,62,"center",S),(40,38,"center",S),(90,31,"center",S)]
    for name,(lx,ly,haa,c) in zip(t["pkt"],lagen):
        ax.text(lx,ly,name,color=c,fontsize=10.5,ha=haa,fontproperties=SCHRIFT[500])
    ax.set_xlim(0,100); ax.set_ylim(0,100); ax.set_xticks([0,50,100]); ax.set_yticks([0,50,100])
    for lab in ax.get_xticklabels()+ax.get_yticklabels():
        lab.set_fontproperties(SCHRIFT[400]); lab.set_fontsize(10); lab.set_color(G)
    ax.spines.left.set_visible(True); ax.spines.left.set_linewidth(2); ax.spines.left.set_color(S)
    ax.axhline(50,color="#dddddd",lw=1,zorder=1); ax.axvline(50,color="#dddddd",lw=1,zorder=1)
    ax.set_xlabel(t["xl"],fontproperties=SCHRIFT[400],fontsize=10.5,color=G)
    ax.set_ylabel(t["yl"],fontproperties=SCHRIFT[400],fontsize=10.5,color=G)
    ax.tick_params(length=0)
    fertig(f,ax,"",f"001-reform.{t['sfx']}.svg")

for lang in ("de","en"): build(T[lang])
print("12 charts ok")
