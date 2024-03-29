import sys
import logging

import numpy as np
from collections import Counter

class OverSampler():

  def __init__(self,sampling = None):
    self.alpha = sampling
  
  def fit_resample(self, x, y):
    self.x = x
    self.y = y

    labels,label_counts = np.unique(self.y,return_counts = True)
    zero_idxs = np.where(self.y == labels[0])[0]
    ones_idxs = np.where(self.y == labels[1])[0]
    idxs = [zero_idxs ,ones_idxs]
    major_idx = np.argmax(label_counts)
    # print(major_idx,label_counts[major_idx])
    major_idxs = idxs[major_idx]
    minor_idxs = idxs[(major_idx + 1)%2]

    minor_size = len(minor_idxs)
    major_size = len(major_idxs)
    if self.alpha is None:
      new_idxs = np.random.choice(minor_idxs,int(major_size - minor_size),replace = True)
    
    else:
      sizes = int((-self.alpha*(major_size + minor_size) + major_size)/(self.alpha))
      if sizes <=0:
        return self.x,self.y
      # print(minor_idxs,sizes)
      new_idxs = np.random.choice(minor_idxs,int(sizes), replace = True)
    
    new_xs, new_ys = self.x[new_idxs], self.y[new_idxs]
    # print(np.shape(self.x),np.shape(self.y),np.shape(new_xs),np.shape(new_ys))
    self.x = np.append(self.x,new_xs,axis = 0)
    self.y = np.append(self.y,new_ys,axis = 0)
    return self.x, self.y


    
def get_logger(filename):
    # Logging configuration: set the basic configuration of the logging system
    log_formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)-5.5s] %(message)s',
                                      datefmt='%Y-%b-%d %H:%M')
    logger = logging.getLogger()
    if logger.hasHandlers():
      print('clearing logger handlers')
      logger.handlers.clear()
      
    # if not logger.hasHandlers():
    logger.setLevel(logging.DEBUG)
    # File logger
    print('adding file handler')
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    # Stderr logger
    std_handler = logging.StreamHandler(sys.stdout)
    std_handler.setFormatter(log_formatter)
    std_handler.setLevel(logging.DEBUG)
    logger.addHandler(std_handler)
    print(logger.handlers)
    return logger


# Helpers for MDMN
def np_softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)


def np_sigmoid(x):
    """Numerically stable sigmoid function."""
    y = np.zeros_like(x, dtype=np.float32)
    y[x >= 0] = 1. / (1. + np.exp(-x[x >= 0]))
    y[x < 0] = np.exp(x[x < 0]) / (1. + np.exp(x[x < 0]))
    return y


def get_mask(d):  # d is batch x num_domain (one-hot)
    masks = np.zeros((d.shape[0], d.shape[1]), dtype=np.float32)
    for i in range(d.shape[1]):
        sum_d = max(np.sum(d[:, i]), 1)  # at least one sample for that domain i
        masks[:, i] = d[:, i] / sum_d
    return masks


def get_fspecific_domain_weights(d, pred, target_idx):
    masks = get_mask(d)  # compute average mask
    num_domains = d.shape[1]
    fdomain_weights = np.zeros((num_domains,), dtype=np.float32)
    for i in range(num_domains):
        if pred is None:
            fdomain_weights[i] = 1.
        else:
            # this is E_{D_s} f_s - E_{D_/s} f_s
            fdomain_weights[i] = np.sum((masks[:, i] - masks[:, target_idx]) * pred)
    fdomain_weights = np_sigmoid(fdomain_weights)  # this seems to be different from the paper...
    fdomain_weights[target_idx] = 1
    return fdomain_weights.astype('float32')


def compute_weights(d, pred, batch_size):
    # print(np.shape(d),np.shape(pred))
    num_domains = d.shape[1]
    num_tot_sample = num_domains * batch_size

    domain_weights = np.zeros((num_domains, num_domains), dtype=np.float32)
    for i in range(num_domains):
        domain_weights[:, i] = get_fspecific_domain_weights(d, pred[:, i], i)
        # Note: the i has weight 1, others have sigmoid weights

    f_weights = np.zeros((num_domains,), dtype=np.float32)
    for i in range(num_domains):
        temp = np.repeat(np.reshape(domain_weights[:, i], (1, num_domains)), num_tot_sample, axis=0)
        masks = get_mask(d)
        masks[:, i] = -masks[:, i]
        temp = np.sum(temp * masks, axis=1)
        f_weights[i] = np.sum(temp * pred[:, i].reshape(-1))  # why reshape?
    t_idx = -1
    f_weights[t_idx] = -1000
    f_weights = np_softmax(f_weights)
    f_weights[t_idx] = 1

    weights = np.zeros(d.shape, dtype=np.float32)
    for i in range(num_domains):
        domain_weights_repeat = np.repeat(np.reshape(domain_weights[:, i], (1, num_domains)),
                                          num_tot_sample, axis=0)
        masks = get_mask(d)
        masks[:, i] = -masks[:, i]
        temp = d * masks * domain_weights_repeat
        weights[:, i] = f_weights[i] * np.sum(temp, axis=1)

    return weights, f_weights[:-1]


# MSDA helper based on the paper
# https://github.com/VisionLearningGroup/VisionLearningGroup.github.io/blob/master/M3SDA/code_MSDA_digit/metric/msda.py
def msda_regulizer(features_s, features_t, moment_order=4):

    def euclidean(x1, x2):
        return ((x1 - x2) ** 2).sum().sqrt()

    n_domains = len(features_s)
    moment_reg = 0.
    features_power_s, features_power_t = list(features_s), features_t
    for k in range(moment_order):
        # compute moment difference then multiply to get the next moment
        for d1 in range(n_domains):
            moment_reg = moment_reg + euclidean(features_power_t.mean(0),
                                                features_power_s[d1].mean(0))
            for d2 in range(d1 + 1, n_domains):
                moment_reg = moment_reg + euclidean(features_power_s[d1].mean(0),
                                                    features_power_s[d2].mean(0))
            features_power_s[d1] = features_power_s[d1] * features_s[d1]
        features_power_t = features_power_t * features_t

    return moment_reg


def reset_optimizers(*optimizers):
    for optimizer in optimizers:
        optimizer.zero_grad()


def step_optimizers(*optimizers):
    for optimizer in optimizers:
        optimizer.step()


def msda_train_step(model, xs, ys, tinputs, opt_G, opt_C1, opt_C2):

    # first step: joint opt
    reset_optimizers(opt_G, opt_C1, opt_C2)
    task_loss, disc_loss = model(xs, ys, tinputs)
    task_loss.backward()
    step_optimizers(opt_G, opt_C1, opt_C2)

    # second step: fixed G to make C1 & C2 different
    reset_optimizers(opt_G, opt_C1, opt_C2)
    task_loss, disc_loss = model(xs, ys, tinputs)
    loss = task_loss - disc_loss
    loss.backward()
    step_optimizers(opt_C1, opt_C2)

    # third step: opt G
    reset_optimizers(opt_G, opt_C1, opt_C2)
    task_loss, disc_loss = model(xs, ys, tinputs)
    disc_loss.backward()
    opt_G.step()

    return task_loss

def set_configs(input_dim, src_dom_num):

  # configs = {
  #       "input_dim" : input_dim,
  #       "channels" : 1,
  #       "conv_layers" : [4, 8],
  #       "cls_fc_layers" :[2048, 1024],
  #       "dom_fc_layers" : [2048, 2048],
  #       "num_classes" : 2,
  #       "drop_rate" : 0.5,
  #       "mode" : "L2",
  #       }
  
  configs = {
        "input_dim": input_dim,
        "hidden_layers": [2000,1000],
        "num_classes": 2,
        "drop_rate": 0.5,
        "moments" : 1
        }


  return configs