from fastapi import APIRouter
from fastapi import FastAPI, Depends


from app.api.routes import fileUpload, fileDownload, index
from fastapi.security import APIKeyHeader


API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)


api_router = APIRouter()

# app.main() 에서 router 관련 분리


# app.include_router(index.router)
api_router.include_router(fileDownload.router, tags=["Download"], prefix="/api/v1/file")
api_router.include_router(fileUpload.router, tags=["Upload"], prefix="/api/v1/file", dependencies=[Depends(API_KEY_HEADER)])


