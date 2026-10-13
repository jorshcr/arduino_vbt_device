from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

DEST = Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none'})
fig, ax = plt.subplots(figsize=(17,10))
fig.subplots_adjust(0,0,1,1)
ax.set(xlim=(0,17),ylim=(0,10)); ax.axis('off')
ink='#172D40'; muted='#526574'; blue='#326788'; teal='#287A72'; amber='#9B6C2E'
def txt(x,y,s,size=11,color=ink,weight='normal',ha='left'):
    ax.text(x,y,s,fontsize=size,color=color,weight=weight,ha=ha,va='center',linespacing=1.55)
def box(x,y,w,h,title,body,color=blue,fill='#F3F7FA'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.02,rounding_size=0.08',facecolor=fill,edgecolor=color,linewidth=1.2))
    txt(x+.18,y+h-.26,title,12,color,'bold')
    if body: txt(x+.18,y+(h-.42)/2,body,10)
def arrow(points,color=blue,dashed=False):
    for p,q in zip(points[:-2],points[1:-1]):
        ax.plot([p[0],q[0]],[p[1],q[1]],color=color,lw=1.35,ls='--' if dashed else '-')
    ax.add_patch(FancyArrowPatch(points[-2],points[-1],arrowstyle='-|>',mutation_scale=12,color=color,lw=1.35,linestyle='--' if dashed else '-'))

txt(.55,9.5,'Arduino VBT | Data pipeline',25,weight='bold')
txt(.55,9.04,'From weight-stack motion to a post-set estimate of repetitions in reserve (RIR)',13,muted)
for x,w,label,c in [(.55,4.25,'A  /  ON-DEVICE SIGNAL PROCESSING',blue),(6.05,4.6,'B  /  HOST-SIDE ANALYSIS',teal),(11.9,4.55,'C  /  MODEL & USER INTERFACE',amber)]:
    txt(x,8.48,label,11,c,'bold')
    ax.plot([x,x+w],[8.22,8.22],color=c,lw=2)

box(.55,6.95,4.25,1.0,'Weight-stack motion → IMU','Arduino Nano 33 BLE Sense • LSM9DS1\n3-axis acceleration; g → m/s²')
box(.55,5.59,4.25,1.0,'Acceleration conditioning','First-order high-pass filter: 0.3 Hz\nFilter coefficients assume 119 Hz')
box(.55,4.23,4.25,1.0,'Velocity estimation','Integrate using measured Δt\nHigh-pass velocity again at 0.3 Hz')
box(.55,2.87,4.25,1.0,'USB serial transport','115200 baud • CSV records\nt [µs], vx, vy, vz [m/s]')
for y in [6.95,5.59,4.23]: arrow([(2.675,y),(2.675,y-.36)])

box(6.05,6.95,4.6,1.0,'Serial ingestion','Parse 4 fields; convert timestamp to seconds\nSpeed: ‖v‖ = √(vx² + vy² + vz²)',teal,'#F1F8F6')
box(6.05,5.59,4.6,1.0,'Concentric rep segmentation','vz < −0.05 m/s; accept duration > 0.3 s\nStore completed rep windows and count',teal,'#F1F8F6')
box(6.05,4.23,4.6,1.0,'Post-set feature extraction','Mean and peak speed for each valid rep\nLast-rep mean speed; completed-rep count',teal,'#F1F8F6')
box(6.05,2.87,4.6,1.0,'Three-input feature vector','[load %, last-rep mean speed, rep count]',teal,'#F1F8F6')
for y in [6.95,5.59,4.23]: arrow([(8.35,y),(8.35,y-.36)],teal)
arrow([(4.8,3.37),(5.35,3.37),(5.35,7.45),(6.05,7.45)])
txt(5.18,7.87,'CSV',9,blue,ha='center')

box(11.9,6.95,4.55,1.0,'Browser dashboard','Live speed chart + rep count\nPost-set RIR and velocity analytics',amber,'#FCF8F0')
box(11.9,5.59,4.55,1.0,'User input / recording control','Load % = 100 × load / exercise 1RM\nPOST /start; POST /stop',amber,'#FCF8F0')
box(11.9,2.87,4.55,1.0,'Random forest regression','200 trees • random_state = 42\nPredict after recording; round RIR',amber,'#FCF8F0')
box(11.9,.96,4.55,1.13,'Embedded labeled examples','3 input columns + actual_RIR target\nModel fitted at backend startup',amber,'#FCF8F0')
arrow([(10.65,3.37),(11.9,3.37)],teal)
arrow([(14.17,2.09),(14.17,2.87)],amber,True)
txt(14.35,2.46,'fit',9,amber)
arrow([(16.45,3.37),(16.75,3.37),(16.75,7.45),(16.45,7.45)],amber)
txt(15.8,4.47,'RIR',9,amber)
arrow([(11.9,6.08),(11.35,6.08),(11.35,3.65),(10.65,3.65)],amber,True)
txt(11.38,6.33,'load %',9,amber,ha='center')
arrow([(10.65,7.45),(11.9,7.45)],teal)
txt(11.28,7.79,'Socket.IO',9,teal,ha='center')

box(6.05,.96,4.6,1.13,'Parallel display analytics','Velocity loss (%) + peak-speed trend\nIncluded in post-set results; not model inputs',teal,'#F1F8F6')
arrow([(6.05,4.73),(5.7,4.73),(5.7,1.52),(6.05,1.52)],teal)
txt(.55,2.15,'Recording ends at:',11,weight='bold')
txt(.55,1.52,'70 s, manual stop, or speed range < 0.1 m/s\nover 476 samples (nominally 4 s).',10,muted)
txt(.55,.53,'Solid arrows: data / predictions     Dashed arrows: configuration / model fitting',10,muted)
txt(.55,.2,'Implementation snapshot: 8c6756b • Python runtime path; MATLAB and the formatter are auxiliary tools.',9,muted)
DEST.mkdir(parents=True,exist_ok=True)
for ext in ['svg','png']:
    target=DEST/f'data-pipeline.{ext}'
    fig.savefig(target,dpi=220,facecolor='white')


