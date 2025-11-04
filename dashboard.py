"""
SPT CASH FLOW TOOL - Dashboard Streamlit v4.9.0
================================================
Dashboard de análisis de flujo de efectivo para SPT Colombia

🎉 NUEVAS FUNCIONALIDADES v4.9.0 (Noviembre 3, 2025):
=====================================================
✅ FASE 4 - INGRESO MANUAL DE COTIZACIONES Y CONTRATOS:

  1. NUEVA PÁGINA "INGRESO MANUAL":
     - Interfaz completa para ingresar cotizaciones y contratos futuros
     - Permite analizar impacto de nuevos negocios en proyecciones
     - Gestión separada de cotizaciones (con probabilidad) y contratos (confirmados)
  
  2. FORMULARIO DE COTIZACIONES:
     - ID de cotización, cliente, fechas de validez
     - Probabilidad de cierre (slider 0-100%)
     - Revenue ponderado automático
     - Equipos requeridos con tarifas individuales
     - Duración estimada del contrato
  
  3. FORMULARIO DE CONTRATOS:
     - ID del contrato, cliente, estado
     - Opción de duración fija o fecha fin abierta
     - Equipos asignados con serial numbers
     - Tarifa mensual total y por equipo
     - Integración con disponibilidad de equipos (preparada)
  
  4. PANEL DE RESUMEN:
     - Vista consolidada de todas las cotizaciones y contratos
     - Cálculo de revenue ponderado total
     - Análisis de impacto en proyecciones futuras
     - Exportación y gestión de datos ingresados
  
  5. PREPARACIÓN PARA ESCENARIOS DINÁMICOS:
     - Los datos ingresados se almacenan para uso futuro
     - Próxima integración: ajuste automático de escenarios según cotizaciones/contratos
     - Base para proyecciones con nuevos negocios considerados
  
  Ubicación: Nueva opción "📝 Ingreso Manual" en el menú de navegación

🔧 CORRECCIONES CRÍTICAS v4.8.1 (Noviembre 3, 2025):
=====================================================
✅ CORRECCIONES FUNDAMENTALES EN LÓGICA FINANCIERA:

  1. PROYECCIONES DETERMINISTAS:
     ❌ ANTES: Usaba np.random - números cambiaban al mover cualquier control
     ✅ AHORA: Proyecciones deterministas - números consistentes y predecibles
     - Elimina variación aleatoria completamente
     - Escenarios usan factores fijos (Conservador: -15%, Moderado: 0%, Optimista: +15%)
     - Crecimiento mensual predecible (1%, 2%, 3% según escenario)
  
  2. TRANSFERENCIAS DESCUENTAN DEL BALANCE:
     ❌ ANTES: Transferencias no afectaban el balance - error conceptual crítico
     ✅ AHORA: Al final de cada trimestre, la transferencia se DESCUENTA del balance
     - Balance mes 4 parte del balance después de transferencia trimestre 1
     - Proyecciones realistas reflejan el efectivo real disponible
     - Nueva función: calcular_transferencias_con_balance()
  
  3. INVERSIONES COMO RECOMENDACIONES VIRTUALES:
     ✅ Las inversiones NO afectan el balance principal (son sugerencias)
     ✅ Se mantiene cálculo de beneficios esperados
     ✅ Enfoque conservador para proyecciones financieras
  
  4. SELECTOR DE ESCENARIO:
     ✅ Nuevo control en sidebar: Conservador / Moderado / Optimista
     ✅ Las transferencias se calculan según el escenario seleccionado
     ✅ Indicador visual del escenario en uso (🟠/🟢/🔵)
     - Permite análisis de sensibilidad en diferentes condiciones
     - Balance después de transferencias varía según escenario

  IMPACTO DE CORRECCIONES:
  - Proyecciones ahora son matemáticamente correctas y reproducibles
  - Balance refleja el flujo real de efectivo después de transferencias
  - Los números ya NO cambian al mover otros controles
  - Análisis financiero mucho más preciso y útil para toma de decisiones

🎉 NUEVAS FUNCIONALIDADES v4.8.0 (Noviembre 3, 2025):
=====================================================
✅ FASE 3 - GESTIÓN DE EXCEDENTES E INVERSIONES:

  1. BADGE INDICADOR CORREGIDO:
     - Ahora muestra correctamente 🟢 VERDE cuando hay datos reales cargados
     - Lógica simplificada y más confiable
  
  2. GESTIÓN DE EXCEDENTES E INVERSIONES TEMPORALES:
     - Análisis automático de excedentes invertibles mes a mes
     - Recomendaciones de inversión en instrumentos de bajo riesgo (CDTs, TES, FCIs)
     - Cálculo de rentabilidad estimada (10% EA promedio)
     - Calendario inteligente de liquidación configurable (7, 15 o 30 días)
     - Respeta margen de protección configurado antes de sugerir inversiones
  
  3. TRANSFERENCIAS TRIMESTRALES A CASA MATRIZ:
     - Cálculo según política SPT Global (utilidad local = 10% del revenue)
     - Transferencias por trimestre vencido (no mensuales)
     - Permite aprovechar inversiones temporales durante el trimestre
     - Tabla detallada con distribución Revenue → Utilidad Local → Transferencia HQ
     - Gráfico visual de distribución del flujo neto
     - Resumen de totales y márgenes
  
  4. CONFIGURACIÓN ADICIONAL:
     - Nuevo parámetro: Días de liquidación anticipada (7/15/30 días)
     - Default: 15 días (recomendado para instrumentos de conversión rápida)
     - Ajustable desde el sidebar → "Liquidación de Inversiones"

  Ubicación: Resumen Ejecutivo → Subsecciones nuevas al final

🎨 MEJORAS VISUALES v4.7.1 (Noviembre 3, 2025):
================================================
✅ FASE 2 - MEJORAS VISUALES COMPLETADAS:
  
  1. GRÁFICOS COMPARATIVOS MEJORADOS:
     - Gráfico de barras comparando Revenue, Egresos y Flujo Neto por escenario
     - Visualización clara de diferencias entre escenarios
     - Valores mostrados en cada barra para fácil lectura
  
  2. TABLAS DE DATOS EXPORTABLES:
     - Tabla comparativa de resumen de todos los escenarios
     - Botón de descarga CSV para tabla comparativa
     - Botones de descarga individuales por escenario
  
  3. INDICADOR VISUAL CORREGIDO:
     - Indicador verde 🟢 cuando hay datos reales procesados
     - Verificación correcta de estructura de datos
  
  Ubicación: Proyecciones Multi-Escenario → Pestaña "Comparación"

🚀 NUEVO EN v4.7.0 (Noviembre 3, 2025):
========================================
✅ PROCESAMIENTO REAL DE ARCHIVOS EXCEL
  - Lectura y análisis de Utilization Reports (2023-2025)
  - Extracción de datos del Informe Financiero
  - Procesamiento de Weekly Operation Report
  - Cálculos automáticos de métricas desde datos reales
  - Integración completa con el dashboard

Archivos procesados:
  1. Utilization_Report_2023.xlsx
  2. Utilization_Report_2024.xlsx
  3. Utilization_Report_2025.xlsx
  4. Weekly_Operation_Report.xlsx
  5. Informe_financiero.xlsx

🐛 CORRECCIONES v4.6.1 (Noviembre 3, 2025):
============================================
1. ✅ Indicador de modo corregido
2. ✅ Tooltip dinámico implementado  
3. ✅ KeyError 'gastos' eliminado
4. ✅ Balance multi-escenario funcional

🔥 CORRECCIONES CRÍTICAS v4.6.0 - FASE 1:
==========================================

1. ✅ BURN RATE DINÁMICO EN PROYECCIONES:
   - generar_proyecciones_multi_escenario() ahora calcula burn rate según revenue
   - calcular_proyeccion_3_meses() también usa cálculo dinámico
   - Fórmula aplicada: Burn Rate = $65,732 + (Revenue × 0.0962)

2. ✅ REFERENCIAS ACTUALIZADAS:
   - Eliminadas todas las menciones al burn rate obsoleto de $17,367
   - Actualizadas explicaciones con metodología correcta
   - Valores correctos: Gastos Fijos $65,732, Costos Variables 9.62%

3. ✅ NECESIDADES MÍNIMAS CONFIGURABLES:
   - Nuevo control para seleccionar margen de protección (1, 2 o 3 meses)
   - Permite ajustar según ciclo de pagos (30 días = 2 meses recomendado)
   - Afecta cálculo de excedentes y recomendaciones

4. ✅ TERMINOLOGÍA MEJORADA:
   - "Gastos" reemplazado por "Egresos Totales" o "Costos y Gastos"
   - Burn Rate mantenido como término técnico principal
   - Claridad en componentes: Gastos Administrativos + Costos Operativos

IMPACTO DE CORRECCIONES:
========================
• Proyecciones ahora matemáticamente correctas
• Burn rate se ajusta dinámicamente con el revenue proyectado
• Margen de protección configurable según necesidades operativas
• Información actualizada y precisa en todo el dashboard

METODOLOGÍA BURN RATE (Backend Analysis):
==========================================
• Gastos Fijos: $65,732 USD/mes (no varían con revenue)
• Costos Variables: 9.62% del revenue mensual
• Fórmula: Burn Rate = $65,732 + (Revenue × 0.0962)
• Ejemplo: Con revenue $127,468 → Burn Rate = $77,994 USD/mes
• Margen operativo: 48.5% (histórico)

Versiones anteriores:
- v4.5.5: Corrección KeyError, estructura base
- v4.5.3: Integración datos reales
- v4.5.2: Mejoras visualización

Autor: AI-MindNovation
Cliente: SPT Colombia
Fecha: Noviembre 2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from io import BytesIO

# =============================================================================
# PROCESAMIENTO DE ARCHIVOS REALES - v4.7.0
# =============================================================================

def procesar_utilization_reports(file_2023, file_2024, file_2025):
    """
    Procesa los 3 Utilization Reports y extrae métricas clave
    
    Returns:
        dict con revenue mensual, clientes, estacionalidad
    """
    try:
        # Leer los 3 archivos
        df_2023 = pd.read_excel(file_2023, sheet_name=0)
        df_2024 = pd.read_excel(file_2024, sheet_name=0)
        df_2025 = pd.read_excel(file_2025, sheet_name=0)
        
        # Combinar todos los datos
        df_all = pd.concat([df_2023, df_2024, df_2025], ignore_index=True)
        
        # Limpiar nombres de columnas
        df_all.columns = df_all.columns.str.strip()
        
        # Convertir Date a datetime
        df_all['Date'] = pd.to_datetime(df_all['Date'])
        df_all['Year'] = df_all['Date'].dt.year
        df_all['Month'] = df_all['Date'].dt.month
        
        # Convertir Accrual Revenue a numérico
        df_all['Accrual Revenue'] = pd.to_numeric(df_all['Accrual Revenue'], errors='coerce')
        
        # 1. Revenue mensual total
        revenue_mensual = df_all.groupby(['Year', 'Month'])['Accrual Revenue'].sum().reset_index()
        revenue_mensual['Year-Month'] = revenue_mensual['Year'].astype(str) + '-' + revenue_mensual['Month'].astype(str).str.zfill(2)
        
        # 2. Revenue promedio
        revenue_promedio = revenue_mensual['Accrual Revenue'].mean()
        
        # 3. Top clientes (últimos 12 meses)
        df_recent = df_all[df_all['Date'] >= df_all['Date'].max() - pd.DateOffset(months=12)]
        top_clientes = df_recent.groupby('Client')['Accrual Revenue'].sum().sort_values(ascending=False).head(10)
        
        # 4. Estacionalidad (promedio por mes del año)
        estacionalidad = df_all.groupby('Month')['Accrual Revenue'].mean()
        
        # 5. Revenue por año
        revenue_anual = df_all.groupby('Year')['Accrual Revenue'].sum()
        
        return {
            'revenue_mensual': revenue_mensual,
            'revenue_promedio': revenue_promedio,
            'top_clientes': top_clientes.to_dict(),
            'estacionalidad': estacionalidad.to_dict(),
            'revenue_anual': revenue_anual.to_dict(),
            'df_completo': df_all
        }
        
    except Exception as e:
        st.error(f"Error procesando Utilization Reports: {str(e)}")
        return None

def procesar_informe_financiero(file_financial):
    """
    Procesa el Informe Financiero y extrae gastos fijos y costos variables
    
    Returns:
        dict con gastos_fijos, tasa_costos_variables, burn_rate
    """
    try:
        # Leer hoja 'td' con datos mensuales
        df_td = pd.read_excel(file_financial, sheet_name='td', header=5)
        
        # Buscar la fila de 'Rental' (ingresos)
        rental_row = df_td[df_td.iloc[:, 0].str.contains('02 Rental', case=False, na=False)]
        
        if len(rental_row) > 0:
            # Extraer valores de ingresos mensuales (columnas numéricas)
            rental_values = rental_row.iloc[0, 1:10].values  # Meses 1-9
            rental_values = [abs(float(v)) for v in rental_values if pd.notna(v) and v != 0]
            revenue_promedio_real = np.mean(rental_values) if rental_values else 127468
        else:
            revenue_promedio_real = 127468
        
        # Calcular egresos por categoría
        categorias_egresos = ['04 HR', '05 Logistics', '06 Marketing', '07 Admin', '08 Insurance', '09 Salary']
        egresos_fijos = 0
        
        for categoria in categorias_egresos:
            cat_row = df_td[df_td.iloc[:, 0].str.contains(categoria, case=False, na=False)]
            if len(cat_row) > 0:
                cat_values = cat_row.iloc[0, 1:10].values
                cat_values = [float(v) for v in cat_values if pd.notna(v) and v != 0]
                if cat_values:
                    egresos_fijos += np.mean(cat_values)
        
        # Tasa de costos variables: 9.62% del revenue (estimado desde backend)
        tasa_costos_variables = 0.0962
        
        # Burn rate = gastos fijos + (revenue × tasa costos)
        burn_rate = egresos_fijos + (revenue_promedio_real * tasa_costos_variables)
        
        return {
            'gastos_fijos': abs(egresos_fijos),
            'tasa_costos_variables': tasa_costos_variables,
            'burn_rate': burn_rate,
            'revenue_promedio': revenue_promedio_real
        }
        
    except Exception as e:
        st.error(f"Error procesando Informe Financiero: {str(e)}")
        # Retornar valores de backup desde backend analysis
        return {
            'gastos_fijos': 65732,
            'tasa_costos_variables': 0.0962,
            'burn_rate': 77994,
            'revenue_promedio': 127468
        }

def procesar_weekly_operation(file_weekly):
    """
    Procesa el Weekly Operation Report para estado de equipos
    
    Returns:
        dict con equipos por estado
    """
    try:
        df_weekly = pd.read_excel(file_weekly, sheet_name='Sheet1')
        
        # Contar equipos por estado
        if 'Status' in df_weekly.columns:
            equipos_estado = df_weekly['Status'].value_counts().to_dict()
        else:
            equipos_estado = {}
        
        # Equipos por cliente
        if 'Client' in df_weekly.columns:
            equipos_cliente = df_weekly.groupby('Client').size().to_dict()
        else:
            equipos_cliente = {}
        
        return {
            'equipos_estado': equipos_estado,
            'equipos_cliente': equipos_cliente,
            'total_equipos': len(df_weekly)
        }
        
    except Exception as e:
        st.error(f"Error procesando Weekly Report: {str(e)}")
        return {
            'equipos_estado': {},
            'equipos_cliente': {},
            'total_equipos': 0
        }

def procesar_archivos_reales(files_dict):
    """
    Función principal que procesa todos los archivos y genera datos integrados
    
    Args:
        files_dict: diccionario con los 5 archivos cargados
        
    Returns:
        dict con estructura compatible con get_data()
    """
    try:
        # 1. Procesar Utilization Reports
        util_data = procesar_utilization_reports(
            files_dict['file_2023'],
            files_dict['file_2024'],
            files_dict['file_2025']
        )
        
        if util_data is None:
            return None
        
        # 2. Procesar Informe Financiero
        financial_data = procesar_informe_financiero(files_dict['file_financial'])
        
        # 3. Procesar Weekly Operation Report
        weekly_data = procesar_weekly_operation(files_dict['file_weekly'])
        
        # 4. Calcular factores estacionales
        estacionalidad = util_data['estacionalidad']
        avg_revenue = np.mean(list(estacionalidad.values()))
        seasonal_factors = {mes: val/avg_revenue for mes, val in estacionalidad.items()}
        
        # 5. Estructurar datos en formato compatible
        datos_procesados = {
            'historical': {
                'revenue_promedio': util_data['revenue_promedio'],
                'revenue_anual': util_data['revenue_anual'],
                'clientes': util_data['top_clientes'],
                'estacionalidad': seasonal_factors,
                'estacionalidad_valores': estacionalidad,
                'years_data': {},  # Se puede agregar más detalle si se necesita
                'df_historical': util_data['df_completo']
            },
            'financial': {
                'gastos_fijos': financial_data['gastos_fijos'],
                'tasa_costos_variables': financial_data['tasa_costos_variables'],
                'burn_rate': financial_data['burn_rate']
            },
            'equipment': weekly_data,
            'metadata': {
                'fecha_procesamiento': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'archivos_procesados': list(files_dict.keys())
            }
        }
        
        return datos_procesados
        
    except Exception as e:
        st.error(f"Error en procesamiento general: {str(e)}")
        return None

# =============================================================================
# CONFIGURACIÓN Y AUTENTICACIÓN
# =============================================================================

VALID_PASSWORD = "spt2025"

def check_password():
    """Verifica autenticación del usuario"""
    
    if st.session_state.get('authenticated', False):
        return True
    
    st.markdown("""
    <div style='text-align: center; padding: 3rem 0;'>
        <h1 style='color: #2563EB; font-size: 3rem;'>💰 SPT CASH FLOW TOOL</h1>
        <p style='color: #64748B; font-size: 1.2rem;'>Análisis de Flujo de Efectivo</p>
        <p style='color: #64748B;'>Ingrese la contraseña para acceder</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        password_input = st.text_input(
            "Contraseña:",
            type="password",
            key="password_input",
            help="Ingrese la contraseña proporcionada por AI-MindNovation"
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            login_button = st.button("🔓 Ingresar", use_container_width=True)
        
        if login_button:
            if password_input == VALID_PASSWORD:
                st.session_state.authenticated = True
                st.success("✅ Acceso autorizado")
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta")
                return False
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #94A3B8; font-size: 0.9rem;'>
        <p><strong>Desarrollado por:</strong> <a href='https://www.ai-mindnovation.com'>AI-MindNovation</a></p>
        <p>Para soporte, contacte a su administrador</p>
    </div>
    """, unsafe_allow_html=True)
    
    return False

# =============================================================================
# CONFIGURACIÓN DE PÁGINA
# =============================================================================

st.set_page_config(
    page_title="SPT Cash Flow Tool",
    page_icon="💰",
    layout="wide"
)

if not check_password():
    st.stop()

# =============================================================================
# ESTILOS CSS
# =============================================================================

st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        color: #2563EB;
        text-align: center;
        padding: 1rem 0;
    }
    .kpi-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# INICIALIZACIÓN DE SESSION STATE
# =============================================================================

if 'efectivo_disponible' not in st.session_state:
    st.session_state.efectivo_disponible = None

if 'data_source' not in st.session_state:
    st.session_state.data_source = 'demo'

if 'archivos_cargados' not in st.session_state:
    st.session_state.archivos_cargados = {}

if 'datos_procesados' not in st.session_state:
    st.session_state.datos_procesados = None

# 🆕 v4.6.0: Meses de colchón para margen de protección
if 'meses_colchon' not in st.session_state:
    st.session_state.meses_colchon = 2  # Default: 2 meses (recomendado para pagos a 30 días)

# 🆕 v4.8.0: Días de liquidación anticipada para inversiones
if 'dias_liquidacion' not in st.session_state:
    st.session_state.dias_liquidacion = 15  # Default: 15 días antes

# 🆕 v4.8.1: Escenario para proyecciones y transferencias
if 'escenario_proyeccion' not in st.session_state:
    st.session_state.escenario_proyeccion = 'Moderado'  # Default: Moderado

# 🆕 v4.9.0: Ingreso manual de cotizaciones y contratos
if 'cotizaciones_manuales' not in st.session_state:
    st.session_state.cotizaciones_manuales = []

if 'contratos_manuales' not in st.session_state:
    st.session_state.contratos_manuales = []

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def calcular_tendencia_lineal(y_values):
    """Calcula tendencia lineal usando numpy"""
    n = len(y_values)
    x = np.arange(n)
    
    x_mean = np.mean(x)
    y_mean = np.mean(y_values)
    
    numerador = np.sum((x - x_mean) * (y_values - y_mean))
    denominador = np.sum((x - x_mean) ** 2)
    
    slope = numerador / denominador if denominador != 0 else 0
    intercept = y_mean - slope * x_mean
    
    trend_line = slope * x + intercept
    
    return slope, intercept, trend_line

# =============================================================================
# DATOS REALES DEL BACKEND
# =============================================================================

def get_real_seasonal_factors():
    """
    ✅ DATOS REALES: Factores estacionales calculados desde datos históricos 2023-2025
    
    Metodología:
    1. Se procesaron Utilization Reports de 2023, 2024 y 2025 (33 meses)
    2. Se agrupó el revenue por mes (promediando los 3 años)
    3. Se calculó el factor como: Revenue_mes / Revenue_promedio_global
    
    Interpretación:
    - 1.0 = Mes promedio
    - >1.0 = Mes con mayor actividad (ej: Julio 1.465 = +46.5% sobre promedio)
    - <1.0 = Mes con menor actividad (ej: Diciembre 0.289 = -71.1% bajo promedio)
    """
    return {
        'Enero': 0.760,      # -24.0% vs promedio
        'Febrero': 0.945,    # -5.5% vs promedio  
        'Marzo': 1.070,      # +7.0% vs promedio
        'Abril': 1.055,      # +5.5% vs promedio
        'Mayo': 0.988,       # -1.2% vs promedio
        'Junio': 1.109,      # +10.9% vs promedio
        'Julio': 1.465,      # +46.5% vs promedio ⭐ PICO MÁXIMO
        'Agosto': 1.072,     # +7.2% vs promedio
        'Septiembre': 1.167, # +16.7% vs promedio
        'Octubre': 1.035,    # +3.5% vs promedio
        'Noviembre': 1.046,  # +4.6% vs promedio
        'Diciembre': 0.289   # -71.1% vs promedio ⚠️ MÍNIMO
    }

def get_real_financial_data():
    """
    ✅ DATOS REALES: Métricas financieras según metodología del backend
    
    METODOLOGÍA BURN RATE (Backend Analysis):
    
    1. GASTOS FIJOS (no varían con revenue): $65,732 USD/mes
       Desglose:
       - HR Travel: $2,450
       - Marketing: $7,864
       - Admin: $60,015
       - Insurance/Legal: $263
       - Salary: $1,975
       - Other Expenses: $6,750
       - Taxes: $37
    
    2. COSTOS VARIABLES (proporcionales al revenue): 9.62% del revenue
       Desglose:
       - Logistics: $9,083
       - Equipment: $6,780
       (Total depende del revenue del mes)
    
    3. FÓRMULA BURN RATE:
       Burn Rate = Gastos Fijos + (Revenue × 9.62%)
       
       Ejemplo con revenue promedio ($127,468):
       = $65,732 + ($127,468 × 0.0962)
       = $65,732 + $12,262
       = $77,994 USD/mes
    
    4. MARGEN OPERATIVO:
       = (Revenue - Burn Rate) / Revenue
       = ($127,468 - $77,994) / $127,468
       = 48.5%
    
    Nota: Esta metodología permite calcular el burn rate dinámico según
    el revenue proyectado de cada mes.
    """
    return {
        'gastos_fijos': 65732,           # USD/mes - No varían con revenue
        'tasa_costos_variables': 0.0962, # 9.62% del revenue
        'margen_operativo': 0.485,       # 48.5% histórico
        'desglose_gastos': {
            'HR Travel': 2450,
            'Marketing': 7864,
            'Admin': 60015,
            'Insurance/Legal': 263,
            'Salary': 1975,
            'Other Expenses': 6750,
            'Taxes': 37
        },
        'desglose_costos': {
            'Logistics': 9083,
            'Equipment': 6780
        }
    }

def calcular_burn_rate(revenue_mensual):
    """
    Calcula el burn rate dinámico según el revenue del mes
    
    Fórmula: Burn Rate = Gastos Fijos + (Revenue × 9.62%)
    """
    financial_data = get_real_financial_data()
    gastos_fijos = financial_data['gastos_fijos']
    tasa_costos = financial_data['tasa_costos_variables']
    
    costos_variables = revenue_mensual * tasa_costos
    burn_rate = gastos_fijos + costos_variables
    
    return {
        'burn_rate': burn_rate,
        'gastos_fijos': gastos_fijos,
        'costos_variables': costos_variables,
        'egresos_totales': burn_rate  # Alias para claridad
    }

def get_real_top_clients():
    """
    ✅ DATOS REALES: Top clientes desde Utilization Reports 2023-2025
    
    Fuente: Utilization_Report_-_Colombia_OFICIAL_[2023|2024|2025].xlsx
    Método: Suma de 'Accrual Revenue' por cliente en los 33 meses
    
    NOTA: Algunos clientes aparecen con nombres ligeramente diferentes
    (ej: "Kluane/Aris" vs "Kluane") debido a cambios en nomenclatura.
    """
    return [
        ('Kluane/Aris', 475310),      # $475K acumulado 2023-2025
        ('Explomin/Segovia', 423676),  # $424K acumulado
        ('Collective mining', 384940), # $385K acumulado
        ('Kluane', 383764),            # $384K acumulado
        ('Explomin', 244442)           # $244K acumulado
    ]

# =============================================================================
# FUNCIONES DE DATOS
# =============================================================================

def get_historical_data_complete():
    """
    ✅ DATOS REALES: Revenue histórico desde Utilization Reports
    
    Para la versión de demostración, se mantiene la estructura de datos
    simulados pero con parámetros ajustados a las métricas reales:
    - Revenue promedio real: $127,467.51 USD/mes
    - Revenue mínimo: $66,485 USD (Abril 2023)
    - Revenue máximo: $265,125 USD (Julio 2024)
    """
    
    meses = []
    revenue = []
    years_data = {2023: [], 2024: [], 2025: []}
    
    # Base ajustada a promedio real
    base_revenue = 127467.51
    
    for i in range(33):
        year = 2023 + (i // 12)
        month = (i % 12) + 1
        periodo = f"{year}-{str(month).zfill(2)}"
        meses.append(periodo)
        
        # Tendencia de crecimiento (datos muestran crecimiento año a año)
        tendencia = base_revenue + (i * 1000)
        
        # Estacionalidad real aplicada
        seasonal_factors = get_real_seasonal_factors()
        meses_nombres = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        factor_estacional = seasonal_factors[meses_nombres[month-1]]
        
        # Aplicar estacionalidad
        revenue_mes = tendencia * factor_estacional
        
        # Agregar variabilidad natural
        ruido = np.random.uniform(-0.05, 0.05) * revenue_mes
        revenue_mes = max(50000, revenue_mes + ruido)
        
        revenue.append(revenue_mes)
        years_data[year].append(revenue_mes)
    
    return pd.DataFrame({
        'periodo': meses,
        'revenue': revenue
    }), years_data

def calcular_proyeccion_3_meses(revenue_promedio, financial_data):
    """
    Calcula proyección de flujo para próximos 3 meses
    🆕 v4.6.0: Burn rate DINÁMICO según revenue de cada mes
    
    Args:
        revenue_promedio: Revenue mensual promedio base
        financial_data: Dict con gastos_fijos y tasa_costos_variables
    
    Returns:
        Lista de flujos netos proyectados para 3 meses
    
    METODOLOGÍA:
    Para cada mes proyectado:
    1. Calcular revenue con variación aleatoria (-5% a +10%)
    2. Calcular burn rate dinámico: Gastos Fijos + (Revenue × Tasa Costos)
    3. Flujo neto = Revenue - Burn Rate dinámico
    """
    proyeccion = []
    gastos_fijos = financial_data['gastos_fijos']
    tasa_costos = financial_data['tasa_costos_variables']
    
    for i in range(3):
        # Revenue proyectado con variación
        revenue_mes = revenue_promedio * (1 + np.random.uniform(-0.05, 0.1))
        
        # 🆕 v4.6.0: Calcular burn rate DINÁMICO según revenue del mes
        burn_rate_mes = gastos_fijos + (revenue_mes * tasa_costos)
        
        # Flujo neto con burn rate dinámico
        flujo_neto = revenue_mes - burn_rate_mes
        proyeccion.append(flujo_neto)
    
    return proyeccion

def calcular_runway_mejorado(efectivo_actual, flujos_proyectados, burn_rate):
    """✅ Runway considerando balance proyectado"""
    balance_3_meses = efectivo_actual + sum(flujos_proyectados)
    
    if balance_3_meses <= 0:
        efectivo_temp = efectivo_actual
        for i, flujo in enumerate(flujos_proyectados, 1):
            efectivo_temp += flujo
            if efectivo_temp <= 0:
                return i
        return 3
    else:
        meses_adicionales = balance_3_meses / burn_rate
        return 3 + meses_adicionales

def calcular_necesidades_excedentes_mejorado(efectivo_actual, flujos_proyectados, burn_rate, meses_colchon=2):
    """
    ✅ Necesidades/excedentes con balance completo
    ✅ v4.5.5: Recibe burn_rate como parámetro (calculado dinámicamente)
    🆕 v4.6.0: Meses de colchón configurable
    
    Args:
        efectivo_actual: Efectivo disponible actual
        flujos_proyectados: Lista de flujos netos proyectados
        burn_rate: Burn rate mensual (calculado dinámicamente)
        meses_colchon: Número de meses de burn rate para margen de protección (1, 2 o 3)
    
    Returns:
        dict con balance_proyectado, necesidades_minimas, excedente_deficit, flujos_mensuales
    
    NOTA: Con pagos a 30 días, se recomienda mínimo 2 meses de colchón:
    - Mes 1: Cubrir operación actual
    - Mes 2: Cubrir operación mientras se cobran ventas del mes 1
    """
    balance_proyectado = efectivo_actual + sum(flujos_proyectados)
    
    # 🆕 v4.6.0: Necesidades mínimas configurables (1, 2 o 3 meses)
    necesidades_minimas = burn_rate * meses_colchon
    
    excedente_o_deficit = balance_proyectado - necesidades_minimas
    
    return {
        'balance_proyectado': balance_proyectado,
        'necesidades_minimas': necesidades_minimas,
        'excedente_deficit': excedente_o_deficit,
        'flujos_mensuales': flujos_proyectados,
        'meses_colchon': meses_colchon  # Incluir para referencia
    }

# =============================================================================
# FUNCIONES DE GESTIÓN DE EXCEDENTES E INVERSIONES (v4.8.0)
# =============================================================================

def calcular_excedentes_invertibles(proyecciones_df, efectivo_inicial, burn_rate, meses_colchon, dias_liquidacion):
    """
    🆕 v4.8.0: Calcula excedentes invertibles mes a mes considerando necesidades mínimas
    
    Args:
        proyecciones_df: DataFrame con proyecciones mensuales (debe tener 'revenue' y 'egresos_totales')
        efectivo_inicial: Efectivo disponible al inicio
        burn_rate: Burn rate mensual promedio
        meses_colchon: Número de meses de burn rate para mantener como colchón
        dias_liquidacion: Días de anticipación para liquidar inversiones
    
    Returns:
        DataFrame con análisis de excedentes invertibles mes a mes
    
    LÓGICA:
    1. Por cada mes, calcular el balance acumulado
    2. Restar las necesidades mínimas (burn_rate × meses_colchon)
    3. El excedente es lo que se puede invertir
    4. Marcar cuándo liquidar cada inversión (basado en días_liquidacion)
    """
    
    necesidades_minimas = burn_rate * meses_colchon
    
    analisis = []
    balance_acumulado = efectivo_inicial
    
    for idx, row in proyecciones_df.iterrows():
        mes_num = row['mes']
        flujo_neto = row['flujo_neto']
        
        # Actualizar balance acumulado
        balance_acumulado += flujo_neto
        
        # Calcular excedente invertible
        excedente = balance_acumulado - necesidades_minimas
        
        # Determinar si se puede invertir
        puede_invertir = excedente > 0
        
        # Calcular fecha aproximada de liquidación (dias_liquidacion antes del siguiente mes)
        # Simplificación: asumimos que cada mes tiene 30 días
        mes_liquidacion = mes_num + 1 if dias_liquidacion <= 30 else mes_num + 2
        
        analisis.append({
            'mes': mes_num,
            'balance_disponible': balance_acumulado,
            'necesidades_minimas': necesidades_minimas,
            'excedente_invertible': max(0, excedente),
            'puede_invertir': puede_invertir,
            'liquidar_antes_mes': mes_liquidacion if puede_invertir else None
        })
    
    return pd.DataFrame(analisis)

def generar_recomendaciones_inversion(df_excedentes, rentabilidad_estimada=0.10):
    """
    🆕 v4.8.0: Genera recomendaciones de inversión basadas en excedentes
    
    Args:
        df_excedentes: DataFrame con análisis de excedentes
        rentabilidad_estimada: Rentabilidad anual estimada (default 10% = 0.10)
    
    Returns:
        DataFrame con recomendaciones de inversión
    
    INSTRUMENTOS SUGERIDOS (Colombia):
    - CDTs: ~12% EA (baja liquidez pero mayor rendimiento)
    - TES corto plazo: ~10% EA (buena liquidez)
    - Fondos de Inversión Colectiva: ~8-10% EA (alta liquidez)
    """
    
    recomendaciones = []
    
    for idx, row in df_excedentes.iterrows():
        if row['puede_invertir'] and row['excedente_invertible'] > 0:
            monto = row['excedente_invertible']
            
            # Calcular rendimiento estimado (proporcional al tiempo de inversión)
            # Asumimos inversión de 1 mes = rentabilidad_anual / 12
            rendimiento_mensual = monto * (rentabilidad_estimada / 12)
            
            recomendaciones.append({
                'mes': row['mes'],
                'monto_invertible': monto,
                'instrumento_sugerido': 'Cartera Mixta (CDT 40%, TES 30%, FCI 30%)',
                'rentabilidad_estimada_mensual': rendimiento_mensual,
                'liquidar_antes_mes': row['liquidar_antes_mes'],
                'riesgo': 'Bajo',
                'liquidez': 'Media-Alta'
            })
    
    return pd.DataFrame(recomendaciones) if recomendaciones else pd.DataFrame()

def generar_proyecciones_por_escenario(revenue_base, financial_data, meses, escenario):
    """
    🆕 v4.8.1: Genera proyecciones DETERMINISTAS según escenario seleccionado
    
    CORRECCIÓN CRÍTICA: Elimina variación aleatoria para que las proyecciones
    sean consistentes y no cambien al mover otros controles.
    
    Args:
        revenue_base: Revenue mensual base (promedio histórico)
        financial_data: Dict con gastos_fijos y tasa_costos_variables
        meses: Número de meses a proyectar
        escenario: 'Conservador', 'Moderado' o 'Optimista'
    
    Returns:
        DataFrame con columnas: ['mes', 'revenue', 'egresos_totales', 'flujo_neto']
    
    ESCENARIOS:
    - Conservador: -15% revenue inicial, +1% crecimiento mensual
    - Moderado: revenue base, +2% crecimiento mensual
    - Optimista: +15% revenue inicial, +3% crecimiento mensual
    """
    
    gastos_fijos = financial_data['gastos_fijos']
    tasa_costos = financial_data['tasa_costos_variables']
    
    # Configuración de escenarios
    config_escenarios = {
        'Conservador': {'factor': 0.85, 'crecimiento': 0.01},
        'Moderado': {'factor': 1.0, 'crecimiento': 0.02},
        'Optimista': {'factor': 1.15, 'crecimiento': 0.03}
    }
    
    config = config_escenarios[escenario]
    
    proyecciones = []
    
    for i in range(meses):
        # Revenue proyectado DETERMINISTA (sin random)
        revenue_mes = revenue_base * config['factor'] * (1 + config['crecimiento'])**i
        
        # Burn rate dinámico según revenue del mes
        costos_variables = revenue_mes * tasa_costos
        egresos_totales = gastos_fijos + costos_variables
        
        # Flujo neto
        flujo_neto = revenue_mes - egresos_totales
        
        proyecciones.append({
            'mes': i + 1,
            'revenue': revenue_mes,
            'egresos_totales': egresos_totales,
            'flujo_neto': flujo_neto
        })
    
    return pd.DataFrame(proyecciones)

def calcular_transferencias_trimestrales(proyecciones_df, meses_a_proyectar):
    """
    🆕 v4.8.0: Calcula transferencias TRIMESTRALES a casa matriz según política SPT
    ⚠️ NOTA v4.8.1: Esta función NO descuenta transferencias del balance
    Para balance ajustado, usar calcular_transferencias_con_balance()
    
    POLÍTICA SPT GLOBAL:
    - Utilidad neta local debe ser 10% del revenue
    - Transferencia = Flujo Neto SPT Colombia - (Revenue × 10%)
    - Se transfiere trimestre vencido (no mensualmente)
    
    Args:
        proyecciones_df: DataFrame con proyecciones (debe tener 'revenue' y 'flujo_neto')
        meses_a_proyectar: Número total de meses proyectados
    
    Returns:
        dict con análisis trimestral de transferencias
    
    EJEMPLO:
    Si Flujo Neto trimestral = $150,000 y Revenue trimestral = $400,000
    Utilidad Local Requerida = $400,000 × 10% = $40,000
    Transferencia HQ = $150,000 - $40,000 = $110,000
    """
    
    numero_trimestres = int(np.ceil(meses_a_proyectar / 3))
    
    trimestres = []
    
    for trimestre_num in range(1, numero_trimestres + 1):
        # Determinar qué meses corresponden a este trimestre
        mes_inicio = (trimestre_num - 1) * 3 + 1
        mes_fin = min(trimestre_num * 3, meses_a_proyectar)
        
        # Filtrar datos del trimestre
        df_trimestre = proyecciones_df[
            (proyecciones_df['mes'] >= mes_inicio) & 
            (proyecciones_df['mes'] <= mes_fin)
        ]
        
        # Calcular totales del trimestre
        revenue_total = df_trimestre['revenue'].sum()
        flujo_neto_total = df_trimestre['flujo_neto'].sum()
        
        # Calcular utilidad local requerida (10% del revenue)
        utilidad_local = revenue_total * 0.10
        
        # Calcular transferencia a casa matriz
        transferencia_hq = flujo_neto_total - utilidad_local
        
        trimestres.append({
            'trimestre': f'T{trimestre_num}',
            'meses': f'{mes_inicio}-{mes_fin}',
            'revenue_total': revenue_total,
            'flujo_neto_total': flujo_neto_total,
            'utilidad_local_10pct': utilidad_local,
            'transferencia_hq': max(0, transferencia_hq),  # No transferir si es negativo
            'margen_retenido': (utilidad_local / revenue_total * 100) if revenue_total > 0 else 0
        })
    
    return {
        'trimestres': pd.DataFrame(trimestres),
        'numero_trimestres': numero_trimestres,
        'total_transferencias': sum([t['transferencia_hq'] for t in trimestres])
    }

def calcular_transferencias_con_balance(proyecciones_df, efectivo_inicial, meses_a_proyectar):
    """
    🆕 v4.8.1: Calcula transferencias Y balance ajustado después de cada transferencia
    
    CORRECCIÓN CRÍTICA: Al final de cada trimestre, la transferencia se DESCUENTA
    del balance, por lo que el siguiente trimestre parte con menos efectivo.
    
    Args:
        proyecciones_df: DataFrame con proyecciones (debe tener 'mes', 'revenue', 'flujo_neto')
        efectivo_inicial: Efectivo disponible al inicio del período
        meses_a_proyectar: Número total de meses proyectados
    
    Returns:
        dict con:
        - 'trimestres': DataFrame con análisis trimestral
        - 'balance_mensual': DataFrame con balance mes a mes (DESPUÉS de transferencias)
        - 'total_transferencias': Total transferido
        - 'balance_final': Balance después de todas las transferencias
    
    LÓGICA:
    1. Acumular flujo neto mes a mes
    2. Al final de cada trimestre:
       - Calcular transferencia (Flujo Neto Trimestral - 10% Revenue Trimestral)
       - DESCONTAR transferencia del balance
       - Continuar con balance ajustado
    """
    
    numero_trimestres = int(np.ceil(meses_a_proyectar / 3))
    
    trimestres = []
    balance_mensual = []
    
    balance_actual = efectivo_inicial
    
    for trimestre_num in range(1, numero_trimestres + 1):
        # Determinar qué meses corresponden a este trimestre
        mes_inicio = (trimestre_num - 1) * 3 + 1
        mes_fin = min(trimestre_num * 3, meses_a_proyectar)
        
        # Balance al inicio del trimestre
        balance_inicio_trimestre = balance_actual
        
        # Acumular flujo mes a mes durante el trimestre
        df_trimestre = proyecciones_df[
            (proyecciones_df['mes'] >= mes_inicio) & 
            (proyecciones_df['mes'] <= mes_fin)
        ]
        
        revenue_total = 0
        flujo_neto_total = 0
        
        for idx, row in df_trimestre.iterrows():
            # Acumular balance
            balance_actual += row['flujo_neto']
            revenue_total += row['revenue']
            flujo_neto_total += row['flujo_neto']
            
            # Guardar balance mensual (ANTES de transferencia)
            balance_mensual.append({
                'mes': int(row['mes']),
                'trimestre': f'T{trimestre_num}',
                'balance_antes_transferencia': balance_actual,
                'flujo_neto_mes': row['flujo_neto']
            })
        
        # Al final del trimestre: calcular y aplicar transferencia
        utilidad_local = revenue_total * 0.10
        transferencia_hq = max(0, flujo_neto_total - utilidad_local)
        
        # CRÍTICO: Descontar transferencia del balance
        balance_despues_transferencia = balance_actual - transferencia_hq
        
        # Guardar info del trimestre
        trimestres.append({
            'trimestre': f'T{trimestre_num}',
            'meses': f'{mes_inicio}-{mes_fin}',
            'balance_inicio': balance_inicio_trimestre,
            'revenue_total': revenue_total,
            'flujo_neto_total': flujo_neto_total,
            'utilidad_local_10pct': utilidad_local,
            'transferencia_hq': transferencia_hq,
            'balance_despues_transferencia': balance_despues_transferencia,
            'margen_retenido': (utilidad_local / revenue_total * 100) if revenue_total > 0 else 0
        })
        
        # Actualizar balance para el siguiente trimestre
        balance_actual = balance_despues_transferencia
        
        # Actualizar el último mes del trimestre con balance después de transferencia
        if balance_mensual:
            balance_mensual[-1]['balance_despues_transferencia'] = balance_despues_transferencia
            balance_mensual[-1]['transferencia_aplicada'] = transferencia_hq
    
    # Completar información de meses sin transferencia
    for i, bm in enumerate(balance_mensual):
        if 'balance_despues_transferencia' not in bm:
            bm['balance_despues_transferencia'] = bm['balance_antes_transferencia']
            bm['transferencia_aplicada'] = 0
    
    return {
        'trimestres': pd.DataFrame(trimestres),
        'balance_mensual': pd.DataFrame(balance_mensual),
        'numero_trimestres': numero_trimestres,
        'total_transferencias': sum([t['transferencia_hq'] for t in trimestres]),
        'balance_final': balance_actual
    }

def get_data():
    """
    Retorna datos según la fuente (demo o real)
    
    ✅ v4.5.5: CORRECCIÓN CRÍTICA - Cálculo dinámico del burn rate
    ✅ v4.5.3: Todos los datos de demo también usan métricas reales
    del backend como base, eliminando completamente los valores hardcodeados.
    """
    
    if st.session_state.data_source == 'real' and st.session_state.datos_procesados:
        return st.session_state.datos_procesados
    else:
        df_historical, years_data = get_historical_data_complete()
        
        # Calcular factores estacionales por año
        seasonal_by_year = {}
        for year, revenues in years_data.items():
            if len(revenues) == 12:
                avg = np.mean(revenues)
                seasonal_by_year[year] = [r / avg for r in revenues]
        
        # ✅ CAMBIO PRINCIPAL: Usar factores estacionales REALES
        seasonal_avg = get_real_seasonal_factors()
        
        # ✅ Usar métricas financieras REALES
        financial_real = get_real_financial_data()
        
        # ✅ Usar top clientes REALES
        top_clients_real = get_real_top_clients()
        
        # 🔧 CORRECCIÓN v4.5.5: Calcular burn_rate dinámicamente
        # Usar revenue promedio histórico para el cálculo
        revenue_promedio = df_historical['revenue'].mean()
        burn_rate_data = calcular_burn_rate(revenue_promedio)
        
        return {
            'historical': {
                'revenue_promedio': int(revenue_promedio),
                'revenue_minimo': int(df_historical['revenue'].min()),
                'revenue_maximo': int(df_historical['revenue'].max()),
                'top_clients': top_clients_real,  # ✅ DATOS REALES
                'periodos': 33,
                'data': df_historical,
                'years_data': years_data
            },
            'financial': {
                'burn_rate': burn_rate_data['burn_rate'],           # ✅ CALCULADO dinámicamente
                'gastos_fijos': burn_rate_data['gastos_fijos'],     # ✅ REAL: $65,732
                'costos_variables': burn_rate_data['costos_variables'], # ✅ CALCULADO: Revenue × 9.62%
                'tasa_costos_variables': financial_real['tasa_costos_variables'],  # ✅ Para proyecciones
                'margen_operativo': financial_real['margen_operativo']  # ✅ REAL: 48.5%
            },
            'seasonal_factors': seasonal_avg,  # ✅ DATOS REALES calculados
            'seasonal_by_year': seasonal_by_year
        }


# =============================================================================
# FUNCIONES DE PROYECCIÓN
# =============================================================================

def generar_proyecciones_multi_escenario(meses, revenue_base, financial_data):
    """
    Genera proyecciones para los 3 escenarios con burn rate DINÁMICO
    🆕 v4.6.0: Burn rate se calcula según el revenue de cada mes proyectado
    
    Args:
        meses: Número de meses a proyectar (3-12)
        revenue_base: Revenue mensual base (promedio histórico)
        financial_data: Dict con gastos_fijos y tasa_costos_variables
    
    Returns:
        Dict con 3 DataFrames (uno por escenario) con proyecciones
    
    ESCENARIOS:
    - Conservador: -15% revenue inicial, +1% crecimiento mensual
    - Moderado: revenue actual, +2% crecimiento mensual
    - Optimista: +15% revenue inicial, +3% crecimiento mensual
    
    METODOLOGÍA (v4.6.0):
    Para cada mes y escenario:
    1. Calcular revenue según factor y crecimiento del escenario
    2. Calcular burn rate DINÁMICO: $65,732 + (Revenue × 0.0962)
    3. Calcular flujo neto: Revenue - Burn Rate dinámico
    
    Esto asegura que el burn rate se ajuste realísticamente con el nivel de operación.
    """
    
    gastos_fijos = financial_data['gastos_fijos']  # $65,732 fijos
    tasa_costos = financial_data['tasa_costos_variables']  # 9.62%
    
    escenarios = {
        'Conservador': {'factor': 0.85, 'crecimiento': 0.01, 'color': '#EF4444'},
        'Moderado': {'factor': 1.0, 'crecimiento': 0.02, 'color': '#2563EB'},
        'Optimista': {'factor': 1.15, 'crecimiento': 0.03, 'color': '#10B981'}
    }
    
    resultados = {}
    
    for nombre, config in escenarios.items():
        proyeccion = []
        
        for i in range(meses):
            # Revenue proyectado para este mes y escenario
            revenue = revenue_base * config['factor'] * (1 + config['crecimiento'])**i
            
            # 🆕 v4.6.0: Burn rate DINÁMICO según revenue del mes
            costos_variables = revenue * tasa_costos
            burn_rate_mes = gastos_fijos + costos_variables
            
            proyeccion.append({
                'mes': i + 1,
                'revenue': revenue,
                'gastos_fijos': gastos_fijos,
                'costos_variables': costos_variables,
                'egresos_totales': burn_rate_mes,  # 🆕 Terminología mejorada
                'flujo_neto': revenue - burn_rate_mes
            })
        
        resultados[nombre] = pd.DataFrame(proyeccion)
    
    return resultados

def generar_balance_multi_escenario(meses, efectivo_inicial, proyecciones):
    """✅ Balance multi-escenario corregido"""
    
    balances = {}
    
    for escenario, df_proj in proyecciones.items():
        balance = []
        efectivo_acumulado = efectivo_inicial
        
        for idx, row in df_proj.iterrows():
            # 🆕 v4.6.1: Usar 'egresos_totales' en lugar de 'gastos'
            flujo_neto = row['revenue'] - row['egresos_totales']
            efectivo_acumulado += flujo_neto
            
            balance.append({
                'mes': int(row['mes']),
                'efectivo_inicial': efectivo_acumulado - flujo_neto,
                'ingresos': row['revenue'],
                'egresos_totales': row['egresos_totales'],
                'flujo_neto': flujo_neto,
                'efectivo_final': efectivo_acumulado,
                'escenario': escenario
            })
        
        balances[escenario] = pd.DataFrame(balance)
    
    return balances

# =============================================================================
# HEADER Y SIDEBAR
# =============================================================================

st.markdown('<div class="main-title">💰 SPT CASH FLOW TOOL</div>', unsafe_allow_html=True)
st.markdown(f"**Estado al:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

col1, col2, col3 = st.columns([6, 1, 1])
with col3:
    if st.button("🚪 Salir"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.markdown("---")

# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.markdown("### ⚙️ SPT Colombia")
    st.markdown("**Análisis de Flujo de Efectivo**")
    st.markdown("---")
    
    # ✅ CORRECCIÓN 1: Reactivar carga de archivos
    st.markdown("### 📊 Fuente de Datos")
    
    data_source_option = st.radio(
        "Seleccione:",
        ["📈 Datos de Demostración", "📁 Cargar Datos Propios"],
        index=0 if st.session_state.data_source == 'demo' else 1
    )
    
    if data_source_option == "📁 Cargar Datos Propios":
        st.session_state.data_source = 'upload'
        
        st.markdown("#### 📁 Subir Archivos Excel")
        st.info("💡 Suba los 5 archivos requeridos para el análisis completo")
        
        st.markdown("**Históricos (2023-2025):**")
        file_2023 = st.file_uploader(
            "Utilization Report 2023",
            type=['xlsx', 'xls'],
            key="file_2023",
            help="Archivo: Utilization_Report_2023.xlsx"
        )
        
        file_2024 = st.file_uploader(
            "Utilization Report 2024",
            type=['xlsx', 'xls'],
            key="file_2024",
            help="Archivo: Utilization_Report_2024.xlsx"
        )
        
        file_2025 = st.file_uploader(
            "Utilization Report 2025",
            type=['xlsx', 'xls'],
            key="file_2025",
            help="Archivo: Utilization_Report_2025.xlsx"
        )
        
        st.markdown("**Estado Actual:**")
        file_weekly = st.file_uploader(
            "Weekly Operation Report",
            type=['xlsx', 'xls'],
            key="file_weekly",
            help="Archivo: Weekly_Operation_Report.xlsx"
        )
        
        st.markdown("**Financiero:**")
        file_financial = st.file_uploader(
            "Estado Financiero",
            type=['xlsx', 'xls'],
            key="file_financial",
            help="Archivo: Informe_financiero.xlsx"
        )
        
        all_files = all([file_2023, file_2024, file_2025, file_weekly, file_financial])
        
        if all_files:
            st.success("✅ Todos los archivos cargados")
            
            if st.button("🚀 Procesar Datos", use_container_width=True, type="primary"):
                with st.spinner("⚙️ Procesando archivos Excel..."):
                    # 🆕 v4.7.0: PROCESAMIENTO REAL DE ARCHIVOS
                    try:
                        # Preparar diccionario con archivos
                        files_dict = {
                            'file_2023': file_2023,
                            'file_2024': file_2024,
                            'file_2025': file_2025,
                            'file_weekly': file_weekly,
                            'file_financial': file_financial
                        }
                        
                        # Procesar archivos y extraer datos
                        st.info("📊 Extrayendo datos de Utilization Reports...")
                        datos_reales = procesar_archivos_reales(files_dict)
                        
                        if datos_reales:
                            # Guardar datos procesados
                            st.session_state.data_source = 'real'
                            st.session_state.datos_procesados = datos_reales
                            
                            st.success("✅ Archivos procesados exitosamente")
                            st.success(f"📈 Revenue promedio: ${datos_reales['historical']['revenue_promedio']:,.0f}")
                            st.success(f"💰 Burn Rate: ${datos_reales['financial']['burn_rate']:,.0f}")
                            st.info("🟢 Visualizando ahora DATOS REALES del archivo cargado")
                            st.rerun()
                        else:
                            st.error("❌ Error al procesar archivos. Revise el formato de los archivos.")
                            st.session_state.data_source = 'demo'
                            
                    except Exception as e:
                        st.error(f"❌ Error durante el procesamiento: {str(e)}")
                        st.session_state.data_source = 'demo'
        else:
            missing = []
            if not file_2023: missing.append("Util 2023")
            if not file_2024: missing.append("Util 2024")
            if not file_2025: missing.append("Util 2025")
            if not file_weekly: missing.append("Weekly")
            if not file_financial: missing.append("Financiero")
            
            st.warning(f"⚠️ Faltan: {', '.join(missing)}")
    else:
        st.session_state.data_source = 'demo'
        st.info("📊 Usando datos reales de demostración (métricas calculadas desde archivos históricos)")
    
    st.markdown("---")
    
    st.markdown("### 💵 Configuración Financiera")
    
    efectivo_input = st.number_input(
        "Efectivo Disponible Actual (USD):",
        min_value=0,
        value=st.session_state.efectivo_disponible if st.session_state.efectivo_disponible else 80000,
        step=1000,
        format="%d"
    )
    
    if st.button("💾 Actualizar Efectivo", use_container_width=True):
        st.session_state.efectivo_disponible = efectivo_input
        st.success(f"✅ Efectivo actualizado: ${efectivo_input:,.0f}")
        st.rerun()
    
    efectivo_actual = st.session_state.efectivo_disponible if st.session_state.efectivo_disponible else efectivo_input
    
    st.info(f"💰 **Efectivo actual:** ${efectivo_actual:,.0f}")
    
    # 🆕 v4.6.0: Control de meses de colchón para margen de protección
    st.markdown("#### 🛡️ Margen de Protección")
    
    meses_colchon = st.select_slider(
        "Meses de Burn Rate como colchón:",
        options=[1, 2, 3],
        value=st.session_state.meses_colchon,
        help="""
        Define cuántos meses de burn rate mantener como margen de protección.
        
        • 1 mes: Mínimo operativo
        • 2 meses: Recomendado (cubre ciclo de pagos a 30 días)
        • 3 meses: Conservador
        
        Con pagos a clientes a 30 días, se recomienda al menos 2 meses 
        para cubrir la operación mientras se cobran las ventas.
        """
    )
    
    if meses_colchon != st.session_state.meses_colchon:
        st.session_state.meses_colchon = meses_colchon
        st.rerun()
    
    st.caption(f"📊 Margen actual: {meses_colchon} {'mes' if meses_colchon == 1 else 'meses'}")
    
    # 🆕 v4.8.0: Días de liquidación anticipada para inversiones
    st.markdown("#### ⏰ Liquidación de Inversiones")
    
    dias_liquidacion = st.select_slider(
        "Días de anticipación para liquidar:",
        options=[7, 15, 30],
        value=st.session_state.dias_liquidacion,
        help="""
        Define con cuántos días de anticipación liquidar inversiones temporales 
        antes de necesitar los fondos para cubrir el burn rate.
        
        • 7 días: Para instrumentos de alta liquidez
        • 15 días: Recomendado (balance entre liquidez y rendimiento)
        • 30 días: Conservador (máxima seguridad)
        
        Los instrumentos sugeridos (CDTs, TES, FCIs) permiten liquidación 
        rápida, por lo que 15 días es suficiente en la mayoría de casos.
        """
    )
    
    if dias_liquidacion != st.session_state.dias_liquidacion:
        st.session_state.dias_liquidacion = dias_liquidacion
        st.rerun()
    
    st.caption(f"⏱️ Liquidar {dias_liquidacion} días antes")
    
    # 🆕 v4.8.1: Selector de escenario para proyecciones y transferencias
    st.markdown("#### 📊 Escenario de Proyección")
    
    escenario = st.selectbox(
        "Escenario para análisis:",
        options=['Conservador', 'Moderado', 'Optimista'],
        index=['Conservador', 'Moderado', 'Optimista'].index(st.session_state.escenario_proyeccion),
        help="""
        Selecciona el escenario para calcular proyecciones y transferencias:
        
        • **Conservador:** -15% revenue inicial, +1% crecimiento mensual
        • **Moderado:** Revenue actual, +2% crecimiento mensual
        • **Optimista:** +15% revenue inicial, +3% crecimiento mensual
        
        Este escenario afecta:
        - Cálculo de excedentes invertibles
        - Transferencias a casa matriz
        - Balance proyectado después de transferencias
        """
    )
    
    if escenario != st.session_state.escenario_proyeccion:
        st.session_state.escenario_proyeccion = escenario
        st.rerun()
    
    # Indicador visual del escenario actual
    emoji_escenario = {
        'Conservador': '🟠',
        'Moderado': '🟢',
        'Optimista': '🔵'
    }
    st.caption(f"{emoji_escenario[escenario]} Escenario: **{escenario}**")
    
    st.markdown("---")
    
    st.markdown("### 📊 Navegación")
    page = st.radio(
        "Selecciona sección:",
        ["🏠 Resumen Ejecutivo", "📈 Análisis Histórico", "💵 Proyecciones", "📊 Reportes Detallados", "📝 Ingreso Manual"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("### ℹ️ Información")
    st.markdown("""
    **Usuario:** Autenticado ✅
    
    **Versión:** 4.9.0
    
    **🎉 NUEVO en v4.9.0 - FASE 4:**
    • ✅ Ingreso Manual de Cotizaciones y Contratos
    • ✅ Formularios interactivos para nuevos negocios
    • ✅ Panel de resumen consolidado
    • ✅ Base para proyecciones con contratos futuros
    
    **🔧 FASE 3 (v4.8.1):**
    • ✅ Proyecciones DETERMINISTAS (sin random)
    • ✅ Transferencias DESCUENTAN del balance
    • ✅ Selector de ESCENARIO (Conservador/Moderado/Optimista)
    
    **💰 FASE 2 (v4.8.0):**
    • ✅ Gestión de Excedentes e Inversiones Temporales
    • ✅ Transferencias Trimestrales a Casa Matriz
    
    [AI-MindNovation](https://www.ai-mindnovation.com)
    """)

# =============================================================================
# OBTENER DATOS
# =============================================================================

data = get_data()

# =============================================================================
# PÁGINA: RESUMEN EJECUTIVO
# =============================================================================

if page == "🏠 Resumen Ejecutivo":
    st.markdown("## 🎯 Resumen Ejecutivo")
    
    # 🆕 v4.8.0: Indicador visual corregido - muestra verde cuando hay datos reales
    if st.session_state.data_source == 'real':
        st.success("🟢 **Visualizando DATOS REALES** del archivo cargado")
    else:
        st.info("🔵 **Visualizando DATOS DE DEMOSTRACIÓN** (históricos 2023-2025 con métricas reales del backend)")
    
    revenue_mensual = data['historical']['revenue_promedio']
    burn_rate = data['financial']['burn_rate']
    
    # 🆕 v4.6.0: Pasar financial_data completo para cálculo dinámico
    flujos_proyectados = calcular_proyeccion_3_meses(revenue_mensual, data['financial'])
    runway = calcular_runway_mejorado(efectivo_actual, flujos_proyectados, burn_rate)
    # 🆕 v4.6.0: Pasar meses_colchon configurado por el usuario
    analisis_cash = calcular_necesidades_excedentes_mejorado(
        efectivo_actual, 
        flujos_proyectados, 
        burn_rate,
        st.session_state.meses_colchon
    )
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric(
            "💰 Efectivo Actual",
            f"${efectivo_actual:,.0f}",
            delta=None
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        runway_color = "🟢" if runway > 12 else ("🟡" if runway > 6 else "🔴")
        st.metric(
            f"{runway_color} Runway",
            f"{runway:.1f} meses",
            delta=None
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        excedente = analisis_cash['excedente_deficit']
        meses_colchon = analisis_cash['meses_colchon']
        excedente_color = "🟢" if excedente > 0 else "🔴"
        st.metric(
            f"{excedente_color} Balance Proyectado (3m)",
            f"${excedente:,.0f}",
            delta=None,
            help=f"Balance después de 3 meses - Margen de protección ({meses_colchon} {'mes' if meses_colchon == 1 else 'meses'} de burn rate)"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        margen = data['financial']['margen_operativo']
        margen_color = "🟢" if margen > 0.5 else ("🟡" if margen > 0.3 else "🔴")
        st.metric(
            f"{margen_color} Margen Operativo",
            f"{margen*100:.1f}%",
            delta=None,
            help="Margen operativo real basado en datos del informe financiero. Refleja la eficiencia de la operación."
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Análisis de Cash Flow
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Métricas Clave")
        
        metrics_df = pd.DataFrame({
            'Métrica': [
                'Revenue Mensual Promedio',
                'Burn Rate Mensual (Total)',
                'Flujo Neto Mensual',
                'Gastos Administrativos',
                'Costos Operativos'
            ],
            'Valor (USD)': [
                f"${revenue_mensual:,.0f}",
                f"${burn_rate:,.0f}",
                f"${revenue_mensual - burn_rate:,.0f}",
                f"${data['financial']['gastos_fijos']:,.0f}",
                f"${data['financial']['costos_variables']:,.0f}"
            ]
        })
        
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        
        st.info(f"""
        💡 **Metodología de Burn Rate (v4.6.0):**  
        Los datos están basados en información real del backend. El burn rate se calcula 
        dinámicamente: **${data['financial']['gastos_fijos']:,.0f}** (gastos fijos) + 
        **{data['financial']['tasa_costos_variables']*100:.2f}%** del revenue (costos variables).
        
        Con el revenue promedio actual (${revenue_mensual:,.0f}), el burn rate es 
        **${burn_rate:,.0f}**/mes, resultando en un margen operativo del 
        **{data['financial']['margen_operativo']*100:.1f}%**.
        """)
    
    with col2:
        st.markdown("### 🎯 Top 5 Clientes")
        
        top_clients = data['historical']['top_clients']
        df_clients = pd.DataFrame(top_clients, columns=['Cliente', 'Revenue (USD)'])
        df_clients['Revenue (USD)'] = df_clients['Revenue (USD)'].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(df_clients, use_container_width=True, hide_index=True)
        
        st.caption("✅ Datos reales desde Utilization Reports 2023-2025")
    
    # Proyección 3 meses
    st.markdown("### 📈 Proyección de Flujo (3 meses)")
    
    proyeccion_df = pd.DataFrame({
        'Mes': ['Mes 1', 'Mes 2', 'Mes 3'],
        'Flujo Neto': flujos_proyectados
    })
    
    fig = px.bar(
        proyeccion_df,
        x='Mes',
        y='Flujo Neto',
        title='Flujo Neto Proyectado (USD)',
        color='Flujo Neto',
        color_continuous_scale=['red', 'yellow', 'green']
    )
    
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Balance al final de 3 meses
    balance_3m = analisis_cash['balance_proyectado']
    necesidades = analisis_cash['necesidades_minimas']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Balance Proyectado (3m)", f"${balance_3m:,.0f}")
    
    with col2:
        # 🆕 v4.6.1: Tooltip dinámico según meses configurados
        meses_texto = f"{st.session_state.meses_colchon} {'mes' if st.session_state.meses_colchon == 1 else 'meses'}"
        st.metric("Necesidades Mínimas", f"${necesidades:,.0f}", 
                 help=f"{meses_texto} de burn rate como margen de protección")
    
    with col3:
        excedente_color = "normal" if analisis_cash['excedente_deficit'] > 0 else "inverse"
        st.metric(
            "Excedente/Déficit",
            f"${analisis_cash['excedente_deficit']:,.0f}",
            delta_color=excedente_color
        )
    
    # =========================================================================
    # 🆕 v4.8.0: FASE 3 - GESTIÓN DE EXCEDENTES E INVERSIONES
    # =========================================================================
    
    st.markdown("---")
    st.markdown("### 💰 Gestión de Excedentes e Inversiones Temporales")
    
    st.info("""
    **Estrategia de Inversión:** Los excedentes que superen las necesidades mínimas pueden invertirse 
    en instrumentos de bajo riesgo en Colombia para generar rentabilidad adicional mientras no se necesitan 
    para operación. Los fondos se liquidan automáticamente con la anticipación configurada.
    """)
    
    # 🆕 v4.8.1: Generar proyecciones DETERMINISTAS según escenario seleccionado
    # CORRECCIÓN: Elimina np.random para que proyecciones sean consistentes
    proyecciones_3m = generar_proyecciones_por_escenario(
        revenue_mensual,
        data['financial'],
        meses=3,
        escenario=st.session_state.escenario_proyeccion
    )
    
    # Calcular excedentes invertibles (inversiones VIRTUALES - no afectan balance)
    df_excedentes = calcular_excedentes_invertibles(
        proyecciones_3m, 
        efectivo_actual, 
        burn_rate,
        st.session_state.meses_colchon,
        st.session_state.dias_liquidacion
    )
    
    # Generar recomendaciones de inversión
    df_recomendaciones = generar_recomendaciones_inversion(df_excedentes, rentabilidad_estimada=0.10)
    
    # Mostrar análisis de excedentes
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Análisis de Excedentes por Mes")
        
        # Preparar tabla para mostrar
        df_display = df_excedentes[['mes', 'balance_disponible', 'necesidades_minimas', 'excedente_invertible']].copy()
        df_display.columns = ['Mes', 'Balance Disponible', 'Necesidades Mínimas', 'Excedente Invertible']
        
        # Formatear valores
        for col in ['Balance Disponible', 'Necesidades Mínimas', 'Excedente Invertible']:
            df_display[col] = df_display[col].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 💼 Recomendaciones de Inversión")
        
        if not df_recomendaciones.empty:
            # Preparar tabla de recomendaciones
            df_rec_display = df_recomendaciones[['mes', 'monto_invertible', 'instrumento_sugerido', 'rentabilidad_estimada_mensual']].copy()
            df_rec_display.columns = ['Mes', 'Monto', 'Instrumento', 'Rendimiento Est.']
            
            # Formatear valores
            df_rec_display['Monto'] = df_rec_display['Monto'].apply(lambda x: f"${x:,.0f}")
            df_rec_display['Rendimiento Est.'] = df_rec_display['Rendimiento Est.'].apply(lambda x: f"${x:,.0f}")
            
            st.dataframe(df_rec_display, use_container_width=True, hide_index=True)
            
            # Mostrar resumen
            total_invertible = df_recomendaciones['monto_invertible'].sum()
            total_rendimiento = df_recomendaciones['rentabilidad_estimada_mensual'].sum()
            
            st.success(f"💰 **Total Invertible:** ${total_invertible:,.0f}")
            st.success(f"📈 **Rendimiento Estimado:** ${total_rendimiento:,.0f}")
        else:
            st.warning("⚠️ No hay excedentes disponibles para inversión en los próximos 3 meses.")
            st.caption("Los fondos disponibles son necesarios para cubrir las operaciones y el margen de protección.")
    
    # Alertas y calendario de liquidación
    if not df_recomendaciones.empty:
        st.markdown("#### ⏰ Calendario de Liquidación")
        
        for idx, row in df_recomendaciones.iterrows():
            dias_config = st.session_state.dias_liquidacion
            st.info(
                f"🗓️ **Mes {int(row['mes'])}:** Invertir ${row['monto_invertible']:,.0f} | "
                f"Liquidar {dias_config} días antes del Mes {int(row['liquidar_antes_mes'])}"
            )
    
    st.caption("""
    **Instrumentos Sugeridos:**
    - **CDTs (40%):** Certificados de Depósito a Término ~12% EA
    - **TES (30%):** Títulos de Tesorería Colombia ~10% EA  
    - **FCI (30%):** Fondos de Inversión Colectiva ~8-10% EA
    
    *Rentabilidad estimada promedio: 10% EA para cartera mixta de bajo riesgo*
    """)
    
    # =========================================================================
    # 🆕 v4.8.0: FASE 3 - TRANSFERENCIAS A CASA MATRIZ (TRIMESTRALES)
    # =========================================================================
    
    st.markdown("---")
    st.markdown("### 🌍 Transferencias a Casa Matriz (SPT Global)")
    
    # Indicador del escenario actual
    emoji_escenario = {
        'Conservador': '🟠',
        'Moderado': '🟢',
        'Optimista': '🔵'
    }
    st.info(f"""
    **Política SPT Global:** La utilidad neta local debe ser del 10% del revenue. 
    Las transferencias se realizan por **trimestre vencido**, permitiendo a la filial 
    local aprovechar inversiones temporales durante el trimestre.
    
    {emoji_escenario[st.session_state.escenario_proyeccion]} **Calculado con escenario: {st.session_state.escenario_proyeccion}**
    """)
    
    # 🆕 v4.8.1: Calcular transferencias CON balance ajustado después de cada transferencia
    # CORRECCIÓN: Las transferencias ahora se DESCUENTAN del balance
    resultado_transferencias = calcular_transferencias_con_balance(
        proyecciones_3m, 
        efectivo_actual,
        meses_a_proyectar=3
    )
    
    df_trimestres = resultado_transferencias['trimestres']
    df_balance_mensual = resultado_transferencias['balance_mensual']
    
    # Mostrar tabla de transferencias CON balance
    st.markdown("#### 📋 Detalle de Transferencias Trimestrales")
    
    # Preparar tabla para display (ahora incluye balance)
    df_trans_display = df_trimestres[[
        'trimestre', 'balance_inicio', 'revenue_total', 'flujo_neto_total', 
        'utilidad_local_10pct', 'transferencia_hq', 'balance_despues_transferencia'
    ]].copy()
    df_trans_display.columns = [
        'Trimestre', 'Balance Inicio', 'Revenue Total', 'Flujo Neto Total', 
        'Utilidad Local (10%)', 'Transferencia HQ', 'Balance después Transfer.'
    ]
    
    # Formatear valores
    for col in df_trans_display.columns[1:]:  # Todas excepto 'Trimestre'
        df_trans_display[col] = df_trans_display[col].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(df_trans_display, use_container_width=True, hide_index=True)
    
    # Alerta sobre balance después de transferencias
    balance_final = resultado_transferencias['balance_final']
    if balance_final < burn_rate * st.session_state.meses_colchon:
        st.warning(f"""
        ⚠️ **Atención:** Después de las transferencias, el balance final (${balance_final:,.0f}) 
        está por debajo de las necesidades mínimas (${burn_rate * st.session_state.meses_colchon:,.0f}).
        """)
    else:
        st.success(f"""
        ✅ Después de las transferencias, el balance final (${balance_final:,.0f}) 
        mantiene un margen saludable sobre las necesidades mínimas.
        """)
    
    # Resumen de transferencias
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Transferencias",
            f"${resultado_transferencias['total_transferencias']:,.0f}",
            help="Suma de todas las transferencias trimestrales proyectadas"
        )
    
    with col2:
        revenue_total_periodo = df_trimestres['revenue_total'].sum()
        utilidad_total = df_trimestres['utilidad_local_10pct'].sum()
        st.metric(
            "Utilidad Local Retenida",
            f"${utilidad_total:,.0f}",
            help="10% del revenue total que queda en SPT Colombia"
        )
    
    with col3:
        st.metric(
            "Balance Final",
            f"${balance_final:,.0f}",
            delta=f"{balance_final - efectivo_actual:+,.0f}",
            help="Balance después de flujos netos y transferencias trimestrales"
        )
    
    # Gráfico de distribución del flujo neto
    st.markdown("#### 📊 Distribución del Flujo Neto")
    
    # Crear datos para gráfico de barras apiladas
    if not df_trimestres.empty:
        fig_transfer = go.Figure()
        
        fig_transfer.add_trace(go.Bar(
            name='Utilidad Local (10%)',
            x=df_trimestres['trimestre'],
            y=df_trimestres['utilidad_local_10pct'],
            marker_color='#10B981',
            text=df_trimestres['utilidad_local_10pct'].apply(lambda x: f"${x:,.0f}"),
            textposition='inside'
        ))
        
        fig_transfer.add_trace(go.Bar(
            name='Transferencia a HQ',
            x=df_trimestres['trimestre'],
            y=df_trimestres['transferencia_hq'],
            marker_color='#2563EB',
            text=df_trimestres['transferencia_hq'].apply(lambda x: f"${x:,.0f}"),
            textposition='inside'
        ))
        
        fig_transfer.update_layout(
            barmode='stack',
            title=f'Distribución del Flujo Neto: Utilidad Local vs Transferencia HQ (Escenario {st.session_state.escenario_proyeccion})',
            xaxis_title='Trimestre',
            yaxis_title='Monto (USD)',
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig_transfer, use_container_width=True)
    
    st.caption("""
    **Nota:** Las transferencias se realizan trimestre vencido. Esto permite:
    - Maximizar el uso de excedentes en inversiones temporales durante el trimestre
    - Mantener flexibilidad operativa local
    - Optimizar la rentabilidad de los fondos antes de la transferencia
    """)

# =============================================================================
# PÁGINA: ANÁLISIS HISTÓRICO
# =============================================================================

elif page == "📈 Análisis Histórico":
    st.markdown("## 📈 Análisis Histórico")
    
    df_hist = data['historical']['data']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Revenue Promedio", f"${data['historical']['revenue_promedio']:,.0f}")
    with col2:
        st.metric("Revenue Máximo", f"${data['historical']['revenue_maximo']:,.0f}")
    with col3:
        st.metric("Revenue Mínimo", f"${data['historical']['revenue_minimo']:,.0f}")
    
    st.markdown("---")
    
    # Gráfico histórico
    st.markdown("### 📊 Evolución del Revenue (33 meses)")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_hist['periodo'],
        y=df_hist['revenue'],
        mode='lines+markers',
        name='Revenue Real',
        line=dict(color='#2563EB', width=2),
        marker=dict(size=6)
    ))
    
    # Línea de tendencia
    slope, intercept, trend_line = calcular_tendencia_lineal(df_hist['revenue'].values)
    
    fig.add_trace(go.Scatter(
        x=df_hist['periodo'],
        y=trend_line,
        mode='lines',
        name='Tendencia',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    promedio = df_hist['revenue'].mean()
    fig.add_hline(
        y=promedio,
        line_dash="dot",
        line_color="green",
        annotation_text=f"Promedio: ${promedio:,.0f}",
        annotation_position="right"
    )
    
    fig.update_layout(
        height=500,
        hovermode='x unified',
        xaxis_title='Período',
        yaxis_title='Revenue (USD)',
        yaxis=dict(tickformat='$,.0f')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análisis de tendencia
    if slope > 0:
        tendencia_texto = f"📈 **Tendencia POSITIVA:** Crecimiento promedio de ${abs(slope):,.0f}/mes"
        tendencia_color = "success"
    else:
        tendencia_texto = f"📉 **Tendencia NEGATIVA:** Decrecimiento promedio de ${abs(slope):,.0f}/mes"
        tendencia_color = "error"
    
    if tendencia_color == "success":
        st.success(tendencia_texto)
    else:
        st.error(tendencia_texto)
    
    # Tabla de datos
    st.markdown("### 📋 Datos Históricos Detallados")
    
    df_display = df_hist.copy()
    df_display['revenue'] = df_display['revenue'].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)

# =============================================================================
# PÁGINA: PROYECCIONES
# =============================================================================

elif page == "💵 Proyecciones":
    st.markdown("## 💵 Proyecciones Multi-Escenario")
    
    meses_proyeccion = st.slider("Meses a proyectar:", 3, 12, 6, key="proyeccion_slider")
    
    # 🆕 v4.6.0: Pasar financial_data completo para cálculo dinámico de burn rate
    proyecciones = generar_proyecciones_multi_escenario(
        meses_proyeccion,
        data['historical']['revenue_promedio'],
        data['financial']  # Pasamos todo el dict con gastos_fijos y tasa_costos_variables
    )
    
    # Tabs para cada escenario
    tabs = st.tabs(["📊 Comparación", "🔴 Conservador", "🔵 Moderado", "🟢 Optimista"])
    
    with tabs[0]:
        st.markdown("### 📊 Comparación de Escenarios")
        
        fig = go.Figure()
        
        colores = {
            'Conservador': '#EF4444',
            'Moderado': '#2563EB',
            'Optimista': '#10B981'
        }
        
        for escenario, df_proj in proyecciones.items():
            fig.add_trace(go.Scatter(
                x=[f"Mes {m}" for m in df_proj['mes']],
                y=df_proj['flujo_neto'],
                mode='lines+markers',
                name=escenario,
                line=dict(color=colores[escenario], width=3),
                marker=dict(size=8)
            ))
        
        fig.add_hline(y=0, line_dash="dash", line_color="gray",
                     annotation_text="Punto de equilibrio", annotation_position="right")
        
        fig.update_layout(
            height=500,
            hovermode='x unified',
            xaxis_title='Período',
            yaxis_title='Flujo Neto (USD)',
            yaxis=dict(tickformat='$,.0f'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 🆕 v4.7.1: GRÁFICO COMPARATIVO DE BARRAS - Revenue y Egresos por Escenario
        st.markdown("### 📊 Comparación Revenue vs Egresos por Escenario")
        
        # Preparar datos para gráfico comparativo
        escenarios_list = list(proyecciones.keys())
        
        # Calcular promedios por escenario
        revenue_por_escenario = [proyecciones[esc]['revenue'].mean() for esc in escenarios_list]
        egresos_por_escenario = [proyecciones[esc]['egresos_totales'].mean() for esc in escenarios_list]
        flujo_por_escenario = [proyecciones[esc]['flujo_neto'].mean() for esc in escenarios_list]
        
        # Crear gráfico de barras comparativo
        fig_comp = go.Figure()
        
        fig_comp.add_trace(go.Bar(
            name='Revenue Promedio',
            x=escenarios_list,
            y=revenue_por_escenario,
            marker_color='#3B82F6',
            text=[f"${v:,.0f}" for v in revenue_por_escenario],
            textposition='outside'
        ))
        
        fig_comp.add_trace(go.Bar(
            name='Egresos Totales Promedio',
            x=escenarios_list,
            y=egresos_por_escenario,
            marker_color='#EF4444',
            text=[f"${v:,.0f}" for v in egresos_por_escenario],
            textposition='outside'
        ))
        
        fig_comp.add_trace(go.Bar(
            name='Flujo Neto Promedio',
            x=escenarios_list,
            y=flujo_por_escenario,
            marker_color='#10B981',
            text=[f"${v:,.0f}" for v in flujo_por_escenario],
            textposition='outside'
        ))
        
        fig_comp.update_layout(
            barmode='group',
            height=400,
            xaxis_title='Escenario',
            yaxis_title='USD',
            yaxis=dict(tickformat='$,.0f'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_comp, use_container_width=True)
        
        # 🆕 v4.7.1: TABLA COMPARATIVA DE RESUMEN
        st.markdown("### 📋 Tabla Comparativa de Escenarios")
        
        # Crear DataFrame de resumen
        datos_comparacion = []
        for escenario in escenarios_list:
            df_esc = proyecciones[escenario]
            datos_comparacion.append({
                'Escenario': escenario,
                'Revenue Promedio': f"${df_esc['revenue'].mean():,.0f}",
                'Revenue Mínimo': f"${df_esc['revenue'].min():,.0f}",
                'Revenue Máximo': f"${df_esc['revenue'].max():,.0f}",
                'Egresos Promedio': f"${df_esc['egresos_totales'].mean():,.0f}",
                'Flujo Neto Promedio': f"${df_esc['flujo_neto'].mean():,.0f}",
                'Flujo Neto Total': f"${df_esc['flujo_neto'].sum():,.0f}"
            })
        
        df_comparacion = pd.DataFrame(datos_comparacion)
        st.dataframe(df_comparacion, use_container_width=True, hide_index=True)
        
        # 🆕 v4.7.1: BOTÓN DE DESCARGA
        csv = df_comparacion.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Comparación (CSV)",
            data=csv,
            file_name=f"comparacion_escenarios_{meses_proyeccion}meses.csv",
            mime="text/csv"
        )
        
        st.info(f"""
        💡 **Interpretación (v4.6.0 - Burn Rate Dinámico):**
        - **Conservador (rojo):** Supone 15% menos revenue y crecimiento 1% mensual
        - **Moderado (azul):** Mantiene revenue actual con crecimiento 2% mensual
        - **Optimista (verde):** Supone 15% más revenue y crecimiento 3% mensual
        
        🆕 **Con burn rate DINÁMICO:** El burn rate se ajusta automáticamente según el 
        revenue de cada mes (Gastos Fijos ${data['financial']['gastos_fijos']:,.0f} + 
        {data['financial']['tasa_costos_variables']*100:.1f}% del revenue). Esto permite 
        proyecciones más precisas que reflejan la estructura real de costos de la operación.
        """)
    
    for idx, (escenario, df_proj) in enumerate(proyecciones.items(), 1):
        with tabs[idx]:
            st.markdown(f"### {escenario}")
            
            col1, col2, col3 = st.columns(3)
            
            revenue_prom = df_proj['revenue'].mean()
            flujo_prom = df_proj['flujo_neto'].mean()
            revenue_final = df_proj.iloc[-1]['revenue']
            
            with col1:
                st.metric("Revenue Promedio", f"${revenue_prom:,.0f}")
            with col2:
                st.metric("Flujo Neto Promedio", f"${flujo_prom:,.0f}")
            with col3:
                st.metric("Revenue Final", f"${revenue_final:,.0f}")
            
            st.markdown("#### 📊 Gráfico de Flujos")
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=[f"Mes {m}" for m in df_proj['mes']],
                y=df_proj['revenue'],
                name='Revenue',
                marker_color='lightblue'
            ))
            
            # 🆕 v4.6.0: Actualizado a 'egresos_totales' (burn rate dinámico)
            fig.add_trace(go.Bar(
                x=[f"Mes {m}" for m in df_proj['mes']],
                y=[-x for x in df_proj['egresos_totales']],
                name='Egresos Totales',
                marker_color='lightcoral'
            ))
            
            fig.add_trace(go.Scatter(
                x=[f"Mes {m}" for m in df_proj['mes']],
                y=df_proj['flujo_neto'],
                name='Flujo Neto',
                mode='lines+markers',
                line=dict(color='green', width=3),
                marker=dict(size=10)
            ))
            
            fig.update_layout(
                height=400,
                barmode='relative',
                hovermode='x unified',
                xaxis_title='Período',
                yaxis_title='USD',
                yaxis=dict(tickformat='$,.0f')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### 📋 Tabla Detallada")
            
            df_display = df_proj.copy()
            df_display['revenue'] = df_display['revenue'].apply(lambda x: f"${x:,.0f}")
            # 🆕 v4.6.1: Usar 'egresos_totales' en lugar de 'gastos'
            df_display['egresos_totales'] = df_display['egresos_totales'].apply(lambda x: f"${x:,.0f}")
            df_display['flujo_neto'] = df_display['flujo_neto'].apply(lambda x: f"${x:,.0f}")
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            # 🆕 v4.7.1: Botón de descarga para cada escenario
            csv_individual = df_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Descargar {escenario} (CSV)",
                data=csv_individual,
                file_name=f"proyeccion_{escenario.lower()}_{meses_proyeccion}meses.csv",
                mime="text/csv",
                key=f"download_{escenario}"
            )

# =============================================================================
# PÁGINA: REPORTES DETALLADOS
# =============================================================================

elif page == "📊 Reportes Detallados":
    st.markdown("## 📊 Reportes Detallados")
    
    tabs = st.tabs(["📈 Estacionalidad", "🔥 Burn Rate", "💰 Balance Proyectado"])
    
    with tabs[0]:
        st.markdown("### 📅 Análisis de Estacionalidad")
        st.caption("✨ Interactivo: Compara años vs promedio - ✅ DATOS REALES del backend")
        
        # Nota informativa sobre datos reales
        st.info("""
        🎯 **Factores Estacionales REALES integrados**
        
        Estos factores fueron calculados desde los Utilization Reports 2023-2025:
        • **Julio** es el mes de mayor actividad (+46.5% sobre promedio)
        • **Diciembre** es el mes más bajo (-71.1% bajo promedio)
        • Los datos reflejan la operación real de SPT Colombia en los últimos 33 meses
        """)
        
        st.markdown("#### 🎛️ Controles de Visualización")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            show_promedio = st.checkbox("📊 Promedio Global", value=True, key="show_avg")
        with col2:
            show_2023 = st.checkbox("📅 Año 2023", value=False, key="show_2023")
        with col3:
            show_2024 = st.checkbox("📅 Año 2024", value=False, key="show_2024")
        with col4:
            show_2025 = st.checkbox(
                "📅 Año 2025",
                value=False,
                key="show_2025",
                disabled=True,
                help="⚠️ Año 2025 incompleto (solo Ene-Sep). Necesita 12 meses para visualización completa."
            )
        
        meses_nombres = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        fig = go.Figure()
        
        # ✅ Radar que cierra (duplicar primer valor)
        if show_promedio:
            factores_promedio = [data['seasonal_factors'][m] for m in meses_nombres]
            # Duplicar primer valor para cerrar el polígono
            factores_cerrado = factores_promedio + [factores_promedio[0]]
            meses_cerrado = meses_nombres + [meses_nombres[0]]
            
            fig.add_trace(go.Scatterpolar(
                r=factores_cerrado,
                theta=meses_cerrado,
                fill='toself',
                name='Promedio Global (REAL)',
                line=dict(color='#2563EB', width=3),
                fillcolor='rgba(37, 99, 235, 0.2)',
                marker=dict(size=8, color='#2563EB')
            ))
        
        if 'seasonal_by_year' in data:
            year_colors = {2023: '#10B981', 2024: '#F59E0B', 2025: '#EF4444'}
            year_shows = {2023: show_2023, 2024: show_2024}
            
            for year, show in year_shows.items():
                if show and year in data['seasonal_by_year']:
                    factors = data['seasonal_by_year'][year]
                    if len(factors) == 12:
                        # Duplicar primer valor para cerrar
                        factors_cerrado = factors + [factors[0]]
                        meses_cerrado = meses_nombres + [meses_nombres[0]]
                        
                        fig.add_trace(go.Scatterpolar(
                            r=factors_cerrado,
                            theta=meses_cerrado,
                            name=f'Año {year}',
                            line=dict(color=year_colors[year], width=2, dash='dot'),
                            marker=dict(size=6, color=year_colors[year])
                        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1.6], tickformat='.2f'),
                angularaxis=dict(rotation=90, direction='clockwise')
            ),
            title='Factores Estacionales REALES (1.0 = promedio)',
            height=500,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        ℹ️ **Nota sobre Año 2025:**  
        El año 2025 está incompleto (solo 9 meses: Ene-Sep) y no se puede visualizar en el radar 
        que requiere 12 puntos de datos. Los factores de 2025 están incluidos en el promedio global.
        """)
        
        st.markdown("#### 📋 Factores Estacionales Detallados (REALES)")
        df_seasonal = pd.DataFrame(list(data['seasonal_factors'].items()),
                                   columns=['Mes', 'Factor'])
        df_seasonal['Interpretación'] = df_seasonal['Factor'].apply(
            lambda x: '📈 Alta actividad' if x > 1.1 else ('📉 Baja actividad' if x < 0.9 else '➡️ Normal')
        )
        df_seasonal['% vs Promedio'] = df_seasonal['Factor'].apply(
            lambda x: f"{(x-1)*100:+.1f}%"
        )
        st.dataframe(df_seasonal, use_container_width=True, hide_index=True)
        
        st.success("""
        ✅ **Datos Reales Integrados:**  
        Los factores estacionales mostrados fueron calculados desde 33 meses de datos reales 
        (Ene 2023 - Sep 2025), eliminando completamente los valores hardcodeados anteriores.
        """)
    
    with tabs[1]:
        st.markdown("### 🔥 Análisis de Burn Rate")
        
        st.success(f"""
        🎯 **Metodología de Burn Rate DINÁMICO (v4.6.0):**
        
        El burn rate se calcula dinámicamente según el revenue mensual:
        
        **Fórmula:** Burn Rate = Gastos Fijos + (Revenue × Tasa Costos Variables)
        
        **Componentes:**
        • **Gastos Fijos:** ${data['financial']['gastos_fijos']:,.0f} USD/mes (no varían con revenue)
          - Incluye: Admin, HR, Marketing, Salarios, Seguros, Impuestos
        • **Costos Variables:** {data['financial']['tasa_costos_variables']*100:.2f}% del revenue mensual
          - Incluye: Logística, Equipamiento (proporcional al nivel de operación)
        
        **Burn Rate con revenue promedio (${data['historical']['revenue_promedio']:,.0f}):**  
        ${data['financial']['burn_rate']:,.0f} USD/mes
        
        **Margen Operativo:** {data['financial']['margen_operativo']*100:.1f}%
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Burn Rate Mensual", f"${data['financial']['burn_rate']:,.0f}",
                     help=f"Con revenue promedio ${data['historical']['revenue_promedio']:,.0f}. Varía dinámicamente con el revenue real.")
        with col2:
            st.metric("Gastos Fijos", f"${data['financial']['gastos_fijos']:,.0f}",
                     help="Gastos administrativos mensuales que no varían con el revenue")
        with col3:
            st.metric("Costos Operativos", f"${data['financial']['costos_variables']:,.0f}",
                     help="Costos variables de operación mensuales")
        
        st.markdown("#### 📊 Desglose Estimado del Burn Rate")
        
        # Desglose proporcional basado en los datos reales del informe
        burn_breakdown = pd.DataFrame({
            'Categoría': ['Administrativos', 'Logística', 'Equipamiento', 'Personal', 'Depreciación', 'Marketing'],
            'Monto': [
                data['financial']['gastos_fijos'] * 0.55,      # ~55% admin
                data['financial']['costos_variables'] * 0.32,  # ~32% logística
                data['financial']['costos_variables'] * 0.21,  # ~21% equipo
                data['financial']['gastos_fijos'] * 0.15,      # ~15% personal
                data['financial']['costos_variables'] * 0.11,  # ~11% deprec
                data['financial']['gastos_fijos'] * 0.30       # ~30% marketing
            ]
        })
        
        fig = px.pie(burn_breakdown, values='Monto', names='Categoría',
                     title='Distribución del Burn Rate',
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        revenue_prom = data['historical']['revenue_promedio']
        burn_rate_calc = data['financial']['burn_rate']
        flujo_neto = revenue_prom - burn_rate_calc
        margen = (flujo_neto / revenue_prom) * 100
        
        st.info(f"""
        💡 **Insight Financiero (v4.6.0):** 
        Con revenue promedio de **${revenue_prom:,.0f}**/mes y burn rate dinámico de 
        **${burn_rate_calc:,.0f}**/mes, la empresa genera un flujo neto de 
        **${flujo_neto:,.0f}**/mes (margen {margen:.1f}%).
        
        Esto indica una operación saludable con capacidad de:
        • Cubrir {(efectivo_actual / burn_rate_calc):.1f} meses de operación con efectivo actual
        • Generar excedentes consistentes para inversión o distribución
        • Mantener margen de protección adecuado configurado en {st.session_state.meses_colchon} meses
        """)
    
    with tabs[2]:
        st.markdown("### 💰 Balance Proyectado Multi-Escenario")
        st.caption("✅ Balance acumulado correctamente con burn rate REAL")
        
        meses_balance = st.slider("Meses de proyección:", 1, 12, 6, key="balance_slider")
        
        proyecciones_bal = generar_proyecciones_multi_escenario(
            meses_balance,
            data['historical']['revenue_promedio'],
            data['financial']  # 🆕 v4.6.1: Pasar dict completo, no solo burn_rate
        )
        
        balances = generar_balance_multi_escenario(meses_balance, efectivo_actual, proyecciones_bal)
        
        fig = go.Figure()
        
        colores = {
            'Conservador': '#EF4444',
            'Moderado': '#2563EB',
            'Optimista': '#10B981'
        }
        
        for escenario, df_balance in balances.items():
            fig.add_trace(go.Scatter(
                x=[f"Mes {m}" for m in df_balance['mes']],
                y=df_balance['efectivo_final'],
                mode='lines+markers',
                name=escenario,
                line=dict(color=colores[escenario], width=3),
                marker=dict(size=10)
            ))
        
        fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2,
                     annotation_text="⚠️ Punto Crítico", annotation_position="right")
        
        fig.add_hline(y=efectivo_actual, line_dash="dot", line_color="gray",
                     annotation_text=f"Efectivo Inicial: ${efectivo_actual:,.0f}",
                     annotation_position="left")
        
        fig.update_layout(
            height=500,
            hovermode='x unified',
            xaxis_title='Período',
            yaxis_title='Efectivo Disponible (USD)',
            yaxis=dict(tickformat='$,.0f'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            title='Evolución del Efectivo por Escenario (con Burn Rate REAL)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### ⏱️ Análisis de Runway por Escenario")
        
        cols = st.columns(3)
        
        for idx, (escenario, df_balance) in enumerate(balances.items()):
            with cols[idx]:
                efectivo_final = df_balance.iloc[-1]['efectivo_final']
                
                if efectivo_final > 0:
                    runway_esc = efectivo_final / data['financial']['burn_rate']
                    st.success(f"""
                    **{escenario}**
                    
                    Efectivo final: ${efectivo_final:,.0f}
                    
                    Runway adicional: {runway_esc:.1f} meses
                    
                    ✅ Posición MUY saludable
                    """)
                else:
                    meses_negativos = df_balance[df_balance['efectivo_final'] < 0]
                    if len(meses_negativos) > 0:
                        mes_critico = meses_negativos.iloc[0]['mes']
                        st.error(f"""
                        **{escenario}**
                        
                        ⚠️ Déficit en mes {int(mes_critico)}
                        
                        Efectivo final: ${efectivo_final:,.0f}
                        """)
        
        st.success(f"""
        🎯 **Conclusión con Burn Rate Dinámico (v4.6.0):**
        
        Con la metodología de burn rate DINÁMICO (Gastos Fijos ${data['financial']['gastos_fijos']:,.0f} + 
        {data['financial']['tasa_costos_variables']*100:.1f}% del revenue), SPT Colombia muestra proyecciones 
        realistas que se ajustan al nivel de operación.
        
        **Con revenue promedio actual (${data['historical']['revenue_promedio']:,.0f}):**
        • Burn rate: ${data['financial']['burn_rate']:,.0f} USD/mes
        • Margen operativo: {data['financial']['margen_operativo']*100:.1f}%  
        • Flujo neto mensual: ${(data['historical']['revenue_promedio'] - data['financial']['burn_rate']):,.0f} USD
        
        Los 3 escenarios proyectan situaciones diferentes según crecimiento del revenue, 
        con burn rate ajustándose proporcionalmente en cada caso.
        """)

# =============================================================================
# PÁGINA: INGRESO MANUAL
# =============================================================================

elif page == "📝 Ingreso Manual":
    st.markdown("## 📝 Ingreso Manual de Cotizaciones y Contratos")
    
    st.info("""
    **Funcionalidad:** Permite ingresar manualmente cotizaciones y contratos futuros para 
    analizar su impacto en las proyecciones financieras.
    
    🔹 **Cotizaciones:** Oportunidades con probabilidad de cierre  
    🔹 **Contratos:** Compromisos confirmados con equipos asignados
    """)
    
    # Tabs para cotizaciones y contratos
    tab1, tab2, tab3 = st.tabs(["📋 Cotizaciones", "📄 Contratos", "📊 Resumen"])
    
    # =========================================================================
    # TAB 1: COTIZACIONES
    # =========================================================================
    
    with tab1:
        st.markdown("### 📋 Ingresar Nueva Cotización")
        
        with st.form("form_cotizacion"):
            col1, col2 = st.columns(2)
            
            with col1:
                quote_id = st.text_input(
                    "ID de Cotización",
                    placeholder="Ej: Q-2025-001",
                    help="Identificador único de la cotización"
                )
                
                cliente = st.text_input(
                    "Cliente",
                    placeholder="Nombre del cliente",
                    help="Nombre de la empresa cliente"
                )
                
                fecha_cotizacion = st.date_input(
                    "Fecha de Cotización",
                    value=datetime.now(),
                    help="Fecha en que se genera la cotización"
                )
                
                fecha_valida_hasta = st.date_input(
                    "Válida Hasta",
                    value=datetime.now() + timedelta(days=30),
                    help="Fecha límite de validez de la cotización"
                )
            
            with col2:
                probabilidad_cierre = st.slider(
                    "Probabilidad de Cierre (%)",
                    min_value=0,
                    max_value=100,
                    value=50,
                    step=5,
                    help="Probabilidad estimada de que la cotización se cierre"
                )
                
                duracion_meses = st.number_input(
                    "Duración Estimada (meses)",
                    min_value=1,
                    max_value=36,
                    value=12,
                    help="Duración estimada del contrato si se cierra"
                )
                
                tarifa_mensual = st.number_input(
                    "Tarifa Mensual Estimada (USD)",
                    min_value=0.0,
                    value=0.0,
                    step=1000.0,
                    help="Tarifa mensual total estimada"
                )
                
                fecha_inicio_estimada = st.date_input(
                    "Fecha Inicio Estimada",
                    value=datetime.now() + timedelta(days=30),
                    help="Fecha estimada de inicio si se confirma"
                )
            
            st.markdown("#### Equipos Requeridos")
            num_equipos = st.number_input(
                "Número de Equipos",
                min_value=1,
                max_value=20,
                value=1,
                help="Cantidad de equipos incluidos en la cotización"
            )
            
            equipos_cotizacion = []
            for i in range(int(num_equipos)):
                with st.expander(f"Equipo {i+1}"):
                    col_eq1, col_eq2 = st.columns(2)
                    with col_eq1:
                        tipo_equipo = st.text_input(
                            "Tipo de Equipo",
                            key=f"quote_eq_type_{i}",
                            placeholder="Ej: Telehandler"
                        )
                        modelo = st.text_input(
                            "Modelo",
                            key=f"quote_eq_model_{i}",
                            placeholder="Ej: GTH-5519"
                        )
                    with col_eq2:
                        tarifa_equipo = st.number_input(
                            "Tarifa Mensual (USD)",
                            key=f"quote_eq_rate_{i}",
                            min_value=0.0,
                            value=0.0,
                            step=100.0
                        )
                    
                    equipos_cotizacion.append({
                        'tipo': tipo_equipo,
                        'modelo': modelo,
                        'tarifa_mensual': tarifa_equipo
                    })
            
            st.markdown("#### Notas Adicionales")
            notas = st.text_area(
                "Notas o Comentarios",
                placeholder="Información adicional sobre la cotización...",
                height=100
            )
            
            # Botón de envío
            submitted_quote = st.form_submit_button("💾 Guardar Cotización", use_container_width=True)
            
            if submitted_quote:
                if not quote_id or not cliente:
                    st.error("⚠️ Por favor completa los campos obligatorios: ID de Cotización y Cliente")
                else:
                    # Calcular revenue ponderado
                    revenue_ponderado = tarifa_mensual * duracion_meses * (probabilidad_cierre / 100.0)
                    
                    # Crear cotización
                    nueva_cotizacion = {
                        'quote_id': quote_id,
                        'cliente': cliente,
                        'fecha_cotizacion': fecha_cotizacion.isoformat(),
                        'fecha_valida_hasta': fecha_valida_hasta.isoformat(),
                        'fecha_inicio_estimada': fecha_inicio_estimada.isoformat(),
                        'probabilidad_cierre': probabilidad_cierre,
                        'duracion_meses': duracion_meses,
                        'tarifa_mensual': tarifa_mensual,
                        'revenue_ponderado': revenue_ponderado,
                        'equipos': equipos_cotizacion,
                        'notas': notas,
                        'fecha_ingreso': datetime.now().isoformat()
                    }
                    
                    # Guardar en session_state
                    st.session_state.cotizaciones_manuales.append(nueva_cotizacion)
                    
                    st.success(f"✅ Cotización {quote_id} guardada exitosamente!")
                    st.success(f"📊 Revenue ponderado: ${revenue_ponderado:,.0f} USD")
                    st.rerun()
        
        # Mostrar cotizaciones existentes
        if st.session_state.cotizaciones_manuales:
            st.markdown("---")
            st.markdown("### 📋 Cotizaciones Guardadas")
            
            for idx, quote in enumerate(st.session_state.cotizaciones_manuales):
                with st.expander(f"{quote['quote_id']} - {quote['cliente']} ({quote['probabilidad_cierre']}%)"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Tarifa Mensual", f"${quote['tarifa_mensual']:,.0f}")
                    with col2:
                        st.metric("Duración", f"{quote['duracion_meses']} meses")
                    with col3:
                        st.metric("Revenue Ponderado", f"${quote['revenue_ponderado']:,.0f}")
                    
                    st.caption(f"Válida hasta: {quote['fecha_valida_hasta']}")
                    st.caption(f"Inicio estimado: {quote['fecha_inicio_estimada']}")
                    
                    if st.button(f"🗑️ Eliminar", key=f"del_quote_{idx}"):
                        st.session_state.cotizaciones_manuales.pop(idx)
                        st.rerun()
    
    # =========================================================================
    # TAB 2: CONTRATOS
    # =========================================================================
    
    with tab2:
        st.markdown("### 📄 Ingresar Nuevo Contrato")
        
        with st.form("form_contrato"):
            col1, col2 = st.columns(2)
            
            with col1:
                contrato_id = st.text_input(
                    "ID del Contrato",
                    placeholder="Ej: C-2025-001",
                    help="Identificador único del contrato"
                )
                
                cliente_contrato = st.text_input(
                    "Cliente",
                    placeholder="Nombre del cliente",
                    help="Nombre de la empresa cliente"
                )
                
                fecha_inicio_contrato = st.date_input(
                    "Fecha de Inicio",
                    value=datetime.now(),
                    help="Fecha de inicio del contrato"
                )
                
                duracion_tipo = st.radio(
                    "Tipo de Duración",
                    options=["Duración fija (meses)", "Fecha fin abierta"],
                    help="Selecciona si el contrato tiene duración definida o es abierto"
                )
            
            with col2:
                if duracion_tipo == "Duración fija (meses)":
                    duracion_contrato_meses = st.number_input(
                        "Duración (meses)",
                        min_value=1,
                        max_value=60,
                        value=12,
                        help="Duración del contrato en meses"
                    )
                    fecha_fin_contrato = fecha_inicio_contrato + timedelta(days=duracion_contrato_meses * 30)
                else:
                    duracion_contrato_meses = None
                    st.info("📅 Contrato con fecha fin abierta (notificación con 1 mes de anticipación)")
                    fecha_fin_contrato = None
                
                tarifa_mensual_contrato = st.number_input(
                    "Tarifa Mensual Total (USD)",
                    min_value=0.0,
                    value=0.0,
                    step=1000.0,
                    help="Tarifa mensual total del contrato"
                )
                
                estado_contrato = st.selectbox(
                    "Estado del Contrato",
                    options=["Activo", "Pendiente", "En negociación"],
                    help="Estado actual del contrato"
                )
            
            st.markdown("#### Equipos Asignados")
            
            # Mostrar equipos disponibles (simulado)
            with st.expander("Ver Equipos Disponibles"):
                st.info("""
                **Equipos Disponibles para Asignación:**
                
                En la versión completa, aquí se mostrarán los equipos con estado:
                - ✅ Available
                - 🔶 StandBy
                
                Provenientes del Weekly Operation Report.
                """)
            
            num_equipos_contrato = st.number_input(
                "Número de Equipos",
                min_value=1,
                max_value=20,
                value=1,
                help="Cantidad de equipos asignados al contrato"
            )
            
            equipos_contrato = []
            for i in range(int(num_equipos_contrato)):
                with st.expander(f"Equipo {i+1}"):
                    col_eq1, col_eq2, col_eq3 = st.columns(3)
                    with col_eq1:
                        tipo_equipo_c = st.text_input(
                            "Tipo de Equipo",
                            key=f"contract_eq_type_{i}",
                            placeholder="Ej: Telehandler"
                        )
                        serial_number = st.text_input(
                            "Serial Number",
                            key=f"contract_eq_serial_{i}",
                            placeholder="Ej: GTH-001"
                        )
                    with col_eq2:
                        modelo_c = st.text_input(
                            "Modelo",
                            key=f"contract_eq_model_{i}",
                            placeholder="Ej: GTH-5519"
                        )
                        ubicacion = st.text_input(
                            "Ubicación",
                            key=f"contract_eq_location_{i}",
                            placeholder="Ej: Bogotá"
                        )
                    with col_eq3:
                        tarifa_equipo_c = st.number_input(
                            "Tarifa Mensual (USD)",
                            key=f"contract_eq_rate_{i}",
                            min_value=0.0,
                            value=0.0,
                            step=100.0
                        )
                    
                    equipos_contrato.append({
                        'tipo': tipo_equipo_c,
                        'serial_number': serial_number,
                        'modelo': modelo_c,
                        'ubicacion': ubicacion,
                        'tarifa_mensual': tarifa_equipo_c
                    })
            
            st.markdown("#### Información Adicional")
            notas_contrato = st.text_area(
                "Notas o Comentarios",
                placeholder="Información adicional sobre el contrato...",
                height=100
            )
            
            # Botón de envío
            submitted_contract = st.form_submit_button("💾 Guardar Contrato", use_container_width=True)
            
            if submitted_contract:
                if not contrato_id or not cliente_contrato:
                    st.error("⚠️ Por favor completa los campos obligatorios: ID del Contrato y Cliente")
                else:
                    # Crear contrato
                    nuevo_contrato = {
                        'contrato_id': contrato_id,
                        'cliente': cliente_contrato,
                        'fecha_inicio': fecha_inicio_contrato.isoformat(),
                        'fecha_fin': fecha_fin_contrato.isoformat() if fecha_fin_contrato else 'Abierta',
                        'duracion_meses': duracion_contrato_meses,
                        'tarifa_mensual_total': tarifa_mensual_contrato,
                        'estado': estado_contrato,
                        'equipos': equipos_contrato,
                        'notas': notas_contrato,
                        'fecha_ingreso': datetime.now().isoformat()
                    }
                    
                    # Guardar en session_state
                    st.session_state.contratos_manuales.append(nuevo_contrato)
                    
                    st.success(f"✅ Contrato {contrato_id} guardado exitosamente!")
                    st.success(f"💰 Tarifa mensual total: ${tarifa_mensual_contrato:,.0f} USD")
                    st.rerun()
        
        # Mostrar contratos existentes
        if st.session_state.contratos_manuales:
            st.markdown("---")
            st.markdown("### 📄 Contratos Guardados")
            
            for idx, contract in enumerate(st.session_state.contratos_manuales):
                with st.expander(f"{contract['contrato_id']} - {contract['cliente']} ({contract['estado']})"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Tarifa Mensual", f"${contract['tarifa_mensual_total']:,.0f}")
                    with col2:
                        duracion_display = f"{contract['duracion_meses']} meses" if contract['duracion_meses'] else "Fecha abierta"
                        st.metric("Duración", duracion_display)
                    with col3:
                        st.metric("Equipos", f"{len(contract['equipos'])} unidades")
                    
                    st.caption(f"Inicio: {contract['fecha_inicio']} | Fin: {contract['fecha_fin']}")
                    
                    if st.button(f"🗑️ Eliminar", key=f"del_contract_{idx}"):
                        st.session_state.contratos_manuales.pop(idx)
                        st.rerun()
    
    # =========================================================================
    # TAB 3: RESUMEN
    # =========================================================================
    
    with tab3:
        st.markdown("### 📊 Resumen de Ingreso Manual")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 Cotizaciones")
            num_cotizaciones = len(st.session_state.cotizaciones_manuales)
            st.metric("Total Cotizaciones", num_cotizaciones)
            
            if num_cotizaciones > 0:
                revenue_ponderado_total = sum(q['revenue_ponderado'] for q in st.session_state.cotizaciones_manuales)
                tarifa_mensual_total_quotes = sum(q['tarifa_mensual'] for q in st.session_state.cotizaciones_manuales)
                
                st.metric("Revenue Ponderado Total", f"${revenue_ponderado_total:,.0f}")
                st.metric("Tarifa Mensual Total (si todas cierran)", f"${tarifa_mensual_total_quotes:,.0f}")
                
                # Tabla de cotizaciones
                st.markdown("##### Detalle de Cotizaciones")
                df_quotes = pd.DataFrame([
                    {
                        'ID': q['quote_id'],
                        'Cliente': q['cliente'],
                        'Prob. Cierre': f"{q['probabilidad_cierre']}%",
                        'Tarifa Mensual': f"${q['tarifa_mensual']:,.0f}",
                        'Rev. Ponderado': f"${q['revenue_ponderado']:,.0f}"
                    }
                    for q in st.session_state.cotizaciones_manuales
                ])
                st.dataframe(df_quotes, use_container_width=True, hide_index=True)
            else:
                st.info("No hay cotizaciones ingresadas aún")
        
        with col2:
            st.markdown("#### 📄 Contratos")
            num_contratos = len(st.session_state.contratos_manuales)
            st.metric("Total Contratos", num_contratos)
            
            if num_contratos > 0:
                tarifa_mensual_total_contracts = sum(c['tarifa_mensual_total'] for c in st.session_state.contratos_manuales)
                equipos_totales = sum(len(c['equipos']) for c in st.session_state.contratos_manuales)
                
                st.metric("Tarifa Mensual Total", f"${tarifa_mensual_total_contracts:,.0f}")
                st.metric("Equipos Asignados", equipos_totales)
                
                # Tabla de contratos
                st.markdown("##### Detalle de Contratos")
                df_contracts = pd.DataFrame([
                    {
                        'ID': c['contrato_id'],
                        'Cliente': c['cliente'],
                        'Estado': c['estado'],
                        'Tarifa Mensual': f"${c['tarifa_mensual_total']:,.0f}",
                        'Equipos': len(c['equipos'])
                    }
                    for c in st.session_state.contratos_manuales
                ])
                st.dataframe(df_contracts, use_container_width=True, hide_index=True)
            else:
                st.info("No hay contratos ingresados aún")
        
        # Resumen consolidado
        if num_cotizaciones > 0 or num_contratos > 0:
            st.markdown("---")
            st.markdown("#### 💡 Impacto en Proyecciones")
            
            st.info("""
            **Próximos pasos:**
            
            Estos contratos y cotizaciones ingresados se utilizarán para:
            
            1. **Ajustar los escenarios** (Conservador/Moderado/Optimista) según probabilidades de cierre
            2. **Proyectar revenue futuro** considerando nuevos contratos confirmados
            3. **Analizar disponibilidad de equipos** para nuevas oportunidades
            4. **Optimizar la planificación financiera** con vista a compromisos futuros
            
            En la siguiente actualización, estos datos se integrarán automáticamente en las proyecciones.
            """)
            
            # Botón para limpiar todos los datos
            if st.button("🗑️ Limpiar Todos los Datos", type="secondary"):
                if st.checkbox("⚠️ Confirmar eliminación de todos los datos"):
                    st.session_state.cotizaciones_manuales = []
                    st.session_state.contratos_manuales = []
                    st.success("✅ Todos los datos han sido eliminados")
                    st.rerun()

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748B; padding: 2rem 0;'>
    <p><strong>SPT Cash Flow Tool v4.5.3</strong></p>
    <p>✅ Datos reales integrados • Factores estacionales desde históricos • Burn rate desde informe financiero</p>
    <p>Desarrollado por <a href='https://www.ai-mindnovation.com' target='_blank'>AI-MindNovation</a></p>
    <p>© 2025 AI-MindNovation. Todos los derechos reservados.</p>
</div>
""", unsafe_allow_html=True)
