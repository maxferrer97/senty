from flask import Flask, render_template, json, request, redirect
from flask.ext.mysql import MySQL
from ScoreCalculate import scoreCalculate
import twitterSentiment
# from werkzeug import generate_password_hash, check_password_hash
app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Snakee667!' # put your sql password here
app.config['MYSQL_DATABASE_DB'] = 'project'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
     return(render_template('Senty.html'))

@app.route("/",methods=['POST'])
def score():

    print('here')
    conn = mysql.connect()
    cur = conn.cursor()
    twitterScore = twitterSentiment.main()
    newticker = request.form['ticker']
    uID = 1

    newscore = scoreCalculate(newticker)
    cur.execute("INSERT INTO scores (ticker,score,twitterScore, user_ID) VALUES (%s, %s, %s, %s)", (newticker, newscore, twitterScore, uID))
    print('added')
    conn.commit()
    cur.close()

    return redirect('/')

@app.route('/signIn')
def showSignIn():
    return(render_template('LogIn.html'))


@app.route('/showSignUp')
def showSignUp():
    return(render_template('signup.html'))


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    # still need to create signup class and transfer below code to new file
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            conn = mysql.connect()
            cur = conn.cursor()
            cur.callproc('sp_createUser',(_name,_email,_password,))
            print "Registered"
            data = cur.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cur.close() 
        conn.close()


if __name__ == "__main__":
    app.run()

def main():
    return(render_template('Senty.html'))


@app.route('/signIn')
def showSignIn():
    return(render_template('LogIn.html'))


@app.route('/showSignUp')
def showSignUp():
    return(render_template('signup.html'))


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    # need to create signup class and transfer code to new file
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            conn = mysql.connect()
            cur = conn.cursor()
            cur.callproc('sp_createUser',(_name,_email,_password,))
            print "Registered"
            data = cur.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cur.close() 
        conn.close()


if __name__ == "__main__":
    app.run()
