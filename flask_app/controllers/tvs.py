from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models import user, tv
from flask_app.models.tv import Tv
from flask import flash


@app.route('/createTv')
def createtv():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user_id']
    }
    return render_template('createTv.html', loggedUser= User.get_user_by_id(data))


@app.route('/create_tv', methods = ['POST'])
def create_tv():
    if 'user_id' not in session:
        return redirect('/logout')
    if not tv.Tv.validate_tv(request.form):
        return redirect('/createTV')
    data ={
        'user_id':session['user_id'],
        'title':request.form['title'],
        'network':request.form['network'],
        'date':request.form['date'],
        'description':request.form['description']
         
    }
    
    tv.Tv.create_tv( data )
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'tv_id': id,
        'user_id': session['user_id']
    }
    currentTv = Tv.get_tv_by_id(data)

    if not session['user_id'] == currentTv['user_id']:
        flash('You cant delete this', 'noAccessError')
        return redirect('/dashboard')

    Tv.delete(data)
    return redirect(request.referrer)


@app.route('/tv/<int:id>')
def showOne(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'tv_id': id,
        'user_id': session['user_id']
    }
    return render_template('tv.html', loggedUser= User.get_user_by_id(data),tv = Tv.get_tv_by_id(data))

@app.route('/edit/<int:id>')
def editForm(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
            'tv_id': id,
            'user_id': session['user_id']
        }
    currentTv = Tv.get_tv_by_id(data)

    if not session['user_id'] == currentTv['user_id']:
        flash('You cant delete this', 'noAccessError')
        return redirect('/dashboard')
   
    return render_template('updateTv.html', loggedUser= User.get_user_by_id(data), tv = Tv.get_tv_by_id(data))

@app.route('/update/<int:id>', methods = ['POST'])
def updateTv(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Tv.validate_tv(request.form):
        return redirect(request.referrer)
    
    currentTv = Tv.get_tv_by_id(request.form)

    if not session['user_id'] == currentTv['user_id']:
        flash('You cant delete this', 'noAccessError')
        return redirect('/dashboard')
    
    Tv.update_tv(request.form)
    return redirect('/')

