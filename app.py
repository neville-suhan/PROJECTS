from flask import Flask, render_template, session, request, url_for, flash, redirect
import pickle
import pandas as pd
import numpy as np 
from supabase_config import supabase
from hashlib import sha256


# create a object for the class flask 
app=Flask(__name__)
app.secret_key='1234'









# # create main function 
# if __name__=='__main__':
#     app.run(debug=True,port=4007)  #different ports for different projects
    



# loading the model 
with open('ipl.pkl','rb') as f:
    model=pickle.load(f)
    


def hash_password(password):
      return sha256(password.encode()).hexdigest()


# prediction logic 
# create a function for prediction
def predict_score(bat_team='Mumbai Indians',bowl_team='Delhi Daredevils',runs=120,wickets=4,
                 overs=6.2,runs_last_5=33,wickets_last_5=1):
    temp_array=list()
    if bat_team=='Chennai Super Kings':
        temp_array=temp_array+[1,0,0,0,0,0,0,0]

    elif bat_team=='Delhi Daredevils':
        temp_array=temp_array+[0,1,0,0,0,0,0,0]

    elif bat_team=='Kings XI Punjab':
         temp_array=temp_array+[0,0,1,0,0,0,0,0]

    elif bat_team=='Kolkata Knight Riders':
          temp_array=temp_array+[0,0,0,1,0,0,0,0]

    elif bat_team=='Mumbai Indians':
          temp_array=temp_array+[0,0,0,0,1,0,0,0]

    elif bat_team=='Rajasthan Royals':
          temp_array=temp_array+[0,0,0,0,0,1,0,0]

    elif bat_team=='Royal Challengers Bangalore':
          temp_array=temp_array+[0,0,0,0,0,0,1,0]

    elif bat_team=='Sunrisers Hyderabad':
          temp_array=temp_array+[0,0,0,0,0,0,0,1]



    if bowl_team=='Chennai Super Kings':
        temp_array=temp_array+[1,0,0,0,0,0,0,0]

    elif bowl_team=='Delhi Daredevils':
        temp_array=temp_array+[0,1,0,0,0,0,0,0]

    elif bowl_team=='Kings XI Punjab':
         temp_array=temp_array+[0,0,1,0,0,0,0,0]

    elif bowl_team=='Kolkata Knight Riders':
          temp_array=temp_array+[0,0,0,1,0,0,0,0]

    elif bowl_team=='Mumbai Indians':
          temp_array=temp_array+[0,0,0,0,1,0,0,0]

    elif bowl_team=='Rajasthan Royals':
          temp_array=temp_array+[0,0,0,0,0,1,0,0]

    elif bowl_team=='Royal Challengers Bangalore':
          temp_array=temp_array+[0,0,0,0,0,0,1,0]

    elif bowl_team=='Sunrisers Hyderabad':
          temp_array=temp_array+[0,0,0,0,0,0,0,1]

    temp_array=temp_array+[runs,wickets,overs,runs_last_5,wickets_last_5]


    # converting to numpy array
    temp_array=np.array([temp_array])


    # prediction
    return int(model.predict(temp_array)[0])













@app.route('/')
def index():
      if 'user_id' not in session:
            return redirect(url_for("login"))
    
      return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
      if request.method=='POST':
            name=request.form.get('name')
            email=request.form.get('email')
            password=request.form.get('password')
            
            existing=supabase.table("users").select("*").eq("email",email).execute()
            
            if existing.data:
                  flash("Email already exists","error")
                  return redirect(url_for("register"))
            
            hashed_password=hash_password(password)
            supabase.table("users").insert({
                  "uname":name,
                  "email":email,
                  "password":hashed_password
                  
            }).execute()
            flash("Register Successful","success")
            return redirect(url_for("login"))
      return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
      if request.method=='POST':
           
            email=request.form.get('email')
            password=request.form.get('password')
            
            response=supabase.table("users").select("*").eq("email",email).execute()
            user=None
            if response.data:
                  user=response.data[0]
                  if user and hash_password(password)==user['password']:
                        session['user_id']=user['uid']
                        session['username']=user['uname']
                        session['email']=user['email']
                        flash("Login successfull","success")
                        return redirect(url_for("index"))
                  else:
                        flash("Invalid Email or Password","error")
                        return redirect(url_for("login"))
            

      return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method=='POST':
          bat_team=request.form.get('bat_team')
          bowl_team=request.form.get('bowl_team')
          runs=int(request.form.get('runs'))
          wickets=int(request.form.get('wickets'))
          overs=float(request.form.get('overs'))
          runs_last_5=int(request.form.get('runs_last_5'))
          wickets_last_5=int(request.form.get('wickets_last_5'))
          
          
          
          score=predict_score(bat_team=bat_team,bowl_team=bowl_team,runs=runs,wickets=wickets,
                 overs=overs,runs_last_5=runs_last_5,wickets_last_5=wickets_last_5)
          
          return render_template('predict.html',prediction=score)
          
          
          
          
          

    return render_template('predict.html')






# create main function 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)#different ports for different projects
    

