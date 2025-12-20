// utils/reporteCooperativista.js
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'
import * as QRCode from 'qrcode'

/**
 * Genera un PDF de perfil del cooperativista en formato A4
 * @param {Object} cooperativista - Datos del cooperativista
 * @param {String} cuadrillaName - Nombre de la cuadrilla
 * @param {String} seccionName - Nombre de la sección
 */
export async function generarPerfilCooperativista(cooperativista, cuadrillaName, seccionName) {
  // Crear documento PDF en formato A4 (210mm x 297mm)
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4'
  })

  const pageWidth = doc.internal.pageSize.getWidth()
  const pageHeight = doc.internal.pageSize.getHeight()
  const margin = 15

  // Colores de la cooperativa
  const colorVerde = [3, 135, 48] // #038730
  const colorAmarillo = [254, 234, 1] // #FEEA01
  const colorVerdeOscuro = [26, 46, 26]

  // ============================================
  // HEADER - Banda superior con logo y nombre
  // ============================================
  doc.setFillColor(...colorVerde)
  doc.rect(0, 0, pageWidth, 35, 'F')

  // Logo en la parte izquierda
  try {
    const logoPath = '/logo.png'
    const logoImg = await loadImageFromPath(logoPath)
    const logoSize = 25
    const logoX = margin
    const logoY = 5
    doc.addImage(logoImg, 'PNG', logoX, logoY, logoSize, logoSize)
  } catch (error) {
    console.warn('No se pudo cargar el logo:', error)
  }

  // Título en el centro-derecha del header
  doc.setTextColor(255, 255, 255)
  doc.setFontSize(20)
  doc.setFont('helvetica', 'bold')
  doc.text('COOPERATIVA MINERA POOPÓ R.L.', pageWidth / 2 + 10, 15, { align: 'center' })
  
  doc.setFontSize(12)
  doc.setFont('helvetica', 'normal')
  doc.text('Perfil de Cooperativista', pageWidth / 2 + 10, 25, { align: 'center' })

  // ============================================
  // FOTO CI - Centro superior
  // ============================================
  let yPosition = 45
  
  const imgWidth = 50
  const imgHeight = 50
  const xPosition = (pageWidth - imgWidth) / 2
  
  if (cooperativista.ci_foto_url) {
    try {
      const img = await loadImage(cooperativista.ci_foto_url)
      
      // Borde dorado alrededor de la foto
      doc.setDrawColor(...colorAmarillo)
      doc.setLineWidth(1)
      doc.rect(xPosition - 2, yPosition - 2, imgWidth + 4, imgHeight + 4)
      
      doc.addImage(img, 'JPEG', xPosition, yPosition, imgWidth, imgHeight)
      yPosition += imgHeight + 10
    } catch (error) {
      console.error('Error cargando foto CI:', error)
      // Dibujar placeholder si falla la carga
      doc.setFillColor(240, 240, 240)
      doc.rect(xPosition, yPosition, imgWidth, imgHeight, 'F')
      doc.setDrawColor(...colorAmarillo)
      doc.setLineWidth(1)
      doc.rect(xPosition, yPosition, imgWidth, imgHeight)
      
      doc.setTextColor(150, 150, 150)
      doc.setFontSize(10)
      doc.text('Sin foto', xPosition + imgWidth/2, yPosition + imgHeight/2, { align: 'center' })
      yPosition += imgHeight + 10
    }
  } else {
    // Placeholder para foto
    doc.setFillColor(240, 240, 240)
    doc.rect(xPosition, yPosition, imgWidth, imgHeight, 'F')
    doc.setDrawColor(...colorAmarillo)
    doc.setLineWidth(1)
    doc.rect(xPosition, yPosition, imgWidth, imgHeight)
    
    doc.setTextColor(150, 150, 150)
    doc.setFontSize(10)
    doc.text('Sin foto', xPosition + imgWidth/2, yPosition + imgHeight/2, { align: 'center' })
    yPosition += imgHeight + 10
  }

  // ============================================
  // NOMBRE COMPLETO - Destacado
  // ============================================
  const nombreCompleto = `${cooperativista.nombres} ${cooperativista.apellido_paterno} ${cooperativista.apellido_materno || ''}`
  doc.setTextColor(...colorVerdeOscuro)
  doc.setFontSize(16)
  doc.setFont('helvetica', 'bold')
  doc.text(nombreCompleto.toUpperCase(), pageWidth / 2, yPosition, { align: 'center' })
  yPosition += 8

  // Rol/Cargo si existe
  if (cooperativista.rol_cuadrilla) {
    doc.setTextColor(...colorAmarillo)
    doc.setFontSize(11)
    doc.setFont('helvetica', 'bold')
    doc.text(cooperativista.rol_cuadrilla.toUpperCase(), pageWidth / 2, yPosition, { align: 'center' })
    yPosition += 10
  } else {
    yPosition += 5
  }

  // ============================================
  // INFORMACIÓN PERSONAL - Tabla
  // ============================================
  doc.setTextColor(...colorVerde)
  doc.setFontSize(12)
  doc.setFont('helvetica', 'bold')
  doc.text('DATOS PERSONALES', margin, yPosition)
  yPosition += 5

  const datosPersonales = []
  
  if (cooperativista.ci) {
    datosPersonales.push(['CI:', `${cooperativista.ci}${cooperativista.ci_expedido ? ` - ${cooperativista.ci_expedido}` : ''}`])
  }
  if (cooperativista.fecha_nacimiento) {
    const edad = calcularEdad(cooperativista.fecha_nacimiento)
    datosPersonales.push(['Fecha de Nacimiento:', `${formatearFecha(cooperativista.fecha_nacimiento)} (${edad} años)`])
  }
  if (cooperativista.email) {
    datosPersonales.push(['Email:', cooperativista.email])
  }
  if (cooperativista.telefono) {
    datosPersonales.push(['Teléfono:', cooperativista.telefono])
  }

  if (datosPersonales.length > 0) {
    autoTable(doc, {
      startY: yPosition,
      head: [],
      body: datosPersonales,
      theme: 'plain',
      margin: { left: margin, right: margin },
      styles: {
        fontSize: 10,
        cellPadding: 2,
        textColor: [50, 50, 50]
      },
      columnStyles: {
        0: { fontStyle: 'bold', cellWidth: 60, textColor: colorVerdeOscuro },
        1: { cellWidth: 'auto' }
      }
    })
    yPosition = doc.lastAutoTable.finalY + 10
  }

  // ============================================
  // INFORMACIÓN LABORAL - Tabla
  // ============================================
  doc.setTextColor(...colorVerde)
  doc.setFontSize(12)
  doc.setFont('helvetica', 'bold')
  doc.text('INFORMACIÓN LABORAL', margin, yPosition)
  yPosition += 5

  const datosLaborales = [
    ['Sección:', seccionName],
    ['Cuadrilla:', cuadrillaName]
  ]

  if (cooperativista.ocupacion) {
    datosLaborales.push(['Ocupación:', cooperativista.ocupacion])
  }
  if (cooperativista.fecha_ingreso) {
    const antiguedad = calcularAntiguedad(cooperativista.fecha_ingreso)
    datosLaborales.push(['Fecha de Ingreso:', `${formatearFecha(cooperativista.fecha_ingreso)}`])
    if (antiguedad) {
      datosLaborales.push(['Antigüedad:', antiguedad])
    }
  }
  datosLaborales.push(['Estado:', cooperativista.is_active ? 'ACTIVO' : 'INACTIVO'])

  autoTable(doc, {
    startY: yPosition,
    head: [],
    body: datosLaborales,
    theme: 'plain',
    margin: { left: margin, right: margin },
    styles: {
      fontSize: 10,
      cellPadding: 2,
      textColor: [50, 50, 50]
    },
    columnStyles: {
      0: { fontStyle: 'bold', cellWidth: 60, textColor: colorVerdeOscuro },
      1: { cellWidth: 'auto' }
    }
  })
  yPosition = doc.lastAutoTable.finalY + 10

  // ============================================
  // INFORMACIÓN DE SEGURO - Tabla (si existe)
  // ============================================
  if (cooperativista.codigo_asegurado || cooperativista.cua || cooperativista.estado_asegurado) {
    doc.setTextColor(...colorVerde)
    doc.setFontSize(12)
    doc.setFont('helvetica', 'bold')
    doc.text('INFORMACIÓN DE SEGURO', margin, yPosition)
    yPosition += 5

    const datosSeguro = []
    if (cooperativista.codigo_asegurado) {
      datosSeguro.push(['Código Asegurado:', cooperativista.codigo_asegurado])
    }
    if (cooperativista.cua) {
      datosSeguro.push(['CUA:', cooperativista.cua])
    }
    if (cooperativista.estado_asegurado) {
      datosSeguro.push(['Estado:', cooperativista.estado_asegurado])
    }

    autoTable(doc, {
      startY: yPosition,
      head: [],
      body: datosSeguro,
      theme: 'plain',
      margin: { left: margin, right: margin },
      styles: {
        fontSize: 10,
        cellPadding: 2,
        textColor: [50, 50, 50]
      },
      columnStyles: {
        0: { fontStyle: 'bold', cellWidth: 60, textColor: colorVerdeOscuro },
        1: { cellWidth: 'auto' }
      }
    })
    yPosition = doc.lastAutoTable.finalY + 10
  }

  // ============================================
  // CÓDIGO QR - Parte inferior
  // ============================================
  if (cooperativista.qr_code) {
    try {
      console.log('Generando QR para código:', cooperativista.qr_code)
      
      // Generar QR code como imagen
      const qrDataUrl = await QRCode.toDataURL(cooperativista.qr_code, {
        width: 300,
        margin: 2,
        errorCorrectionLevel: 'M',
        color: {
          dark: '#1a2e1a',
          light: '#ffffff'
        }
      })

      console.log('QR generado exitosamente')

      const qrSize = 40
      const qrX = (pageWidth - qrSize) / 2
      const qrY = pageHeight - margin - qrSize - 15 // 15mm desde el bottom

      // Fondo blanco para el QR
      doc.setFillColor(255, 255, 255)
      doc.rect(qrX - 2, qrY - 2, qrSize + 4, qrSize + 4, 'F')
      
      // Borde dorado
      doc.setDrawColor(...colorAmarillo)
      doc.setLineWidth(1)
      doc.rect(qrX - 2, qrY - 2, qrSize + 4, qrSize + 4)

      doc.addImage(qrDataUrl, 'PNG', qrX, qrY, qrSize, qrSize)

      // Texto del código QR
      doc.setTextColor(...colorVerdeOscuro)
      doc.setFontSize(9)
      doc.setFont('helvetica', 'bold')
      doc.text(cooperativista.qr_code, pageWidth / 2, qrY + qrSize + 8, { align: 'center' })
    } catch (error) {
      console.error('Error generando QR:', error)
      // Dibujar placeholder si falla
      const qrSize = 40
      const qrX = (pageWidth - qrSize) / 2
      const qrY = pageHeight - margin - qrSize - 15
      
      doc.setFillColor(240, 240, 240)
      doc.rect(qrX, qrY, qrSize, qrSize, 'F')
      doc.setDrawColor(...colorAmarillo)
      doc.setLineWidth(1)
      doc.rect(qrX, qrY, qrSize, qrSize)
      
      doc.setTextColor(150, 150, 150)
      doc.setFontSize(8)
      doc.text('QR no disponible', qrX + qrSize/2, qrY + qrSize/2, { align: 'right' })
       
    }
  } else {
    console.warn('No hay código QR disponible para el cooperativista')
  }

  // ============================================
  // FOOTER - Fecha de generación
  // ============================================
  const fechaGeneracion = new Date().toLocaleDateString('es-BO', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })

  doc.setTextColor(150, 150, 150)
  doc.setFontSize(8)
  doc.setFont('helvetica', 'normal')
  doc.text(`Generado: ${fechaGeneracion}`, pageWidth / 2, pageHeight - 5, { align: 'center' })

  // ============================================
  // GUARDAR PDF
  // ============================================
  const fileName = `Perfil_${cooperativista.nombres}_${cooperativista.apellido_paterno}_${cooperativista.qr_code}.pdf`
  doc.save(fileName)

  return { success: true, fileName }
}

// ============================================
// FUNCIONES AUXILIARES
// ============================================

/**
 * Carga una imagen desde URL y la convierte a base64
 */
function loadImage(url) {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.crossOrigin = 'Anonymous'
    img.onload = () => resolve(img)
    img.onerror = reject
    img.src = url
  })
}

/**
 * Carga una imagen desde el path público (para logo)
 */
function loadImageFromPath(path) {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.onload = () => resolve(img)
    img.onerror = (error) => {
      console.error('Error cargando imagen desde path:', path, error)
      reject(error)
    }
    // En producción y desarrollo, el path debe apuntar a la carpeta public
    img.src = path
  })
}

/**
 * Formatea una fecha al formato español
 */
function formatearFecha(fecha) {
  if (!fecha) return ''
  return new Date(fecha).toLocaleDateString('es-BO', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

/**
 * Calcula la edad a partir de una fecha de nacimiento
 */
function calcularEdad(fechaNacimiento) {
  if (!fechaNacimiento) return null
  const hoy = new Date()
  const nacimiento = new Date(fechaNacimiento)
  let edad = hoy.getFullYear() - nacimiento.getFullYear()
  const mes = hoy.getMonth() - nacimiento.getMonth()
  if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
    edad--
  }
  return edad
}

/**
 * Calcula la antigüedad desde fecha de ingreso
 */
function calcularAntiguedad(fechaIngreso) {
  if (!fechaIngreso) return null
  const hoy = new Date()
  const ingreso = new Date(fechaIngreso)
  
  let años = hoy.getFullYear() - ingreso.getFullYear()
  let meses = hoy.getMonth() - ingreso.getMonth()
  
  if (meses < 0) {
    años--
    meses += 12
  }
  
  if (años > 0 && meses > 0) {
    return `${años} años y ${meses} meses`
  } else if (años > 0) {
    return `${años} ${años === 1 ? 'año' : 'años'}`
  } else if (meses > 0) {
    return `${meses} ${meses === 1 ? 'mes' : 'meses'}`
  } else {
    return 'Menos de 1 mes'
  }
}