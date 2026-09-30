import re,subprocess,json,sys,html
COLS={1:[('sno',0,45),('rank',45,90),('quota',90,180),('inst',180,539),('course',539,651),('acat',651,696),('ccat',696,752),('rem',752,9999)],
2:[('rank',0,46),('quota',358,418),('inst',418,550),('course',550,636),('acat',636,690),('ccat',690,736),('opt',736,782),('rem',782,9999)],
3:[('rank',0,44),('quota',577,621),('inst',621,866),('course',866,991),('acat',991,1036),('ccat',1036,1080),('opt',1080,1124),('rem',1124,9999)]}
RX=re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>')
HDR={'SNo','Rank','NEET-PG','Counselling','Allotted','Alloted','Candidate','Remarks','Round','Round-','Quota','Institute','Course','Category'}
def cell(ws):
    ws=sorted(ws,key=lambda w:(round(w[1]/4),w[0])); lines=[];cy=None
    for w in ws:
        if cy is None or abs(w[1]-cy)>3: lines.append([]);cy=w[1]
        lines[-1].append(w[4])
    t=''
    for l in lines:
        l=' '.join(l); t=(t+l) if t.endswith('-') else (t+' '+l if t else l)
    return t.strip()
def page_records(rnd,ws,last,st):
    cols=COLS[rnd]; rx=cols[1][2] if rnd==1 else cols[0][2]
    fy=None
    for i,w in enumerate(ws[:-1]):
        if w[4]=='Page' and ws[i+1][4]=='No.': fy=w[1]
    if fy: ws=[w for w in ws if w[1]<fy-1]
    sx=45 if rnd==1 else cols[0][2]
    starts=sorted([w for w in ws if w[4].isdigit() and (w[0]+w[2])/2<sx and w[0]<sx-4],key=lambda w:w[1])
    if rnd==1: rcol=cols[1]
    else: rcol=cols[0]
    out=[]
    ys=[s[1] for s in starts]
    buckets=[[] for _ in starts]; orphan=[]
    for w in ws:
        if not ys or w[1]<ys[0]-1: orphan.append(w); continue
        k=0
        for j,y in enumerate(ys):
            if y<=w[1]+1: k=j
            else: break
        buckets[k].append(w)
    if orphan and last is not None and not any(w[4] in HDR for w in orphan):
        st['orphan']+=1
        for w in orphan:
            c=(w[0]+w[2])/2
            for n,a,b in cols:
                if a<=c<b: last['_w'].setdefault(n,[]).append(w)
    for s,b in zip(starts,buckets):
        rec={'_w':{}}
        for w in b:
            c=(w[0]+w[2])/2
            for n,a,bb in cols:
                if a<=c<bb: rec['_w'].setdefault(n,[]).append(w)
        out.append(rec)
    return out
def run(rnd,path,outp):
    p=subprocess.Popen(['pdftotext','-bbox',path,'-'],stdout=subprocess.PIPE,text=True,bufsize=1<<20)
    ws=[];last=None;st={'orphan':0,'pages':0};recs=[]
    def flush():
        nonlocal ws,last
        rs=page_records(rnd,ws,last,st)
        if recs and rs: pass
        for r in rs: recs.append(r)
        if rs: last=rs[-1]
        elif last is None: pass
        ws=[];st['pages']+=1
    for line in p.stdout:
        line=line.lstrip()
        if line.startswith('<word'):
            m=RX.search(line)
            if m: ws.append((float(m[1]),float(m[2]),float(m[3]),float(m[4]),html.unescape(m[5])))
        elif line.startswith('</page>'):
            flush()
            if st['pages']%200==0: print(rnd,st['pages'],len(recs),flush=True)
    with open(outp,'w') as f:
        for r in recs:
            d={n:cell(w) for n,w in r['_w'].items()}
            f.write(json.dumps(d)+'\n')
    print('done',rnd,st,len(recs),flush=True)
if __name__=='__main__':
    files=[l.strip() for l in open('/home/claude/t/files.txt')]
    for r in (1,2,3): run(r,files[r-1],f'/home/claude/raw{r}.jsonl')
