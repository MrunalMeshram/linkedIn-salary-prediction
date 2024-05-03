from flask import Flask, request, jsonify, render_template
import psycopg2
import pandas as pd
from joblib import dump, load

app = Flask(__name__)
loaded_model = load('salary_pred_model_new.joblib')

conn = psycopg2.connect(database="Linkedin_data",
                        host="pg-1f35c88a-mrunal.f.aivencloud.com",
                        user="avnadmin",
                        password="AVNS_vSd06WgTYUnr3Wqzk00",
                        port="25762")


# Open a cursor to perform database operations
cur = conn.cursor()
get_all_data = "SELECT * FROM linkedin_cleaned_data;"
companies_data=pd.read_sql_query(get_all_data, conn)
cur.close()
conn.close()
print(companies_data)

@app.route("/api/get-result", methods=["POST", "GET"])
def get_result():

    if request.method == "POST":
        data = request.get_json()
        designation = data.get("designation")
        employmentLevel = data.get("employmentLevel")
        employmentType = data.get("employmentType")

        new_data = pd.DataFrame({
            'designation': [f'{designation}'],
            'level': [f'{employmentLevel}'],
            'emp_type': [f'{employmentType}']
            })
        print(designation, employmentLevel, employmentType)

        # filtered_data = companies_data.loc[
        #     (companies_data['designation'] == designation) &
        #     (companies_data['level'] == employmentLevel) &
        #     (companies_data['emp_type'].isin(employmentType)),
        #     ['designation', 'level', 'emp_type', 'min_salary', 'max_salary']
        #     ]
        # print(filtered_data)
        #print(designation, employmentLevel, employmentType)
        predicted_salary = loaded_model.predict(new_data)
        print("Predicted Salary:", predicted_salary)
        return jsonify({"salary": predicted_salary[0]}), 200
    return jsonify({"result": "GET request"})


@app.route("/")
def home():
    designations = companies_data["designation"].unique()
    employmentLevels = companies_data["level"].unique()
    employmentTypes = companies_data["emp_type"].unique()
    return render_template("home.html", designations=designations, employmentLevels=employmentLevels, employmentTypes=employmentTypes)


if __name__=="__main__":
    app.run(debug=True)


