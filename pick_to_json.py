import pickle
import os
import json

pick_files = os.listdir('.')
pick_files = [i for i in pick_files if '.pic' in i]

for file in pick_files:
	name = file.split('.')[0]
	with open(f'{name}.json','w') as json_file:
		with open(f'{file}','rb') as pick_file:
			pic = pickle.loads(pick_file.read())
			fixed = {}
			for subj in pic:
				for key,val in subj.items():
					fixed[key] = val

			out = json.dumps(fixed,indent=4)
			json_file.write(out)
