"""
Redirection from / and /api to swagger-ui is defined here.
"""
from fastapi import APIRouter
import fastapi
from starlette import status


api_router = APIRouter(tags=["system"])


@api_router.get(
    "/",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
@api_router.get(
    "/api/",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
async def redirect_to_swagger_docs():
    "Redirects to **/docs** from **/**"
    return fastapi.responses.RedirectResponse("/docs", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
