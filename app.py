import argparse,sqlite3,hashlib,wave,json,tempfile,unittest,struct
from pathlib import Path
def connect(path):
 db=sqlite3.connect(path);db.execute('CREATE TABLE IF NOT EXISTS samples(path TEXT PRIMARY KEY, sha TEXT, duration REAL, rate INTEGER, channels INTEGER)');return db
def scan(db,folder):
 report={'indexed':0,'errors':[]}
 for p in sorted(Path(folder).rglob('*.wav')):
  try:
   with wave.open(str(p),'rb')as w:duration=w.getnframes()/w.getframerate();rate=w.getframerate();channels=w.getnchannels()
   digest=hashlib.file_digest(p.open('rb'),'sha256').hexdigest();db.execute('INSERT OR REPLACE INTO samples VALUES(?,?,?,?,?)',(str(p.resolve()),digest,duration,rate,channels));report['indexed']+=1
  except(wave.Error,OSError,EOFError)as e:report['errors'].append({'file':str(p),'error':str(e)})
 db.commit();return report
def search(db,term='',minimum=0):return [dict(zip(['path','sha256','seconds','rate','channels'],row))for row in db.execute('SELECT * FROM samples WHERE path LIKE ? AND duration>=? ORDER BY path',('%'+term+'%',minimum))]
def duplicates(db):return [dict(sha256=r[0],copies=r[1])for r in db.execute('SELECT sha,COUNT(*) FROM samples GROUP BY sha HAVING COUNT(*)>1')]
class Tests(unittest.TestCase):
 def test_catalog(self):
  with tempfile.TemporaryDirectory()as d:
   p=Path(d)/'one.wav'
   with wave.open(str(p),'wb')as w:w.setparams((1,2,8000,0,'NONE',''));w.writeframes(struct.pack('<hh',0,1))
   (Path(d)/'copy.wav').write_bytes(p.read_bytes());db=connect(':memory:');self.assertEqual(scan(db,d)['indexed'],2);self.assertEqual(duplicates(db)[0]['copies'],2);self.assertEqual(len(search(db,'one')),1);self.assertEqual(search(db,'',1),[])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('folder',nargs='?');p.add_argument('--db',default='catalog.sqlite');p.add_argument('--search',default='');p.add_argument('--minimum',type=float,default=0);p.add_argument('--self-test',action='store_true');a=p.parse_args()
 if a.self_test:unittest.main(argv=['catalog'])
 else:
  with connect(a.db)as db:
   if a.folder:print(json.dumps(scan(db,a.folder),indent=2))
   print(json.dumps({'samples':search(db,a.search,a.minimum),'duplicates':duplicates(db)},indent=2))
