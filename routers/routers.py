from fastapi import APIRouter

from routers.auth import router as auth_router
from routers.user import router as user_router
from routers.category import router as category_router
from routers.project import router as project_router
from routers.task import router as task_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(category_router)
router.include_router(project_router)
router.include_router(task_router)
