import numpy as np

def get_metrics(target, prediction):
    # assert(len(target) == len(prediction), 'target and prediction lists should be of same length')
    sample_nb = len(target)
    confusion_mat = np.zeros([2,2])
    # cast predictions to 0 or 1 in prediction value not binary
    prediction = [1 if pred>0.5 else 0 for pred in prediction]
    true_positives = sum(1 for tar, pred in zip(target, prediction) if (tar and pred)) 
    true_negatives = sum(1 for tar, pred in zip(target, prediction) if (not tar and not pred)) 
    false_positives = sum(1 for tar, pred in zip(target, prediction) if (not tar and pred)) 
    false_negatives = sum(1 for tar, pred in zip(target, prediction) if (tar and not pred))
    confusion_mat[1, 1] = true_positives
    confusion_mat[0, 0] = true_negatives
    confusion_mat[1, 0] = false_positives
    confusion_mat[0, 1] = false_negatives
    accuracy = (true_positives + true_negatives)/sample_nb
    return confusion_mat, accuracy

