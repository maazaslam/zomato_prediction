from flask import Flask, render_template, request
from flask_cors import CORS
import training
from pickle import load
import mongodb
import numpy as np
from os import getcwd

#Getting feature transformed data from database
mongodb = mongodb.MongoDBOperation()
cuisine_transform = mongodb.get_records("Training", "cuisines")
rest_type_transform = mongodb.get_records("Training", "rest_type")
type_transform = mongodb.get_records("Training", "type")

app = Flask(__name__)
cors = CORS(app)

with open("model.pkl", "rb") as file:
    model = load(file)
with open("scaler.pkl", "rb") as file:
    scaled = load(file)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["GET","POST"])
def predict():
    if request.method=="POST":
        online_order = request.form.get("Online Order")
        if online_order == "Yes":
            online_order= 1
        else:
            online_order=2

        book_table = request.form.get("Book Table")
        if book_table == "Yes":
            book_table=1
        else:
            book_table=2

        votes = request.form.get("Votes")

        rest_type = request.form.get("Restaurant Type")
        if rest_type in rest_type_transform.keys():
            rest_type = rest_type_transform[rest_type]
        else:
            rest_type = 0

        dish_liked = request.form.get("Dishes Liked")

        cuisines = request.form.get("Cuisines")
        if cuisines in cuisine_transform.keys():
            cuisines = cuisine_transform[cuisines]
        else:
            cuisines = 0
        cost = request.form.get("Cost")

        type = request.form.get("Type")
        if type in type_transform.keys():
            type = type_transform[type]
        else:
            type = 0

        input = [[online_order,book_table,votes,rest_type,dish_liked,cuisines,cost,type]]

        scaled_data = scaled.transform(np.array(input))
        output = model.predict(scaled_data)
        rating = f"Rating for the Restaurant is: {output[0]:.2f}"
        return render_template("index.html", prediction_text=rating)

if __name__=="__main__":
    app.run(debug=True)

    # Creating model pickle file if doesn't exist
    if "model.pkl" not in getcwd():
        # initializing Training Object
        train = training.Training()
        train.train()

