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