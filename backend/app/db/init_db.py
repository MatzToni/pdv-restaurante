from sqlalchemy.orm import Session
from app.db.session import engine, SessionLocal, Base
from app.models import (
    Usuario, RolUsuario,
    Area, Mesa, EstadoMesa,
    Categoria, Producto,
    ArticuloInventario, TipoArticulo,
    Receta
)

# En producción se utiliza bcrypt; para el seed inicial asignamos contraseñas hasheadas o identificadores
def init_db(db: Session) -> None:
    # 1. Crear todas las tablas en PostgreSQL si no existen
    Base.metadata.create_all(bind=engine)

    # Si ya existen usuarios, no re-sembrar
    if db.query(Usuario).first():
        print("Base de datos ya inicializada con datos previos.")
        return

    print("Inicializando base de datos de Edén Café con datos semilla...")

    # 2. Usuarios con sus Roles
    admin = Usuario(
        nombre="Administrador Edén",
        email="admin@edencafe.com",
        password_hash="admin123",
        rol=RolUsuario.ADMINISTRADOR,
        pin_seguridad="1111",
        activo=True
    )
    gerente = Usuario(
        nombre="Gerente General",
        email="gerente@edencafe.com",
        password_hash="gerente123",
        rol=RolUsuario.GERENTE,
        pin_seguridad="2222",
        activo=True
    )
    jefe = Usuario(
        nombre="Jefe de Turno",
        email="jefe@edencafe.com",
        password_hash="jefe123",
        rol=RolUsuario.JEFE,
        pin_seguridad="3333",
        activo=True
    )
    cocinero = Usuario(
        nombre="Chef Cocina",
        email="cocina@edencafe.com",
        password_hash="cocina123",
        rol=RolUsuario.COCINA,
        pin_seguridad="4444",
        activo=True
    )
    mesero1 = Usuario(
        nombre="Carlos López",
        email="carlos@edencafe.com",
        password_hash="mesero123",
        rol=RolUsuario.MESERO,
        pin_seguridad="5555",
        activo=True
    )
    auxiliar = Usuario(
        nombre="Auxiliar Bodega",
        email="auxiliar@edencafe.com",
        password_hash="auxiliar123",
        rol=RolUsuario.AUXILIAR_GENERAL,
        pin_seguridad="6666",
        activo=True
    )
    db.add_all([admin, gerente, jefe, cocinero, mesero1, auxiliar])
    db.commit()

    # 3. Áreas y Mesas
    salon = Area(nombre="Salón Principal")
    terraza = Area(nombre="Terraza Jardín")
    barra = Area(nombre="Barra Café")
    db.add_all([salon, terraza, barra])
    db.commit()

    mesas = [
        Mesa(numero="Mesa 1", area_id=salon.id, capacidad=4, estado=EstadoMesa.LIBRE),
        Mesa(numero="Mesa 2", area_id=salon.id, capacidad=2, estado=EstadoMesa.OCUPADA),
        Mesa(numero="Mesa 3", area_id=salon.id, capacidad=4, estado=EstadoMesa.LIBRE),
        Mesa(numero="Mesa 4", area_id=salon.id, capacidad=6, estado=EstadoMesa.LIBRE),
        Mesa(numero="Mesa 5", area_id=salon.id, capacidad=4, estado=EstadoMesa.CUENTA),
        Mesa(numero="Terraza 1", area_id=terraza.id, capacidad=4, estado=EstadoMesa.LIBRE),
        Mesa(numero="Terraza 2", area_id=terraza.id, capacidad=4, estado=EstadoMesa.LIBRE),
        Mesa(numero="Terraza 3", area_id=terraza.id, capacidad=2, estado=EstadoMesa.LIBRE),
        Mesa(numero="Barra 1", area_id=barra.id, capacidad=1, estado=EstadoMesa.LIBRE),
        Mesa(numero="Barra 2", area_id=barra.id, capacidad=1, estado=EstadoMesa.LIBRE),
    ]
    db.add_all(mesas)
    db.commit()

    # 4. Inventario clasificado por tipos
    # A) Ingredientes (recetas)
    cafe_grano = ArticuloInventario(nombre="Café en grano selección Edén", tipo=TipoArticulo.INGREDIENTE, unidad_medida="kg", stock_actual=25.0, stock_minimo=5.0, costo_unitario=280.0)
    leche_entera = ArticuloInventario(nombre="Leche entera pasteurizada", tipo=TipoArticulo.INGREDIENTE, unidad_medida="lt", stock_actual=40.0, stock_minimo=10.0, costo_unitario=26.0)
    pollo_pechuga = ArticuloInventario(nombre="Pechuga de pollo fresca", tipo=TipoArticulo.INGREDIENTE, unidad_medida="kg", stock_actual=18.0, stock_minimo=4.0, costo_unitario=125.0)
    tortillas = ArticuloInventario(nombre="Tortilla de maíz nixtamalizada", tipo=TipoArticulo.INGREDIENTE, unidad_medida="kg", stock_actual=15.0, stock_minimo=3.0, costo_unitario=22.0)
    carne_res = ArticuloInventario(nombre="Carne de res para hamburguesa", tipo=TipoArticulo.INGREDIENTE, unidad_medida="kg", stock_actual=12.0, stock_minimo=3.0, costo_unitario=190.0)
    piloncillo_canela = ArticuloInventario(nombre="Piloncillo y canela para café", tipo=TipoArticulo.INGREDIENTE, unidad_medida="kg", stock_actual=8.0, stock_minimo=2.0, costo_unitario=65.0)
    
    # B) Desechables
    vaso_12oz = ArticuloInventario(nombre="Vaso térmico para café 12oz", tipo=TipoArticulo.DESECHABLE, unidad_medida="pza", stock_actual=500.0, stock_minimo=100.0, costo_unitario=1.80)
    tapa_12oz = ArticuloInventario(nombre="Tapa para vaso 12oz", tipo=TipoArticulo.DESECHABLE, unidad_medida="pza", stock_actual=500.0, stock_minimo=100.0, costo_unitario=0.90)
    servilletas = ArticuloInventario(nombre="Servilleta de papel kraft", tipo=TipoArticulo.DESECHABLE, unidad_medida="pza", stock_actual=2000.0, stock_minimo=300.0, costo_unitario=0.15)
    
    # C) Utensilios / Vajilla
    platos_barro = ArticuloInventario(nombre="Platos trinche de cerámica artesanal", tipo=TipoArticulo.UTENSILIO, unidad_medida="pza", stock_actual=48.0, stock_minimo=12.0, costo_unitario=75.0)
    tazas_cafe = ArticuloInventario(nombre="Tazas de café Edén", tipo=TipoArticulo.UTENSILIO, unidad_medida="pza", stock_actual=60.0, stock_minimo=15.0, costo_unitario=45.0)
    colador = ArticuloInventario(nombre="Colador de malla fina para cocina", tipo=TipoArticulo.UTENSILIO, unidad_medida="pza", stock_actual=4.0, stock_minimo=2.0, costo_unitario=85.0)
    
    # D) Limpieza
    escoba = ArticuloInventario(nombre="Escoba uso rudo para restaurante", tipo=TipoArticulo.LIMPIEZA, unidad_medida="pza", stock_actual=5.0, stock_minimo=2.0, costo_unitario=95.0)
    jabon_trastes = ArticuloInventario(nombre="Detergente líquido concentrado", tipo=TipoArticulo.LIMPIEZA, unidad_medida="lt", stock_actual=20.0, stock_minimo=5.0, costo_unitario=42.0)
    
    db.add_all([
        cafe_grano, leche_entera, pollo_pechuga, tortillas, carne_res, piloncillo_canela,
        vaso_12oz, tapa_12oz, servilletas,
        platos_barro, tazas_cafe, colador,
        escoba, jabon_trastes
    ])
    db.commit()

    # 5. Categorías y Productos del Menú
    cat_cafe = Categoria(nombre="Cafetería Tradicional", descripcion="Café de especialidad y recetas tradicionales", orden=1)
    cat_desayunos = Categoria(nombre="Desayunos Tradicionales", descripcion="Chilaquiles, huevos y antojitos", orden=2)
    cat_fuertes = Categoria(nombre="Platos Fuertes", descripcion="Comidas completas tradicionales", orden=3)
    cat_bebidas = Categoria(nombre="Bebidas Frías", descripcion="Aguas frescas y refrescos", orden=4)
    db.add_all([cat_cafe, cat_desayunos, cat_fuertes, cat_bebidas])
    db.commit()

    prod_cafe_olla = Producto(categoria_id=cat_cafe.id, nombre="Café de Olla Tradicional", descripcion="Café de grano con piloncillo y canela", precio=45.0, requiere_cocina=True)
    prod_cafe_leche = Producto(categoria_id=cat_cafe.id, nombre="Café con Leche Cremoso", descripcion="Espresso doble con leche espumada", precio=55.0, requiere_cocina=True)
    prod_chilaquiles = Producto(categoria_id=cat_desayunos.id, nombre="Chilaquiles Verdes con Pollo", descripcion="Totopos artesanales bañados en salsa verde con pollo deshebrado, crema y queso", precio=135.0, requiere_cocina=True)
    prod_hamburguesa = Producto(categoria_id=cat_fuertes.id, nombre="Hamburguesa Edén Especial", descripcion="Carne de res 200g, queso gratinado y aderezo de la casa", precio=185.0, requiere_cocina=True)
    prod_limonada = Producto(categoria_id=cat_bebidas.id, nombre="Limonada con Chía", descripcion="Limón recién exprimido con semillas de chía", precio=48.0, requiere_cocina=False)

    db.add_all([prod_cafe_olla, prod_cafe_leche, prod_chilaquiles, prod_hamburguesa, prod_limonada])
    db.commit()

    # 6. Recetas (Escandallo para descuento automático de stock)
    recetas = [
        # Café de Olla: 20g café, 10g canela/piloncillo
        Receta(producto_id=prod_cafe_olla.id, articulo_id=cafe_grano.id, cantidad_requerida=0.020),
        Receta(producto_id=prod_cafe_olla.id, articulo_id=piloncillo_canela.id, cantidad_requerida=0.010),
        # Café con Leche: 20g café, 250ml leche
        Receta(producto_id=prod_cafe_leche.id, articulo_id=cafe_grano.id, cantidad_requerida=0.020),
        Receta(producto_id=prod_cafe_leche.id, articulo_id=leche_entera.id, cantidad_requerida=0.250),
        # Chilaquiles con Pollo: 150g tortillas, 120g pechuga pollo
        Receta(producto_id=prod_chilaquiles.id, articulo_id=tortillas.id, cantidad_requerida=0.150),
        Receta(producto_id=prod_chilaquiles.id, articulo_id=pollo_pechuga.id, cantidad_requerida=0.120),
        # Hamburguesa: 200g carne de res
        Receta(producto_id=prod_hamburguesa.id, articulo_id=carne_res.id, cantidad_requerida=0.200),
    ]
    db.add_all(recetas)
    db.commit()

    print("¡Base de datos sembrada exitosamente con usuarios, mesas, productos, inventario y recetas!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
