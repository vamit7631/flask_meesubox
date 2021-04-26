from meesubox import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(int(id))

class UserModel(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(length=30), nullable=False)
    lastname = db.Column(db.String(length=30), nullable=False)
    mobile_no = db.Column(db.String(length=12), nullable=False, unique=True)
    email_id  = db.Column(db.String(length=200), nullable=False, unique=True)
    password = db.Column(db.String(length=200), nullable = False)
    user_role = db.Column(db.String(length=200), nullable = False, default= 'buyer')
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f'UserModel {self.id}'


class ProductItem(db.Model):
    product_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(length=200), nullable=False)
    product_price = db.Column(db.String(length=200), nullable=False)
    product_category = db.Column(db.String(length=50), nullable=False)
    product_size = db.Column(db.String(length=50), nullable=False)
    # product_colour = db.Column(db.String(length=50), nullable=False)
    product_description = db.Column(db.String(length=1000), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    product_discount = db.Column(db.String(length=200), nullable=False)
    # sku_id = db.Column(db.BigInteger(), nullable=False)
    # store_id = db.Column(db.BigInteger(), nullable=False)
    store_name = db.Column(db.String(length=100), nullable=False)
    new_product = db.Column(db.Boolean(), default = False)
    # featured_product = db.Column(db.Boolean(), default=False)
    best_seller = db.Column(db.Boolean(), default = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f'ProductItem {self.product_name}'    


class CartDetails(db.Model):
    cart_id = db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.Integer(), db.ForeignKey('product_item.product_id'))
    product_name = db.Column(db.String(length=200), nullable=False)
    product_price = db.Column(db.String(length=200), nullable=False)
    product_category = db.Column(db.String(length=50), nullable=False)
    product_size = db.Column(db.String(length=50), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('user_model.id'))

    def __repr__(self):
        return f'CartDetails {self.product_name}' 



class CategoryModel(db.Model):
    category_id = db.Column(db.Integer(), primary_key=True)
    category_name = db.Column(db.String(length=200), nullable=False)
    category_slug = db.Column(db.String(length=200), nullable=False)
    category_level = db.Column(db.Integer(), default = 0)
    parent_category = db.Column(db.Integer(), default = 0)
    assign_parent_category = db.Column(db.Boolean(), default = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f'CategoryModel {self.category_name}'     
