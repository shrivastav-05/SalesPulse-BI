from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Load the trained Decision Tree Pipeline
model = joblib.load("sales_return_prediction_model.pkl")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    # Get data from HTML form
    input_data = pd.DataFrame({
        "Order_Date": [request.form["Order_Date"]],
        "Gender": [request.form["Gender"]],
        "Age": [int(request.form["Age"])],
        "City": [request.form["City"]],
        "State": [request.form["State"]],
        "Region": [request.form["Region"]],
        "Category": [request.form["Category"]],
        "Sub_Category": [request.form["Sub_Category"]],
        "Brand": [request.form["Brand"]],
        "Quantity": [int(request.form["Quantity"])],
        "Unit_Price": [float(request.form["Unit_Price"])],
        "Discount_Percent": [float(request.form["Discount_Percent"])],
        "Sales": [float(request.form["Sales"])],
        "Cost": [float(request.form["Cost"])],
        "Profit": [float(request.form["Profit"])],
        "Payment_Method": [request.form["Payment_Method"]],
        "Sales_Channel": [request.form["Sales_Channel"]],
        "Sales_Person": [request.form["Sales_Person"]],
        "Customer_Type": [request.form["Customer_Type"]]
    })

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Get probability
    probability = model.predict_proba(input_data)[0][1]

    # Convert prediction into readable result
    if prediction == 1:
        result = "Returned"
    else:
        result = "Not Returned"

    # Send result back to HTML
    return render_template(
        "index.html",
        prediction=result,
        probability=round(probability * 100, 2)
    )


if __name__ == "__main__":
    app.run(debug=True)