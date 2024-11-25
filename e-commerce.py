from fastapi import FastAPI, HTTPException
from models import Product

# Initialize FastAPI app
app = FastAPI()

# In-memory product database
products = []

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce API"}

# Get all products
@app.get("/products")
def get_products():
    if not products:
        return {"message": "No products available"}
    return {"products": products}

# Get a single product by ID
@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {"product": product}
    raise HTTPException(status_code=404, detail="Product not found")

# Add a new product
@app.post("/products")
def add_product(product: Product):
    # Check for duplicate ID
    for p in products:
        if p["id"] == product.id:
            raise HTTPException(status_code=400, detail="Product ID already exists")
    products.append(product.dict())
    return {"message": "Product added successfully", "product": product}

# Update a product
@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            products[index] = updated_product.dict()
            return {"message": "Product updated successfully", "product": updated_product}
    raise HTTPException(status_code=404, detail="Product not found")

# Delete a product
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            products.pop(index)
            return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")
