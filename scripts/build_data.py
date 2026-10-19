"""Build site/data.json from the tracker snapshot (results + defects) and the UAT case specs.
usage: python3 scripts/build_data.py <tracker_dir> <uat_dir>"""
import json,glob,os,re,sys,time
trk,uat=sys.argv[1],sys.argv[2]
cases=json.load(open(os.path.join(uat,'cases.json')))
secs=json.load(open(os.path.join(uat,'sections.json')))
names={}
for k,v in secs.items():
    m=re.search(r'^## ([A-Z])\. (.+)$',v,re.M)
    if m: names[m.group(1)]=m.group(2).strip()
def load(d):
    out={}
    for f in glob.glob(os.path.join(trk,d,'*.json')):
        j=json.load(open(f)); out[os.path.basename(f)[:-5]]=j.get('data',j)
    return out
R=load('results'); D=load('defects')
def ms(v):
    try: return int(float(v))
    except: return None
rows=[]
for c in cases:
    r=R.get(c['id'],{})
    rows.append({'id':c['id'],'area':c['area'],'title':c['title'],'pri':c.get('pri'),'type':c.get('type'),'req':c.get('req'),
      'pre':c.get('pre'),'data':c.get('data'),'steps':c.get('steps',[]),'exp':c.get('exp',[]),
      'status':r.get('status','Not run'),'actual':r.get('actual',''),'defect':r.get('defect',''),'evidence':r.get('evidence',''),
      'date':r.get('date',''),'updated':ms(r.get('updatedAt'))})
defs=[]
for k,d in D.items():
    defs.append({'ref':d.get('ref') or k,'case':d.get('caseId',''),'sev':d.get('sev',''),'owner':d.get('owner',''),'status':d.get('status',''),
      'title':d.get('title',''),'desc':d.get('desc',''),'work':d.get('work',''),'target':d.get('target',''),'created':ms(d.get('createdAt')),'updated':ms(d.get('updatedAt'))})
defs.sort(key=lambda d:d['ref'])
json.dump({'generated':int(time.time()*1000),'areas':names,'cases':rows,'defects':defs},open('site/data.json','w'),indent=0)
print(len(rows),'cases',len(defs),'defects')
