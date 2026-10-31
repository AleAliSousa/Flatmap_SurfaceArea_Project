from prepare_precision import *
logdir=OUT/'validation';logdir.mkdir(exist_ok=True)
for paper in sorted({c['paper'] for c in json.loads((OUT/'applied_changes.json').read_text())}):
 root=FM/paper;full=(root/'scripts/rebuild_all.py').exists()
 command=[sys.executable,'-B',str(root/('scripts/rebuild_all.py' if full else 'scripts/measure_flatmaps.py'))]
 if not full:command+=['--rebuild']
 command+=['--java',JAVA,'--ij-jar',IJ]
 print('Rebuilding',paper,flush=True)
 with (logdir/(paper+'.log')).open('w') as log:
  result=subprocess.run(command,cwd=root,stdout=log,stderr=subprocess.STDOUT)
 if result.returncode:
  print((logdir/(paper+'.log')).read_text()[-5000:],flush=True);raise RuntimeError(paper)
 print('Passed',paper,flush=True)
print('All six publication rebuilds passed',flush=True)
