from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.posts import Posts
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/post', methods=['POST'])
def publish():
    # print('in create route')
    # print(request.form)
    is_valid = Posts.verify_post(request.form)
    user = session['id']
    if not is_valid:
        return redirect('/wall')
    post_data = {
        'user_id': session['id'],
        'content':request.form['content'],
    }
    post_id = Posts.save(post_data)

    return redirect("/wall")


@app.route('/post/delete/<post_id>')
def delete_post(post_id):
    print ('Deleting post - ', post_id)
    Posts.delete(post_id)
    return redirect('/wall')


