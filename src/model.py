import numpy as np
import torch

from src import patient


def make_train_test_lists(pos_patients, neg_patients):
    """
    If needed make the number of patients even
    @return training_set and test_set with same number of positive and negative patients
    """
    if(len(pos_patients) % 2 != 0):
        pos_patients = pos_patients[:-1]
    if(len(neg_patients) % 2 != 0):
        neg_patients = neg_patients[:-1]
    split_pos = np.split(np.random.permutation(pos_patients), 2)
    split_neg = np.split(np.random.permutation(neg_patients), 2)

    training_set = list(split_pos[0]) + list(split_neg[0])
    test_set = list(split_pos[1]) + list(split_neg[1])
    return training_set, test_set


def list_to_tensor(tensor_list):
    """
    Turns a list of tensors into one big tensor
    list's tensors are concatenated on the first dimension
    """
    tensor_nb = len(tensor_list)
    tensor_shape = tensor_list[0].numpy().shape
    tensor = torch.Tensor(np.zeros([tensor_nb, 1] + list(tensor_shape)))
    for idx in range(len(tensor_list)):
        tensor[idx, 0,] = tensor_list[idx]
    return tensor

def create_patch_target(patient_list, patient_patches, patient_df):
    """
    Get all patches as list of tensors and targets as list
    @patient_list contains the list of patients
    @patient_patches is the dictionnary with all patients id as key and patches as values
    @patient_df is the dataframe that contains all patient's info
    """
    all_patches = []
    all_targets = []
    for hpv_patient in patient_list:
        patches = torch.Tensor(patient_patches[hpv_patient])
        tumor_rec = patient.get_hpv_status(patient_df, hpv_patient)
        if(len(patches)):
            nb_patch = patches.numpy().shape[0]
            for idx_patch in range(nb_patch):
                all_patches.append(patches[idx_patch,:,:])
                all_targets.append(tumor_rec)
    return all_patches, all_targets         


def get_mean_patch(train_patches):
    train_patches_tensor = list_to_tensor(train_patches)
    mean_patch = torch.mean(train_patches_tensor, 0)
    return mean_patch[0,0,:,:]

def remove_to_balance(patches, targets, disp=False):
    """
    Returns the list of indexes of patches to remove to obtain a balanced data set
    """
    # Make copies for safety
    patches = patches[:]
    targets = targets[:]

    all_pos_indexes = np.where(np.asarray(targets) == 1)[0]
    all_neg_indexes = np.where(np.asarray(targets) == 0)[0]

    if(disp):
        # Display number of positive and negative patches
        print('{pos_nb} positive patches'.format(pos_nb=len(all_pos_indexes)))
        print('{neg_nb} negative patches'.format(neg_nb=len(all_neg_indexes)))
    if(len(all_neg_indexes) > len(all_pos_indexes)):
        indexes_to_remove = np.random.choice(all_neg_indexes, len(all_neg_indexes) - len(all_pos_indexes), replace=False)
    else:
        indexes_to_remove = np.random.choice(all_pos_indexes, len(all_pos_indexes) - len(all_neg_indexes), replace=False)
    patches = np.delete(patches, indexes_to_remove)
    targets = np.delete(targets, indexes_to_remove)
    return patches, targets 

def create_balanced_tensors(train_targets, train_patches, disp=False):
    """
    creates balanced dataset with same number of positive and negative samples
    """
    train_targets = train_targets[:]
    train_patches = train_patches[:]
    # Balance dataset
    train_patches, train_targets = remove_to_balance(train_patches, train_targets, disp=disp)

    train_targets = [torch.Tensor([int(tumor_rec), 1 - int(tumor_rec)]) for tumor_rec in train_targets]
    train_targets = list_to_tensor(train_targets)
    train_patches = list_to_tensor(train_patches)
    return train_targets, train_patches
