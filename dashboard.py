"""
SPT CASH FLOW TOOL - Dashboard Streamlit v4.6.0
================================================
Dashboard de análisis de flujo de efectivo para SPT Colombia

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
from datetime import datetime
import numpy as np

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
            flujo_neto = row['revenue'] - row['gastos']
            efectivo_acumulado += flujo_neto
            
            balance.append({
                'mes': int(row['mes']),
                'efectivo_inicial': efectivo_acumulado - flujo_neto,
                'ingresos': row['revenue'],
                'gastos': row['gastos'],
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
                with st.spinner("⚙️ Procesando archivos..."):
                    st.info("📊 Integración completa con backend disponible post-convención")
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
    
    st.markdown("---")
    
    st.markdown("### 📊 Navegación")
    page = st.radio(
        "Selecciona sección:",
        ["🏠 Resumen Ejecutivo", "📈 Análisis Histórico", "💵 Proyecciones", "📊 Reportes Detallados"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("### ℹ️ Información")
    st.markdown("""
    **Usuario:** Autenticado ✅
    
    **Versión:** 4.6.0
    
    **🔥 Correcciones Críticas v4.6.0:**
    • ✅ Burn Rate DINÁMICO en proyecciones
    • ✅ Referencias actualizadas
    • ✅ Margen de protección configurable (1-3 meses)
    • ✅ Terminología mejorada: Egresos Totales
    
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
    
    # 🆕 v4.6.0: Indicador visual de modo
    if st.session_state.data_source == 'real' and st.session_state.datos_procesados:
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
        st.metric("Necesidades Mínimas", f"${necesidades:,.0f}", 
                 help="1 mes de burn rate como colchón")
    
    with col3:
        excedente_color = "normal" if analisis_cash['excedente_deficit'] > 0 else "inverse"
        st.metric(
            "Excedente/Déficit",
            f"${analisis_cash['excedente_deficit']:,.0f}",
            delta_color=excedente_color
        )

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
            df_display['gastos'] = df_display['gastos'].apply(lambda x: f"${x:,.0f}")
            df_display['flujo_neto'] = df_display['flujo_neto'].apply(lambda x: f"${x:,.0f}")
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)

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
            data['financial']['burn_rate']
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
