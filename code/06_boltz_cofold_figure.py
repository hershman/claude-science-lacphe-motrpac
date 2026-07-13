"""Regenerate the Boltz-2 co-fold figure (Figure 7) from the affinity scores.
Reads data/boltz_affinity_scores.csv (10 ligand x receptor complexes) and reproduces
the two-panel figure: predicted log10 IC50 per target, and HCAR1 binder probability
per ligand against the parent reference. Boltz-2 co-folding itself is run separately
via data/boltz_local.tar.gz on a local GPU; this script only plots its outputs."""
import pandas as pd, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

aff = pd.read_csv("data/boltz_affinity_scores.csv")
order = ["Lac-Phe_parent","D-Phe","Thioamide","Triazole","Reduced_amide"]
names = {"Lac-Phe_parent":"Lac-Phe\n(parent)","D-Phe":"D-Phe","Thioamide":"Thioamide",
         "Triazole":"Triazole","Reduced_amide":"Reduced\namide"}
HCAR,MRG,FOCAL = "#2c6fbf","#a8c4e0","#c0392b"
x = np.arange(len(order)); w = 0.38
fig,(a1,a2) = plt.subplots(1,2,figsize=(9.5,4.3))
h = [aff[(aff.ligand==l)&(aff.receptor=="HCAR1")].affinity_pred_value.iloc[0] for l in order]
m = [aff[(aff.ligand==l)&(aff.receptor=="MRGPRD")].affinity_pred_value.iloc[0] for l in order]
a1.bar(x-w/2,h,w,color=HCAR,label="HCAR1"); a1.bar(x+w/2,m,w,color=MRG,label="MRGPRD")
a1.set_xticks(x); a1.set_xticklabels([names[l] for l in order],fontsize=7)
a1.set_ylabel(r"Predicted log$_{10}$(IC$_{50}$ / $\mu$M)"); a1.legend(frameon=False,fontsize=7)
a1.set_title("HCAR1 is the preferred target for every ligand",loc="left",fontsize=9)
prob = [aff[(aff.ligand==l)&(aff.receptor=="HCAR1")].affinity_probability_binary.iloc[0] for l in order]
cols = ["0.6" if l=="Lac-Phe_parent" else (FOCAL if l=="Triazole" else HCAR) for l in order]
a2.bar(x,prob,0.6,color=cols); a2.axhline(prob[0],ls="--",color="0.5",lw=0.9)
for i,p in enumerate(prob): a2.text(i,p+0.012,f"{p:.2f}",ha="center",fontsize=7)
a2.set_xticks(x); a2.set_xticklabels([names[l] for l in order],fontsize=7)
a2.set_ylabel("Boltz-2 binder probability (HCAR1)"); a2.set_ylim(0,max(prob)*1.18)
a2.set_title("Triazole and reduced amide match or exceed the parent",loc="left",fontsize=9)
fig.suptitle("Boltz-2 co-folding of the shortlisted analogs against the two prioritized HCAR-family targets",fontsize=9.5,y=1.0)
fig.tight_layout(rect=[0,0,1,0.95])
fig.savefig("paper/figures/figure7_boltz_cofold.png",dpi=200,facecolor="white")
print("wrote paper/figures/figure7_boltz_cofold.png")
print("HCAR1 binder probs:",dict(zip(order,[round(p,2) for p in prob])))
