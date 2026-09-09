from fastapi import FastAPI

from .routers import categories, products, movements



app = FastAPI(title="API Gestão de Inventário")


#inclusão de rotas
app.include_router(categories.router)
#app.include_router(movements.router)
#app.include_router(products.router)



