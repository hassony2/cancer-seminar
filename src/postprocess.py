def write_predictions(prediction_dic, result_path):
    """
    writes result to csv in kaggle format
    """
    with open(result_path, 'wb') as outfile:
        outfile.write(bytes('Patient_ID,HPV/p16_status\n', 'UTF-8'))
        for patient_id, pred in prediction_dic.items():
            outfile.write(bytes(str(patient_id) + ',' + str(pred) + '\n', 'UTF-8'))
                    
