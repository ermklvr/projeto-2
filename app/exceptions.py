class ProductNotFoundError(Exception):
    pass

class CategoryNotFoundError(Exception):
    pass

class InsufficientStockError(Exception):
    pass

class CategoryHasProductsError(Exception):
    pass

class MovementNotFoundError(Exception):
    pass