/**
 * Utilidad para formateo e impresión de tickets térmicos (80mm / 58mm)
 * Compatible con impresoras de tickets térmicas y visor estándar de navegador.
 */

function obtenerDatosNegocio() {
  let cfg = {
    nombreRestaurante: 'Edén Café',
    slogan: 'Comida Tradicional y Café',
    direccion: '',
    telefono: '',
    rfc: '',
    anchoPapelTicket: '80mm'
  }
  try {
    const raw = localStorage.getItem('eden_configuracion')
    if (raw) {
      cfg = { ...cfg, ...JSON.parse(raw) }
    }
  } catch (e) {
    console.error('Error leyendo datos de negocio para ticket:', e)
  }
  return cfg
}

export function generarTicketPreCuenta(orden, mensajePersonalizado = '') {
  const negocio = obtenerDatosNegocio()
  const fecha = new Date().toLocaleString('es-MX', {
    dateStyle: 'short',
    timeStyle: 'short'
  })

  const itemsValidos = orden.items?.filter(i => i.estado !== 'cancelado') || []
  const subtotalProds = Number(orden.subtotal || orden.total)
  const costoEnvio = Number(orden.costo_envio || 0)
  const total = Number(orden.total)

  // Sugerencias de propina
  const p10 = (total * 0.10).toFixed(2)
  const p15 = (total * 0.15).toFixed(2)
  const p20 = (total * 0.20).toFixed(2)

  const itemsHtml = itemsValidos.map(i => {
    const itemTotal = (Number(i.precio_unitario) * i.cantidad).toFixed(2)
    const extraTxt = i.extras?.length ? `<div style="font-size: 10px; color: #555;">+ ${i.extras.map(e => e.nombre).join(', ')}</div>` : ''
    const llevarTxt = i.para_llevar ? `<div style="font-size: 10px; color: #555;">[Para llevar: +$${(Number(i.cargo_desechable || 0) * i.cantidad).toFixed(2)}]</div>` : ''
    return `
      <tr>
        <td style="text-align: left; vertical-align: top; padding: 2px 0;">
          ${i.cantidad}x ${i.producto_nombre}
          ${extraTxt}
          ${llevarTxt}
        </td>
        <td style="text-align: right; vertical-align: top; padding: 2px 0; font-family: monospace;">$${itemTotal}</td>
      </tr>
    `
  }).join('')

  const clienteEnvioHtml = orden.datos_entrega ? `
    <div style="margin: 6px 0; padding: 4px; border: 1px dashed #777; font-size: 11px;">
      <div><strong>Cliente:</strong> ${orden.datos_entrega.cliente || 'N/A'}</div>
      ${orden.datos_entrega.telefono ? `<div><strong>Tel:</strong> ${orden.datos_entrega.telefono}</div>` : ''}
      ${orden.datos_entrega.direccion ? `<div><strong>Dirección:</strong> ${orden.datos_entrega.direccion}</div>` : ''}
    </div>
  ` : ''

  const anchoPx = negocio.anchoPapelTicket === '58mm' ? '200px' : '280px'

  return `
    <div style="font-family: 'Courier New', Courier, monospace; width: ${anchoPx}; margin: 0 auto; color: #000; font-size: 12px; line-height: 1.3;">
      <div style="text-align: center; margin-bottom: 8px;">
        <h2 style="margin: 0; font-size: 18px; font-weight: bold; text-transform: uppercase;">${negocio.nombreRestaurante}</h2>
        <div style="font-size: 11px;">${negocio.slogan}</div>
        ${negocio.direccion ? `<div style="font-size: 10px; color: #444;">${negocio.direccion}</div>` : ''}
        ${negocio.telefono ? `<div style="font-size: 10px; color: #444;">Tel: ${negocio.telefono}</div>` : ''}
        <div style="font-size: 10px; color: #555; margin-top: 2px;">*** PRE-CUENTA (NO FISCAL) ***</div>
      </div>

      <div style="border-top: 1px dashed #000; border-bottom: 1px dashed #000; padding: 4px 0; margin-bottom: 6px; font-size: 11px;">
        <div><strong>Folio:</strong> #${orden.id}</div>
        <div><strong>Referencia:</strong> ${orden.mesa_numero || `Mesa ${orden.mesa_id || 'Mostrador'}`}</div>
        <div><strong>Mesero:</strong> ${orden.mesero_nombre || 'N/A'}</div>
        <div><strong>Fecha:</strong> ${fecha}</div>
        ${orden.tipo_pedido !== 'comedor' ? `<div><strong>Tipo:</strong> ${orden.tipo_pedido.toUpperCase()}</div>` : ''}
      </div>

      ${clienteEnvioHtml}

      <table style="width: 100%; border-collapse: collapse; font-size: 11px; margin-bottom: 8px;">
        <thead>
          <tr style="border-bottom: 1px solid #000;">
            <th style="text-align: left; padding-bottom: 2px;">CANT / DESCRIPCIÓN</th>
            <th style="text-align: right; padding-bottom: 2px;">IMPORTE</th>
          </tr>
        </thead>
        <tbody>
          ${itemsHtml}
        </tbody>
      </table>

      <div style="border-top: 1px dashed #000; padding-top: 4px; font-size: 11px;">
        <div style="display: flex; justify-content: space-between;">
          <span>Subtotal:</span>
          <span style="font-family: monospace;">$${(total - costoEnvio).toFixed(2)}</span>
        </div>
        ${costoEnvio > 0 ? `
          <div style="display: flex; justify-content: space-between;">
            <span>Envío / Entrega:</span>
            <span style="font-family: monospace;">+$${costoEnvio.toFixed(2)}</span>
          </div>
        ` : ''}
        ${Number(orden.descuento || 0) > 0 ? `
          <div style="display: flex; justify-content: space-between; color: #555;">
            <span>Descuento aplicado:</span>
            <span style="font-family: monospace;">-$${Number(orden.descuento).toFixed(2)}</span>
          </div>
        ` : ''}
        <div style="display: flex; justify-content: space-between; font-size: 15px; font-weight: bold; margin-top: 4px; border-top: 1px solid #000; padding-top: 4px;">
          <span>TOTAL:</span>
          <span style="font-family: monospace;">$${total.toFixed(2)}</span>
        </div>
      </div>

      <div style="margin-top: 10px; padding: 6px; border: 1px dashed #aaa; font-size: 10px;">
        <div style="text-align: center; font-weight: bold; margin-bottom: 3px;">SUGERENCIAS DE PROPINA (VOLUNTARIA)</div>
        <div style="display: flex; justify-content: space-between;"><span>10%: $${p10}</span> <span>Total: $${(total + Number(p10)).toFixed(2)}</span></div>
        <div style="display: flex; justify-content: space-between;"><span>15%: $${p15}</span> <span>Total: $${(total + Number(p15)).toFixed(2)}</span></div>
        <div style="display: flex; justify-content: space-between;"><span>20%: $${p20}</span> <span>Total: $${(total + Number(p20)).toFixed(2)}</span></div>
      </div>

      ${mensajePersonalizado ? `
        <div style="margin-top: 8px; padding: 6px; border: 1px dashed #555; text-align: center; font-size: 11px; white-space: pre-line; background: #fafafa;">
          ${mensajePersonalizado}
        </div>
      ` : ''}

      <div style="text-align: center; margin-top: 12px; font-size: 10px;">
        <div>¡Gracias por su visita y preferencia!</div>
        <div style="margin-top: 4px; color: #777;">Favor de solicitar su ticket final al liquidar en caja.</div>
      </div>
    </div>
  `
}

export function generarTicketVenta(pago, orden, mensajePersonalizado = '') {
  const negocio = obtenerDatosNegocio()
  const fecha = new Date(pago.fecha || Date.now()).toLocaleString('es-MX', {
    dateStyle: 'short',
    timeStyle: 'short'
  })

  const itemsValidos = orden?.items?.filter(i => i.estado !== 'cancelado') || []
  const subtotal = Number(orden?.total || pago.monto)
  const propina = Number(pago.propina || 0)
  const granTotal = subtotal + propina
  const recibido = Number(pago.monto_recibido || (subtotal + propina))
  const cambio = Number(pago.cambio || 0)

  const itemsHtml = itemsValidos.map(i => {
    const itemTotal = (Number(i.precio_unitario) * i.cantidad).toFixed(2)
    return `
      <tr>
        <td style="text-align: left; padding: 2px 0;">${i.cantidad}x ${i.producto_nombre}</td>
        <td style="text-align: right; padding: 2px 0; font-family: monospace;">$${itemTotal}</td>
      </tr>
    `
  }).join('')

  const anchoPx = negocio.anchoPapelTicket === '58mm' ? '200px' : '280px'

  return `
    <div style="font-family: 'Courier New', Courier, monospace; width: ${anchoPx}; margin: 0 auto; color: #000; font-size: 12px; line-height: 1.3;">
      <div style="text-align: center; margin-bottom: 8px;">
        <h2 style="margin: 0; font-size: 18px; font-weight: bold; text-transform: uppercase;">${negocio.nombreRestaurante}</h2>
        <div style="font-size: 11px;">${negocio.slogan}</div>
        ${negocio.direccion ? `<div style="font-size: 10px; color: #444;">${negocio.direccion}</div>` : ''}
        ${negocio.telefono ? `<div style="font-size: 10px; color: #444;">Tel: ${negocio.telefono}</div>` : ''}
        ${negocio.rfc ? `<div style="font-size: 9px; color: #555;">RFC: ${negocio.rfc}</div>` : ''}
        <div style="font-size: 10px; color: #555; margin-top: 2px;">TICKET DE VENTA Y PAGO</div>
      </div>

      <div style="border-top: 1px dashed #000; border-bottom: 1px dashed #000; padding: 4px 0; margin-bottom: 6px; font-size: 11px;">
        <div><strong>Ticket:</strong> #${pago.id} (Orden #${pago.orden_id})</div>
        <div><strong>Mesa:</strong> ${orden?.mesa_numero || `Mesa ${orden?.mesa_id || 'Mostrador'}`}</div>
        <div><strong>Mesero:</strong> ${orden?.mesero_nombre || 'N/A'}</div>
        <div><strong>Fecha:</strong> ${fecha}</div>
        <div><strong>Método de Pago:</strong> ${pago.metodo ? pago.metodo.toUpperCase() : 'EFECTIVO'}</div>
      </div>

      <table style="width: 100%; border-collapse: collapse; font-size: 11px; margin-bottom: 8px;">
        <thead>
          <tr style="border-bottom: 1px solid #000;">
            <th style="text-align: left; padding-bottom: 2px;">CANT / PRODUCTO</th>
            <th style="text-align: right; padding-bottom: 2px;">IMPORTE</th>
          </tr>
        </thead>
        <tbody>
          ${itemsHtml}
        </tbody>
      </table>

      <div style="border-top: 1px dashed #000; padding-top: 4px; font-size: 11px;">
        <div style="display: flex; justify-content: space-between;">
          <span>Consumo:</span>
          <span style="font-family: monospace;">$${subtotal.toFixed(2)}</span>
        </div>
        ${Number(orden?.descuento || 0) > 0 ? `
          <div style="display: flex; justify-content: space-between; color: #555;">
            <span>Descuento aplicado:</span>
            <span style="font-family: monospace;">-$${Number(orden.descuento).toFixed(2)}</span>
          </div>
        ` : ''}
        ${propina > 0 ? `
          <div style="display: flex; justify-content: space-between;">
            <span>Propina:</span>
            <span style="font-family: monospace;">+$${propina.toFixed(2)}</span>
          </div>
        ` : ''}
        <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: bold; margin-top: 3px; border-top: 1px solid #000; padding-top: 3px;">
          <span>TOTAL PAGADO:</span>
          <span style="font-family: monospace;">$${granTotal.toFixed(2)}</span>
        </div>
        ${pago.metodo === 'efectivo' ? `
          <div style="display: flex; justify-content: space-between; margin-top: 4px;">
            <span>Entregado:</span>
            <span style="font-family: monospace;">$${recibido.toFixed(2)}</span>
          </div>
          <div style="display: flex; justify-content: space-between; font-weight: bold;">
            <span>Cambio:</span>
            <span style="font-family: monospace;">$${cambio.toFixed(2)}</span>
          </div>
        ` : ''}
      </div>

      ${mensajePersonalizado ? `
        <div style="margin-top: 8px; padding: 6px; border: 1px dashed #555; text-align: center; font-size: 11px; white-space: pre-line; background: #fafafa;">
          ${mensajePersonalizado}
        </div>
      ` : ''}

      <div style="text-align: center; margin-top: 12px; font-size: 10px;">
        <div>¡CUENTA PAGADA - GRACIAS POR SU COMPRA!</div>
        <div style="margin-top: 4px; color: #777;">Esperamos verle pronto de vuelta en ${negocio.nombreRestaurante}.</div>
      </div>
    </div>
  `
}

export function generarTicketPruebaHardware(ancho = '80mm') {
  const negocio = obtenerDatosNegocio()
  const fecha = new Date().toLocaleString('es-MX', {
    dateStyle: 'full',
    timeStyle: 'medium'
  })

  const anchoPx = ancho === '58mm' ? '200px' : '280px'

  return `
    <div style="font-family: 'Courier New', Courier, monospace; width: ${anchoPx}; margin: 0 auto; color: #000; font-size: 12px; line-height: 1.3;">
      <div style="text-align: center; margin-bottom: 8px;">
        <h2 style="margin: 0; font-size: 18px; font-weight: bold; text-transform: uppercase;">${negocio.nombreRestaurante}</h2>
        <div style="font-size: 11px;">${negocio.slogan}</div>
        <div style="font-size: 11px; font-weight: bold; margin-top: 4px; padding: 3px; border: 1px solid #000;">
          *** PRUEBA DE HARDWARE POS ***
        </div>
      </div>

      <div style="border-top: 1px dashed #000; border-bottom: 1px dashed #000; padding: 4px 0; margin-bottom: 6px; font-size: 11px;">
        <div><strong>Dispositivo:</strong> Impresora Térmica (${ancho})</div>
        <div><strong>Cajón de Dinero:</strong> Puerto DK / RJ11</div>
        <div><strong>Fecha/Hora:</strong> ${fecha}</div>
        ${negocio.direccion ? `<div><strong>Dirección:</strong> ${negocio.direccion}</div>` : ''}
        ${negocio.telefono ? `<div><strong>Teléfono:</strong> ${negocio.telefono}</div>` : ''}
      </div>

      <div style="margin: 8px 0; font-size: 11px; text-align: justify;">
        ¡Enhorabuena! Si este ticket se imprimió con claridad y el papel se cortó, tu impresora térmica está correctamente comunicada con el sistema.
      </div>

      <div style="border: 1px dashed #000; padding: 6px; margin: 8px 0; font-size: 10px; text-align: center; background: #fafafa;">
        <strong>COMPROBACIÓN DEL CAJÓN DE COBRO:</strong><br/>
        El pulso de apertura se envió a través del puerto RJ11 (DK). Si el cajón de dinero se botó automáticamente, tu configuración está 100% lista para operaciones en caja.
      </div>

      <div style="text-align: center; font-size: 10px; margin-top: 10px;">
        <div>================================</div>
        <div>PRUEBA EXITOSA - EDÉN CAFÉ PDV</div>
        <div>================================</div>
      </div>
    </div>
  `
}

export function imprimirContenidoHtml(html) {
  const printWindow = window.open('', '_blank', 'width=380,height=600')
  if (!printWindow) {
    alert('Por favor permite ventanas emergentes (pop-ups) en tu navegador para imprimir tickets.')
    return
  }

  printWindow.document.write(`
    <!DOCTYPE html>
    <html lang="es">
      <head>
        <meta charset="utf-8">
        <title>Impresión de Ticket - Edén Café</title>
        <style>
          @page {
            margin: 3mm;
            size: auto;
          }
          body {
            margin: 0;
            padding: 4px;
            background: #fff;
            color: #000;
          }
        </style>
      </head>
      <body>
        ${html}
      </body>
    </html>
  `)
  printWindow.document.close()
  printWindow.focus()

  setTimeout(() => {
    printWindow.print()
    printWindow.close()
  }, 300)
}
