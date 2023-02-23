from flask import Flask, request
import json
import sqlite3

def connect_to_db():
    conn = sqlite3.connect("./database/hackers.db")
    return conn


app = Flask(__name__)

#=================================================================================
# Creating the database and inserting data



# f = open("./database/HTN_2023_BE_Challenge_Data.json")
# data = json.load(f)
# conn = connect_to_db()
# cursor = conn.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, company TEXT, email TEXT, phone TEXT)")
# cursor.execute("CREATE TABLE IF NOT EXISTS skills(user_id INTEGER, skill TEXT, rating INTEGER, FOREIGN KEY(user_id) REFERENCES users(id))")

# for row in data:
#     skills = json.dumps(row["skills"])
#     cursor.execute("INSERT INTO users(name, company, email, phone, skills) VALUES(?, ?, ?, ?, ?)", (row["name"], row["company"], row["email"], row["phone"], skills))
#     conn.commit()
# cursor.close()

# new solution

# for row in data:
#     cursor.execute("INSERT INTO users(name, company, email, phone) VALUES(?, ?, ?, ?)", (row["name"], row["company"], row["email"], row["phone"]))
#     conn.commit()

# index = 1
# for row in data:
#     for skill in row["skills"]:
#         cursor.execute("INSERT INTO skills(user_id, skill, rating) VALUES(?, ?, ?)", (index, skill["skill"], skill["rating"]))
#         conn.commit()
#     index = index + 1
#=================================================================================

# API

# route: /users
# type: GET
# purpose: gets the information of all hackers in the database
@app.route("/users")
def get_users():
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        for i in rows:
            user = {}
            user["name"] = i["name"]
            user["company"] = i["company"]
            user["email"] = i["email"]
            user["phone"] = i["phone"]
            user["skills"] = []
            cur.execute("SELECT skill,rating FROM skills WHERE skills.user_id = ?", (i["id"],))
            skills = cur.fetchall()
            for j in skills:
                new_skill = {}
                new_skill["skill"] = j["skill"]
                new_skill["rating"] = j["rating"]
                user["skills"].append(new_skill)
            users.append(user)

    except:
        users = []
        return users, 400

    return users, 200


# route: /users/<id>
# type: GET
# purpose: gets the information of a specific user, identified by a unique id
@app.route("/users/<id>")
def get_user(id):
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE users.id = ?", (id,))
        row = cur.fetchone()
        res = {}
        res["name"] = row["name"]
        res["company"] = row["company"]
        res["email"] = row["email"]
        res["phone"] = row["phone"]
        res["skills"] = []
        cur.execute("SELECT skill,rating FROM skills WHERE skills.user_id = ?", (id,))
        skills = cur.fetchall()
        for j in skills:
            new_skill = {}
            new_skill["skill"] = j["skill"]
            new_skill["rating"] = j["rating"]
            res["skills"].append(new_skill)
        return res, 200
    except:
        return {}, 400




def update_data(key, value, id):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(f'UPDATE users SET {key} = ? WHERE users.id = ?', (value, id))
    conn.commit()

def update_skills(skill, id):
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT skill,rating FROM skills WHERE skills.user_id = ?", (id,))
    row = cur.fetchall()
    for s in row:
        if s["skill"] == skill["skill"]:
            cur.execute("UPDATE skills SET rating = ? WHERE skills.user_id = ? AND skills.skill = ?", (skill["rating"], id, skill["skill"]))
            conn.commit()
            return 
    cur.execute("INSERT INTO skills(user_id, skill, rating) VALUES(?, ?, ?)", (id, skill["skill"], skill["rating"]))
    conn.commit()
    

# route: /users/<id>
# type: PUT
# purpose: updates information of a specific user, identified by a unique id
@app.route("/users/<id>", methods = ['PUT'])
def update_user(id):
    res = {}
    try:
        change = request.get_json()
        try:
            name = change["name"]
            update_data("name", name, id)
        except:
            name=""
        try:
            email = change["email"]
            update_data("email", email, id)
        except:
            email=""
        try:
            company = change["company"]
            update_data("company", company, id)
        except:
            company=""
        try:
            phone = change["phone"]
            update_data("phone", phone, id)
        except:
            phone=""
        try:
            skill = change["skills"]
            update_skills(skill, id)
        except: 
            res["skills"] = ""
    except:
        # conn.rollback()
        return {}, 400
    return get_user(id)



# route: /skills/
# type: GET
# purpose: provides the number of users with a particular skill, can be filtered with parameters
@app.route("/skills/")
def aggregate_skills():
    min_freq = int(request.args.get("min_frequency"))
    max_freq = int(request.args.get("max_frequency"))
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT skill, COUNT(skill) FROM skills GROUP BY skill HAVING COUNT(skill)<=? AND COUNT(skill)>=? ORDER BY COUNT(skill) ASC", (max_freq, min_freq))
    skills = cur.fetchall()
    res = []
    for skill in skills:
        res.append({"skill": skill[0], "frequency": skill[1]})

    return res, 200


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000, host='0.0.0.0')