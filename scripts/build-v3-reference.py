"""Build compact geography and first-observation metadata from reviewed local inputs."""
from pathlib import Path
import json,re,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def write(p,j):(ROOT/p).write_text(json.dumps(j,ensure_ascii=False,separators=(',',':'))+'\n')
html=(ROOT/'index.html').read_text()
def embedded(name):
 m=re.search(r'const '+re.escape(name)+r' = JSON.parse\(("(?:[^"\\]|\\.)*")\)',html)
 return json.loads(json.loads(m[1]))
geo=read('data/geography/national-ufs.geojson');old=embedded('value$3');codes={f['code']:f['uf'] for f in old['features']}
def project(p):return [round((p[0]+75)*13.5*.9659258263,2),round((6-p[1])*13.5,2)]
features=[]
for f in geo['features']:
 polygons=f['geometry']['coordinates'] if f['geometry']['type']=='MultiPolygon' else [f['geometry']['coordinates']]
 rings=[ring for poly in polygons for ring in poly]
 path=' '.join('M'+' L'.join(','.join(map(str,project(p))) for p in ring)+' Z' for ring in rings)
 features.append({'uf':codes[f['properties']['codarea']],'path':path})
spatial=read('data/scenarios/phase3_spatial.json');socio=read('data/scenarios/socioeconomic.json');centers={m['code']:m for m in spatial['geography']['centroids']};dealers=embedded('value$2')
municipalities=[]
for m in socio['rows']:
 c=centers.get(m['code']);municipalities.append({k:m.get(k) for k in ['code','name','uf','population','boundaryAttention']}|({'lon':c['lon'],'lat':c['lat'],'x':project([c['lon'],c['lat']])[0],'y':project([c['lon'],c['lat']])[1]} if c else {}))
write('data/geography/v3-reference.json',{'schemaVersion':'market-v3-reference-1','source':'IBGE national UF polygons + derived municipal polygon centroids','sourceUrl':'https://servicodados.ibge.gov.br/api/v3/malhas/paises/BR?formato=application/vnd.geo+json&qualidade=minima&intrarregiao=UF','ufSourceSha256':hashlib.sha256((ROOT/'data/geography/national-ufs.geojson').read_bytes()).hexdigest(),'viewBox':'0 0 670 570','features':features,'municipalities':municipalities,'dealers':dealers['municipalities'],'dealerLocations':dealers['totalLocations'],'dealerAsOf':dealers['asOf'],'centroidCount':len(centers),'limits':'Centroids are derived planar polygon centers, not dealer addresses. Missing coordinates stay in the accessible table.'})
manifest=read('data/manifest.json');first={};retail_monthly=[]
for i,meta in enumerate(manifest['months']):
 if not meta.get('cubePath'):continue
 with gzip.open(ROOT/'data'/meta['cubePath'],'rt') as stream:c=json.load(stream)
 idx={k:i for i,k in enumerate(c['columns'])};d=c['dictionaries'];models=set();retail=0;known=any(v in ['VAREJO','VD'] for v in d.get('tipo_venda',[]))
 for row in c['rows']:
  if row[idx['count']]>0 and d['segmento'][row[idx['segmento']]] in ['Auto','Comercial Leve']:
   models.add(d['modelo'][row[idx['modelo']]])
   if d.get('tipo_venda',[])[row[idx['tipo_venda']]]=='VAREJO':retail+=row[idx['count']]
 for model in models:first.setdefault(model,meta['month'])
 retail_monthly.append({'month':meta['month'],'retail':retail if known else None})
 if i%24==0:print('First observations:',i,flush=True)
write('data/v3-model-observations.json',{'schemaVersion':'market-model-observations-1','coverageStart':manifest['coverageStart'],'coverageEnd':manifest['coverageEnd'],'firstObserved':first,'method':'First positive observation in the reviewed light-vehicle archive, not confirmed commercial launch. Source-model spelling preserved. Gaps and the left edge of the archive can censor first observation.'})
print('Built national geometry, network reference and first-observation metadata.',flush=True)

credit=read('data/scenarios/phase23_models.json')['economics']['realCredit'];credit_index={r['month']:r for r in credit['monthly']}
write('data/v3-retail-credit.json',{'schemaVersion':'market-retail-credit-1','scope':'Fixed national light-vehicle retail; global filters do not recompute this reference','creditUnit':credit['unit'],'deflatorBaseMonth':credit['deflatorBaseMonth'],'rows':[r|{'realCredit':credit_index.get(r['month'],{}).get('value')} for r in retail_monthly]})
