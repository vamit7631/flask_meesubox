from meesubox import app
from flask import render_template, redirect, url_for, flash
from meesubox.models import UserModel, ProductItem
from meesubox.forms import RegisterForm , LoginForm, AddProductDetails
from werkzeug.security import generate_password_hash, check_password_hash
from meesubox import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/home')
@login_required
def login_home_page():
    return render_template('home.html', name=current_user.firstname)    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user_record = UserModel(firstname = form.firstname.data, lastname = form.lastname.data, mobile_no = form.mobile_no.data, email_id = form.email_id.data, password = generate_password_hash(form.password.data, method='sha256') )
        try:
            db.session.add(new_user_record)
            db.session.commit()
            return redirect(url_for('signin'))
        except:
            print('There was an error with creating a user')   
    else:
        return render_template('signup.html', form=form)    




@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        if current_user.user_role == 'admin':
            return redirect(url_for('dashboard'))
        elif current_user.user_role == 'buyer':
            return redirect(url_for('login_home_page'))
    else:
        form = LoginForm()            
        if form.validate_on_submit(): 
            user = UserModel.query.filter_by(email_id = form.email_id.data).first()
            if not user or not check_password_hash(user.password, form.password.data):   
                return redirect(url_for('signin'))

            login_user(user, remember=True)    
            if current_user.is_authenticated:
                if current_user.user_role == 'admin':
                    return redirect(url_for('dashboard'))
                elif current_user.user_role == 'buyer':
                    return redirect(url_for('login_home_page'))

        return render_template('signin.html', form=form)            

@app.route('/signout')
@login_required
def logout_page():
    logout_user()
    return redirect(url_for("home_page"))



@app.route('/wishlist')
@login_required
def wishlist():
    return render_template('wishlist.html')    

@app.route('/cart-details')
@login_required
def cart_details():
    return render_template('shopping-cart.html')    


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated and current_user.user_role == 'admin':    
        return render_template('dashboard/index.html')    
    else:
        return redirect(url_for('login_home_page'))

@app.route('/dashboard/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.is_authenticated and current_user.user_role == 'admin':
        form = AddProductDetails()
        if form.validate_on_submit():
            add_new_product = ProductItem(product_name = form.product_name.data, product_price = form.product_price.data, product_category = form.product_category.data, product_size = form.product_size.data, product_description = form.product_description.data, quantity = form.quantity.data, product_discount = form.product_discount.data, store_name = form.store_name.data, new_product = form.new_product.data, best_seller = form.best_seller.data )
            print('Amit test user')   
            try:
                db.session.add(add_new_product)
                db.session.commit()
                return redirect(url_for('login_home_page'))
            except:
                print('Srry unable to create product')
        return render_template('dashboard/add-products.html', form=form)                  
    else:
        return redirect(url_for('login_home_page'))            
