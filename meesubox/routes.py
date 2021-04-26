from meesubox import app
from flask import render_template,request, redirect, url_for, flash
from meesubox.models import UserModel, ProductItem, CartDetails, CategoryModel
from meesubox.forms import RegisterForm , LoginForm, AddProductDetails, AddCategoryDetails
from werkzeug.security import generate_password_hash, check_password_hash
from meesubox import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == "GET":
          new_product_items = ProductItem.query.filter_by(new_product = 1).all()
          best_product_items = ProductItem.query.filter_by(best_seller = 1).all()
    return render_template('home.html', new_product_items = new_product_items, best_seller_items = best_product_items)

@app.route('/home', methods=['GET', 'POST'])
@login_required
def login_home_page():
    if request.method == "GET":
          new_product_items = ProductItem.query.filter_by(new_product = 1).all()
          best_product_items = ProductItem.query.filter_by(best_seller = 1).all()
    return render_template('home.html', name=current_user.firstname, new_product_items = new_product_items, best_seller_items = best_product_items)


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
  

@app.route('/single-product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def single_product(product_id):
    if request.method == "GET":
          product_item = ProductItem.query.filter_by(product_id = product_id).first()
    return render_template('single-product.html', product_item = product_item)


@app.route('/add-cart-details/<int:product_id>', methods=['GET', 'POST'])
@login_required
def add_cart_details(product_id):
    if request.method == "GET":
        product_item = ProductItem.query.filter_by(product_id = product_id).first()
        add_cart_details = CartDetails(product_id = product_item.product_id, product_name = product_item.product_name, product_price = product_item.product_price, product_category = product_item.product_category, product_size = product_item.product_size, quantity = product_item.quantity, user_id = current_user.id)
        try:
            db.session.add(add_cart_details)
            db.session.commit()
            return redirect(url_for('login_home_page'))
        except:
            print('There was an error for adding product in your cart')       
        return render_template('shopping-cart.html')  



@app.route('/cart-details', methods=['GET', 'POST'])
@login_required
def cart_details():
    if request.method == "GET":
        cart_items = CartDetails.query.filter_by(user_id = current_user.id).all()
        return render_template('shopping-cart.html', cart_items = cart_items)


@app.route('/delete-cart/<int:product_id>', methods=['GET', 'POST'])
@login_required
def delete_cart(product_id):
    if request.method == "GET":
        cart_items = CartDetails.query.filter_by(user_id = current_user.id, product_id = product_id).first()
        try:
            db.session.delete(cart_items)
            db.session.commit()
            return redirect(url_for('cart_details'))
        except:
            print('There was an error for removing product in your cart')         
        
        return render_template('shopping-cart.html') 


@app.route('/checkout')
@login_required
def checkout():
    return render_template('checkout.html')


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated and current_user.user_role == 'admin':    
        return render_template('dashboard/index.html')    
    else:
        return redirect(url_for('login_home_page'))


@app.route('/dashboard/product-list', methods=['GET', 'POST'])
@login_required
def product_list():
    if current_user.is_authenticated and current_user.user_role == 'admin':
        product_items = ProductItem.query.all()
        return render_template('dashboard/product-list.html', product_items = product_items)
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
                return redirect(url_for('product_list'))
            except:
                print('Srry unable to create product')
        return render_template('dashboard/add-products.html', form=form)                  
    else:
        return redirect(url_for('login_home_page'))            





@app.route('/dashboard/category-list', methods=['GET', 'POST'])
@login_required
def category_list():
    if current_user.is_authenticated and current_user.user_role == 'admin':
        category_lists = CategoryModel.query.all()
        return render_template('dashboard/category-list.html', category_lists = category_lists)
    else:
        return redirect(url_for('login_home_page'))    


@app.route('/dashboard/add-category', methods=['GET', 'POST'])
@login_required
def add_category():
    if current_user.is_authenticated and current_user.user_role == 'admin':
        form = AddCategoryDetails()
        category_lists = CategoryModel.query.all()
        category_level = 0
        add_new_category = ''
        if form.validate_on_submit():
            print(form.data,"--------------------------------Amit")
            is_parent_category = CategoryModel.query.filter_by(category_id = form.parent_category.data).first()
            if(is_parent_category == None):
                print(is_parent_category,"--------------------------------Ashwini")
                add_new_category = CategoryModel(category_name = form.category_name.data, category_slug = form.category_slug.data, assign_parent_category = form.assign_parent_category.data, category_level = category_level, parent_category = form.parent_category.data )
            else:

                print(is_parent_category ,"-----------------------------------------Poorva")    
            
                if is_parent_category.category_level == (category_level + 1) and form.assign_parent_category.data == 1:
                    category_level = is_parent_category.category_level + 1
                    print(category_level,"category_level------------------------")
                    add_new_category = CategoryModel(category_name = form.category_name.data, category_slug = form.category_slug.data, assign_parent_category = form.assign_parent_category.data, category_level = category_level, parent_category = form.parent_category.data ) 
                elif is_parent_category.category_level == category_level and form.assign_parent_category.data == 1:
                    category_level = is_parent_category.category_level + 1
                    print(category_level,"category_level2-----------------------")  
                    add_new_category = CategoryModel(category_name = form.category_name.data, category_slug = form.category_slug.data, assign_parent_category = form.assign_parent_category.data, category_level = category_level, parent_category = form.parent_category.data )
            try:
                db.session.add(add_new_category)
                db.session.commit()
                return redirect(url_for('category_list'))
            except:
                print('Srry unable to create category')                          
        return render_template('dashboard/add-category.html', form = form, category_lists = category_lists)
        # if form.validate_on_submit():
        #     if category_list
    else:
        return redirect(url_for('login_home_page'))            


