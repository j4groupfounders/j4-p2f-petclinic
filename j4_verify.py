"""Evidence-first runner: separate infrastructure failures from detections."""
import pathlib,json,subprocess,os,sys,time,re,hashlib,urllib.request,urllib.error,xml.etree.ElementTree as ET
P=pathlib.Path('.');E=P/'Evidence';E.mkdir(exist_ok=True);c=json.loads((P/'j4_config.json').read_text());n=c['name'];mutation=int(os.environ.get('J4_MUTATION','-1'));result={'mutation':mutation,'infrastructure':False}
def run(cmd,file,timeout=420):
 with (E/file).open('w') as f:
  r=subprocess.run(cmd,shell=True,executable='/bin/bash',stdout=f,stderr=subprocess.STDOUT,timeout=timeout)
 return r.returncode
def inventory():
 if n=='mongoose-demo':
  text=(E/'tests.log').read_text();ids=re.findall(r'^# (.+)$',text,re.M);ids=[x for x in ids if not re.match(r'(tests |pass |fail |ok$)',x)]
  total=re.search(r'^# tests\s+(\d+)',text,re.M)
  assert total and int(total[1])>0,'No complete TAP test plan'
  fail=bool(re.search(r'^not ok ',text,re.M));return {'ids':ids,'assertions':int(total[1]),'skips':[]},fail
 files=list(P.glob('target/surefire-reports/TEST-*.xml')) if n=='petclinic' else [E/'junit.xml']
 assert files and all(f.exists() for f in files),'Missing test XML; infrastructure not detection'
 ids=[];skips=[];fails=[]
 for f in files:
  root=ET.parse(f).getroot()
  for t in root.iter('testcase'):
   ident=t.get('classname',t.get('class',''))+'::'+t.get('name','');ids.append(ident)
   if t.find('skipped') is not None:skips.append(ident)
   if t.find('failure') is not None or t.find('error') is not None:fails.append(ident)
 assert ids,'No project tests executed'
 return {'ids':sorted(ids),'skips':sorted(skips)},bool(fails)
def snapshots():
 rows=[]
 class NoRedirect(urllib.request.HTTPRedirectHandler):
  def redirect_request(self,*a,**kw):return None
 op=urllib.request.build_opener(NoRedirect)
 for route in c['routes']:
  req=urllib.request.Request('http://127.0.0.1:8080'+route,headers={'Accept':'application/json' if n=='laravelreal' else 'text/html'})
  try:r=op.open(req,timeout=15)
  except urllib.error.HTTPError as e:r=e
  b=r.read().decode('utf-8','replace');assert r.code<500,(route,r.code,b[:200])
  b=re.sub(r'(name="_csrf"[^>]*value=")[^"]+',r'\1<CSRF>',b)
  b=re.sub(r'(name="_token"[^>]*value=")[^"]+',r'\1<CSRF>',b)
  rows.append({'route':route,'status':r.code,'type':r.headers.get('Content-Type',''),'redirect':r.headers.get('Location'),'hash':hashlib.sha256(b.encode()).hexdigest(),'body':b})
 return rows
try:
 if mutation>=0:
  m=json.loads((P/'j4_mutations.json').read_text())[mutation];f=P/m['file'];s=f.read_text();assert s.count(m['old'])==m.get('count',1),'Seed target drift';f.write_text(s.replace(m['old'],m['new']));result['fault']=m['name']
 if n=='laravelreal':
  pathlib.Path('/tmp/j4.sqlite').touch();assert run('php artisan migrate:fresh --force','migration.log')==0
  rc=run('vendor/bin/phpunit --log-junit Evidence/junit.xml','tests.log')
 elif n=='petclinic':
  rc=run('./mvnw -B -ntp -Dcheckstyle.skip -Dspring-javaformat.skip=true test','tests.log')
 else:rc=run('npm test','tests.log')
 inv,detected=inventory();(E/'inventory.json').write_text(json.dumps(inv,indent=2));result.update(project_rc=rc,project_detected=detected)
 assert rc==0 or detected,'Test process failed without test failure: infrastructure'
 if (P/'j4-inventory.json').exists() and not detected:
  assert inv==json.loads((P/'j4-inventory.json').read_text()),'Test inventory changed'
 if n=='petclinic':
  assert run('./mvnw -B -ntp -Dcheckstyle.skip -Dspring-javaformat.skip=true -DskipTests package','build.log')==0,'Build failed: infrastructure'
  jars=[f for f in P.glob('target/*.jar') if not f.name.endswith('.original')];assert len(jars)==1
  cmd=['java','-jar',str(jars[0]),'--server.port=8080']
 elif n=='laravelreal':cmd=['php','artisan','serve','--host=127.0.0.1','--port=8080']
 else:cmd=['node','server.js']
 env=os.environ.copy();env['PORT']='8080'
 with (E/'server.log').open('w') as log:
  server=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,env=env)
  try:
   ready=False
   for _ in range(90):
    if server.poll() is not None:raise RuntimeError('Server exited: see log')
    try:
     urllib.request.urlopen('http://127.0.0.1:8080'+c['routes'][0],timeout=2);ready=True;break
    except Exception:time.sleep(1)
   assert ready,'Server did not boot'
   surface=snapshots();again=snapshots();assert surface==again,'Unstable baseline surface'
  finally:server.terminate();server.wait(timeout=20)
 (E/'surface.json').write_text(json.dumps(surface,indent=2));http_detected=(P/'surface.json').exists() and surface!=json.loads((P/'surface.json').read_text());result['http_detected']=http_detected
 result['combined_detected']=detected or http_detected
 if n=='laravelreal':(E/'composer.lock').write_bytes((P/'composer.lock').read_bytes())
 if n=='mongoose-demo':(E/'package-lock.json').write_bytes((P/'package-lock.json').read_bytes())
 if n=='petclinic':
  assert run('./mvnw -B -ntp dependency:tree -DoutputFile=Evidence/dependency-tree.txt','dependencies.log')==0
 result['success']= (not detected and not http_detected) if mutation<0 else True
except Exception as e:
 result.update(infrastructure=True,error=str(e),success=False)
finally:
 (E/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));sys.exit(0 if result.get('success') else 1)
