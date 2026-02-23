#!/usr/bin/env python
"""
Railway startup script - optimized for fast startup
Disables migrations on startup to avoid 502 timeouts
"""
import os
import sys
import logging

# Configure logging before anything else
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger("railway")

try:
    logger.info("🚀 Initializing ClientFlow API for Railway...")
    
    # Disable migrations during startup - they're slow and cause 502 errors
    os.environ['RUN_MIGRATIONS_ON_STARTUP'] = 'false'
    
    logger.info("✓ Environment configured")
    
    # Test imports
    logger.info("📦 Testing imports...")
    from backend.main import app
    logger.info("✓ App imported successfully")
    
    # Quick health check
    logger.info("🏥 Running health check...")
    from backend.database import engine
    from sqlalchemy import text
    
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✓ Database connection OK")
    except Exception as e:
        logger.warning(f"⚠️  Database not available yet (this is OK): {e}")
        logger.info("   App will still start - migrations can be run manually")
    
    logger.info("✅ Railway initialization complete - app ready")
    print("")
    sys.exit(0)
    
except Exception as e:
    logger.error(f"❌ Initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
