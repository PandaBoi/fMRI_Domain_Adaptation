import os
import pickle
import numpy as np



def data_loader(inputs, targets, batch_size, shuffle=True):
    assert inputs.shape[0] == targets.shape[0]
    inputs_size = inputs.shape[0]
    if shuffle:
        random_order = np.arange(inputs_size)
        np.random.shuffle(random_order)
        inputs, targets = inputs[random_order, :], targets[random_order]
    num_blocks = int(inputs_size / batch_size)
    for i in range(num_blocks):
        yield inputs[i * batch_size: (i+1) * batch_size, :], targets[i * batch_size: (i+1) * batch_size]
    if num_blocks * batch_size != inputs_size:
        yield inputs[num_blocks * batch_size:, :], targets[num_blocks * batch_size:]



def load_fmri_data(db_name, data_path, logger,mod = 0,alpha = None):

  data = []
  with open(data_path,'rb') as fp:
    data = pickle.load(fp)
  fp.close()
  keys = list(data.keys())
  
  if mod:
    for key in keys:
      if np.unique(data[key]['label']).shape[0] == 1:
        data.pop(key,None)
        continue
    if alpha is None:
      sampler = imblearn.over_sampling.RandomOverSampler(sampling_strategy='minority')
    else:
      assert type(alpha) == float
      # sampler = imblearn.over_sampling.RandomOverSampler(sampling_strategy= alpha)
      sampler = OverSampler(sampling = alpha)
  

  data_names = list(data.keys())
  print(data_names)
  train_insts, train_labels, test_insts, test_labels = {}, {}, {}, {}

  for idx,dataset in enumerate(data_names):
    
    files = np.array(data[dataset]['data'])
    labels = np.array(data[dataset]['label'])

    train_insts[idx] = files
    train_labels[idx] = labels
    test_insts[idx] = files
    test_labels[idx] = labels

    _,class_dist = np.unique(labels,return_counts=True)

    print(min(class_dist)/sum(class_dist))
    if mod:
      
      if alpha is None:
        continue

      if min(class_dist)/sum(class_dist) < alpha:
        train_insts[idx] = files
        train_labels[idx] = labels
        print(np.unique(train_labels[idx],return_counts=True))
        train_insts[idx], train_labels[idx] = sampler.fit_resample(np.squeeze(files), labels) 
        train_insts[idx] = np.expand_dims(train_insts[idx],1)
        print(np.unique(train_labels[idx],return_counts=True))

        #debugging
      # print(np.shape(train_insts[idx]))

    # debugging
    # print(np.unique(train_labels[idx],return_counts=True),np.unique(test_labels[idx],return_counts=True))
  

  return  data_names, train_insts, train_labels, test_insts, test_labels  

def multi_data_loader(source_insts, source_labels, batch_size, shuffle = True):

  input_sizes = [ v.shape[0] for k,v in source_insts.items()]
  max_input_size = max(input_sizes)
  min_input_size = min(input_sizes)
  replace_ = False
  if min_input_size < batch_size:
    replace_ = True #cant have batches bigger than smallest site
  num_domains = len(input_sizes)

  if shuffle:
    for i,key in enumerate(source_insts.keys()):
      r_order = np.arange(input_sizes[i])
      np.random.shuffle(r_order)
      source_insts[key], source_labels[key] = source_insts[key][r_order], source_labels[key][r_order] 
  

  
  num_blocks = max_input_size // batch_size

  for j in range(num_blocks):
    xs, ys = [], []
    for i,key in enumerate(source_insts.keys()):
      ridx = np.random.choice(input_sizes[i], batch_size, replace = replace_)
      xs.append(source_insts[key][ridx])
      ys.append(source_labels[key][ridx])
    yield xs, ys



def add_site_info(train_insts, train_labels, test_insts, test_labels):
  num_sites = len(train_insts.keys())

  for key in train_insts.keys():
    
    loc = np.ones(train_insts[key].shape[0],dtype=int)*int(key)
    site_info = np.expand_dims(np.eye(num_sites)[loc],1)
    train_insts[key] = np.append(train_insts[key],site_info,axis = 2)
    
    loc = np.ones(test_insts[key].shape[0],dtype=int)*int(key)
    site_info = np.expand_dims(np.eye(num_sites)[loc],1)
    test_insts[key] = np.append(test_insts[key],site_info,axis = 2)
  
  return train_insts, train_labels, test_insts, test_labels
    
