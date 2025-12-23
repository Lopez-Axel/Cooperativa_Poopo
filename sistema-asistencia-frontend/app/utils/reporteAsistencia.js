// utils/reporteAsistencia.js
import { jsPDF } from 'jspdf'
import autoTable from 'jspdf-autotable'

/**
 * Genera un reporte PDF de asistencias para un período específico
 * @param {Object} periodo - Objeto del período con nombre, descripción, fecha, etc.
 * @param {Array} asistencias - Array de asistencias del período
 * @param {Function} getCooperativistaById - Función para obtener cooperativista por ID
 * @param {Function} getCuadrillaById - Función para obtener cuadrilla por ID
 * @param {Function} getSeccionById - Función para obtener sección por ID
 */
export const generarReporteAsistencia = async (
  periodo,
  asistencias,
  getCooperativistaById,
  getCuadrillaById,
  getSeccionById
) => {
  const doc = new jsPDF()
  
  // Configuración de colores (tema cooperativa)
  const colorPrimario = [3, 135, 48] // Verde cooperativa
  const colorSecundario = [255, 215, 0] // Dorado
  const colorTexto = [33, 33, 33]
  
  let yPosition = 20
  
  // Logo (intentar cargarlo)
  try {
    const logo = await fetch('/logo.png')
    const blob = await logo.blob()
    const reader = new FileReader()
    
    await new Promise((resolve) => {
      reader.onloadend = () => {
        const imgData = reader.result
        doc.addImage(imgData, 'PNG', 10, yPosition - 5, 25, 25)
        resolve()
      }
      reader.readAsDataURL(blob)
    })
  } catch (error) {
    console.log('No se pudo cargar el logo')
  }
  
  // Título principal - Encabezado de la cooperativa
  doc.setFontSize(18)
  doc.setTextColor(...colorPrimario)
  doc.setFont('helvetica', 'bold')
  doc.text('Cooperativa Minera Poopó R.L.', 45, yPosition)
  
  yPosition += 8
  doc.setFontSize(12)
  doc.setTextColor(...colorTexto)
  doc.setFont('helvetica', 'normal')
  doc.text('Fundada 26 de Diciembre de 1953', 45, yPosition)
  
  yPosition += 20
  
  // Título del reporte
  doc.setFontSize(20)
  doc.setFont('helvetica', 'bold')
  doc.setTextColor(...colorPrimario)
  doc.text(` ${periodo.nombre} `, 15, yPosition)
  
  // Información del período
  doc.setFillColor(245, 245, 245)
  doc.setTextColor(...colorTexto)
  doc.setFontSize(11)
  doc.setFont('helvetica', 'normal')
  
  // Descripción del período (si existe)
  if (periodo.descripcion) {
    doc.text(`Descripción: ${periodo.descripcion}`, 20, yPosition + 15)
  }
  
  // Fecha y horario
  const fechaFormateada = formatearFecha(periodo.fecha_asistencia)
  const horario = `${periodo.hora_inicio.substring(0, 5)} - ${periodo.hora_fin.substring(0, 5)}`
  doc.text(`Fecha: ${fechaFormateada} | Horario: ${horario}`, 20, yPosition + 22)
  
  yPosition += 35
  
  // Fecha de generación
  doc.setFontSize(9)
  doc.setTextColor(100, 100, 100)
  doc.text(`Fecha de generación: ${new Date().toLocaleDateString('es-BO', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })}`, 15, yPosition)
  
  yPosition += 8
  
  // Estadísticas rápidas
  doc.setFillColor(...colorPrimario)
  doc.rect(15, yPosition, 180, 8, 'F')
  
  doc.setFontSize(11)
  doc.setFont('helvetica', 'bold')
  doc.setTextColor(255, 255, 255)
  doc.text('Resumen de Asistencias', 17, yPosition + 5.5)
  
  yPosition += 12
  
  // Contar tipos de asistencia
  const entradas = asistencias.filter(a => a.tipo === 'entrada').length
  const salidas = asistencias.filter(a => a.tipo === 'salida').length
  
  doc.setFontSize(10)
  doc.setFont('helvetica', 'normal')
  doc.setTextColor(...colorTexto)
  doc.text(`• Total de registros: ${asistencias.length}`, 20, yPosition)
  yPosition += 6
  doc.text(`• Entradas: ${entradas}`, 20, yPosition)
  yPosition += 6
  doc.text(`• Salidas: ${salidas}`, 20, yPosition)
  
  yPosition += 10
  
  // Preparar datos para la tabla
  const cooperativistasUnicos = new Map()
  
  asistencias.forEach(asistencia => {
    const cooperativista = getCooperativistaById(asistencia.cooperativista_id)
    
    if (cooperativista) {
      const cuadrilla = cooperativista.id_cuadrilla 
        ? getCuadrillaById(cooperativista.id_cuadrilla) 
        : null
      
      const seccion = cuadrilla && cuadrilla.id_seccion 
        ? getSeccionById(cuadrilla.id_seccion) 
        : null
      
      // Usar el cooperativista_id como clave para evitar duplicados
      // pero guardar la primera asistencia registrada
      if (!cooperativistasUnicos.has(asistencia.cooperativista_id)) {
        cooperativistasUnicos.set(asistencia.cooperativista_id, {
          cooperativista,
          cuadrilla,
          seccion,
          asistencia
        })
      }
    }
  })
  
  // Convertir a array y ordenar por nombre
  const datosTabla = Array.from(cooperativistasUnicos.values())
    .sort((a, b) => {
      const nombreA = `${a.cooperativista.apellido_paterno} ${a.cooperativista.nombres}`
      const nombreB = `${b.cooperativista.apellido_paterno} ${b.cooperativista.nombres}`
      return nombreA.localeCompare(nombreB)
    })
    .map((item, idx) => {
      const nombreCompleto = `${item.cooperativista.nombres} ${item.cooperativista.apellido_paterno} ${item.cooperativista.apellido_materno || ''}`.trim()
      const cuadrillaName = item.cuadrilla ? item.cuadrilla.nombre : 'Sin Cuadrilla'
      const seccionName = item.seccion ? item.seccion.nombre : 'Sin Sección'
      
      // Formatear fecha de registro usando timestamp o fecha+hora
      let fechaRegistro = ''
      if (item.asistencia.timestamp) {
        fechaRegistro = formatearFechaHora(item.asistencia.timestamp)
      } else if (item.asistencia.fecha && item.asistencia.hora) {
        fechaRegistro = `${formatearFecha(item.asistencia.fecha)} ${item.asistencia.hora.substring(0, 5)}`
      }
      
      return [
        idx + 1,
        nombreCompleto,
        cuadrillaName,
        seccionName,
        fechaRegistro
      ]
    })
  
  // Tabla de asistencias
  if (datosTabla.length > 0) {
    autoTable(doc, {
      startY: yPosition,
      head: [['#', 'Nombre Completo', 'Cuadrilla', 'Sección', 'Fecha Registro']],
      body: datosTabla,
      theme: 'striped',
      headStyles: {
        fillColor: colorSecundario,
        textColor: [13, 27, 13],
        fontStyle: 'bold',
        halign: 'left',
        fontSize: 10
      },
      styles: {
        fontSize: 9,
        cellPadding: 3,
        overflow: 'linebreak'
      },
      columnStyles: {
        0: { halign: 'center', cellWidth: 10 },
        1: { cellWidth: 60 },
        2: { cellWidth: 40 },
        3: { cellWidth: 35 },
        4: { cellWidth: 35 }
      },
      margin: { left: 15, right: 15 },
      alternateRowStyles: {
        fillColor: [250, 250, 250]
      }
    })
    
    yPosition = doc.lastAutoTable.finalY + 10
  } else {
    doc.setFontSize(11)
    doc.setTextColor(150, 150, 150)
    doc.setFont('helvetica', 'italic')
    doc.text('No hay asistencias registradas en este período', 15, yPosition)
  }
  
  // Pie de página en todas las páginas
  const pageCount = doc.internal.getNumberOfPages()
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i)
    doc.setFontSize(8)
    doc.setTextColor(150, 150, 150)
    doc.text(
      `Página ${i} de ${pageCount}`,
      doc.internal.pageSize.width / 2,
      doc.internal.pageSize.height - 10,
      { align: 'center' }
    )
  }
  
  // Guardar el PDF
  const fecha = new Date().toISOString().split('T')[0]
  const nombreArchivo = `Asistencias_${periodo.nombre.replace(/\s+/g, '_')}_${fecha}.pdf`
  doc.save(nombreArchivo)
}

/**
 * Genera un reporte detallado con todas las asistencias (incluye entradas y salidas separadas)
 */
export const generarReporteAsistenciaDetallado = async (
  periodo,
  asistencias,
  getCooperativistaById,
  getCuadrillaById,
  getSeccionById
) => {
  const doc = new jsPDF()
  
  const colorPrimario = [3, 135, 48]
  const colorSecundario = [255, 215, 0]
  const colorTexto = [33, 33, 33]
  
  let yPosition = 20
  
  // Logo
  try {
    const logo = await fetch('/logo.png')
    const blob = await logo.blob()
    const reader = new FileReader()
    
    await new Promise((resolve) => {
      reader.onloadend = () => {
        const imgData = reader.result
        doc.addImage(imgData, 'PNG', 15, yPosition - 5, 25, 25)
        resolve()
      }
      reader.readAsDataURL(blob)
    })
  } catch (error) {
    console.log('No se pudo cargar el logo')
  }
  
  // Encabezado
  doc.setFontSize(18)
  doc.setTextColor(...colorPrimario)
  doc.setFont('helvetica', 'bold')
  doc.text('Cooperativa Minera Poopó R.L.', 45, yPosition)
  
  yPosition += 8
  doc.setFontSize(12)
  doc.setTextColor(...colorTexto)
  doc.setFont('helvetica', 'normal')
  doc.text('Fundada 26 de Diciembre de 1953', 45, yPosition)
  
  yPosition += 15
  
  doc.setFontSize(16)
  doc.setFont('helvetica', 'bold')
  doc.setTextColor(...colorPrimario)
  doc.text('Reporte Detallado de Asistencias', 15, yPosition)
  
  yPosition += 10
  
  // Info del período
  doc.setFillColor(245, 245, 245)
  doc.rect(15, yPosition, 180, 25, 'F')
  
  doc.setFontSize(14)
  doc.setFont('helvetica', 'bold')
  doc.setTextColor(...colorTexto)
  doc.text(`Período: ${periodo.nombre}`, 20, yPosition + 8)
  
  doc.setFontSize(11)
  doc.setFont('helvetica', 'normal')
  const fechaFormateada = formatearFecha(periodo.fecha_asistencia)
  const horario = `${periodo.hora_inicio.substring(0, 5)} - ${periodo.hora_fin.substring(0, 5)}`
  doc.text(`${fechaFormateada} | ${horario}`, 20, yPosition + 15)
  
  yPosition += 30
  
  // Preparar datos para tabla detallada
  const datosTabla = asistencias
    .sort((a, b) => {
      // Ordenar por timestamp o por fecha+hora
      const timeA = a.timestamp || `${a.fecha}T${a.hora}`
      const timeB = b.timestamp || `${b.fecha}T${b.hora}`
      return timeA.localeCompare(timeB)
    })
    .map((asistencia, idx) => {
      const cooperativista = getCooperativistaById(asistencia.cooperativista_id)
      
      if (!cooperativista) {
        return [
          idx + 1,
          'Cooperativista no encontrado',
          '-',
          '-',
          '-',
          asistencia.tipo.toUpperCase()
        ]
      }
      
      const nombreCompleto = `${cooperativista.nombres} ${cooperativista.apellido_paterno} ${cooperativista.apellido_materno || ''}`.trim()
      
      const cuadrilla = cooperativista.id_cuadrilla 
        ? getCuadrillaById(cooperativista.id_cuadrilla) 
        : null
      const cuadrillaName = cuadrilla ? cuadrilla.nombre : 'Sin Cuadrilla'
      
      const seccion = cuadrilla && cuadrilla.id_seccion 
        ? getSeccionById(cuadrilla.id_seccion) 
        : null
      const seccionName = seccion ? seccion.nombre : 'Sin Sección'
      
      let fechaRegistro = ''
      if (asistencia.timestamp) {
        fechaRegistro = formatearFechaHora(asistencia.timestamp)
      } else if (asistencia.fecha && asistencia.hora) {
        fechaRegistro = `${formatearFecha(asistencia.fecha)} ${asistencia.hora.substring(0, 5)}`
      }
      
      return [
        idx + 1,
        nombreCompleto,
        cuadrillaName,
        seccionName,
        fechaRegistro,
        asistencia.tipo.toUpperCase()
      ]
    })
  
  // Tabla
  if (datosTabla.length > 0) {
    autoTable(doc, {
      startY: yPosition,
      head: [['#', 'Nombre', 'Cuadrilla', 'Sección', 'Fecha/Hora', 'Tipo']],
      body: datosTabla,
      theme: 'grid',
      headStyles: {
        fillColor: colorSecundario,
        textColor: [13, 27, 13],
        fontStyle: 'bold',
        halign: 'left',
        fontSize: 9
      },
      styles: {
        fontSize: 8,
        cellPadding: 2.5,
        overflow: 'linebreak'
      },
      columnStyles: {
        0: { halign: 'center', cellWidth: 8 },
        1: { cellWidth: 55 },
        2: { cellWidth: 35 },
        3: { cellWidth: 30 },
        4: { cellWidth: 32 },
        5: { halign: 'center', cellWidth: 20 }
      },
      margin: { left: 15, right: 15 },
      didDrawCell: (data) => {
        // Colorear la celda de tipo según sea entrada o salida
        if (data.column.index === 5 && data.row.section === 'body') {
          const tipo = data.cell.text[0]
          if (tipo === 'ENTRADA') {
            doc.setFillColor(72, 199, 116)
          } else if (tipo === 'SALIDA') {
            doc.setFillColor(255, 221, 87)
          }
          doc.rect(data.cell.x, data.cell.y, data.cell.width, data.cell.height, 'F')
          
          doc.setTextColor(tipo === 'ENTRADA' ? 255 : 13, tipo === 'ENTRADA' ? 255 : 27, tipo === 'ENTRADA' ? 255 : 13)
          doc.setFontSize(8)
          doc.setFont('helvetica', 'bold')
          doc.text(tipo, data.cell.x + data.cell.width / 2, data.cell.y + data.cell.height / 2 + 1, {
            align: 'center',
            baseline: 'middle'
          })
        }
      }
    })
  } else {
    doc.setFontSize(11)
    doc.setTextColor(150, 150, 150)
    doc.setFont('helvetica', 'italic')
    doc.text('No hay asistencias registradas', 15, yPosition)
  }
  
  // Pie de página
  const pageCount = doc.internal.getNumberOfPages()
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i)
    doc.setFontSize(8)
    doc.setTextColor(150, 150, 150)
    doc.text(
      `Página ${i} de ${pageCount}`,
      doc.internal.pageSize.width / 2,
      doc.internal.pageSize.height - 10,
      { align: 'center' }
    )
  }
  
  const fecha = new Date().toISOString().split('T')[0]
  const nombreArchivo = `Asistencias_Detallado_${periodo.nombre.replace(/\s+/g, '_')}_${fecha}.pdf`
  doc.save(nombreArchivo)
}

// Funciones auxiliares
function formatearFecha(fechaString) {
  if (!fechaString) return 'N/A'
  const fecha = new Date(fechaString)
  return fecha.toLocaleDateString('es-BO', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}

function formatearFechaHora(timestamp) {
  if (!timestamp) return 'N/A'
  const fecha = new Date(timestamp)
  return fecha.toLocaleDateString('es-BO', { 
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}