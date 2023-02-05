# wtforms
import dbfunctions as db
from flask import Flask,render_template,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import (StringField,SubmitField)
from wtforms.validators import DataRequired
import logging
 

app=Flask(__name__)
app.config['SECRET_KEY']="mysecretkey"
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)



class PetInfoForm(FlaskForm):
    name=StringField("owner name")
    pnum=StringField("Phone Number")
    type=StringField("Pet Type")
    breed=StringField("Pet Breed")
    pname=StringField("pet name")
    submit=SubmitField("Submit")

# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('display'))
    return render_template('login.html', error=error)


@app.route('/register', methods =["GET", "POST"])
def register():
    try:
        
        if request.method == "POST":
        # getting input in HTML form
            name = request.form.get("name")
            pnum= request.form.get("pnum")
            breed= request.form.get("breed")
            atype= request.form.get("animaltype")
            pname=request.form.get("pname")

            db.DbConnection.connect_db()
            tbname="pets"

            """checks if table already exists or not """
            if not db.DbConnection.check_table(tbname):
                db.DbConnection.create_table(tbname,"name","pnum","breed","type","pname")
                
            """inserts form data into table"""
            db.DbConnection.insert_db(tbname,name,pnum,breed,atype,pname)
            db.DbConnection.select_records(tbname)
            db.DbConnection.close_db()

            """" data entered succesfully"""
            return "Your name is "+name+" your phone number is "+str(pnum)+" and your pet name is "+pname+" of type "+atype+" and breed is "+str(breed)

        logger.info(f'Added pet: {pname}')

    except Exception as e:
        logger.error(f'Error registering pet: {e}')

    return render_template("register.html")


@app.route('/display', methods =["GET","POST"])
def display():
    # form=PetInfoForm()
    tbname="pets"
    db.DbConnection.connect_db()
    records=db.DbConnection.select_records(tbname)
    return render_template('display.html',records=records)

@app.route('/edit',methods =["GET","POST"])
def edit():

    try:

        form=PetInfoForm()
        if request.method == "POST":
            name = request.form.get("name")
            pnum= request.form.get("pnum")
            breed= request.form.get("breed")
            atype= request.form.get("animaltype")
            pname=request.form.get("pname")

            db.DbConnection.connect_db()
            db.DbConnection.update_table("pets",name,pnum,breed,atype,pname)
            db.DbConnection.select_records("pets")
            db.DbConnection.close_db()

            return "updated succesfully"

        logger.info(f'Edited pet: {pname}')

    except Exception as e:
        logger.error(f'Error editing pet: {e}')


        
    return  render_template("edit.html",form=form)

@app.route('/delete',methods =["GET","POST"])
def delete():

    try:
        form=PetInfoForm()
        name = request.form.get("name")
        pname= request.form.get("pname")
        if request.method == "POST":
                db.DbConnection.connect_db()
                db.DbConnection.delete_record("pets",name)
                db.DbConnection.select_records("pets")
                db.DbConnection.close_db()
                return "deleted succesfully"

        logger.info(f'Deleted pet: {pname}')

    except Exception as e:
        logger.error(f'Error deleting pet: {e}')

        
    return  render_template("delete.html",form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__=='__main__':
   app.run(debug=True)