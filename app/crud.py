from .models import Category





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