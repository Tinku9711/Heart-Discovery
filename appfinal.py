#imports 
import pandas as pd
import json
from pymongo import MongoClient
from pymongo.collection import ObjectId
from flask import Flask, request
app = Flask(__name__)
import pickle

#connection with MongoDB Database
client = MongoClient("mongodb+srv://shash800:thisisapassword@users.wfsvr.mongodb.net/<dbname>?retryWrites=true&w=majority")

db = client.get_database("users")

k = db.userdata

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
    
    
#function to classify user as high mortality or low mortality
classifies = pickle.load(open("modelfinal.pickle", "rb"))
def classify(x):
    return classifies.predict([x])[0]

#register
def register(username, password):
 
    a = k.find_one({"username":username})

    if a == None:
        y = {"username":username, "password":password}
        k.insert_one(y)
        return {"status":"success"}
    else:
        #no duplicate usernames
        return {"status":"failed"}

    
#user adds or updates health data
def add_update_data(username, password, age, anaemia, creatinine, diabetes, ejectionfrac, highbp, platlet, serum_creatinine, serum_sodium, sex, smoking):
        a = k.find_one({"username":username})

        if a == None:
            return {"status":"failed"}
        else:
            if a["username"] == username and a["password"] == password:
                #update the data
                k.update_one({"username":username}, {"$set":{"age":age}})
                k.update_one({"username":username}, {"$set":{"anaemia":anaemia}})
                k.update_one({"username":username}, {"$set":{"creatinine":creatinine}})
                k.update_one({"username":username}, {"$set":{"diabetes":diabetes}})
                k.update_one({"username":username}, {"$set":{"ejectionfrac":ejectionfrac}})
                k.update_one({"username":username}, {"$set":{"highbp":highbp}})
                k.update_one({"username":username}, {"$set":{"platlet":platlet}})
                k.update_one({"username":username}, {"$set":{"serum_creatinine":serum_creatinine}})
                k.update_one({"username":username}, {"$set":{"serum_sodium":serum_sodium}})
                k.update_one({"username":username}, {"$set":{"sex":sex}})
                k.update_one({"username":username}, {"$set":{"smoking":smoking}})
                return {"status":"success"}
            else:
                return {"status":"failed"}

            
#login system
def login(username, password):
    a = k.find_one({"username":username})
    

    if a == None:
        return {"status":"failed"}
    else:
        if a["username"] == username and a["password"] == password:
            #can login
            return {"status":"success"}
        else:
            #can't login
            return {"status":"failed"}


#tips 
def tips(age, anaemia, creatinine, diabetes, ejectionfrac, highbp, platlet, serum_creatinine, serum_sodium, sex, smoking):
    if classify([age, anaemia, creatinine, diabetes, ejectionfrac, highbp, platlet, serum_creatinine, serum_sodium, sex, smoking]) == 1:
        s = ""
        if anaemia == 1:
            s = s + "Anaemia increases the mortality risk through cardiovascular diseases. Here are some remedies for anaemia that you can try: Increase vitamin C intake, consume yogurt with turmeric, eat green vegetables, eat rasins and dates, have soaked sesame seeds with honey. "
        if creatinine > 120:
            s = s + "Your creatinine levels are high. This may affect your mortality risk through cardiovascular diseases. Here are some ways you can reduce your creatinine levels: Avoid taking supplements that contain creatinine, reduce your protein intake, eat more fibre, take Chitosan supplements. "
        if platlet < 150000:
            s = s + "Your platlet count is low. This may affect your mortality risk through cardiovascular diseases. Here are some ways you can increase your platlet count: Eating kale, eggs, green leafy vegetables, liver, meat, cabbage, parsley help increase your platlet count, as well as taking vitamin B-12 supplements. "
        if diabetes == 1:
            s = s + "Diabetes is a major factor that determines your mortality risk through cardiovascular diseases. There is no known cure for diabetes, but here are some ways that you can keep your diabetes under control: Avoid intake of refined carbs and sugar, lower your stress by meditation or relaxation, stay hydrated, increase your fibre intake, exercise regularly. "
        if smoking == 1:
            s = s + "Smoking is a major factor that determines your mortality risk through cardiovascular diseases. You can quit smoking by: Try nicotine replacement therepy, get physical exercise, meditation helps overcome addiction."
        return(s)
    else:
        return("Your mortality risk is low!")


#get requests
@app.route('/register', methods=["GET", "POST"])
def register_endpoint():
    data = request.json

    return JSONEncoder().encode(register(data["username"], data["password"]))

@app.route('/login', methods=["GET", "POST"])
def login_endpoint():
    data = request.json

    return login(data["username"], data["password"])


@app.route('/add_update_data', methods=["GET", "POST"])
def add_update_data_endpoint():
    data = request.json

    return add_update_data(data["username"], data["password"], data["age"], data["anaemia"], data["creatinine"], data["diabetes"], data["ejectionfrac"], data["highbp"], data["platlet"], data["serum_creatinine"], data["serum_sodium"], data["sex"], data["smoking"])


@app.route('/tips', methods=["GET", "POST"])
def tips_endpoint():
    data = request.json

    return JSONEncoder().encode(tips(data["age"], data["anaemia"], data["creatinine"], data["diabetes"], data["ejectionfrac"], data["highbp"], data["platlet"], data["serum_creatinine"], data["serum_sodium"], data["sex"], data["smoking"]))


if __name__ == "__main__":
    app.run()
