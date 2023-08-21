from flask import Flask,request,render_template,jsonify,make_response,redirect,url_for
from flask_restful import Resource, Api,fields,marshal_with,reqparse,abort
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Users(db.Model):
    uid=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String,unique=True,nullable=False)
    #udecks=db.relationship('Decks',backref='user_name')
class Decks(db.Model):
    did=db.Column(db.Integer,primary_key=True,autoincrement=True)
    dname=db.Column(db.String,unique=False,nullable=False)
    duid=db.Column(db.Integer,db.ForeignKey('users.uid'),nullable=False)
    deck_score=db.Column(db.String,nullable=True)

class cards(db.Model):
    card_no=db.Column(db.Integer,primary_key=True,autoincrement=True)
    card_face=db.Column(db.String,unique=False,nullable=False)
    card_back=db.Column(db.String,unique=False,nullable=False)
    dcid=db.Column(db.Integer,db.ForeignKey('decks.did'),nullable=False)
    card_score=db.Column(db.Integer,unique=False,nullable=True)


resource_fields={'user_name':fields.String}
parser1=reqparse.RequestParser()
parser2=reqparse.RequestParser()
parser3=reqparse.RequestParser()
parser1.add_argument('user_name')
parser2.add_argument('deck_name')
parser3.add_argument('card_face')
parser3.add_argument('card_back')
api=Api(app)

class A(Resource):
    @marshal_with(resource_fields)
    def post(self):
        data=parser1.parse_args()
        print(data)
        user_name=data.get('user_name')
        u=Users.query.filter_by(name=user_name).first()
        if(u is not None):
            abort(409,message='User Already exists, Try with Another Name')
        else:
            t=Users(name=user_name)
            db.session.add(t)
            db.session.commit()
            return 'Successfully Created',200

class B(Resource):
  #@marshal_with(resource_fields)
  def get(self,user_name):
    u=Users.query.filter_by(name=user_name).first()
    if(u):
      res=[]
      d=Decks.query.filter_by(duid=u.uid).all()
      print(d)
      for i in d:
        res.append(i.dname)
      print(res)
      return jsonify({'User':u.name , 'List of Decks':res})
    else:
      abort(409,message='User doesnt exist')

  def post(self,user_name):
    u=Users.query.filter_by(name=user_name).first()
    if(u):
      data=parser2.parse_args()
      print(data)
      p = Users.query.filter_by(name=user_name).first()
      if(Decks.query.filter_by(dname=data['deck_name'],duid=p.uid).first()):
        abort(401,message='Deck Already Exists for this user')
      else:
        a=Decks(dname=data['deck_name'],duid=u.uid)
        db.session.add(a)
        db.session.commit()
        return 'Created Successfully',200
    else:
      abort(409,message='User already Exists!')
  
  def put(self,user_name,dname):
    u=Users.query.filter_by(name=user_name).first()
    if(u):
      data=parser2.parse_args()
     #print(data,user_name,dname)
      d=Decks.query.filter_by(dname=dname,duid=u.uid).first()
      #print(d)
      if(d):
        d.dname=data['deck_name']
        db.session.commit()
        print(d.dname)
      else:
        abort(405,message='Deck Doesnot Exist, Update not Possible')
    else:
      abort(409,message='User Doesnot Exist')

  def delete(self,user_name,dname):
    b=Users.query.filter_by(name=user_name).first()
    if(b):
      a=Decks.query.filter_by(dname=dname,duid=b.uid).first()
      if(a):
        c=cards.query.filter_by(dcid=a.did).all()
        for i in c:
            db.session.delete(i)
        db.session.delete(a)
        db.session.commit()
        return 'Deck Deleted Successfully'
      else:
        abort(405,message='Deck doesnot exist')
    else:
      abort(409,message='User Doesnot Exist')





class C(Resource):
  def get(self,dname,user_name):
     u=Users.query.filter_by(name=user_name).first()
     d=Decks.query.filter_by(dname=dname,duid=u.uid).first()
     print(u,d)
     if(u):
      if(d):
        c=cards.query.filter_by(dcid=d.did).all()
        print(c)
        res={}
        fin=[]
        res['card_no']=0
        res['Card Face']=''
        res['Card Back']=''
        res['Deck id']=0
        for i in c:
          res['card_no']=i.card_no
          res['Card Face']=i.card_face
          res['Card Back']=i.card_back
          res['Deck id']=i.dcid
          print(res)
          fin.append(res)
        print(fin)
        return jsonify(fin)
      else:
        abort(405,message='Deck doesnot Exist')

     else:
      abort(409,message='User does not exist')

  def post(self,dname,user_name):
     u=Users.query.filter_by(name=user_name).first()
     if(u):
       d=Decks.query.filter_by(dname=dname,duid=u.uid).first()
       if(d):
         data=parser3.parse_args()
         print(data)
         a=Users.query.filter_by(name=user_name).first()         
         c=cards(card_face=data['card_face'],card_back=data['card_back'],dcid=d.did)
         db.session.add(c)
         db.session.commit()
         return 'Card Successfully Added',200
       else:
          abort(405,message='Deck doesnot exist')
     else:
        abort(409,message='User doesnot exist')

  def put(self,dname,card_no,user_name):
    u=Users.query.filter_by(name=user_name).first()
    if(u):
      d=Decks.query.filter_by(dname=dname,duid=u.uid).first()
      if(d):
        c=cards.query.filter_by(card_no=card_no).first()
        if(c):
          data=parser3.parse_args()
          c.card_face=data['card_face']
          c.card_back=data['card_back']
          db.session.commit()
          return 'Card Updated Successfully',200
        else:
          abort(400,message='Card Number Invalid')
      else:
          abort(405,message='Deck doesnot exist')
    else:
        abort(409,message='User doesnot exist')

  
  def delete(self,dname,card_no,user_name):
    u=Users.query.filter_by(name=user_name).first()
    if(u):
      d=Decks.query.filter_by(dname=dname,duid=u.uid).first()
      if(d):
        c=cards.query.filter_by(card_no=card_no).first()
        print(c)
        if(c):
          db.session.delete(c)
          db.session.commit()
        else:
          abort(400,message='Card Number Invalid')
        db.session.commit()
        return 'Card Successfully Delete',200
      else:
          abort(405,message='Deck doesnot exist')
    else:
        abort(409,message='User doesnot exist')
    

class D(Resource):
  def get(self,did):
    a=Decks.query.filter_by(did=did).first()
    if(a):
      return jsonify({'score':a.deck_score})
    else:
      abort(405,message='Deck doesnot exist')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if(request.method=='GET'):
        return render_template('login.html')
    else:
        if(Users.query.filter_by(name=request.form['uname']).first()):
            x=Users.query.filter_by(name=request.form['uname']).first()
            b=Decks.query.filter_by(duid=x.uid).all()
            return redirect(url_for('x',uname=request.form['uname']))
            #return render_template('general.html',a=request.form['uname'],b=b,uname=request.form['uname'])
        else:
            return render_template('incorrectlogin.html')

@app.route('/login/<string:uname>/',methods=['GET','POST'])
def x(uname):
    x = Users.query.filter_by(name=uname).first()
    b = Decks.query.filter_by(duid=x.uid).all()
    return render_template('general.html',a=uname,uname=uname,b=b)

@app.route('/create/user',methods=['GET','POST'])
def create():
    if(request.method=='GET'):
        return render_template('adduser.html')
    else:
        a=Users(name=request.form['uname']) # Have to add that part if user uses some name that already exists
        db.session.add(a)
        db.session.commit()
        return render_template('user_created.html')

@app.route('/<string:uname>/addeck/',methods=['GET','POST'])
def add(uname):
    if(request.method=='GET'):
        return render_template('addeck.html',a=uname)
    else:
        dnaame=request.form['dname']
        print(dnaame)
        p = Users.query.filter_by(name=uname).first()
        if(Decks.query.filter_by(dname=dnaame,duid=p.uid).first()):
            return render_template('deckexists.html',a=uname)
        else:
            c=Users.query.filter_by(name=uname).first()
            a=Decks(dname=dnaame,duid=c.uid)
            db.session.add(a)
            db.session.commit()
            b=Decks.query.filter_by(duid=c.uid).all()
            return redirect(url_for('x', uname=uname))
            #return render_template('general.html',b=b,a=uname)

@app.route('/<string:uname>/updeck/<string:dname>',methods=['GET','POST'])
def upd(uname,dname):
    un = Users.query.filter_by(name=uname).first()
    dn = Decks.query.filter_by(duid=un.uid,dname=dname).first()
    if(request.method=='GET'):
        return render_template('updeck.html',a=uname,b=dn.dname)
    else:
        upd=request.form['dname']
        upl=Decks.query.filter_by(duid=un.uid,dname=dn.dname).first()
        upl.dname=upd
        db.session.commit()
        b=Decks.query.filter_by(duid=un.uid).all()
        return redirect(url_for('x', uname=uname))
        #return render_template('general.html',a=uname,b=b)

@app.route('/<string:uname>/deldeck/<string:dname>',methods=['GET','POST'])
def deli(uname,dname):
    b=Users.query.filter_by(name=uname).first()
    a=Decks.query.filter_by(dname=dname,duid=b.uid).first()
    c=cards.query.filter_by(dcid=a.did).all()
    for i in c:
        db.session.delete(i)
    db.session.delete(a)
    db.session.commit()
    return redirect(url_for('x', uname=uname))
    #return render_template('general.html',a=uname,b=Decks.query.filter_by(duid=b.uid).all())

@app.route('/<string:uname>/card_list/<string:dname>')
def card(uname,dname):
    u=Users.query.filter_by(name=uname).first()
    d=Decks.query.filter_by(duid=u.uid,dname=dname).first()
    c=cards.query.filter_by(dcid=d.did).all()
    return render_template('cardlist.html',c=c,a=uname,deckname=dname)

@app.route('/<string:uname>/<string:dname>/addcard/',methods=['GET','POST'])
def adcard(uname,dname):
    if(request.method=='GET'):
        return render_template('addcard.html',deckname=dname,a=uname)
    else:
        cf=request.form['cface']
        cb=request.form['cback']
        a=Users.query.filter_by(name=uname).first()
        b=Decks.query.filter_by(dname=dname,duid=a.uid).first()
        c=cards(card_face=cf,card_back=cb,dcid=b.did)
        db.session.add(c)
        db.session.commit()
        c=cards.query.filter_by(dcid=b.did).all()
        return render_template('cardlist.html',c=c,a=uname,deckname=dname)

@app.route('/<string:uname>/<string:dname>/<int:cn>/upcard/',methods=['GET','POST'])
def upc(uname,dname,cn):
    print(uname,dname,cn)
    if(request.method=='GET'):
        return render_template('upcard.html',a=uname,deckname=dname,cn=cn)
    else:
        a = Users.query.filter_by(name=uname).first()
        b = Decks.query.filter_by(dname=dname, duid=a.uid).first()
        x=cards.query.filter_by(card_no=cn).first()
        print('xb',x)
        x.card_face=request.form['cface']
        x.card_back=request.form['cback']
        print('xa',x)
        db.session.commit()
        return render_template('cardlist.html',c=cards.query.filter_by(dcid=b.did).all(),a=uname,deckname=dname)

@app.route('/<string:uname>/<string:dname>/<int:cn>/delcard/',methods=['GET','POST'])
def delu(uname,dname,cn):
    a = Users.query.filter_by(name=uname).first()
    b = Decks.query.filter_by(dname=dname, duid=a.uid).first()
    c=cards.query.filter_by(card_no=cn).first()
    db.session.delete(c)
    db.session.commit()
    return render_template('cardlist.html', c=cards.query.filter_by(dcid=b.did).all(),a=uname,deckname=dname)

@app.route('/<string:uname>/<string:dname>/<int:n>',methods=['GET','POST'])
def fina(uname,dname,n):
    a = Users.query.filter_by(name=uname).first()
    b = Decks.query.filter_by(dname=dname, duid=a.uid).first()
    c = cards.query.filter_by(dcid=b.did).all()
    if(n!=0):
        t=request.form['score']
        if(t=='EASY'):
            c[n-1].card_score=1
        else:
            c[n-1].card_score=4
        db.session.commit()
    if(n<len(c)):
        return render_template('testing.html',deckname=dname,a=c[n].card_face,b=c[n].card_back,u=uname,n=n)
    else:
      avg=0
      for i in c:
        avg=avg+(i.card_score)
      b.deck_score=str(avg/(len(c)))
      db.session.commit()
      return render_template('done.html',a=uname,avg=avg/(len(c)))

@app.route('/<string:uname>/<string:dname>/<int:n>/ans/',methods=['GET','POST'])
def ans(uname,dname,n):
    a = Users.query.filter_by(name=uname).first()
    b = Decks.query.filter_by(dname=dname, duid=a.uid).first()
    c = cards.query.filter_by(dcid=b.did).all()
    if (n < len(c)):
        return render_template('testans.html', deckname=dname, a=c[n].card_face, b=c[n].card_back, u=uname, n=n)
    else:
        return '<h1>Done for the Day!</h1>'



api.add_resource(A,'/api/user/')
api.add_resource(B,'/api/<string:user_name>','/api/<string:user_name>/<string:dname>')
api.add_resource(C,'/api/<string:user_name>/<string:dname>/cards','/api/<string:user_name>/<string:dname>/cards/<int:card_no>')
api.add_resource(D,'/api/<int:did>')
if __name__=='__main__':
  app.run('0.0.0.0',debug=True)