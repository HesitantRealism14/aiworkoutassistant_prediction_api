#libraries
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score

#in case that unstable performance would occur
np.random.seed(100)

class Trainer():

    def __init__(self,X,y):
        self.X = X
        self.y = y
        # self.experiment_name = EXPERIMENT_NAME

    def set_experiment_name(self, experiment_name):
        self.experiment_name = experiment_name

    def split(self):

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=2)

        return X_train, X_test, y_train, y_test

    def run(self):

        model = make_pipeline(StandardScaler(),GradientBoostingClassifier())

        return model

    def evaluate(self,X_test,y_test,model):

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test,y_pred)

        return accuracy

    def save_model(self, model):
        with open("pipeline.pkl", "wb") as file:
            pickle.dump(model, file)

if __name__ == "__main__":
    df = pd.read_csv('raw_data/fitness_poses_csvs_out_basic_5.csv')

    X = df.drop('class', axis=1) # features
    y = df['class'] # target value

    trainer = Trainer(X,y)

    X_train,X_test,y_train,y_test = trainer.split()

    print('Fitting')
    model = trainer.run()
    model.fit(X_train,y_train)

    print('Evaluating')
    acc = trainer.evaluate(X_test,y_test,model)
    print(acc)

    print('Saving')
    trainer.save_model(model)

# import mlflow
# from memoized_property import memoized_property
# from mlflow.tracking import MlflowClient
    # MLFlow methods
    # @memoized_property
    # def mlflow_client(self):
    #     mlflow.set_tracking_uri(MLFLOW_URI)
    #     return MlflowClient()

    # @memoized_property
    # def mlflow_experiment_id(self):
    #     try:
    #         return self.mlflow_client.create_experiment(self.experiment_name)
    #     except BaseException:
    #         return self.mlflow_client.get_experiment_by_name(
    #             self.experiment_name).experiment_id

    # @memoized_property
    # def mlflow_run(self):
    #     return self.mlflow_client.create_run(self.mlflow_experiment_id)

    # def mlflow_log_param(self, key, value):
    #     self.mlflow_client.log_param(self.mlflow_run.info.run_id, key, value)

    # def mlflow_log_metric(self, key, value):
    #     self.mlflow_client.log_metric(self.mlflow_run.info.run_id, key, value)
