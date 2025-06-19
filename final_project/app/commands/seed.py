import click
from flask.cli import with_appcontext
from app import db
from models import User, Product, Category, Order, OrderItem, Customer, ChatSession
from datetime import datetime, timedelta
import random
import faker

fake = faker.Faker()

@click.command('seed_db')
@with_appcontext
def seed_db():
    """Seed the database with dummy data."""
    click.echo("🌱 Seeding database...")

    db.drop_all()
    db.create_all()

    # Users
    roles = ['admin', 'manager', 'customer']
    users = []
    for _ in range(10):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            role=random.choice(roles),
        )
        user.set_password("password123")
        db.session.add(user)
        users.append(user)
    db.session.commit()
    click.echo("✔️ Users added.")

    # Customers (only for 'customer' role)
    for user in users:
        if user.role == 'customer':
            customer = Customer(
                user_id=user.id,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number(),
                address=fake.address()
            )
            db.session.add(customer)
    db.session.commit()
    click.echo("✔️ Customers added.")

    # Categories
    categories = []
    for _ in range(5):
        category = Category(
            name=fake.unique.word().capitalize(),
            description=fake.sentence()
        )
        db.session.add(category)
        categories.append(category)
    db.session.commit()
    click.echo("✔️ Categories added.")

    # Products
    products = []
    for _ in range(20):
        product = Product(
            name=fake.word().capitalize(),
            description=fake.text(100),
            price=round(random.uniform(10, 300), 2),
            stock_quantity=random.randint(5, 100),
            category_id=random.choice(categories).id
        )
        db.session.add(product)
        products.append(product)
    db.session.commit()
    click.echo("✔️ Products added.")

    # Orders and OrderItems
    for user in users:
        if user.role == 'customer':
            order = Order(
                user_id=user.id,
                total_amount=0,
                status=random.choice(['pending', 'shipped', 'delivered']),
                created_at=fake.date_time_this_year()
            )
            db.session.add(order)
            db.session.flush()  # Get order.id

            total = 0
            for _ in range(random.randint(1, 3)):
                product = random.choice(products)
                quantity = random.randint(1, 4)
                item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price
                )
                total += product.price * quantity
                db.session.add(item)
            order.total_amount = round(total, 2)
    db.session.commit()
    click.echo("✔️ Orders and order items added.")

    # Chat Sessions
    for _ in range(25):
        chat = ChatSession(
            user_id=random.choice(users).id,
            description=fake.sentence(),
            response=fake.paragraph()
        )
        db.session.add(chat)
    db.session.commit()
    click.echo("✔️ Chat sessions added.")

    click.echo("🎉 Database seeding complete!")
