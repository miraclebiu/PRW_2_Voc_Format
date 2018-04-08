import xml.etree.ElementTree as ET
import pickle 
import copy
import os
from scipy.io import loadmat


import pdb

xml_save_folder = 'F:\dataset\\big\PRW-v16.04.20\\xml'
id_train  = loadmat('ID_train.mat')['ID_train']
id_test   = loadmat('ID_test.mat')['ID_test2']
cache_file = 'cache_file.pkl'
fid = open(cache_file,'rb')
annos = pickle.load(fid)
fid.close()
xml_template = 'new_template.xml'
root = ET.parse(xml_template)
op_root2 = root.getroot()

obj_template = root.find('object')
obj_temp = copy.deepcopy(obj_template)
op_root2.remove(obj_template) 
# op_root.remove(obj_template) 
# person_id = ET.Element('id')
# person_id.text = '-2'
# obj_temp.insert(1,person_id)
# op_root.append(obj_temp)
# root.write('new_template.xml')
num_annos = len(annos)
for i in range(num_annos):
	anno = annos[i]
	print(anno['image_name'])
	print(anno['bboxes'])
	root_cp = copy.deepcopy(root)
	op_root = root_cp.getroot()
	num_person = len(anno['person'])
	bbox_anno = anno['bboxes']
	personid_anno = anno['person']
	root_cp.find('folder').text = 'PRW-v16.04.20'
	root_cp.find('source').find('database').text = 'PRW-v16.04.20'
	person_num = ET.Element('num_person')
	person_num.text = str(num_person)
	root_cp.find('source').insert(1,person_num)
	root_cp.find('filename').text = anno['image_name']
	root_cp.find('size').find('width').text = str(anno['width'])
	root_cp.find('size').find('height').text = str(anno['height'])
	save_name = anno['image_name'][:-4]+'.xml'
	save_name = os.path.join(xml_save_folder,save_name)
	for j in range(num_person):
		obj_cur = copy.deepcopy(obj_temp)
		pid = int(personid_anno[j])
		is_train = ET.Element('is_train')
		is_train.text = 'False'
		is_test = ET.Element('is_test')
		is_test.text = 'False'
		if pid in id_train:
			is_train.text = 'True'	
		elif pid in id_test:
			is_test.text = 'True'
		obj_cur.insert(2,is_train)
		obj_cur.insert(3,is_test)			
		obj_cur.find('id').text = str(pid)
		xml_bbox = obj_cur.find('bndbox')
		xml_bbox.find('xmin').text = str(bbox_anno[j][0])
		xml_bbox.find('ymin').text = str(bbox_anno[j][1])
		xml_bbox.find('xmax').text = str(bbox_anno[j][2]+bbox_anno[j][0])
		xml_bbox.find('ymax').text = str(bbox_anno[j][3]+bbox_anno[j][1])
		op_root.append(obj_cur)
	root_cp.write(save_name)
	# pdb.set_trace()
print('Done!')