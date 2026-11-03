from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class ConfiguracionSistema(Base):
    __tablename__ = "configuracion_sistema"

    id = Column(Integer, primary_key=True, default=1)
    nombre_restaurante = Column(String(150), default="Edén Café", nullable=False)
    slogan = Column(String(250), default="Comida Tradicional y Café de Especialidad", nullable=True)
    logo_url = Column(Text, default="/logo.png", nullable=True)
    telefono = Column(String(50), default="961 123 4567", nullable=True)
    direccion = Column(String(250), default="Av. Central Poniente #123, Centro", nullable=True)
    rfc = Column(String(30), default="ECA240101XYZ", nullable=True)
    dias_servicio = Column(String(100), default="Lunes a Domingo", nullable=True)
    horario_apertura = Column(String(20), default="08:00", nullable=True)
    horario_cierre = Column(String(20), default="21:00", nullable=True)
    mensaje_ticket = Column(Text, default="🎉 ¡Gracias por su visita y preferencia! Vuelva pronto.", nullable=True)
    titulo_carta = Column(String(150), default="Nuestra Carta", nullable=True)
    subtitulo_carta = Column(Text, default="Platillos preparados al momento con ingredientes frescos, recetas mexicanas tradicionales y café tostado artesanal.", nullable=True)
    nota_pie_carta = Column(Text, default="Precios incluyen IVA. Para dudas sobre ingredientes o alérgenos, consulta a tu mesero.", nullable=True)
    ancho_papel_ticket = Column(String(20), default="80mm", nullable=True)
    moneda = Column(String(10), default="MXN", nullable=True)
    simbolo_moneda = Column(String(5), default="$", nullable=True)
    abrir_cajon_automatico = Column(Boolean, default=True, nullable=False)
    modo_impresion = Column(String(30), default="navegador", nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
