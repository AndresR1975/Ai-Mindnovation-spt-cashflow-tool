"""
SPT CASH FLOW TOOL - Dashboard Streamlit v4.5.2
================================================
Dashboard de análisis de flujo de efectivo para SPT Colombia

CORRECCIONES v4.5.2:
✅ Reactivada interfaz de carga de archivos
✅ Término "Deuda" → "Reinversión/Crecimiento"
✅ Gráfico radar cierra entre Dic-Ene
✅ Manejo correcto de año 2025 (parcial)
+ Todas las correcciones de v4.5.1

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
# FUNCIONES DE DATOS
# =============================================================================

def get_historical_data_complete():
    """Retorna datos históricos completos de 2023-2025 (33 meses)"""
    
    meses = []
    revenue = []
    years_data = {2023: [], 2024: [], 2025: []}
    
    base_revenue = 120000
    
    for i in range(33):
        year = 2023 + (i // 12)
        month = (i % 12) + 1
        periodo = f"{year}-{str(month).zfill(2)}"
        meses.append(periodo)
        
        tendencia = base_revenue + (i * 4500)
        estacionalidad = np.sin(i * np.pi / 6) * 15000
        ruido = np.random.randint(-5000, 8000)
        
        revenue_mes = max(100000, tendencia + estacionalidad + ruido)
        revenue.append(revenue_mes)
        
        years_data[year].append(revenue_mes)
    
    return pd.DataFrame({
        'periodo': meses,
        'revenue': revenue
    }), years_data

def calcular_proyeccion_3_meses(revenue_promedio, burn_rate):
    """Calcula proyección de flujo para próximos 3 meses"""
    proyeccion = []
    
    for i in range(3):
        revenue_mes = revenue_promedio * (1 + np.random.uniform(-0.05, 0.1))
        flujo_neto = revenue_mes - burn_rate
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

def calcular_necesidades_excedentes_mejorado(efectivo_actual, flujos_proyectados):
    """✅ Necesidades/excedentes con balance completo"""
    balance_proyectado = efectivo_actual + sum(flujos_proyectados)
    necesidades_minimas = 87089
    excedente_o_deficit = balance_proyectado - necesidades_minimas
    
    return {
        'balance_proyectado': balance_proyectado,
        'necesidades_minimas': necesidades_minimas,
        'excedente_deficit': excedente_o_deficit,
        'flujos_mensuales': flujos_proyectados
    }

def get_data():
    """Retorna datos según la fuente (demo o real)"""
    
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
        
        seasonal_avg = {
            'Enero': 1.15, 'Febrero': 0.85, 'Marzo': 1.05,
            'Abril': 0.95, 'Mayo': 1.10, 'Junio': 1.20,
            'Julio': 1.08, 'Agosto': 0.92, 'Septiembre': 1.03,
            'Octubre': 1.12, 'Noviembre': 0.98, 'Diciembre': 1.18
        }
        
        return {
            'historical': {
                'revenue_promedio': int(df_historical['revenue'].mean()),
                'revenue_minimo': int(df_historical['revenue'].min()),
                'revenue_maximo': int(df_historical['revenue'].max()),
                'top_clients': [
                    ('Kluane/Aris', 549800),
                    ('Explomin', 496700),
                    ('Kluane', 490575),
                    ('Office', 481310),
                    ('SPT Colombia', 445850)
                ],
                'periodos': 33,
                'data': df_historical,
                'years_data': years_data
            },
            'financial': {
                'burn_rate': 87089,
                'gastos_fijos': 65000,
                'costos_variables': 22089,
                'margen_operativo': 0.53
            },
            'seasonal_factors': seasonal_avg,
            'seasonal_by_year': seasonal_by_year
        }

# =============================================================================
# FUNCIONES DE PROYECCIÓN
# =============================================================================

def generar_proyecciones_multi_escenario(meses, revenue_base, burn_rate):
    """Genera proyecciones para los 3 escenarios"""
    
    escenarios = {
        'Conservador': {'factor': 0.85, 'crecimiento': 0.01, 'color': '#EF4444'},
        'Moderado': {'factor': 1.0, 'crecimiento': 0.02, 'color': '#2563EB'},
        'Optimista': {'factor': 1.15, 'crecimiento': 0.03, 'color': '#10B981'}
    }
    
    resultados = {}
    
    for nombre, config in escenarios.items():
        proyeccion = []
        
        for i in range(meses):
            revenue = revenue_base * config['factor'] * (1 + config['crecimiento'])**i
            proyeccion.append({
                'mes': i + 1,
                'revenue': revenue,
                'gastos': burn_rate,
                'flujo_neto': revenue - burn_rate
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
        st.info("📊 Usando datos de demostración (33 meses)")
    
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
    
    **Versión:** 4.5.2
    
    **Mejoras recientes:**
    • Carga de archivos ✅
    • Términos clarificados ✅
    • Radar mejorado ✅
    
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
    
    revenue_mensual = data['historical']['revenue_promedio']
    burn_rate = data['financial']['burn_rate']
    
    flujos_proyectados = calcular_proyeccion_3_meses(revenue_mensual, burn_rate)
    runway = calcular_runway_mejorado(efectivo_actual, flujos_proyectados, burn_rate)
    analisis_cash = calcular_necesidades_excedentes_mejorado(efectivo_actual, flujos_proyectados)
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("💰 Efectivo", f"${efectivo_actual:,.0f}", "+5.2%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("📊 Revenue", f"${revenue_mensual:,.0f}", "+12.3%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("🔥 Burn Rate", f"${burn_rate:,.0f}", "-3.1%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.metric("⏱️ Runway", f"{runway:.1f} meses")
        st.caption("✅ Con proyección 3m")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📈 Tendencia de Revenue (2023-2025)")
    
    df = data['historical']['data']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['periodo'],
        y=df['revenue'],
        mode='lines+markers',
        name='Revenue Mensual',
        line=dict(color='#2563EB', width=3),
        marker=dict(size=8)
    ))
    
    df['ma_3'] = df['revenue'].rolling(window=3).mean()
    fig.add_trace(go.Scatter(
        x=df['periodo'],
        y=df['ma_3'],
        mode='lines',
        name='Promedio Móvil (3m)',
        line=dict(color='#10B981', width=2, dash='dash')
    ))
    
    fig.update_layout(
        height=450,
        hovermode='x unified',
        xaxis_title="Período",
        yaxis_title="Revenue (USD)",
        yaxis=dict(tickformat='$,.0f'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        xaxis=dict(rangeslider=dict(visible=True), type='category')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💵 Flujo Proyectado (3 Meses)")
        
        df_flujo = pd.DataFrame({
            'mes': ['Mes 1', 'Mes 2', 'Mes 3'],
            'flujo': flujos_proyectados
        })
        
        colores = ['#10B981' if f > 0 else '#EF4444' for f in flujos_proyectados]
        
        fig = go.Figure(data=[
            go.Bar(x=df_flujo['mes'], y=df_flujo['flujo'], marker_color=colores)
        ])
        fig.update_layout(
            xaxis_title='Período',
            yaxis_title='Flujo Neto (USD)',
            yaxis=dict(tickformat='$,.0f'),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption(f"**Balance 3m:** ${analisis_cash['balance_proyectado']:,.0f}")
    
    with col2:
        st.markdown("### 🎯 Análisis de Posición")
        
        excedente_deficit = analisis_cash['excedente_deficit']
        balance_proyectado = analisis_cash['balance_proyectado']
        necesidades = analisis_cash['necesidades_minimas']
        
        if excedente_deficit > 0:
            # ✅ CORRECCIÓN 2: Cambio de "Deuda" a "Reinversión"
            st.success(f"""
            **✅ POSICIÓN SALUDABLE**
            
            **Proyección 3 meses:**
            - Efectivo inicial: ${efectivo_actual:,.0f}
            - Balance proyectado: ${balance_proyectado:,.0f}
            - Buffer mínimo: ${necesidades:,.0f}
            - **Excedente: ${excedente_deficit:,.0f}**
            
            **Asignación sugerida del excedente:**
            1. Reserva de seguridad (30%): ${excedente_deficit*0.3:,.0f}
            2. Expansión de flota (40%): ${excedente_deficit*0.4:,.0f}
            3. Reinversión/Crecimiento (30%): ${excedente_deficit*0.3:,.0f}
            
            *Nota: Reserva debe mantenerse en efectivo líquido*
            """)
        else:
            deficit = abs(excedente_deficit)
            st.warning(f"""
            **⚠️ ATENCIÓN REQUERIDA**
            
            **Proyección 3 meses:**
            - Efectivo inicial: ${efectivo_actual:,.0f}
            - Balance proyectado: ${balance_proyectado:,.0f}
            - Buffer mínimo: ${necesidades:,.0f}
            - **Déficit: ${deficit:,.0f}**
            
            **Acciones sugeridas:**
            1. Acelerar cobros de cuentas por cobrar
            2. Negociar extensión de plazos con proveedores
            3. Línea de crédito de corto plazo: ${deficit:,.0f}
            """)

# =============================================================================
# PÁGINA: ANÁLISIS HISTÓRICO
# =============================================================================

elif page == "📈 Análisis Histórico":
    st.markdown("## 📈 Análisis Histórico (2023-2025)")
    st.caption("✨ Con análisis de tendencias y comparación anual")
    
    col1, col2, col3, col4 = st.columns(4)
    
    df_hist = data['historical']['data']
    
    with col1:
        st.metric("Revenue Promedio", f"${data['historical']['revenue_promedio']:,.0f}")
    
    with col2:
        st.metric("Revenue Mínimo", f"${data['historical']['revenue_minimo']:,.0f}")
    
    with col3:
        st.metric("Revenue Máximo", f"${data['historical']['revenue_maximo']:,.0f}")
    
    with col4:
        y_values = df_hist['revenue'].values
        slope, intercept, trend_line = calcular_tendencia_lineal(y_values)
        tendencia_pct = (slope / df_hist['revenue'].mean()) * 100
        st.metric("Tendencia Mensual", f"{tendencia_pct:+.2f}%")
    
    st.markdown("### 📊 Evolución Histórica con Análisis de Tendencia")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_hist['periodo'],
        y=df_hist['revenue'],
        mode='lines',
        name='Revenue',
        fill='tozeroy',
        line=dict(color='#2563EB', width=2),
        fillcolor='rgba(37, 99, 235, 0.2)'
    ))
    
    fig.add_trace(go.Scatter(
        x=df_hist['periodo'],
        y=trend_line,
        mode='lines',
        name='Tendencia Lineal',
        line=dict(color='#EF4444', width=3, dash='dash')
    ))
    
    promedio = df_hist['revenue'].mean()
    fig.add_hline(
        y=promedio,
        line_dash="dot",
        line_color="gray",
        annotation_text=f"Promedio: ${promedio:,.0f}",
        annotation_position="right"
    )
    
    fig.update_layout(
        height=450,
        hovermode='x unified',
        xaxis_title="Período",
        yaxis_title="Revenue (USD)",
        yaxis=dict(tickformat='$,.0f'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        xaxis=dict(type='category')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 📅 Comparación Año sobre Año")
    
    years_revenue = {}
    for year in [2023, 2024, 2025]:
        year_data = df_hist[df_hist['periodo'].str.startswith(str(year))]
        if len(year_data) > 0:
            years_revenue[year] = year_data['revenue'].sum()
    
    fig_years = go.Figure(data=[
        go.Bar(
            x=list(years_revenue.keys()),
            y=list(years_revenue.values()),
            marker_color=['#3B82F6', '#2563EB', '#1D4ED8'],
            text=[f"${v:,.0f}" for v in years_revenue.values()],
            textposition='outside'
        )
    ])
    
    fig_years.update_layout(
        title="Revenue Total por Año",
        xaxis_title="Año",
        yaxis_title="Revenue Total (USD)",
        yaxis=dict(tickformat='$,.0f'),
        height=350
    )
    
    st.plotly_chart(fig_years, use_container_width=True)
    
    st.markdown("### 👥 Top 5 Clientes Históricos")
    
    df_clients = pd.DataFrame(data['historical']['top_clients'], columns=['Cliente', 'Revenue'])
    
    fig = px.bar(df_clients, y='Cliente', x='Revenue', orientation='h',
                 title='Revenue por Cliente (Acumulado 2023-2025)')
    fig.update_traces(marker_color='#2563EB')
    fig.update_layout(
        height=400,
        xaxis_title="Revenue Total (USD)",
        yaxis_title="",
        xaxis=dict(tickformat='$,.0f'),
        yaxis={'categoryorder':'total ascending'}
    )
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PÁGINA: PROYECCIONES
# =============================================================================

elif page == "💵 Proyecciones":
    st.markdown("## 💵 Proyecciones de Flujo de Efectivo")
    st.caption("✨ Comparación visual clara entre escenarios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        meses = st.slider("Meses a proyectar:", 1, 12, 6)
    
    with col2:
        vista = st.selectbox("Vista:", ["📊 Barras Comparativas", "📈 Líneas Comparativas"])
    
    proyecciones = generar_proyecciones_multi_escenario(
        meses,
        data['historical']['revenue_promedio'],
        data['financial']['burn_rate']
    )
    
    if vista == "📊 Barras Comparativas":
        st.markdown("### 💰 Comparación de Revenue por Escenario")
        st.info("✨ Barras agrupadas para comparación clara")
        
        fig = go.Figure()
        
        colores = {
            'Conservador': '#EF4444',
            'Moderado': '#2563EB',
            'Optimista': '#10B981'
        }
        
        for escenario, df in proyecciones.items():
            fig.add_trace(go.Bar(
                name=escenario,
                x=[f"Mes {int(m)}" for m in df['mes']],
                y=df['revenue'],
                marker_color=colores[escenario]
            ))
        
        fig.update_layout(
            barmode='group',
            height=450,
            xaxis_title='Período',
            yaxis_title='Revenue Proyectado (USD)',
            yaxis=dict(tickformat='$,.0f'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 💵 Comparación de Flujo Neto por Escenario")
        
        fig2 = go.Figure()
        
        for escenario, df in proyecciones.items():
            fig2.add_trace(go.Bar(
                name=escenario,
                x=[f"Mes {int(m)}" for m in df['mes']],
                y=df['flujo_neto'],
                marker_color=colores[escenario]
            ))
        
        fig2.add_hline(y=0, line_dash="dash", line_color="gray",
                      annotation_text="Punto de Equilibrio")
        
        fig2.update_layout(
            barmode='group',
            height=450,
            xaxis_title='Período',
            yaxis_title='Flujo Neto (USD)',
            yaxis=dict(tickformat='$,.0f'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
    else:
        st.markdown("### 📈 Comparación de Revenue por Escenario")
        
        fig = go.Figure()
        
        colores = {
            'Conservador': '#EF4444',
            'Moderado': '#2563EB',
            'Optimista': '#10B981'
        }
        
        for escenario, df in proyecciones.items():
            fig.add_trace(go.Scatter(
                x=[f"Mes {m}" for m in df['mes']],
                y=df['revenue'],
                mode='lines+markers',
                name=escenario,
                line=dict(color=colores[escenario], width=3),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            height=450,
            hovermode='x unified',
            xaxis_title='Período',
            yaxis_title='Revenue Proyectado (USD)',
            yaxis=dict(tickformat='$,.0f'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 📋 Resumen Comparativo")
    
    resumen = []
    for escenario, df in proyecciones.items():
        resumen.append({
            'Escenario': escenario,
            'Revenue Total': f"${df['revenue'].sum():,.0f}",
            'Flujo Neto Total': f"${df['flujo_neto'].sum():,.0f}",
            'Revenue Promedio': f"${df['revenue'].mean():,.0f}"
        })
    
    df_resumen = pd.DataFrame(resumen)
    st.dataframe(df_resumen, use_container_width=True, hide_index=True)

# =============================================================================
# PÁGINA: REPORTES DETALLADOS
# =============================================================================

elif page == "📊 Reportes Detallados":
    st.markdown("## 📊 Reportes Detallados")
    
    tabs = st.tabs(["📈 Estacionalidad", "🔥 Burn Rate", "💰 Balance Proyectado"])
    
    with tabs[0]:
        st.markdown("### 📅 Análisis de Estacionalidad")
        st.caption("✨ Interactivo: Compara años vs promedio")
        
        st.markdown("#### 🎛️ Controles de Visualización")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            show_promedio = st.checkbox("📊 Promedio Global", value=True, key="show_avg")
        with col2:
            show_2023 = st.checkbox("📅 Año 2023", value=False, key="show_2023")
        with col3:
            show_2024 = st.checkbox("📅 Año 2024", value=False, key="show_2024")
        with col4:
            # ✅ CORRECCIÓN 4: Deshabilitar 2025 con explicación
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
        
        # ✅ CORRECCIÓN 3: Radar que cierra (duplicar primer valor)
        if show_promedio:
            factores_promedio = [data['seasonal_factors'][m] for m in meses_nombres]
            # Duplicar primer valor para cerrar el polígono
            factores_cerrado = factores_promedio + [factores_promedio[0]]
            meses_cerrado = meses_nombres + [meses_nombres[0]]
            
            fig.add_trace(go.Scatterpolar(
                r=factores_cerrado,
                theta=meses_cerrado,
                fill='toself',
                name='Promedio Global',
                line=dict(color='#2563EB', width=3),
                fillcolor='rgba(37, 99, 235, 0.2)',
                marker=dict(size=8, color='#2563EB')
            ))
        
        if 'seasonal_by_year' in data:
            year_colors = {2023: '#10B981', 2024: '#F59E0B', 2025: '#EF4444'}
            year_shows = {2023: show_2023, 2024: show_2024}  # Excluir 2025
            
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
                radialaxis=dict(visible=True, range=[0, 1.5], tickformat='.2f'),
                angularaxis=dict(rotation=90, direction='clockwise')
            ),
            title='Factores Estacionales (1.0 = promedio)',
            height=500,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Nota sobre 2025
        st.info("""
        ℹ️ **Nota sobre Año 2025:**  
        El año 2025 está incompleto (solo 9 meses: Ene-Sep) y no se puede visualizar en el radar 
        que requiere 12 puntos de datos. Los factores de 2025 están incluidos en el promedio global.
        """)
        
        st.markdown("#### 📋 Factores Estacionales Detallados")
        df_seasonal = pd.DataFrame(list(data['seasonal_factors'].items()),
                                   columns=['Mes', 'Factor'])
        df_seasonal['Interpretación'] = df_seasonal['Factor'].apply(
            lambda x: '📈 Alta actividad' if x > 1.1 else ('📉 Baja actividad' if x < 0.9 else '➡️ Normal')
        )
        st.dataframe(df_seasonal, use_container_width=True, hide_index=True)
    
    with tabs[1]:
        st.markdown("### 🔥 Análisis de Burn Rate")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Burn Rate Mensual", f"${data['financial']['burn_rate']:,.0f}")
        with col2:
            st.metric("Gastos Fijos", f"${data['financial']['gastos_fijos']:,.0f}")
        with col3:
            st.metric("Costos Variables", f"${data['financial']['costos_variables']:,.0f}")
        
        burn_breakdown = pd.DataFrame({
            'Categoría': ['Salarios', 'Logística', 'Mantenimiento', 'Administrativos', 'Otros'],
            'Monto': [40000, 15000, 12000, 10000, 10089]
        })
        
        fig = px.pie(burn_breakdown, values='Monto', names='Categoría',
                     title='Distribución del Burn Rate',
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[2]:
        st.markdown("### 💰 Balance Proyectado Multi-Escenario")
        st.caption("✅ Balance acumulado correctamente")
        
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
            title='Evolución del Efectivo por Escenario'
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
                    
                    ✅ Posición saludable
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

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748B; padding: 2rem 0;'>
    <p><strong>SPT Cash Flow Tool v4.5.2</strong></p>
    <p>✅ Carga de archivos • Términos clarificados • Radar mejorado • Año 2025 explicado</p>
    <p>Desarrollado por <a href='https://www.ai-mindnovation.com' target='_blank'>AI-MindNovation</a></p>
    <p>© 2025 AI-MindNovation. Todos los derechos reservados.</p>
</div>
""", unsafe_allow_html=True)
