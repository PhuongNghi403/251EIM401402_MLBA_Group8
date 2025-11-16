from flask import Flask, render_template, request
from FileUtil import FileUtil 
app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')

@app.route("/")
def main():
    return render_template("index.html")
@app.route("/doprediction", methods=['GET','POST'])
def doprediction():
    area_income_value = float(request.form['area_income_value'])
    area_house_age_value = float(request.form['area_house_age_value'])
    area_number_of_rooms_value = float(request.form['area_number_of_rooms_value'])
    area_number_of_bedrooms_value = float(request.form['area_number_of_bedrooms_value'])
    area_population_value = float(request.form["area_population_value"])
    trainedModel = FileUtil.loadmodel('housingmodel_2024-07-15_13-30-34.zip')
    result = trainedModel.predict([[area_income_value,
                                    area_house_age_value,
                                    area_number_of_rooms_value,
                                    area_number_of_bedrooms_value,
                                    area_population_value]])
    return f"{result[0]}"
if __name__ == "__main__":
    app.run(host="localhost", port=9500, debug=True)