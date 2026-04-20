from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__, template_folder='shop_templates')
app.config['SECRET_KEY'] = 'kenny-shop-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kenny_shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(500))
    category = db.Column(db.String(50))
    stock = db.Column(db.Integer, default=10)
    rating = db.Column(db.Float, default=4.5)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product = db.relationship('Product')

def add_sample_products():
    if Product.query.count() == 0:
        products = [
            # Apple Products
            Product(name='iPhone 15 Pro Max', description='Apple iPhone 15 Pro Max 256GB Natural Titanium with A17 Pro chip', price=1199.99, category='Apple', stock=30, rating=4.9,
                image='https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop'),
            Product(name='iPhone 15 Pro', description='Apple iPhone 15 Pro 128GB Black Titanium with A17 Pro chip', price=999.99, category='Apple', stock=40, rating=4.8,
                image='https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop'),
            Product(name='iPhone 15', description='Apple iPhone 15 128GB Pink with A16 Bionic chip', price=799.99, category='Apple', stock=50, rating=4.7,
                image='https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop'),
            Product(name='iPhone 14', description='Apple iPhone 14 128GB Blue with A15 Bionic chip', price=699.99, category='Apple', stock=35, rating=4.6,
                image='https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop'),
            Product(name='MacBook Pro 16"', description='Apple MacBook Pro 16-inch M3 Pro chip 18GB RAM 512GB SSD', price=2499.99, category='Apple', stock=15, rating=4.9,
                image='https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop'),
            Product(name='MacBook Pro 14"', description='Apple MacBook Pro 14-inch M3 chip 8GB RAM 512GB SSD', price=1999.99, category='Apple', stock=20, rating=4.8,
                image='https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop'),
            Product(name='MacBook Air M2', description='Apple MacBook Air 13-inch M2 chip 8GB RAM 256GB SSD Midnight', price=1099.99, category='Apple', stock=25, rating=4.8,
                image='https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop'),
            Product(name='iPad Pro 12.9"', description='Apple iPad Pro 12.9-inch M2 chip 128GB WiFi Space Grey', price=1099.99, category='Apple', stock=20, rating=4.8,
                image='https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop'),
            Product(name='iPad Air', description='Apple iPad Air 10.9-inch M1 chip 64GB WiFi Blue', price=599.99, category='Apple', stock=30, rating=4.7,
                image='https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop'),
            Product(name='Apple Watch Series 9', description='Apple Watch Series 9 GPS 45mm Midnight Aluminium', price=429.99, category='Apple', stock=40, rating=4.8,
                image='https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400&h=400&fit=crop'),
            Product(name='AirPods Pro 2nd Gen', description='Apple AirPods Pro 2nd generation with MagSafe charging case', price=249.99, category='Apple', stock=60, rating=4.8,
                image='https://images.unsplash.com/photo-1603351154351-5e2d0600bb77?w=400&h=400&fit=crop'),
            Product(name='AirPods 3rd Gen', description='Apple AirPods 3rd generation with Lightning charging case', price=169.99, category='Apple', stock=80, rating=4.6,
                image='https://images.unsplash.com/photo-1603351154351-5e2d0600bb77?w=400&h=400&fit=crop'),

            # Itel Phones
            Product(name='Itel A70', description='Itel A70 3GB RAM 64GB Storage 5000mAh battery', price=89.99, category='Phones', stock=100, rating=4.1,
                image='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop'),
            Product(name='Itel P40', description='Itel P40 2GB RAM 32GB Storage 6000mAh massive battery', price=69.99, category='Phones', stock=120, rating=4.0,
                image='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop'),
            Product(name='Itel S23+', description='Itel S23+ 4GB RAM 128GB Storage 50MP camera', price=129.99, category='Phones', stock=80, rating=4.2,
                image='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop'),
            Product(name='Itel Vision 3', description='Itel Vision 3 3GB RAM 64GB 6.6-inch HD+ display', price=99.99, category='Phones', stock=90, rating=4.1,
                image='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop'),
            Product(name='Itel A58', description='Itel A58 2GB RAM 32GB Storage Android 12', price=59.99, category='Phones', stock=150, rating=3.9,
                image='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop'),

            # Other Phones
            Product(name='Samsung Galaxy S24 Ultra', description='Samsung Galaxy S24 Ultra 256GB Titanium Black with S-Pen', price=1299.99, category='Phones', stock=25, rating=4.8,
                image='https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400&h=400&fit=crop'),
            Product(name='Samsung Galaxy A54', description='Samsung Galaxy A54 5G 128GB Awesome Violet', price=399.99, category='Phones', stock=60, rating=4.5,
                image='https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400&h=400&fit=crop'),
            Product(name='Tecno Spark 20', description='Tecno Spark 20 8GB RAM 256GB Storage 6.56-inch display', price=149.99, category='Phones', stock=80, rating=4.2,
                image='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop'),
            Product(name='Infinix Hot 40', description='Infinix Hot 40 8GB RAM 256GB 5000mAh battery', price=159.99, category='Phones', stock=70, rating=4.3,
                image='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop'),

            # Laptops
            Product(name='Dell XPS 15', description='Dell XPS 15 Intel Core i7 16GB RAM 512GB SSD OLED display', price=1799.99, category='Laptops', stock=15, rating=4.7,
                image='https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400&h=400&fit=crop'),
            Product(name='HP Spectre x360', description='HP Spectre x360 14 Intel Core i7 16GB RAM 512GB SSD', price=1499.99, category='Laptops', stock=20, rating=4.6,
                image='https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400&h=400&fit=crop'),
            Product(name='Lenovo ThinkPad X1', description='Lenovo ThinkPad X1 Carbon Gen 11 Intel i7 16GB 512GB', price=1399.99, category='Laptops', stock=18, rating=4.7,
                image='https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400&h=400&fit=crop'),
            Product(name='ASUS ROG Zephyrus', description='ASUS ROG Zephyrus G14 AMD Ryzen 9 RTX 4060 16GB RAM', price=1599.99, category='Laptops', stock=12, rating=4.8,
                image='https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&h=400&fit=crop'),
            Product(name='Acer Nitro 5', description='Acer Nitro 5 Gaming Intel i5 16GB RAM RTX 3050 512GB', price=799.99, category='Laptops', stock=30, rating=4.4,
                image='https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&h=400&fit=crop'),
            Product(name='HP Pavilion 15', description='HP Pavilion 15 Intel Core i5 8GB RAM 256GB SSD', price=599.99, category='Laptops', stock=40, rating=4.3,
                image='https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400&h=400&fit=crop'),
            Product(name='Lenovo IdeaPad 3', description='Lenovo IdeaPad 3 AMD Ryzen 5 8GB RAM 512GB SSD', price=499.99, category='Laptops', stock=50, rating=4.2,
                image='https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400&h=400&fit=crop'),

            # Gadgets
            Product(name='DJI Mini 4 Pro Drone', description='DJI Mini 4 Pro drone with 4K camera and obstacle avoidance', price=759.99, category='Gadgets', stock=15, rating=4.8,
                image='https://images.unsplash.com/photo-1579829366248-204fe8413f31?w=400&h=400&fit=crop'),
            Product(name='GoPro Hero 12', description='GoPro HERO12 Black waterproof action camera 5.3K', price=399.99, category='Gadgets', stock=25, rating=4.7,
                image='https://images.unsplash.com/photo-1564466809058-bf4114d55352?w=400&h=400&fit=crop'),
            Product(name='Sony WH-1000XM5', description='Sony WH-1000XM5 wireless noise cancelling headphones', price=349.99, category='Gadgets', stock=40, rating=4.9,
                image='https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop'),
            Product(name='JBL Charge 5', description='JBL Charge 5 portable waterproof bluetooth speaker', price=179.99, category='Gadgets', stock=60, rating=4.7,
                image='https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=400&fit=crop'),
            Product(name='Anker PowerBank 26800', description='Anker 26800mAh portable charger with 65W fast charging', price=79.99, category='Gadgets', stock=80, rating=4.6,
                image='https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=400&h=400&fit=crop'),
            Product(name='Smart 4K TV 55"', description='Samsung 55-inch 4K QLED Smart TV with Alexa built-in', price=799.99, category='Gadgets', stock=20, rating=4.7,
                image='https://images.unsplash.com/photo-1593359677879-a4bb92f4834c?w=400&h=400&fit=crop'),
            Product(name='PlayStation 5', description='Sony PlayStation 5 Console with DualSense controller', price=499.99, category='Gadgets', stock=10, rating=4.9,
                image='https://images.unsplash.com/photo-1607853202273-797f1c22a38e?w=400&h=400&fit=crop'),
            Product(name='Xbox Series X', description='Microsoft Xbox Series X 1TB gaming console', price=499.99, category='Gadgets', stock=10, rating=4.8,
                image='https://images.unsplash.com/photo-1621259182978-fbf93132d53d?w=400&h=400&fit=crop'),
            Product(name='Nintendo Switch OLED', description='Nintendo Switch OLED model with 7-inch screen', price=349.99, category='Gadgets', stock=25, rating=4.8,
                image='https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=400&h=400&fit=crop'),
            Product(name='Ring Video Doorbell', description='Ring Video Doorbell Pro 2 with 3D motion detection', price=249.99, category='Gadgets', stock=35, rating=4.5,
                image='https://images.unsplash.com/photo-1558002038-1055907df827?w=400&h=400&fit=crop'),
            Product(name='Kindle Paperwhite', description='Kindle Paperwhite 11th Gen 8GB waterproof e-reader', price=139.99, category='Gadgets', stock=50, rating=4.7,
                image='https://images.unsplash.com/photo-1592496001020-d31bd830651f?w=400&h=400&fit=crop'),
            Product(name='Portable Projector', description='Anker Nebula Capsule portable smart projector 200 ANSI', price=299.99, category='Gadgets', stock=20, rating=4.5,
                image='https://images.unsplash.com/photo-1589254065878-42c9da997008?w=400&h=400&fit=crop'),

            # Books
            Product(name='Atomic Habits', description='James Clear - An Easy and Proven Way to Build Good Habits', price=16.99, category='Books', stock=200, rating=4.9,
                image='https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=400&fit=crop'),
            Product(name='The Psychology of Money', description='Morgan Housel - Timeless lessons on wealth and happiness', price=14.99, category='Books', stock=180, rating=4.8,
                image='https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=400&fit=crop'),
            Product(name='Deep Work', description='Cal Newport - Rules for focused success in a distracted world', price=15.99, category='Books', stock=150, rating=4.7,
                image='https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400&h=400&fit=crop'),
            Product(name='Think and Grow Rich', description='Napoleon Hill - The landmark bestseller on success', price=12.99, category='Books', stock=200, rating=4.8,
                image='https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400&h=400&fit=crop'),
            Product(name='AI Superpowers', description='Kai-Fu Lee - China, Silicon Valley and the New World Order', price=18.99, category='Books', stock=120, rating=4.6,
                image='https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400&h=400&fit=crop'),
            Product(name='Clean Code', description='Robert Martin - A Handbook of Agile Software Craftsmanship', price=39.99, category='Books', stock=100, rating=4.7,
                image='https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400&h=400&fit=crop'),
            Product(name='Python Crash Course', description='Eric Matthes - A Hands-On Introduction to Programming', price=29.99, category='Books', stock=150, rating=4.8,
                image='https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400&h=400&fit=crop'),
            Product(name='The Pragmatic Programmer', description='Hunt & Thomas - Your Journey to Mastery 20th Anniversary', price=44.99, category='Books', stock=80, rating=4.8,
                image='https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400&h=400&fit=crop'),
            Product(name='Rich Dad Poor Dad', description='Robert Kiyosaki - What the rich teach their kids about money', price=13.99, category='Books', stock=220, rating=4.7,
                image='https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=400&fit=crop'),
            Product(name='The Lean Startup', description='Eric Ries - How constant innovation creates success', price=17.99, category='Books', stock=130, rating=4.6,
                image='https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=400&fit=crop'),
            Product(name='Zero to One', description='Peter Thiel - Notes on Startups or How to Build the Future', price=16.99, category='Books', stock=140, rating=4.7,
                image='https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=400&fit=crop'),
            Product(name='Sapiens', description='Yuval Noah Harari - A Brief History of Humankind', price=18.99, category='Books', stock=160, rating=4.8,
                image='https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400&h=400&fit=crop'),

            # Food
            Product(name='Premium Coffee Beans 1kg', description='Ethiopian Yirgacheffe single origin arabica coffee beans', price=24.99, category='Food', stock=200, rating=4.8,
                image='https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=400&h=400&fit=crop'),
            Product(name='Luxury Chocolate Box', description='Lindt luxury assorted chocolate gift box 400g', price=34.99, category='Food', stock=150, rating=4.7,
                image='https://images.unsplash.com/photo-1548907040-4baa42d10919?w=400&h=400&fit=crop'),
            Product(name='Organic Honey 500g', description='Raw organic forest honey from Nigeria certified organic', price=14.99, category='Food', stock=100, rating=4.6,
                image='https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=400&h=400&fit=crop'),
            Product(name='Green Tea Collection', description='Japanese premium green tea variety pack 20 sachets', price=19.99, category='Food', stock=120, rating=4.5,
                image='https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&h=400&fit=crop'),
            Product(name='Mixed Nuts Premium', description='Premium roasted mixed nuts almonds cashews walnuts 500g', price=22.99, category='Food', stock=130, rating=4.7,
                image='https://images.unsplash.com/photo-1536591375673-a5e4c2fdce7b?w=400&h=400&fit=crop'),
            Product(name='Protein Powder Vanilla', description='Optimum Nutrition Gold Standard 100% Whey 2lb vanilla', price=44.99, category='Food', stock=80, rating=4.8,
                image='https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400&h=400&fit=crop'),
            Product(name='Olive Oil Extra Virgin', description='Italian extra virgin olive oil cold pressed 1 litre', price=18.99, category='Food', stock=100, rating=4.6,
                image='https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&h=400&fit=crop'),
            Product(name='Vitamin C Supplements', description='Nature Made Vitamin C 1000mg 300 tablets immune support', price=19.99, category='Food', stock=150, rating=4.7,
                image='https://images.unsplash.com/photo-1612532275214-e4ca76d0e4d1?w=400&h=400&fit=crop'),
            Product(name='Pasta Gift Set', description='Italian artisan pasta variety gift set 6 types', price=29.99, category='Food', stock=80, rating=4.5,
                image='https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb?w=400&h=400&fit=crop'),
            Product(name='Basmati Rice 5kg', description='Premium long grain basmati rice from India 5kg bag', price=12.99, category='Food', stock=200, rating=4.6,
                image='https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=400&fit=crop'),

            # Musical Instruments
            Product(name='Fender Stratocaster', description='Fender Player Stratocaster electric guitar Polar White', price=799.99, category='Music', stock=15, rating=4.8,
                image='https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=400&h=400&fit=crop'),
            Product(name='Yamaha Acoustic Guitar', description='Yamaha FG800 solid top acoustic guitar natural finish', price=249.99, category='Music', stock=25, rating=4.7,
                image='https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=400&h=400&fit=crop'),
            Product(name='Roland Digital Piano', description='Roland FP-30X digital piano 88 weighted keys bluetooth', price=699.99, category='Music', stock=10, rating=4.9,
                image='https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=400&h=400&fit=crop'),
            Product(name='Pioneer DJ Controller', description='Pioneer DDJ-400 2-channel rekordbox DJ controller', price=299.99, category='Music', stock=20, rating=4.7,
                image='https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?w=400&h=400&fit=crop'),
            Product(name='Shure SM58 Microphone', description='Shure SM58 cardioid dynamic vocal microphone', price=99.99, category='Music', stock=40, rating=4.8,
                image='https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop'),
            Product(name='Drum Kit Complete', description='Pearl Roadshow complete drum kit with cymbals jet black', price=599.99, category='Music', stock=8, rating=4.6,
                image='https://images.unsplash.com/photo-1519892300165-cb5542fb47c7?w=400&h=400&fit=crop'),
            Product(name='Violin 4/4 Set', description='Cecilio CVN-300 solidwood violin with case bow and rosin', price=149.99, category='Music', stock=20, rating=4.5,
                image='https://images.unsplash.com/photo-1558584673-c834fb1cc3ca?w=400&h=400&fit=crop'),
            Product(name='Audio Interface', description='Focusrite Scarlett 2i2 4th Gen USB audio interface', price=159.99, category='Music', stock=30, rating=4.8,
                image='https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?w=400&h=400&fit=crop'),

            # Fashion
            Product(name='Nike Air Max 270', description='Nike Air Max 270 mens running shoes black and white', price=149.99, category='Fashion', stock=60, rating=4.6,
                image='https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop'),
            Product(name='Adidas Ultraboost 23', description='Adidas Ultraboost 23 mens running shoes core black', price=179.99, category='Fashion', stock=50, rating=4.7,
                image='https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop'),
            Product(name='Leather Handbag', description='Genuine leather handbag for women brown tote bag', price=89.99, category='Fashion', stock=40, rating=4.5,
                image='https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=400&fit=crop'),
            Product(name='Ray-Ban Sunglasses', description='Ray-Ban RB3025 Aviator classic sunglasses gold frame', price=154.99, category='Fashion', stock=35, rating=4.7,
                image='https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=400&fit=crop'),
            Product(name='Casio G-Shock Watch', description='Casio G-Shock GW-M5610 solar radio controlled watch black', price=129.99, category='Fashion', stock=45, rating=4.6,
                image='https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop'),

            # Home & Kitchen
            Product(name='Instant Pot Duo 7-in-1', description='Instant Pot Duo 7-in-1 electric pressure cooker 6 quart', price=89.99, category='Home', stock=40, rating=4.8,
                image='https://images.unsplash.com/photo-1585515320310-259814833e62?w=400&h=400&fit=crop'),
            Product(name='Ninja Air Fryer', description='Ninja AF101 air fryer 4 quart capacity 1550 watts', price=99.99, category='Home', stock=35, rating=4.7,
                image='https://images.unsplash.com/photo-1585515320310-259814833e62?w=400&h=400&fit=crop'),
            Product(name='Nespresso Machine', description='Nespresso Vertuo Next coffee machine with milk frother', price=179.99, category='Home', stock=25, rating=4.8,
                image='https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=400&fit=crop'),
            Product(name='Dyson V15 Vacuum', description='Dyson V15 Detect cordless vacuum cleaner with laser', price=749.99, category='Home', stock=15, rating=4.9,
                image='https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop'),
            Product(name='KitchenAid Stand Mixer', description='KitchenAid Artisan 5-quart stand mixer empire red', price=449.99, category='Home', stock=20, rating=4.8,
                image='https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop'),

            # Sports
            Product(name='Yoga Mat Premium', description='Lululemon The Reversible Mat 5mm thick non-slip yoga mat', price=88.99, category='Sports', stock=60, rating=4.7,
                image='https://images.unsplash.com/photo-1601925228239-a5d7abcfa441?w=400&h=400&fit=crop'),
            Product(name='Adjustable Dumbbells', description='Bowflex SelectTech 552 adjustable dumbbells pair 5-52lbs', price=349.99, category='Sports', stock=20, rating=4.8,
                image='https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400&h=400&fit=crop'),
            Product(name='Treadmill Foldable', description='NordicTrack T 6.5 Si treadmill with iFIT membership', price=799.99, category='Sports', stock=10, rating=4.6,
                image='https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop'),
            Product(name='Wilson Tennis Racket', description='Wilson Pro Staff 97 v13 tennis racket 310g unstrung', price=219.99, category='Sports', stock=30, rating=4.7,
                image='https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop'),
            Product(name='Football Nike', description='Nike Premier League Flight official match football size 5', price=49.99, category='Sports', stock=80, rating=4.6,
                image='https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=400&h=400&fit=crop'),
        ]
        for p in products:
            db.session.add(p)
        db.session.commit()
        print(f"Added {len(products)} products!")

with app.app_context():
    db.create_all()
    add_sample_products()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_cart():
    return session.get('cart', {})

def get_cart_count():
    cart = get_cart()
    return sum(cart.values())

def get_cart_total():
    cart = get_cart()
    total = 0
    for product_id, qty in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            total += product.price * qty
    return round(total, 2)

app.jinja_env.globals['get_cart_count'] = get_cart_count

@app.route('/')
def home():
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    query = Product.query
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    products = query.all()
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]
    return render_template('shop_home.html', products=products, categories=categories, selected=category, search=search)

@app.route('/product/<int:id>')
def product(id):
    product = Product.query.get_or_404(id)
    related = Product.query.filter_by(category=product.category).filter(Product.id != id).limit(4).all()
    return render_template('product.html', product=product, related=related)

@app.route('/cart')
def cart():
    cart = get_cart()
    items = []
    for product_id, qty in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            items.append({'product': product, 'quantity': qty, 'subtotal': round(product.price * qty, 2)})
    return render_template('cart.html', items=items, total=get_cart_total())

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    cart = get_cart()
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    flash('Item added to cart! 🛒', 'success')
    return redirect(request.referrer or url_for('home'))

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = get_cart()
    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = get_cart()
    if not cart:
        flash('Your cart is empty!', 'danger')
        return redirect(url_for('cart'))
    if request.method == 'POST':
        order = Order(user_id=current_user.id, total=get_cart_total())
        db.session.add(order)
        db.session.flush()
        for product_id, qty in cart.items():
            product = Product.query.get(int(product_id))
            if product:
                item = OrderItem(order_id=order.id, product_id=product.id, quantity=qty, price=product.price)
                db.session.add(item)
        db.session.commit()
        session['cart'] = {}
        flash(f'Order placed successfully! Order #{order.id} 🎉', 'success')
        return redirect(url_for('orders'))
    return render_template('checkout.html', total=get_cart_total())

@app.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=user_orders)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'danger')
            return redirect(url_for('register'))
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('shop_register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid credentials!', 'danger')
    return render_template('shop_login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5007)