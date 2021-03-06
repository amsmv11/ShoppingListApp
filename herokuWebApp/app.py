from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)


    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        item_content = request.form['content']
        new_item = Item(content=item_content)

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        except:
            return "ERROR ao tentar criar um item"


    else:
        items = Item.query.order_by(Item.date_created).all()
        return render_template("index.html", items=items)


@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Item.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "ERROR a tentar apagar item"


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    item_to_update = Item.query.get_or_404(id)

    if request.method == 'POST':
        item_to_update.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "ERROR ao tentar atualizar item"
    else:
        return render_template('update.html', item=item_to_update)




if __name__ == "__main__":
    app.run(debug=True)