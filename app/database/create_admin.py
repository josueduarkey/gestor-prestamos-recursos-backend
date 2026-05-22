import sys
import os
from pathlib import Path

# Añadir el directorio raíz al path para poder importar la app
# Si estamos en /app/app/database, el root es /app
root_dir = str(Path(__file__).parent.parent.parent)
sys.path.append(root_dir)
os.environ["PYTHONPATH"] = root_dir

from app.database.session import SessionLocal, Base
# Importar todos los modelos para que SQLAlchemy los reconozca
import app.models.user
import app.models.laboratory
import app.models.resource
import app.models.loan
import app.models.loan_detail
import app.models.return_
import app.models.material_3d
import app.models.printing_3d

from app.services.user_service import UserService
from app.schemas.user import UserCreate

def create_admin():
    db = SessionLocal()
    service = UserService(db)
    
    admin_data = UserCreate(
        carnet=101010,
        nombre="Admin de Prueba",
        correo="admin@keytest.edu.sv",
        password="adminpassword123",
        generacion="2024",
        role="admin"
    )
    
    try:
        user = service.create_staff_user(admin_data)
        print(f"✅ Usuario Admin creado exitosamente:")
        print(f"   Carnet: {user.carnet}")
        print(f"   Email:  {user.correo}")
        print(f"   Role:   {user.role}")
    except Exception as e:
        print(f"❌ Error al crear admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
