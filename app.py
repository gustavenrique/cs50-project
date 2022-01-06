from cs50 import SQL
from flask import Flask, redirect, render_template, request, url_for, session, Response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Session config
app.config['SESSION_FILE_DIR'] = mkdtemp()
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


db = SQL("sqlite:///store.db")

def usd(value):
    # Format value as USD
    return f"${value:,.2f}"

@app.route('/')
def index():
  if not session.get('user_id'):
    return redirect('/login')
  
  # Get user cash
  user_cash = db.execute('SELECT cash FROM users WHERE id = ?', session['user_id'])[0]['cash']
  
  # To get 5 products of eletronics, books, clothes, sports and beauty
  eletronics = db.execute('SELECT * FROM products WHERE category="Eletronics" ORDER BY RANDOM() LIMIT 0, 5')
  books = db.execute('SELECT * FROM products WHERE category="Books" ORDER BY RANDOM() LIMIT 0, 5')
  clothes = db.execute('SELECT * FROM products WHERE category="Clothes" ORDER BY RANDOM() LIMIT 0, 5')
  sports = db.execute('SELECT * FROM products WHERE category="Sports" ORDER BY RANDOM() LIMIT 0, 5')
  beauty = db.execute('SELECT * FROM products WHERE category="Beauty" OR category="Health & Person Care" ORDER BY RANDOM() LIMIT 0, 5')
  
  # To make a list of products lists
  categories = [eletronics, books, clothes, sports, beauty] 
  categories_name = ['Eletronics', 'Books', 'Clothes', 'Sports', 'Beauty, Health & Person Care']
  
  return render_template('index.html', cash=user_cash, usd=usd, categories=categories, categories_name = categories_name)

@app.route('/login', methods=['POST', 'GET'])
def login():
  # Forget any username
  session.clear()

  if request.method == 'POST':
    # Getting the user data
    user_data = db.execute('SELECT * FROM users WHERE username = ?', request.form.get('username'))
    
    # User checking
    if len(user_data) != 1 or not check_password_hash(user_data[0]['hash'], request.form.get('password')):
      return render_template('login.html', message='invalid username and/or password')
    
    # Remember the user id
    session['user_id'] = user_data[0]['id']
    return redirect('/')
    
  return render_template('login.html')
  
@app.route('/register', methods=['POST', 'GET'])
def register():
  if request.method == 'POST':
    # Check if username is taken
    username = request.form.get('username')
    user = db.execute('SELECT * FROM users WHERE username=?', username)
    
    if user:
      return render_template('register.html', message='username already taken')
      
    # Check if pass matches confirmation
    if request.form.get('password') != request.form.get('confirm'):
      return render_template('register.html', message='pass does not match confirmation')
    
    # Generate pass hash and insert user to the database
    pass_hash = generate_password_hash(request.form.get('password'))
    
    db.execute('INSERT INTO users(username, hash) VALUES(?, ?)', username, pass_hash)
    
    # Redirect to login page
    return redirect('/login')
  else:
    return render_template('register.html')  
  
@app.route('/logout')
def logout():
  # Forget the user
  session.clear()
  
  return redirect('/')
  

@app.route('/user-settings')
def settings():
  if not session.get('user_id'):
    return redirect('/login')
    
  return render_template('user-settings.html')
  
@app.route('/change-pass', methods=['POST', 'GET'])
def change_pass():
  if not session.get('user_id'):
    return redirect('/login')
  
  if request.method == 'GET':
    return render_template('change-pass.html')
  else:
    # Get pass and confirmation
    pw = request.form.get('pw')
    conf_pw = request.form.get('conf-pw')
    
    # Verify if confirmation matches
    if pw != conf_pw:
      return render_template('change-pass.html', message='incorrect confirmation')
    else:
      # If it does, update the user pass
      pass_hash = generate_password_hash(pw)
      db.execute('UPDATE users SET hash=? WHERE id=?', pass_hash, session['user_id'])
      return render_template('change-pass.html', message='pass changed!')

# IMAGE GENERATOR ROUTE
@app.route('/img/<int:id>')
def img_display(id):
  img = (db.execute('SELECT * FROM images WHERE id=?', id))[0]
  
  if not img:
    return "ERROR: there's no image with that id"
    
  return Response(img['img'], mimetype=img['mimetype'])
  
  
@app.route('/sell')
def sell():
  if not session.get('user_id'):
    return redirect('/login')
 
  user_prod = db.execute('SELECT id, name, img_id, price FROM products WHERE seller_id=?', session['user_id'])
  return render_template('sell.html', userProducts=user_prod, usd=usd)

categories = [
    'Baby Products',
    'Beauty',
    'Books',
    'Camera & Photo',
    'Cellphone & Accessories',
    'Clothes',
    'Eletronics', 
    'Grocery & Gourmet Foods',
    'Health & Person Care',
    'Home & Garden',
    'Musical Instruments',
    'Office Products',
    'Sports',
    'Toys & Games',
    'Video Games'
  ]
  
@app.route('/add-product', methods=['POST', 'GET'])
def add_product():
  if not session.get('user_id'):
    return redirect('/login')
    
  if request.method == 'GET':
    return render_template('add-product.html', categories=categories)
  else:
    # Getting the product informations
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    category = request.form.get('category')
    
    # Making sure it's a valid category
    if category:
      if category not in categories:
        return render_template('add-product.html', message='Must select a valid category')
    
    # Getting the image informations
    img = request.files['inpFile']
    imgName = secure_filename(img.filename)
    mimetype = img.mimetype
    
    # Adding the image to the database
    db.execute('INSERT INTO images (img, name, mimetype) VALUES(?, ?, ?)', img.read(), imgName, mimetype)
    
    # Adding the product database
    img_id = ((db.execute('SELECT max(id) AS id FROM images'))[0])['id']
    seller_id = session['user_id']
    
    db.execute('INSERT INTO products (name, price, description, img_id, seller_id, category) VALUES(?, ?, ?, ?, ?, ?)', name, price, description, img_id, seller_id, category)
    
    # Redirect user to the own products list
    return redirect('/sell')
    
    
@app.route('/delete-product', methods=['POST'])
def delete_product():
  if not session.get('user_id'):
    return redirect('/login')
  
  prod_id = request.form.get('prod_id')
  
  seller_id = db.execute('SELECT seller_id FROM products WHERE id=?', prod_id)[0]['seller_id']
  
  if seller_id != session['user_id']:
    return 'You are not the seller of this product'
  else:
    db.execute('DELETE FROM products WHERE id=?', prod_id)
    return redirect('/sell')
    
  
@app.route('/product/<int:id>')
def product(id):
  product = db.execute('SELECT * FROM products WHERE id=?', id)[0]
  seller = db.execute('SELECT * FROM users WHERE id=?', product['seller_id'])[0]
  
  return render_template('view-product.html', product=product, seller=seller, usd=usd)
  
  
@app.route("/update-product/<int:prod_id>", methods=['POST', 'GET'])
def update_product(prod_id):
  if not session.get('user_id'):
    return redirect('/login')
  
  product = db.execute("SELECT * FROM products WHERE id=?", prod_id)[0]
  
  if request.method == 'GET':
    if session['user_id'] != product['seller_id']:
      return 'You can not update a product that you are not selling'
    
    return render_template("update-product.html", product=product, categories=categories, \
    message="Just change what you want!")
    
  else:
    # Getting the product informations
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    category = request.form.get('category')
    
    # Getting the image informations
    img = request.files['inpFile']
    if img:
      imgName = secure_filename(img.filename)
      mimetype = img.mimetype
      
      # Updating the image in the database
      db.execute('UPDATE images SET img = ?, name = ?, mimetype = ? WHERE id = ?', img.read(), imgName, mimetype, product['img_id'])  
    
    # Updating all the others
    if name:
      db.execute("UPDATE products SET name = ? WHERE id=?", name, product['id'])
      
    if price:
      db.execute("UPDATE products SET price = ? WHERE id=?", price, product['id'])
    
    if description:
      db.execute("UPDATE products SET description = ? WHERE id=?", description, product['id'])
    
    if category:
      # Making sure it's a valid category
      if category not in categories:
        return render_template('add-product.html', message='Must select a valid category')
        
      db.execute("UPDATE products SET category = ? WHERE id=?", category, product['id'])
      
    # Redirect user to the own products list
    return redirect('/sell')
    
@app.route('/buy', methods=['POST'])
def buy():
  if not session.get('user_id'):
      return redirect('/login')
  
  # Getting the purchase informations
  prod_id = request.form.get('prod_id')
  product = db.execute('SELECT * FROM products WHERE id=?', prod_id)[0]
  quantity = float(request.form.get('quantity'))
  
  # Making sure it's not the owner of the product
  if session['user_id'] == product['seller_id']:
    return 'Sorry, you can not buy a product you are selling'
    
  #Getting the user and seller informations
  user = db.execute('SELECT * FROM users WHERE id=?', session['user_id'])[0]
  seller = db.execute('SELECT * FROM users WHERE id=?', product['seller_id'])[0]
  
  # Making the purchase 
  if float(user['cash']) >= float(float(product['price'])*quantity):
    # Updating the user and seller cash
    new_user_cash = user['cash'] - product['price']*quantity
    db.execute('UPDATE users SET cash=? WHERE id=?', new_user_cash, session['user_id'])
    
    new_seller_cash = seller['cash'] + product['price']*quantity
    db.execute('UPDATE users SET cash=? WHERE id=?', new_seller_cash, product['seller_id'])
    
    # Computing the purchase in the table transactions
    db.execute('INSERT INTO transactions (buyer_id, seller_id, product_id, price, quantity) VALUES(?, ?, ?, ?, ?)', \
    user['id'], seller['id'], product['id'], product['price'], quantity)
  
    # Redirecting the user to the history of purchases page
    return redirect('/history')
  else:
    return 'not enough cash'

@app.route('/search', methods=['POST', 'GET'])
def search():
  q = request.args.get('q')
  search_input = '%' + q + '%'
  
  result = db.execute("SELECT * FROM products WHERE name LIKE ? OR description LIKE ?", search_input, search_input)
  
  return render_template('search.html', result=result, search_input=q, usd=usd)
  
  
@app.route('/cart', methods = ['POST', 'GET'])
def cart():
  if not session.get('user_id'):
      return redirect('/login')
  
  if request.method == 'POST':
    prod_id = request.form.get('prod_id')
    
    db.execute('INSERT INTO cart (user_id, prod_id) VALUES(?, ?)', session['user_id'], prod_id)
    
    return redirect('/cart')
  
  products = db.execute('SELECT * FROM cart JOIN products ON cart.prod_id = products.id WHERE user_id = ?', session['user_id'])
  
  return render_template('cart.html', products=products, usd=usd)
  
@app.route('/cart/remove', methods=['POST'])
def remove_cart():
  prod_id = request.form.get('prod_id')
  
  db.execute('DELETE FROM cart WHERE prod_id = ? AND user_id = ?', prod_id, session['user_id'])
  
  return redirect('/cart')


@app.route('/history')  
def my_history():
  purchases = db.execute('SELECT * FROM transactions JOIN products ON transactions.product_id = products.id WHERE buyer_id = ?', session['user_id'])
  
  return render_template('history.html', purchases = purchases, usd=usd)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=port, debug=True)