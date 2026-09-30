import json,re,collections
DEG=[('(NBEMS-DIPLOMA)','DNB Diploma'),('(NBEMS)','DNB')]
SP=[('ANAESTH','Anaesthesiology'),('AEROSPACE','Aerospace Medicine'),('BIOCHEM','Biochemistry'),('ANATOMY','Anatomy'),('COMMUNITYHEALTH','Community Medicine'),('PREVENTIVE','Community Medicine'),('COMMUNITYMED','Community Medicine'),('PUBLICHEALTH','Community Medicine'),('EPIDEMIOL','Epidemiology'),('DERM','Dermatology'),('EMERGENCY','Emergency Medicine'),('FAMILY','Family Medicine'),('FORENSIC','Forensic Medicine'),('GENERALMEDICINE','General Medicine'),('GENERALSURGERY','General Surgery'),('ADMIN','Hospital Administration'),('MICROBIO','Microbiology'),('BACTERIOL','Microbiology'),('OBST','Obstetrics & Gynaecology'),('GYNAE','Obstetrics & Gynaecology'),('PAEDIATRICSURGERY','Paediatric Surgery'),('PAEDIATRIC','Paediatrics'),('CHILDHEALTH','Paediatrics'),('PALLIATIVE','Palliative Medicine'),('PATHOLOGY','Pathology'),('PHARMACOL','Pharmacology'),('PHYSICALMED','PMR'),('PHY.MEDICINE','PMR'),('PHYSIOLOGY','Physiology'),('PSYCH','Psychiatry'),('RADIO-DIAGNOSIS','Radiodiagnosis'),('RADIODIAGNOSIS','Radiodiagnosis'),('RADIOTHERAPY','Radiation Oncology'),('RADIO-THERAPY','Radiation Oncology'),('RADIATIONONCOLOGY','Radiation Oncology'),('RADIATIONMEDICINE','Radiation Medicine'),('TROPICAL','Tropical Medicine'),('TUBERCULOSIS','Respiratory Medicine'),('RESPIRATORY','Respiratory Medicine'),('T.B.AND','Respiratory Medicine'),('GERIATRIC','Geriatric Medicine'),('NUCLEAR','Nuclear Medicine'),('TRANSFUSION','Transfusion Medicine'),('IMMUNO','Transfusion Medicine'),('SPORTS','Sports Medicine'),('LABORATORYMED','Laboratory Medicine'),('E.N.T.','ENT'),('OTORHINO','ENT'),('OTO-RHINO','ENT'),('OPHTHAL','Ophthalmology'),('DOMS','Ophthalmology'),('ORTHOPAEDIC','Orthopaedics'),('TRAUMATOLOGY','Orthopaedics'),('CARDIOVASCULAR','CTVS'),('NEUROSURGERY','Neurosurgery'),('PLASTIC','Plastic Surgery'),('DIABETOLOGY','Diabetology')]
def course(c):
    c=re.sub(r'\s+',' ',c).strip(); u=c.upper(); T=u.replace(' ','')
    if u.startswith('(NBEMS-DIPLOMA)'): d='DNB Diploma'
    elif u.startswith('(NBEMS)'): d='DNB'
    elif u.startswith('MD/MS') or ('M.D.' in u[:5] and '/MS' in T): d='MD/MS'
    elif u.startswith('M.D.'): d='MD'
    elif u.startswith('M.S.'): d='MS'
    elif u.startswith('M.CH'): d='MCh'
    elif u.startswith('M.P.H'): d='MPH'
    else: d='Diploma'
    T=T.replace('(NBEMS-DIPLOMA)','').replace('(NBEMS)','')
    s=next((n for k,n in SP if k in T),None)
    if d=='MCh' and s=='Neurosurgery': s='Neurosurgery'
    if s is None: s=c.title()
    return d,s
STS={'Andhra Pradesh':['andhra pradesh','andhra','a.p.'],'Arunachal Pradesh':['arunachal'],'Assam':['assam'],'Bihar':['bihar'],'Chandigarh':['chandigarh'],'Chhattisgarh':['chhattisgarh'],'Delhi':['delhi'],'Goa':['goa'],'Gujarat':['gujarat'],'Haryana':['haryana'],'Himachal Pradesh':['himachal','h.p.'],'Jammu & Kashmir':['jammu','j&k','kashmir'],'Jharkhand':['jharkhand'],'Karnataka':['karnataka','karna'],'Kerala':['kerala'],'Ladakh':['ladakh'],'Madhya Pradesh':['madhya pradesh','m.p.'],'Maharashtra':['maharashtra'],'Manipur':['manipur'],'Meghalaya':['meghalaya'],'Mizoram':['mizoram'],'Nagaland':['nagaland'],'Odisha':['odisha','orissa'],'Puducherry':['puducherry','pondicherry'],'Punjab':['punjab'],'Rajasthan':['rajasthan'],'Sikkim':['sikkim'],'Tamil Nadu':['tamil nadu','tamilnadu'],'Telangana':['telangana'],'Tripura':['tripura'],'Uttar Pradesh':['uttar pradesh','u.p','up '],'Uttarakhand':['uttarakhand','uttarajgand'],'West Bengal':['west bengal'],'Andaman & Nicobar':['andaman'],'Dadra & Nagar Haveli':['dadra']}
CITY={'hardoi':'Uttar Pradesh','korba':'Chhattisgarh','kathua':'Jammu & Kashmir','baramulla':'Jammu & Kashmir','machilipatnam':'Andhra Pradesh','haveri':'Karnataka','lakhimpur':'Assam','soban singh jeena':'Uttarakhand','nandi medical':'Karnataka','kolkata':'West Bengal','chennai':'Tamil Nadu','hyderabad':'Telangana','mumbai':'Maharashtra','pune':'Maharashtra','nagpur':'Maharashtra','jaipur':'Rajasthan','lucknow':'Uttar Pradesh','bengaluru':'Karnataka','mysore':'Karnataka','mysuru':'Karnataka','kochi':'Kerala','kannur':'Kerala','guntur':'Andhra Pradesh','vijayawada':'Andhra Pradesh','visakhapatnam':'Andhra Pradesh','coimbatore':'Tamil Nadu','salem':'Tamil Nadu','ahmedabad':'Gujarat','surat':'Gujarat','bhopal':'Madhya Pradesh','indore':'Madhya Pradesh','noida':'Uttar Pradesh','faridabad':'Haryana','sonipat':'Haryana','rohtak':'Haryana'}
def state(s):
    m=re.search(r',\s*([^,]+?)\s*,\s*\d{6}\s*$',s); t=s.lower()
    if m:
        x=m[1].lower()
        for k,al in STS.items():
            if any(x.startswith(a) or x==a for a in al): return k
    best=(-1,None)
    for k,al in STS.items():
        for a in al:
            i=t.rfind(a)
            if i>best[0]: best=(i,k)
    if best[1]: return best[1]
    for c,k in CITY.items():
        if c in t: return k
    return 'Other'
def inst(s):
    s=re.sub(r'\s+',' ',s).strip(); m=re.search(r'(\d{6})\s*$',s); pin=m[1] if m else ''
    st=state(s); segs=[x.strip() for x in s.split(',')]; nm=segs[0]
    if nm.upper()=='PGIMER' and 'RML' in s.upper(): nm='PGIMER, Dr. RML Hospital (ABVIMS)'; segs=[nm,'New Delhi']
    if nm.isupper(): nm=nm.title()
    return nm,st,pin,', '.join(x for x in segs[1:] if x)[:90],[x for x in segs[1:] if x and x.lower()!=nm.lower()]
QN={'All India':'All India','DNB Quota':'DNB','Self-Financed Merit Seat/(Paid Seat Quota)':'Deemed/Paid','Self-Financed Merit Seat':'Deemed/Paid','Non-Resident Indian':'NRI','Delhi University Quota':'Delhi Univ','IP University Quota':'IP Univ','Aligarh Muslim University':'AMU','Banaras Hindu University':'BHU','Jain Minority Quota':'Jain Minority','Muslim Minority Quota':'Muslim Minority','Armed Forces Medical':'Armed Forces'}
G={};IN={};CO={};stats={}
for r in (1,2,3):
    n=0;allrows=0
    for l in open(f'raw{r}.jsonl'):
        x=json.loads(l);allrows+=1
        if x.get('course','-') in('-','') or x.get('inst','-')=='-' or not x.get('rank','').isdigit(): continue
        n+=1;rk=int(x['rank']);nm,st,pin,addr,alt=inst(x['inst']);ik=(re.sub(r'\W','',nm.lower()),st,pin)
        IN.setdefault(ik,(nm,st,addr,(alt[0].title() if alt else '')))
        d,s=course(x['course']);cl=f'{d} {s}'; CO[cl]=(d,s)
        q=QN.get(re.sub(r'\s+',' ',x['quota']),x['quota']); ac=x['acat'].strip()
        g=G.setdefault((ik,cl,q,ac),{}).setdefault(r,[rk,rk,0]); g[0]=min(g[0],rk);g[1]=max(g[1],rk);g[2]+=1
    stats[r]=(allrows,n)
cnt=collections.Counter(v[0] for v in IN.values())
for k,v in list(IN.items()):
    if cnt[v[0]]>1 and v[3] and v[3].lower()!=v[1].lower(): IN[k]=(v[0]+' ('+v[3]+')',v[1],v[2])
    else: IN[k]=(v[0],v[1],v[2])
cnt=collections.Counter(v[0] for v in IN.values())
for k,v in list(IN.items()):
    if cnt[v[0]]>1: IN[k]=(v[0]+' ['+v[1]+']',v[1],v[2])
il=sorted(IN,key=lambda k:IN[k][0].lower());ii={k:i for i,k in enumerate(il)}
cl=sorted(CO);ci={k:i for i,k in enumerate(cl)}
ql=sorted({k[2] for k in G});cat=sorted({k[3] for k in G})
rows=[]
for (ik,c,q,a),v in G.items():
    row=[ii[ik],ci[c],ql.index(q),cat.index(a)]
    for r in (1,2,3): row+=v.get(r,[0,0,0])
    rows.append(row)
rows.sort()
D={'meta':{'r1':stats[1],'r2':stats[2],'r3':stats[3],'inst':len(il),'course':len(cl),'sp':len({v[1] for v in CO.values()}),'combos':len(rows)},'inst':[list(IN[k]) for k in il],'course':[list(CO[k]) for k in cl],'quota':ql,'cat':cat,'rows':rows}
json.dump(D,open('data.json','w'),separators=(',',':'))
print(stats,'institutes',len(il),'courses',len(cl),'specialties',len({v[1] for v in CO.values()}),'combos',len(rows))
print(cl);print(ql,cat);print(collections.Counter(IN[k][1] for k in il).most_common());print([IN[k][0] for k in il[:12]])
import os;print(os.path.getsize('data.json')/1e6,'MB')
