from scipy.io import loadmat
import glob
import os
import numpy as np
import pickle
from PIL import Image
import pdb
anno_folder = 'F:\dataset\\big\PRW-v16.04.20\\annotations'
base_folder = 'F:\dataset\\big\PRW-v16.04.20'
img_folder = 'F:\dataset\\big\PRW-v16.04.20\\frames'
# annos_files = anno_folder+'\*.jpg'
annos = glob.glob(anno_folder+'\*.jpg.mat')
# pdb.set_trace()
anno_num = len(annos)
all_annos = list()
for i in range(anno_num):
    # size:w x h
	anno = annos[i]
	img_name = os.path.basename(anno)[:-4]
	img_file = os.path.join(img_folder,img_name)
	img = Image.open(img_file)
	width,height = img.size
	# pdb.set_trace()
	print(anno)
	info = loadmat(anno)
	# pdb.set_trace()
	if 'box_new' not in info.keys():
		if 'anno_file' in info.keys():
			persons = info['anno_file']
		if 'anno_previous' in info.keys():
			persons = info['anno_previous']
	else  :
		persons = info['box_new']
	persons_id = persons[:,0]
	bboxes = persons[:,1:]
	bboxes_int = bboxes.astype(np.int32)
	print(bboxes_int)
	# if anno=='F:\dataset\\big\PRW-v16.04.20\\annotations\c1s1_060281.jpg.mat':
	# 	pdb.set_trace()
	# pdb.set_trace()
	if (bboxes_int[:,0]==0).sum()>0 :
		coord_x  = np.where(bboxes_int[:,0]==0)[0]
		bboxes_int[coord_x,0]=1
	if (bboxes_int[:,1]==0).sum()>0 :
		coord_x = np.where(bboxes_int[:,1]==0)[0]
		bboxes_int[coord_x,1]=1	
	one_image_anno = {'image_name':img_name,'width':width,'height':height,'person':persons_id,'bboxes':bboxes_int}
	all_annos.append(one_image_anno)

cache_file = os.path.join(base_folder,'cache_file.pkl')
with open(cache_file,'wb') as fid:
	pickle.dump(all_annos,fid, pickle.HIGHEST_PROTOCOL)
print('save annos to pkl.')