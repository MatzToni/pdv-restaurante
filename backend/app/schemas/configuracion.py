from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ConfiguracionBase(BaseModel):
    nombre_restaurante: str = "Edén Café"
    slogan: Optional[str] = "Comida Tradicional y Café de Especialidad"
    logo_url: Optional[str] = "/logo.png"
    telefono: Optional[str] = "961 123 4567"
    direccion: Optional[str] = "Av. Central Poniente #123, Centro"
    rfc: Optional[str] = "ECA240101XYZ"
    dias_servicio: Optional[str] = "Lunes a Domingo"
    horario_apertura: Optional[str] = "08:00"
    horario_cierre: Optional[str] = "21:00"
    mensaje_ticket: Optional[str] = "🎉 ¡Gracias por su visita y preferencia! Vuelva pronto."
    titulo_carta: Optional[str] = "Nuestra Carta"
    subtitulo_carta: Optional[str] = "Platillos preparados al momento con ingredientes frescos, recetas mexicanas tradicionales y café tostado artesanal."
    nota_pie_carta: Optional[str] = "Precios incluyen IVA. Para dudas sobre ingredientes o alérgenos, consulta a tu mesero."
    ancho_papel_ticket: Optional[str] = "80mm"
    moneda: Optional[str] = "MXN"
    simbolo_moneda: Optional[str] = "$"
    abrir_cajon_automatico: bool = True
    modo_impresion: Optional[str] = "navegador"

class ConfiguracionUpdate(BaseModel):
    nombre_restaurante: Optional[str] = None
    slogan: Optional[str] = None
    logo_url: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    rfc: Optional[str] = None
    dias_servicio: Optional[str] = None
    horario_apertura: Optional[str] = None
    horario_cierre: Optional[str] = None
    mensaje_ticket: Optional[str] = None
    titulo_carta: Optional[str] = None
    subtitulo_carta: Optional[str] = None
    nota_pie_carta: Optional[str] = None
    ancho_papel_ticket: Optional[str] = None
    moneda: Optional[str] = None
    simbolo_moneda: Optional[str] = None
    abrir_cajon_automatico: Optional[bool] = None
    modo_impresion: Optional[str] = None

class ConfiguracionOut(ConfiguracionBase):
    id: int
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
