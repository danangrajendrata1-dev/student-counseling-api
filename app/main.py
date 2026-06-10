from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.routes.health_route import router as health_router
from app.routes.auth_route import router as auth_router
from app.routes.student_route import router as student_router
from app.routes.counseling_record_route import router as counseling_record_router
from app.routes.assessment_route import router as assessment_router
from app.routes.report_route import router as report_router
from app.routes.debug_permission_route import router as debug_permission_router


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(student_router)
    app.include_router(counseling_record_router)
    app.include_router(assessment_router)
    app.include_router(report_router)
    app.include_router(report_router)

    if settings.app_env in {"development", "test"}:
        app.include_router(debug_permission_router)
      

    return app


app = create_app()