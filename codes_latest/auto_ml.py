from supervised.automl import AutoML # mljar-supervised
import pandas as pd

def merge_pred(test, predictions, name, target_cols):
    pred_df = pd.DataFrame(predictions, columns=target_cols)
    
    concatenated_df = pd.concat([test, pred_df], axis=1)
    concatenated_df.to_csv("{}_submission.csv".format(name), index=False)
    
train = pd.read_csv("/home/hpc/iwso/iwso092h/mycodedir/Allergen/work_data/train_encoded.csv")
test = pd.read_csv("/home/hpc/iwso/iwso092h/mycodedir/Allergen/work_data/test_encoded.csv")
target_knn = pd.read_csv("/home/hpc/iwso/iwso092h/mycodedir/Allergen/work_data/target_knn.csv")
target_ir = pd.read_csv("/home/hpc/iwso/iwso092h/mycodedir/Allergen/work_data/target_ir.csv")
test_ori = pd.read_csv("/home/hpc/iwso/iwso092h/mycodedir/Allergen/work_data/test.csv")

train_no9 = pd.read_csv("/home/hpc/iwso/iwso092h/mycodedir/Allergen/work_data/train_encoded_9s_dropped.csv")
test_no9 = pd.read_csv("/home/hpc/iwso/iwso092h/mycodedir/Allergen/work_data/test_encoded_9s_dropped.csv")
target_no9 = pd.read_csv("/home/hpc/iwso/iwso092h/mycodedir/Allergen/work_data/target_9s_dropped.csv")

target_cols = target_knn.columns

automl_knn = AutoML(mode="Compete", results_path="/home/woody/iwso/iwso092h/Allgern/models_knn",
                eval_metric = "f1")
automl_ir = AutoML(mode="Compete", results_path="/home/woody/iwso/iwso092h/Allgern/models_ir",
                eval_metric = "f1")
automl_no9 = AutoML(mode="Compete", results_path="/home/woody/iwso/iwso092h/Allgern/models_no9",
                eval_metric = "f1")
automl_no9_optuna = AutoML(mode="Optuna", results_path="/home/woody/iwso/iwso092h/Allgern/models_no9_optuna",
                eval_metric = "f1")

automl_knn.fit(train, target_knn)
automl_ir.fit(train, target_ir)
automl_no9.fit(train_no9, target_no9)
automl_no9_optuna.fit(train_no9, target_no9)

predictions_knn = automl_knn.predict(test)
predictions_ir = automl_ir.predict(test)
predictions_no9 = automl_no9.predict(test_no9)
predictions_no9_optuna = automl_no9_optuna.predict(test_no9)

merge_pred(test_ori, predictions_knn, "knn", target_cols)
merge_pred(test_ori, predictions_ir, "ir", target_cols)
merge_pred(test_ori, predictions_no9, "dropped_9s", target_cols)
merge_pred(test_ori, predictions_no9_optuna, "dropped_9s_optuna", target_cols)