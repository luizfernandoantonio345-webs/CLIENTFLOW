"""
Public endpoints - no authentication required.
These are accessible from the frontend without JWT.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/health")
def health_check():
    """Public health check - indicates server is alive"""
    return {
        "status": "ok",
        "service": "ClientFlow API",
        "version": "1.0.0"
    }


@router.get("/barbershop/{barber_id}")
def get_barbershop_public(barber_id: str):
    """Public barbershop info endpoint (placeholder for future)"""
    return {
        "id": barber_id,
        "available": True,
        "status": "online"
    }


@router.get("/status")
def server_status():
    """Public server status endpoint for Railway health checks"""
    return {
        "status": "running",
        "ready": True,
        "service": "clientflow-api"
    }
