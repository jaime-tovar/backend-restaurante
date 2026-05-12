from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.auth import get_current_user
from src.database.config import get_db
from src.entities.cliente import Cliente
from src.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter(
    prefix="/clientes", tags=["clientes"], dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=list[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id_cliente == cliente_id).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return cliente


@router.post("", response_model=ClienteResponse, status_code=201)
def crear_cliente(dato: ClienteCreate, db: Session = Depends(get_db)):
    # validar que no exista el correo
    existe = db.query(Cliente).filter(Cliente.email == dato.email).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="El cliente ya existe",
        )

    cliente = Cliente(
        nombre=dato.nombre,
        apellido=dato.apellido,
        email=dato.email,
        telefono=dato.telefono,
        activo=dato.activo,
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    return cliente


@router.put("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(
    cliente_id: UUID, dato: ClienteUpdate, db: Session = Depends(get_db)
):
    cliente = db.query(Cliente).filter(Cliente.id_cliente == cliente_id).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # validar que no exista el correo
    existe = (
        db.query(Cliente)
        .filter(Cliente.email == dato.email, Cliente.id_cliente != cliente_id)
        .first()
    )

    if existe:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está en uso por otro cliente",
        )

    cliente.nombre = dato.nombre
    cliente.apellido = dato.apellido
    cliente.email = dato.email
    cliente.telefono = dato.telefono
    cliente.activo = dato.activo

    db.commit()
    db.refresh(cliente)

    return cliente


@router.delete("/{cliente_id}", status_code=204)
def eliminar_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id_cliente == cliente_id).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    db.delete(cliente)
    db.commit()
