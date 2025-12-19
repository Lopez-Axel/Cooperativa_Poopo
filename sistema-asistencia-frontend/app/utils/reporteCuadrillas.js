// utils/reporteCuadrillas.js
import { jsPDF } from 'jspdf'
import autoTable from 'jspdf-autotable'

export const generarReporteCuadrillas = async (cuadrillasConDetalles, titulo = 'Reporte de Cuadrillas') => {
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
        doc.addImage(imgData, 'JPEG', 15, yPosition - 5, 25, 25)
        resolve()
      }
      reader.readAsDataURL(blob)
    })
  } catch (error) {
    console.log('No se pudo cargar el logo')
  }
  
  // Título principal
  doc.setFontSize(18)
  doc.setTextColor(...colorPrimario)
  doc.setFont('helvetica', 'bold')
  doc.text('Cooperativa Minera Poopó R.L.', 45, yPosition)
  
  yPosition += 8
  doc.setFontSize(12)
  doc.setTextColor(...colorTexto)
  doc.setFont('helvetica', 'normal')
  doc.text('Fundada 26 de Diciembre de 1953', 45, yPosition)
  
  yPosition += 10
  doc.setFontSize(14)
  doc.setFont('helvetica', 'bold')
  doc.text(titulo, 15, yPosition)
  
  yPosition += 5
  doc.setFontSize(10)
  doc.setFont('helvetica', 'normal')
  doc.setTextColor(100, 100, 100)
  doc.text(`Fecha de generación: ${new Date().toLocaleDateString('es-BO', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })}`, 15, yPosition)
  
  yPosition += 10
  
  // Iterar por cada cuadrilla
  cuadrillasConDetalles.forEach((detalle, index) => {
    // Verificar si necesitamos una nueva página
    if (yPosition > 250) {
      doc.addPage()
      yPosition = 20
    }
    
    // Encabezado de la cuadrilla
    doc.setFillColor(...colorPrimario)
    doc.rect(15, yPosition, 180, 10, 'F')
    
    doc.setFontSize(12)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(255, 255, 255)
    doc.text(`${detalle.nombre}`, 17, yPosition + 7)
    
    doc.setFontSize(10)
    doc.setFont('helvetica', 'normal')
    doc.text(`Sección: ${detalle.seccion?.nombre || 'Sin sección'}`, 120, yPosition + 7)
    
    yPosition += 12
    
    // Tabla de cooperativistas
    if (detalle.cooperativistas && detalle.cooperativistas.length > 0) {
      const cooperativistasData = detalle.cooperativistas.map((coop, idx) => [
        idx + 1,
        `${coop.nombres} ${coop.apellido_paterno} ${coop.apellido_materno || ''}`,
        coop.ci || 'Sin CI',
        coop.rol_cuadrilla || '-'
      ])
      
      autoTable(doc, {
        startY: yPosition,
        head: [['#', 'Nombre Completo', 'CI', 'Rol en Cuadrilla']],
        body: cooperativistasData,
        theme: 'striped',
        headStyles: {
          fillColor: colorSecundario,
          textColor: [13, 27, 13],
          fontStyle: 'bold',
          halign: 'left'
        },
        styles: {
          fontSize: 9,
          cellPadding: 3
        },
        columnStyles: {
          0: { halign: 'center', cellWidth: 10 },
          1: { cellWidth: 80 },
          2: { cellWidth: 35 },
          3: { cellWidth: 50 }
        },
        margin: { left: 15, right: 15 }
      })
      
      yPosition = doc.lastAutoTable.finalY + 8
    } else {
      doc.setFontSize(10)
      doc.setTextColor(150, 150, 150)
      doc.setFont('helvetica', 'italic')
      doc.text('Sin cooperativistas asignados', 17, yPosition + 5)
      yPosition += 15
    }
  })
  
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
  doc.save(`Reporte_Cuadrillas_${fecha}.pdf`)
}

export const generarReporteCuadrillaPorSeccion = async (seccionNombre, cuadrillasConDetalles) => {
  await generarReporteCuadrillas(
    cuadrillasConDetalles,
    `Reporte de Cuadrillas - ${seccionNombre}`
  )
}

// Agregar al final de utils/reporteCuadrillas.js

export const generarReporteIndividualCuadrilla = async (detalleCuadrilla) => {
  const doc = new jsPDF()
  
  // Configuración de colores
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
        doc.addImage(imgData, 'JPEG', 15, yPosition - 5, 25, 25)
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
  
  yPosition += 20
  
  // Título del reporte
  doc.setFontSize(16)
  doc.setFont('helvetica', 'bold')
  doc.setTextColor(...colorPrimario)
  doc.text('Reporte de Cuadrilla', 15, yPosition)
  
  yPosition += 10
  
  // Información de la cuadrilla
  doc.setFillColor(245, 245, 245)
  doc.rect(15, yPosition, 180, 25, 'F')
  
  doc.setFontSize(14)
  doc.setFont('helvetica', 'bold')
  doc.setTextColor(...colorTexto)
  doc.text(`Cuadrilla: ${detalleCuadrilla.nombre}`, 20, yPosition + 8)
  
  doc.setFontSize(11)
  doc.setFont('helvetica', 'normal')
  doc.text(`Sección: ${detalleCuadrilla.seccion?.nombre || 'Sin sección'}`, 20, yPosition + 16)
  doc.text(`Total de cooperativistas: ${detalleCuadrilla.total_cooperativistas}`, 20, yPosition + 22)
  
  yPosition += 30
  
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
  
  yPosition += 10
  
  // Tabla de cooperativistas
  if (detalleCuadrilla.cooperativistas && detalleCuadrilla.cooperativistas.length > 0) {
    const cooperativistasData = detalleCuadrilla.cooperativistas.map((coop, idx) => [
      idx + 1,
      `${coop.nombres} ${coop.apellido_paterno} ${coop.apellido_materno || ''}`,
      coop.ci || 'Sin CI',
      coop.rol_cuadrilla || '-'
    ])
    
    autoTable(doc, {
      startY: yPosition,
      head: [['#', 'Nombre Completo', 'CI', 'Rol en Cuadrilla']],
      body: cooperativistasData,
      theme: 'grid',
      headStyles: {
        fillColor: colorSecundario,
        textColor: [13, 27, 13],
        fontStyle: 'bold',
        halign: 'left',
        fontSize: 10
      },
      styles: {
        fontSize: 9,
        cellPadding: 4
      },
      columnStyles: {
        0: { halign: 'center', cellWidth: 15 },
        1: { cellWidth: 85 },
        2: { cellWidth: 35 },
        3: { cellWidth: 45 }
      },
      margin: { left: 15, right: 15 },
      alternateRowStyles: {
        fillColor: [245, 245, 245]
      }
    })
    
    yPosition = doc.lastAutoTable.finalY + 15
    
    // Estadísticas adicionales
    doc.setFillColor(...colorPrimario)
    doc.rect(15, yPosition, 180, 8, 'F')
    
    doc.setFontSize(11)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(255, 255, 255)
    doc.text('Resumen', 17, yPosition + 5.5)
    
    yPosition += 12
    
    // Contar roles
    const roles = {}
    detalleCuadrilla.cooperativistas.forEach(coop => {
      const rol = coop.rol_cuadrilla || 'Sin rol asignado'
      roles[rol] = (roles[rol] || 0) + 1
    })
    
    doc.setFontSize(10)
    doc.setFont('helvetica', 'normal')
    doc.setTextColor(...colorTexto)
    
    Object.entries(roles).forEach(([rol, cantidad]) => {
      doc.text(`• ${rol}: ${cantidad} cooperativista${cantidad !== 1 ? 's' : ''}`, 20, yPosition)
      yPosition += 6
    })
  } else {
    doc.setFontSize(11)
    doc.setTextColor(150, 150, 150)
    doc.setFont('helvetica', 'italic')
    doc.text('Esta cuadrilla no tiene cooperativistas asignados', 15, yPosition)
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
  
  // Guardar con nombre específico
  const fecha = new Date().toISOString().split('T')[0]
  const nombreArchivo = `Cuadrilla_${detalleCuadrilla.nombre.replace(/\s+/g, '_')}_${fecha}.pdf`
  doc.save(nombreArchivo)
}