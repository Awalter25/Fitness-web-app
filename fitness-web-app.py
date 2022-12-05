# fitness web app.py

from flask import Flask, request, render_template

app = Flask(__name__)

def calculate_bmr(weight, height, age, sex, activity_level, units):
  # Convert the user's weight and height to the appropriate units (kg and cm for metric, lb and in for imperial)
  if units == "metric":
    weight_in_kg = weight
    height_in_cm = height
  else:
    weight_in_kg = weight * 0.453592
    height_in_cm = height * 2.54

  # Calculate the basal metabolic rate (BMR) based on the user's weight, height, age, and sex
  if sex == "male":
    bmr = 66 + (6.23 * weight_in_kg) + (12.7 * height_in_cm) - (6.8 * age)
  else:
    bmr = 655 + (4.35 * weight_in_kg) + (4.7 * height_in_cm) - (4.7 * age)
  
  # Adjust the BMR based on the user's activity level
  if activity_level == "sedentary":
    bmr *= 1.2
  elif activity_level == "lightly active":
    bmr *= 1.375
  elif activity_level == "moderately active":
    bmr *= 1.55
  elif activity_level == "very active":
    bmr *= 1.725
  else:
    bmr *= 1.9

  return bmr

@app.route("/", methods=["GET", "POST"])
def home():
  if request.method == "POST":
    # Get the user's input from the form
    weight = float(request.form["weight"])
    height = float(request.form["height"])
    age = int(request.form["age"])
    sex = request.form["sex"]
    activity_level = request.form["activity_level"]
    units = request.form["units"]

    # Calculate the suggested amount of calories to maintain weight, gain 1 pound per week, gain 2 pounds per week, lose 1 pound per week, and lose 2 pounds per week
    bmr = calculate_bmr(weight, height, age, sex, activity_level, units)
    maintain_weight = bmr
    gain_1_pound = bmr + 500
    gain_2_pounds = bmr + 1000
    lose_1_pound = bmr - 500
    lose_2_pounds = bmr - 1000

    return render_template("results.html", maintain_weight=maintain_weight, gain_1_pound=gain_1_pound, gain_2_pounds=gain_2_pounds, lose_1_pound=lose_1_pound, lose_2_pounds=lose_2_pounds)
