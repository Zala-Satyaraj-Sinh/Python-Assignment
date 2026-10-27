class Product:
    def __init__(self, product_id, name, stock, purchase_price, selling_price):
        self.product_id = product_id
        self.name = name
        self.stock = stock
        self.purchase_price = purchase_price
        self.selling_price = selling_price

    def __str__(self):
        return (
            f"{self.product_id} {self.name} "
            f"stock={self.stock} "
            f"purchase={self.purchase_price} "
            f"selling={self.selling_price}"
        )


class Inventory:
    def __init__(self):
        # Dictionary gives average O(1) lookup
        self.products = {}

    # Add a product
    def add_product(self, product):
        if product.product_id in self.products:
            return "Product already exists"

        self.products[product.product_id] = product
        return "Product added"

    # Delete a product
    def delete_product(self, product_id):
        if product_id not in self.products:
            return "Product not found"

        del self.products[product_id]
        return "Product deleted"

    # Update stock
    def update_stock(self, product_id, quantity):
        if product_id not in self.products:
            return "Product not found"

        self.products[product_id].stock = quantity
        return "Stock updated"

    # Calculate total inventory value
    def total_value(self):
        total = 0

        for product in self.products.values():
            total += product.stock * product.selling_price

        return total

    # Compare inventories by total value
    def __lt__(self, other):
        return self.total_value() < other.total_value()

    # Merge inventories using +
    def __add__(self, other):
        merged = Inventory()

        # Copy products from first inventory
        for product in self.products.values():
            merged.products[product.product_id] = Product(
                product.product_id,
                product.name,
                product.stock,
                product.purchase_price,
                product.selling_price
            )

        # Merge second inventory
        for product in other.products.values():

            if product.product_id in merged.products:
                existing = merged.products[product.product_id]

                # Add stock
                existing.stock += product.stock

                # Lower purchase price
                existing.purchase_price = min(
                    existing.purchase_price,
                    product.purchase_price
                )

                # Higher selling price
                existing.selling_price = max(
                    existing.selling_price,
                    product.selling_price
                )

            else:
                merged.products[product.product_id] = Product(
                    product.product_id,
                    product.name,
                    product.stock,
                    product.purchase_price,
                    product.selling_price
                )

        return merged

    # Display inventory
    def display(self):
        for product_id in sorted(self.products):
            print(self.products[product_id])

        print("Total valuation:", self.total_value())


# -------------------------------
# Example
# -------------------------------

inventory_a = Inventory()
inventory_b = Inventory()

inventory_a.add_product(
    Product("P1", "Pen", 10, 5, 8)
)

inventory_b.add_product(
    Product("P1", "Pen", 7, 4, 9)
)

# Merge using operator overloading
merged = inventory_a + inventory_b

merged.display()