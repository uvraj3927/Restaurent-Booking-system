from extensions import db
from models import RestaurantTable, MenuItem

def seed_database():
    """Seeds initial restaurant tables and menu items if empty."""
    # Seed Tables
    if RestaurantTable.query.count() == 0:
        tables = [
            # 2-Seaters
            RestaurantTable(table_number="T-01", capacity=2, location_zone="Patio Terrace"),
            RestaurantTable(table_number="T-02", capacity=2, location_zone="Patio Terrace"),
            RestaurantTable(table_number="T-03", capacity=2, location_zone="Main Dining Room"),
            RestaurantTable(table_number="T-04", capacity=2, location_zone="Main Dining Room"),
            
            # 4-Seaters
            RestaurantTable(table_number="T-05", capacity=4, location_zone="Main Dining Room"),
            RestaurantTable(table_number="T-06", capacity=4, location_zone="Main Dining Room"),
            RestaurantTable(table_number="T-07", capacity=4, location_zone="Main Dining Room"),
            RestaurantTable(table_number="T-08", capacity=4, location_zone="Window Lounge"),
            
            # 6-Seaters
            RestaurantTable(table_number="T-09", capacity=6, location_zone="Main Dining Room"),
            RestaurantTable(table_number="T-10", capacity=6, location_zone="Private Alcove"),
            RestaurantTable(table_number="T-11", capacity=6, location_zone="Private Alcove"),
            
            # 8-Seaters
            RestaurantTable(table_number="T-12", capacity=8, location_zone="Private Alcove"),
            RestaurantTable(table_number="T-13", capacity=8, location_zone="Chef's Table VIP")
        ]
        db.session.add_all(tables)
        print("-> Added 13 restaurant tables.")

    # Seed Menu Items
    if MenuItem.query.count() == 0:
        items = [
            # Grills
            MenuItem(
                name="Pyrites Signature Ribeye Steak (350g)",
                category="Grills",
                description="Prime Aged Angus Ribeye grilled over hickory charcoal with rosemary butter & smoked sea salt.",
                price_inr=1499,
                image_url="https://images.unsplash.com/photo-1558030006-450675393462?auto=format&fit=crop&w=800&q=80",
                is_available=True
            ),
            MenuItem(
                name="Fire-Kissed Rosemary Lamb Chops",
                category="Grills",
                description="Tender New Zealand lamb chops marinated in garlic, mint, and woodfire smoke.",
                price_inr=1299,
                image_url="https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80",
                is_available=True
            ),
            MenuItem(
                name="Smoked Bourbon BBQ Pork Ribs",
                category="Grills",
                description="Slow-cooked full rack of baby back ribs glazed with homemade bourbon BBQ sauce.",
                price_inr=1199,
                image_url="https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?auto=format&fit=crop&w=800&q=80",
                is_available=True
            ),
            MenuItem(
                name="Charcoal Grilled Tandoori Salmon",
                category="Grills",
                description="Fresh Atlantic salmon fillet infused with aromatic Indian spices and grilled to perfection.",
                price_inr=1099,
                image_url="https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=800&q=80",
                is_available=True
            ),
            MenuItem(
                name="Char-Grilled Peri-Peri Half Chicken",
                category="Grills",
                description="Flame-roasted free-range half chicken glazed with spicy African bird's eye chili marinade.",
                price_inr=799,
                image_url="https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?auto=format&fit=crop&w=800&q=80",
                is_available=True
            ),

            # Burgers
            MenuItem(
                name="Smoked Wagyu Truffle Burger",
                category="Burgers",
                description="Double Wagyu beef patty, black truffle aioli, aged cheddar, and caramelized onions on brioche.",
                price_inr=749,
                image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80",
                is_available=True
            ),
            MenuItem(
                name="Pyrites Monster Bacon Cheeseburger",
                category="Burgers",
                description="Flame-grilled Angus patty, crispy smoked bacon, melted gouda, pickles, and signature house sauce.",
                price_inr=649,
                image_url="https://images.unsplash.com/photo-1586190848861-99aa4a171e90?auto=format&fit=crop&w=800&q=80",
                is_available=True
            ),
            MenuItem(
                name="Fiery Chipotle Grilled Chicken Burger",
                category="Burgers",
                description="Spice-rubbed grilled chicken breast, pepper jack cheese, jalapeno slaw, and chipotle Mayo.",
                price_inr=549,
                image_url="https://images.unsplash.com/photo-1625813506062-0aeb1d7a094b?auto=format&fit=crop&w=800&q=80",
                is_available=True
            ),
            MenuItem(
                name="Smokey Black Bean & Portobello Burger",
                category="Burgers",
                description="Handmade black bean patty topped with grilled portobello mushroom and vegan herb aioli.",
                price_inr=499,
                image_url="https://images.unsplash.com/photo-1520072959219-c595dc870360?auto=format&fit=crop&w=800&q=80",
                is_available=True
            ),

            # Starters
            MenuItem(
                name="Charred Garlic Butter Prawns",
                category="Starters",
                description="Jumbo tiger prawns seared on open flames with roasted garlic butter and fresh herbs.",
                price_inr=599,
                image_url="https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?auto=format&fit=crop&w=800&q=80",
                is_available=True
            ),
            MenuItem(
                name="Fire-Roasted Stuffed Mushrooms",
                category="Starters",
                description="Button mushrooms packed with cream cheese, smoked paprika, garlic, and parmesan crust.",
                price_inr=399,
                image_url="https://images.unsplash.com/photo-1625944525533-473f1a3d54e7?auto=format&fit=crop&w=800&q=80",
                is_available=True
            ),
            MenuItem(
                name="Smoked Jalapeno Cheese Poppers",
                category="Starters",
                description="Crispy golden jalapeño halves filled with sharp cheddar & cream cheese, served with ranch.",
                price_inr=349,
                image_url="https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=800&q=80",
                is_available=True
            ),

            # Sides
            MenuItem(
                name="Truffle & Parmesan Hand-Cut Fries",
                category="Sides",
                description="Crispy russet potato fries tossed in white truffle oil, grated parmesan, and sea salt.",
                price_inr=299,
                image_url="https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=800&q=80",
                is_available=True
            ),
            MenuItem(
                name="Charcoal Grilled Asparagus",
                category="Sides",
                description="Tender asparagus spears grilled over flames with lemon zest and shaved parmesan.",
                price_inr=279,
                image_url="https://images.unsplash.com/photo-1515471209610-e3b127a5c318?auto=format&fit=crop&w=800&q=80",
                is_available=True
            ),
            MenuItem(
                name="Creamy Smoky Mac & Cheese",
                category="Sides",
                description="Elbow pasta in a rich four-cheese blend infused with applewood bacon smoke.",
                price_inr=329,
                image_url="https://images.unsplash.com/photo-1543339308-43e59d6b73a6?auto=format&fit=crop&w=800&q=80",
                is_available=True
            ),

            # Drinks
            MenuItem(
                name="Pyrites Smoked Old Fashioned",
                category="Drinks",
                description="Bourbon, angostura bitters, orange peel, smoked under oakwood smoke glass.",
                price_inr=499,
                image_url="https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?auto=format&fit=crop&w=800&q=80",
                is_available=True
            ),
            MenuItem(
                name="Ember Sunset Passion Fruit Mocktail",
                category="Drinks",
                description="Fresh passion fruit pulp, blood orange, sparkling soda, and lime squeeze.",
                price_inr=249,
                image_url="https://images.unsplash.com/photo-1536935338788-846bb9981813?auto=format&fit=crop&w=800&q=80",
                is_available=True
            ),
            MenuItem(
                name="Fire & Ice Craft Berry Lemonade",
                category="Drinks",
                description="Hand-pressed lemon juice with fresh blackberry reduction and crushed mint ice.",
                price_inr=219,
                image_url="https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=800&q=80",
                is_available=True
            )
        ]
        db.session.add_all(items)
        print("-> Added 18 menu items across 5 categories.")

    db.session.commit()
    print("Database seeding completed successfully!")
