from transformation import Transformation
from os import listdir, getcwd
import pandas as pd
from sklearn.model_selection import train_test_split
from hyper_parameter import Tuning
from pickle import dump
import logger

log = logger.Logging("Training")


class Training:
    def __init__(self):
        self.transform = Transformation()
        self.hyperparam = Tuning()

    def train(self):
        try:
            log.log("Started Training")
            if "master.csv" in listdir(getcwd()):
                print("Already Transformed")
                df = pd.read_csv("master.csv")
            else:
                print("Doing Data Processing to make master csv")
                self.transform.data_scaling()
                df = pd.read_csv("master.csv")

            df.drop(columns=["Unnamed: 0"], inplace=True)
            x = df.drop(columns='rate')
            y = df.rate
            log.log("Splitting Dataset")
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=30)
            log.log("Started Initializing models")
            model_details = self.hyperparam.initialize_model()
            log.log("Finished Initializing models")
            log.log("Starting best Model search")
            response = self.hyperparam.find_best_model(x_train,y_train, model_details)
            log.log("Finished Model search")
            best_model = None
            best_score = 0
            for data in response:
                if data['best_score'] > best_score:
                    best_score = data['best_score']
                    best_model = data['best_model']
            print(best_score, best_model)
            log.log("Saving best model")
            self.save_model(best_model)
        except Exception as e:
            log.log("Error while training")
            print(str(e))

    def save_model(self, model, path=None):
        try:
            if path is None:
                dump(model, open("model.pkl", "wb"))
            else:
                dump(model, open(f'{path}.pkl', 'wb'))
        except Exception as e:
            log.log("Error in save_model method")
            raise(e)

if __name__=='__main__':
    train = Training()
    train.train()