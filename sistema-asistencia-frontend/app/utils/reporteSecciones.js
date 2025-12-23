// utils/reporteSecciones.js
import { jsPDF } from 'jspdf'
import autoTable from 'jspdf-autotable'

export const generarReporteSecciones = async (seccionesConDetalles, titulo = 'Reporte de Secciones') => {
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
  
  yPosition += 25
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
  
  // Iterar por cada sección
  seccionesConDetalles.forEach((detalle, index) => {
    // Verificar si necesitamos una nueva página
    if (yPosition > 250) {
      doc.addPage()
      yPosition = 20
    }
    
    // Encabezado de la sección
    doc.setFillColor(...colorPrimario)
    doc.rect(15, yPosition, 180, 10, 'F')
    
    doc.setFontSize(12)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(255, 255, 255)
    doc.text(`Sección: ${detalle.nombre}`, 17, yPosition + 7)
    
    doc.setFontSize(10)
    doc.setFont('helvetica', 'normal')
    doc.text(`Delegado: ${detalle.delegado?.nombres || 'Sin asignar'}`, 120, yPosition + 7)
    
    yPosition += 12
    
    // Agrupar cuadrillas de esta sección
    if (detalle.cuadrillas && detalle.cuadrillas.length > 0) {
      detalle.cuadrillas.forEach((cuadrilla) => {
        // Verificar espacio para cuadrilla
        if (yPosition > 240) {
          doc.addPage()
          yPosition = 20
        }
        
        // Sub-encabezado de cuadrilla
        doc.setFillColor(...colorSecundario)
        doc.rect(20, yPosition, 170, 8, 'F')
        
        doc.setFontSize(11)
        doc.setFont('helvetica', 'bold')
        doc.setTextColor(13, 27, 13)
        doc.text(`Cuadrilla: ${cuadrilla.nombre}`, 22, yPosition + 5.5)
        
        yPosition += 10
        
        // Tabla de cooperativistas de la cuadrilla
        if (cuadrilla.cooperativistas && cuadrilla.cooperativistas.length > 0) {
          const cooperativistasData = cuadrilla.cooperativistas.map((coop, idx) => [
            idx + 1,
            `${coop.nombres} ${coop.apellido_paterno} ${coop.apellido_materno || ''}`,
            coop.ci || 'Sin CI',
            coop.rol_cuadrilla || '-'
          ])
          
          autoTable(doc, {
            startY: yPosition,
            head: [['#', 'Nombre Completo', 'CI', 'Rol']],
            body: cooperativistasData,
            theme: 'striped',
            headStyles: {
              fillColor: [200, 200, 200],
              textColor: [33, 33, 33],
              fontStyle: 'bold',
              halign: 'left',
              fontSize: 9
            },
            styles: {
              fontSize: 8,
              cellPadding: 2
            },
            columnStyles: {
              0: { halign: 'center', cellWidth: 10 },
              1: { cellWidth: 75 },
              2: { cellWidth: 30 },
              3: { cellWidth: 45 }
            },
            margin: { left: 25, right: 25 }
          })
          
          yPosition = doc.lastAutoTable.finalY + 5
        } else {
          doc.setFontSize(9)
          doc.setTextColor(150, 150, 150)
          doc.setFont('helvetica', 'italic')
          doc.text('Sin cooperativistas asignados', 25, yPosition + 3)
          yPosition += 10
        }
      })
    } else {
      doc.setFontSize(10)
      doc.setTextColor(150, 150, 150)
      doc.setFont('helvetica', 'italic')
      doc.text('Esta sección no tiene cuadrillas asignadas', 20, yPosition + 5)
      yPosition += 15
    }
    
    yPosition += 5
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
  doc.save(`Reporte_Secciones_${fecha}.pdf`)
}

export const generarReporteIndividualSeccion = async (detalleSeccion) => {
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
  doc.text('Reporte de Sección', 15, yPosition)
  
  yPosition += 10
  
  // Información de la sección
  doc.setFillColor(245, 245, 245)
  doc.rect(15, yPosition, 180, 30, 'F')
  
  doc.setFontSize(14)
  doc.setFont('helvetica', 'bold')
  doc.setTextColor(...colorTexto)
  doc.text(`Sección: ${detalleSeccion.nombre}`, 20, yPosition + 8)
  
  doc.setFontSize(11)
  doc.setFont('helvetica', 'normal')
  doc.text(`Delegado: ${detalleSeccion.delegado?.nombres || 'Sin asignar'}`, 20, yPosition + 16)
  doc.text(`Total de cuadrillas: ${detalleSeccion.total_cuadrillas || 0}`, 20, yPosition + 22)
  doc.text(`Total de cooperativistas: ${detalleSeccion.total_cooperativistas || 0}`, 110, yPosition + 22)
  
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
  
  yPosition += 10
  
  // Iterar por cada cuadrilla de la sección
  if (detalleSeccion.cuadrillas && detalleSeccion.cuadrillas.length > 0) {
    detalleSeccion.cuadrillas.forEach((cuadrilla, index) => {
      // Verificar espacio
      if (yPosition > 240) {
        doc.addPage()
        yPosition = 20
      }
      
      // Encabezado de cuadrilla
      doc.setFillColor(...colorSecundario)
      doc.rect(15, yPosition, 180, 10, 'F')
      
      doc.setFontSize(12)
      doc.setFont('helvetica', 'bold')
      doc.setTextColor(13, 27, 13)
      doc.text(`Cuadrilla: ${cuadrilla.nombre}`, 17, yPosition + 7)
      
      doc.setFontSize(10)
      doc.setFont('helvetica', 'normal')
      doc.text(`Cooperativistas: ${cuadrilla.cooperativistas?.length || 0}`, 140, yPosition + 7)
      
      yPosition += 12
      
      // Tabla de cooperativistas
      if (cuadrilla.cooperativistas && cuadrilla.cooperativistas.length > 0) {
        const cooperativistasData = cuadrilla.cooperativistas.map((coop, idx) => [
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
            cellPadding: 3
          },
          columnStyles: {
            0: { halign: 'center', cellWidth: 12 },
            1: { cellWidth: 80 },
            2: { cellWidth: 35 },
            3: { cellWidth: 48 }
          },
          margin: { left: 15, right: 15 },
          alternateRowStyles: {
            fillColor: [245, 245, 245]
          }
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
    
    // Estadísticas adicionales al final
    if (yPosition > 230) {
      doc.addPage()
      yPosition = 20
    }
    
    yPosition += 5
    
    doc.setFillColor(...colorPrimario)
    doc.rect(15, yPosition, 180, 8, 'F')
    
    doc.setFontSize(11)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(255, 255, 255)
    doc.text('Resumen General', 17, yPosition + 5.5)
    
    yPosition += 12
    
    // Contar roles por cuadrilla
    const rolesCount = {}
    let totalCooperativistas = 0
    
    detalleSeccion.cuadrillas.forEach(cuadrilla => {
      if (cuadrilla.cooperativistas) {
        totalCooperativistas += cuadrilla.cooperativistas.length
        cuadrilla.cooperativistas.forEach(coop => {
          const rol = coop.rol_cuadrilla || 'Sin rol asignado'
          rolesCount[rol] = (rolesCount[rol] || 0) + 1
        })
      }
    })
    
    doc.setFontSize(10)
    doc.setFont('helvetica', 'normal')
    doc.setTextColor(...colorTexto)
    
    doc.text(`• Total de cuadrillas: ${detalleSeccion.cuadrillas.length}`, 20, yPosition)
    yPosition += 6
    doc.text(`• Total de cooperativistas: ${totalCooperativistas}`, 20, yPosition)
    yPosition += 8
    
    doc.setFont('helvetica', 'bold')
    doc.text('Distribución por roles:', 20, yPosition)
    yPosition += 6
    
    doc.setFont('helvetica', 'normal')
    Object.entries(rolesCount).forEach(([rol, cantidad]) => {
      doc.text(`  - ${rol}: ${cantidad} cooperativista${cantidad !== 1 ? 's' : ''}`, 25, yPosition)
      yPosition += 6
    })
  } else {
    doc.setFontSize(11)
    doc.setTextColor(150, 150, 150)
    doc.setFont('helvetica', 'italic')
    doc.text('Esta sección no tiene cuadrillas asignadas', 15, yPosition)
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
  const nombreArchivo = `Seccion_${detalleSeccion.nombre.replace(/\s+/g, '_')}_${fecha}.pdf`
  doc.save(nombreArchivo)
}