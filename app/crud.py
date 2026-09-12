from .models import Category, Product, Movement, MovementType





#-----------CRUD--------------

#-----------CATEGORY-----------
#-----------CREATE ------------
def create_category(db,category):
    new_category = Category(name=category.name)
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
        
    return new_category

#-----------READ------------
#----Lê todos os ID
def get_categories(db):
    return db.query(Category).order_by(Category.id.asc()).all()

#---Lê somente um ID
def get_category_by_id(db,category_id):
    return db.query(Category).filter(Category.id == category_id).first()

#-----------UPDATE------------
def update_category(db, category_id,category):
    up_category = db.query(Category).filter(Category.id == category_id).first()
    
    if not up_category:
        return None
    
    up_category.name  = category.name
    db.commit()
    db.refresh(up_category)
    return up_category
    
    

#-----------DELETE------------
def delete_category(db,category_id):
    del_category = db.query(Category).filter(Category.id == category_id).first()
    
    if not del_category:
            return None
    
    db.delete(del_category)
    db.commit()
    
    return del_category





#-----------PRODUCTS-----------
#-----------CREATE ------------
def new_product(db, product):
    category = db.query(Category).filter(Category.id == product.category_id).first()
    
    if not category:
        return None
    
    new_product = Product(
        name = product.name,
        price=product.price,
        stock_quantity=product.stock_quantity,
        category_id=product.category_id 
        )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
        
    return new_product
#-----------READ------------
#---- todos os produtos
def get_products(db):
    return db.query(Product).order_by(Product.id.asc()).all()

#--- um unico produto
def get_product_by_id(db,product_id):
    return db.query(Product).filter(Product.id == product_id).first()
#-----------UPDATE------------
def update_product(db, product_id, product):
    up_product = db.query(Product).filter(Product.id == product_id).first()

    if not up_product:
        return None
    
    category = db.query(Category).filter(Category.id == product.category_id).first()

    if not category:
        return None

    up_product.name = product.name
    up_product.price = product.price
    up_product.stock_quantity = product.stock_quantity
    up_product.category_id = product.category_id
    db.commit()
    db.refresh(up_product)
    return up_product
   
#-----------DELETE------------
def delete_product(db,product_id):
    deleted_product = db.query(Product).filter(Product.id == product_id).first()
    
    if not deleted_product:
        return None
    
    db.delete(deleted_product)
    db.commit()
        
    return deleted_product





#-----------MOVEMENTS-----------
#-----------CREATE ------------
def create_movement(db, movement):
    product = db.query(Product).filter(Product.id == movement.product_id).first()
    
    if not product:
        return None
    
    if movement.type == MovementType.IN:
        product.stock_quantity += movement.quantity
    else: # aqui assume-se que as duas unicas entradas de type são in e out
        if product.stock_quantity < movement.quantity:
            return None
         
        product.stock_quantity -= movement.quantity
        
    new_movement = Movement (
        product_id = movement.product_id,
        type  =  movement.type,
        quantity = movement.quantity   
)
    
    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)
    
    return new_movement
        

#-----------READ ------------
#-----------UPDATE ------------
#-----------DELETE ------------