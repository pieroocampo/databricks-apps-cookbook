"""V1 API routes."""

from fastapi import APIRouter

from .healthcheck import router as healthcheck_router
from .tables import router as tables_router
from .volumes import router as volumes_router


router = APIRouter()

# Include endpoint-specific routers
router.include_router(healthcheck_router)
router.include_router(tables_router)
router.include_router(volumes_router)
