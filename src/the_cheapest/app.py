from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_BINDS'] = {'competitors' : 'sqlite:///competitors.db'}
db = SQLAlchemy(app)


class ProductCreate(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ean = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'Product ' + str(self.id)


class CompetitorCreate(db.Model):
    __bind_key__ = 'competitors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)

    def __repr__(self):
        return 'Competitor ' + str(self.id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/products', methods=['GET', 'POST'])
def products():

    if request.method == 'POST':
        product_name = request.form['name']
        product_ean = request.form['ean']
        product_price = request.form['price']

        new_product = ProductCreate(name=product_name, ean=product_ean, price=product_price)
        db.session.add(new_product)
        db.session.commit()
        return redirect('/products')
    else:
        all_products = ProductCreate.query.order_by(ProductCreate.id).all()
        return render_template('products.html', products=all_products)


@app.route('/products/delete/<int:id>')
def product_delete(id):
    product = ProductCreate.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/products')


@app.route('/products/product_edit/<int:id>', methods=['GET', 'POST'])
def product_edit(id):
    product = ProductCreate.query.get_or_404(id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.ean = request.form['ean']
        product.price = request.form['price']
        db.session.commit()
        return redirect('/products')
    else:
        return render_template('product_edit.html', product=product)


@app.route('/competitors', methods=['GET', 'POST'])
def competitors():

    if request.method == 'POST':
        competitor_name = request.form['name']
        competitor_url = request.form['url']

        new_competitor = CompetitorCreate(name=competitor_name, url=competitor_url)
        db.session.add(new_competitor)
        db.session.commit()
        return redirect('/competitors')
    else:
        all_competitors = CompetitorCreate.query.order_by(CompetitorCreate.id).all()
        return render_template('competitors.html', competitors=all_competitors)


@app.route('/competitors/delete/<int:id>')
def competitor_delete(id):
    competitor = CompetitorCreate.query.get_or_404(id)
    db.session.delete(competitor)
    db.session.commit()
    return redirect('/competitors')


@app.route('/competitors/competitor_edit/<int:id>', methods=['GET', 'POST'])
def competitor_edit(id):
    competitor = CompetitorCreate.query.get_or_404(id)

    if request.method == 'POST':
        competitor.name = request.form['name']
        competitor.url = request.form['url']
        db.session.commit()
        return redirect('/competitors')
    else:
        return render_template('competitor_edit.html', competitor=competitor)


if __name__ == "__main__":
    app.run(debug=True)
