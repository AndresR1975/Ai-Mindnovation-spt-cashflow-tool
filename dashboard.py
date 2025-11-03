"""
SPT CASH FLOW TOOL - Dashboard Streamlit v4.4
==============================================
Dashboard de análisis de flujo de efectivo para SPT Colombia

NUEVAS MEJORAS VISUALES EN v4.4:
✅ Mejora 3: Gráfico histórico completo (33 meses, 2023-2025)
✅ Mejora 6: Comparación visual de 3 escenarios simultáneos
✅ Mejora 8: Balance proyectado multi-escenario
+ Todas las funcionalidades de v4.3

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
    st.session_state.archivos_cargados = {
        'util_2023': None,
        'util_2024': None,
        'util_2025': None,
        'weekly': None,
        'financial': None
    }

if 'datos_procesados' not in st.session_state:
    st.session_state.datos_procesados = None

# =============================================================================
# FUNCIONES DE DATOS - MEJORA 3: HISTÓRICO COMPLETO (33 MESES)
# =============================================================================

def get_historical_data_complete():
    """Retorna datos históricos completos de 2023-2025 (33 meses)"""
    
    # Generar 33 meses de datos (Ene 2023 - Sep 2025)
    meses = []
    revenue = []
    
    base_revenue = 120000
    
    for i in range(33):
        year = 2023 + (i // 12)
        month = (i % 12) + 1
        periodo = f"{year}-{str(month).zfill(2)}"
        meses.append(periodo)
        
        # Simular crecimiento con estacionalidad
        tendencia = base_revenue + (i * 4500)
        estacionalidad = np.sin(i * np.pi / 6) * 15000
        ruido = np.random.randint(-5000, 8000)
        
        revenue_mes = max(100000, tendencia + estacionalidad + ruido)
        revenue.append(revenue_mes)
    
    return pd.DataFrame({
        'periodo': meses,
        'revenue': revenue
    })

def get_data():
    """Retorna datos según la fuente (demo o real)"""
    
    if st.session_state.data_source == 'real' and st.session_state.datos_procesados:
        return st.session_state.datos_procesados
    else:
        # Datos demo con histórico completo
        df_historical = get_historical_data_complete()
        
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
                'data': df_historical
            },
            'financial': {
                'burn_rate': 87089,
                'gastos_fijos': 65000,
                'costos_variables': 22089,
                'margen_operativo': 0.53
            },
            'cash_needs': {
                'necesidades_3_meses': 261267,
                'detalle_mensual': [87089, 87089, 87089]
            },
            'seasonal_factors': {
                'Enero': 1.15, 'Febrero': 0.85, 'Marzo': 1.05,
                'Abril': 0.95, 'Mayo': 1.10, 'Junio': 1.20,
                'Julio': 1.08, 'Agosto': 0.92, 'Septiembre': 1.03,
                'Octubre': 1.12, 'Noviembre': 0.98, 'Diciembre': 1.18
            }
        }

# =============================================================================
# FUNCIONES DE PROYECCIÓN - MEJORA 6 Y 8: MULTI-ESCENARIO
# =============================================================================

def generar_proyecciones_multi_escenario(meses, revenue_base, burn_rate):
    """
    Genera proyecciones para los 3 escenarios simultáneamente
    
    MEJORA 6: Comparación visual de escenarios
    """
    
    escenarios = {
        'Conservador': {'factor': 0.85, 'crecimiento': 0.01, 'color': '#EF4444'},
        'Moderado': {'factor': 1.0, 'crecimiento': 0.02, 'color': '#2563EB'},
        'Optimista': {'factor': 1.15, 'crecimiento': 0.03, 'color': '#10B981'}
    }
    
    resultados = {}
    
    for nombre, config in escenarios.items():
        proyeccion = []
        
        for i in range(meses):
            # Revenue con crecimiento mensual
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
    """
    Genera balance proyectado para los 3 escenarios
    
    MEJORA 8: Balance multi-escenario
    """
    
    balances = {}
    
    for escenario, df_proj in proyecciones.items():
        balance = []
        efectivo_acumulado = efectivo_inicial
        
        for _, row in df_proj.iterrows():
            efectivo_acumulado += row['flujo_neto']
            balance.append({
                'mes': int(row['mes']),
                'efectivo': efectivo_acumulado,
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
    
    # Fuente de datos
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
        file_2023 = st.file_uploader("Utilization Report 2023", type=['xlsx', 'xls'], key="file_2023")
        file_2024 = st.file_uploader("Utilization Report 2024", type=['xlsx', 'xls'], key="file_2024")
        file_2025 = st.file_uploader("Utilization Report 2025", type=['xlsx', 'xls'], key="file_2025")
        
        st.markdown("**Estado Actual:**")
        file_weekly = st.file_uploader("Weekly Operation Report", type=['xlsx', 'xls'], key="file_weekly")
        
        st.markdown("**Financiero:**")
        file_financial = st.file_uploader("Estado Financiero", type=['xlsx', 'xls'], key="file_financial")
        
        all_files = all([file_2023, file_2024, file_2025, file_weekly, file_financial])
        
        if all_files:
            st.success("✅ Todos los archivos cargados")
            if st.button("🚀 Procesar Datos", use_container_width=True, type="primary"):
                st.info("⚙️ Procesamiento simulado - Integración backend pendiente")
                st.session_state.data_source = 'demo'
        else:
            missing = []
            if not file_2023: missing.append("Util 2023")
            if not file_2024: missing.append("Util 2024")
            if not file_2025: missing.append("Util 2025")
            if not file_weekly: missing.append("Weekly Report")
            if not file_financial: missing.append("Estado Financiero")
            st.warning(f"⚠️ Faltan: {', '.join(missing)}")
    else:
        st.session_state.data_source = 'demo'
        st.info("📊 Usando datos de demostración con 33 meses de histórico (2023-2025)")
    
    st.markdown("---")
    
    # Efectivo disponible
    st.markdown("### 💵 Configuración Financiera")
    
    efectivo_input = st.number_input(
        "Efectivo Disponible Actual (USD):",
        min_value=0,
        value=st.session_state.efectivo_disponible if st.session_state.efectivo_disponible else 80000,
        step=1000,
        format="%d",
        help="Ingrese el monto de efectivo disponible actual"
    )
    
    if st.button("💾 Actualizar Efectivo", use_container_width=True):
        st.session_state.efectivo_disponible = efectivo_input
        st.success(f"✅ Efectivo actualizado: ${efectivo_input:,.0f}")
        st.rerun()
    
    efectivo_actual = st.session_state.efectivo_disponible if st.session_state.efectivo_disponible else efectivo_input
    
    st.info(f"💰 **Efectivo actual:** ${efectivo_actual:,.0f}")
    
    if st.session_state.data_source == 'real':
        st.success("🟢 Usando datos reales")
    else:
        st.warning("🟡 Usando datos demo (33 meses)")
    
    st.markdown("---")
    
    # Navegación
    st.markdown("### 📊 Navegación")
    page = st.radio(
        "Selecciona sección:",
        ["🏠 Resumen Ejecutivo", "📈 Análisis Histórico", "💵 Proyecciones", "📊 Reportes Detallados"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Información
    st.markdown("### ℹ️ Información")
    st.markdown(f"""
    **Usuario:** Autenticado ✅
    
    **Datos:** {st.session_state.data_source.upper()}
    
    **Períodos:** 33 meses
    
    **Desarrollado por:**  
    [AI-MindNovation](https://www.ai-mindnovation.com)
    
    **Cliente:** SPT Colombia
    
    **Versión:** 4.4
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
    runway = efectivo_actual / burn_rate if burn_rate > 0 else 0
    necesidades_3_meses = data['cash_needs']['necesidades_3_meses']
    
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
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ✅ MEJORA 3: Gráfico histórico completo (33 meses)
    st.markdown("### 📈 Tendencia de Revenue (2023-2025)")
    st.caption("🆕 Vista completa de 33 meses de histórico")
    
    df = data['historical']['data']
    
    # Agregar línea de tendencia
    fig = go.Figure()
    
    # Línea principal de revenue
    fig.add_trace(go.Scatter(
        x=df['periodo'],
        y=df['revenue'],
        mode='lines+markers',
        name='Revenue Mensual',
        line=dict(color='#2563EB', width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
    ))
    
    # Promedio móvil de 3 meses
    df['ma_3'] = df['revenue'].rolling(window=3).mean()
    fig.add_trace(go.Scatter(
        x=df['periodo'],
        y=df['ma_3'],
        mode='lines',
        name='Promedio Móvil (3 meses)',
        line=dict(color='#10B981', width=2, dash='dash'),
        hovertemplate='<b>%{x}</b><br>Promedio: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        height=450,
        hovermode='x unified',
        xaxis_title="Período (YYYY-MM)",
        yaxis_title="Revenue (USD)",
        yaxis=dict(tickformat='$,.0f'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(
            rangeslider=dict(visible=True),  # Slider para zoom
            type='category'
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Análisis de flujo
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💵 Flujo de Efectivo Proyectado")
        cash_flow_data = pd.DataFrame({
            'mes': ['Nov-25', 'Dic-25', 'Ene-26'],
            'flujo': [45000, 52000, 38000]
        })
        
        fig = go.Figure(data=[
            go.Bar(x=cash_flow_data['mes'], y=cash_flow_data['flujo'],
                   marker_color=['#10B981', '#10B981', '#10B981'])
        ])
        fig.update_layout(
            title='Próximos 3 Meses',
            xaxis_title='Mes',
            yaxis_title='Flujo Neto (USD)',
            yaxis=dict(tickformat='$,.0f'),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Recomendación")
        
        excedente = efectivo_actual - necesidades_3_meses
        
        if excedente > 0:
            st.success(f"""
            **✅ EXCEDENTE DE EFECTIVO**
            
            - Efectivo disponible: ${efectivo_actual:,.0f}
            - Necesidades 3 meses: ${necesidades_3_meses:,.0f}
            - **Excedente: ${excedente:,.0f}**
            
            **Recomendaciones:**
            1. Reserva emergencia: ${excedente*0.3:,.0f}
            2. Expansión flota: ${excedente*0.4:,.0f}
            3. Pago adelantado: ${excedente*0.3:,.0f}
            """)
        else:
            deficit = abs(excedente)
            st.warning(f"""
            **⚠️ NECESIDAD DE FINANCIAMIENTO**
            
            - Efectivo disponible: ${efectivo_actual:,.0f}
            - Necesidades 3 meses: ${necesidades_3_meses:,.0f}
            - **Déficit: ${deficit:,.0f}**
            
            **Recomendaciones:**
            1. Acelerar cobros
            2. Negociar plazos proveedores
            3. Línea crédito: ${deficit:,.0f}
            """)

# =============================================================================
# PÁGINA: ANÁLISIS HISTÓRICO
# =============================================================================

elif page == "📈 Análisis Histórico":
    st.markdown("## 📈 Análisis Histórico (2023-2025)")
    st.caption("🆕 Vista expandida con 33 meses de datos")
    
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Revenue Promedio", f"${data['historical']['revenue_promedio']:,.0f}")
    
    with col2:
        st.metric("Revenue Mínimo", f"${data['historical']['revenue_minimo']:,.0f}")
    
    with col3:
        st.metric("Revenue Máximo", f"${data['historical']['revenue_maximo']:,.0f}")
    
    with col4:
        st.metric("Períodos Analizados", f"{data['historical']['periodos']} meses")
    
    # Gráfico histórico mejorado
    df = data['historical']['data']
    
    fig = px.area(df, x='periodo', y='revenue',
                  title='Evolución Histórica del Revenue (Ene 2023 - Sep 2025)')
    fig.update_traces(line_color='#2563EB', fillcolor='rgba(37, 99, 235, 0.2)')
    fig.update_layout(
        height=400,
        xaxis_title="Período (YYYY-MM)",
        yaxis_title="Revenue (USD)",
        yaxis=dict(tickformat='$,.0f'),
        xaxis=dict(type='category')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Top clientes
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
    
    # Tabla
    st.markdown("#### 📋 Detalle de Clientes")
    df_clients_display = df_clients.copy()
    df_clients_display['Revenue'] = df_clients_display['Revenue'].apply(lambda x: f"${x:,.0f}")
    st.dataframe(df_clients_display, use_container_width=True, hide_index=True)

# =============================================================================
# PÁGINA: PROYECCIONES - MEJORA 6: COMPARACIÓN ESCENARIOS
# =============================================================================

elif page == "💵 Proyecciones":
    st.markdown("## 💵 Proyecciones de Flujo de Efectivo")
    st.caption("🆕 Comparación visual de los 3 escenarios simultáneamente")
    
    st.info("📊 Visualice cómo varían las proyecciones según el escenario conservador, moderado u optimista")
    
    # Parámetros
    col1, col2 = st.columns(2)
    
    with col1:
        meses = st.slider("Meses a proyectar:", 1, 12, 6)
    
    with col2:
        vista = st.selectbox("Vista:", ["Comparación Completa", "Escenario Individual"])
    
    # Generar proyecciones multi-escenario
    proyecciones = generar_proyecciones_multi_escenario(
        meses,
        data['historical']['revenue_promedio'],
        data['financial']['burn_rate']
    )
    
    if vista == "Comparación Completa":
        # ✅ MEJORA 6: Gráfico comparativo de 3 escenarios
        st.markdown("### 📊 Comparación de Revenue por Escenario")
        
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
                name=f'{escenario}',
                line=dict(color=colores[escenario], width=3),
                marker=dict(size=8),
                hovertemplate=f'<b>{escenario}</b><br>Revenue: $%{{y:,.0f}}<extra></extra>'
            ))
        
        fig.update_layout(
            height=450,
            hovermode='x unified',
            xaxis_title='Período',
            yaxis_title='Revenue Proyectado (USD)',
            yaxis=dict(tickformat='$,.0f'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico de Flujo Neto Comparativo
        st.markdown("### 💰 Comparación de Flujo Neto por Escenario")
        
        fig2 = go.Figure()
        
        for escenario, df in proyecciones.items():
            fig2.add_trace(go.Scatter(
                x=[f"Mes {m}" for m in df['mes']],
                y=df['flujo_neto'],
                mode='lines+markers',
                name=f'{escenario}',
                line=dict(color=colores[escenario], width=3),
                marker=dict(size=8),
                fill='tonexty' if escenario != 'Conservador' else None,
                fillcolor=f"rgba{tuple(list(int(colores[escenario][i:i+2], 16) for i in (1, 3, 5)) + [0.1])}",
                hovertemplate=f'<b>{escenario}</b><br>Flujo Neto: $%{{y:,.0f}}<extra></extra>'
            ))
        
        # Línea de referencia en $0
        fig2.add_hline(y=0, line_dash="dash", line_color="gray", 
                       annotation_text="Punto de equilibrio")
        
        fig2.update_layout(
            height=450,
            hovermode='x unified',
            xaxis_title='Período',
            yaxis_title='Flujo Neto (USD)',
            yaxis=dict(tickformat='$,.0f'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Tabla comparativa
        st.markdown("### 📋 Tabla Comparativa de Escenarios")
        
        cols = st.columns(3)
        
        for idx, (escenario, df) in enumerate(proyecciones.items()):
            with cols[idx]:
                st.markdown(f"#### {escenario}")
                df_display = df[['mes', 'revenue', 'flujo_neto']].copy()
                df_display['mes'] = df_display['mes'].apply(lambda x: f"Mes {int(x)}")
                df_display['revenue'] = df_display['revenue'].apply(lambda x: f"${x:,.0f}")
                df_display['flujo_neto'] = df_display['flujo_neto'].apply(lambda x: f"${x:,.0f}")
                df_display.columns = ['Período', 'Revenue', 'Flujo Neto']
                st.dataframe(df_display, use_container_width=True, hide_index=True, height=400)
    
    else:
        # Vista individual (como antes)
        escenario_seleccionado = st.selectbox("Seleccione escenario:", 
                                              ["Conservador", "Moderado", "Optimista"])
        
        df_proj = proyecciones[escenario_seleccionado]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Ingresos', x=[f"Mes {m}" for m in df_proj['mes']], 
                            y=df_proj['revenue'], marker_color='#10B981'))
        fig.add_trace(go.Bar(name='Gastos', x=[f"Mes {m}" for m in df_proj['mes']], 
                            y=df_proj['gastos'], marker_color='#EF4444'))
        fig.add_trace(go.Scatter(name='Flujo Neto', x=[f"Mes {m}" for m in df_proj['mes']], 
                                y=df_proj['flujo_neto'],
                                mode='lines+markers', line=dict(color='#2563EB', width=3),
                                marker=dict(size=10)))
        
        fig.update_layout(
            title=f'Proyección - Escenario {escenario_seleccionado}',
            xaxis_title='Período',
            yaxis_title='Monto (USD)',
            yaxis=dict(tickformat='$,.0f'),
            height=500,
            barmode='group',
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PÁGINA: REPORTES DETALLADOS - MEJORA 8: BALANCE MULTI-ESCENARIO
# =============================================================================

elif page == "📊 Reportes Detallados":
    st.markdown("## 📊 Reportes Detallados")
    
    tabs = st.tabs(["📈 Estacionalidad", "🔥 Burn Rate", "💰 Balance Proyectado"])
    
    with tabs[0]:
        st.markdown("### 📅 Análisis de Estacionalidad")
        
        df_seasonal = pd.DataFrame(list(data['seasonal_factors'].items()), 
                                   columns=['Mes', 'Factor'])
        
        # Radar con enero arriba
        fig = go.Figure(data=go.Scatterpolar(
            r=df_seasonal['Factor'],
            theta=df_seasonal['Mes'],
            fill='toself',
            line=dict(color='#2563EB', width=2),
            marker=dict(size=8, color='#2563EB')
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1.5], tickformat='.2f'),
                angularaxis=dict(rotation=90, direction='clockwise')
            ),
            title='Factores Estacionales por Mes (1.0 = promedio)',
            height=500,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabla
        st.markdown("#### 📋 Factores Estacionales Detallados")
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
        # ✅ MEJORA 8: Balance proyectado multi-escenario
        st.markdown("### 💰 Balance Proyectado Multi-Escenario")
        st.caption("🆕 Compare la evolución del efectivo en diferentes escenarios")
        
        # Parámetros
        meses_balance = st.slider("Meses de proyección:", 1, 12, 6, key="balance_slider")
        
        # Generar proyecciones y balances
        proyecciones = generar_proyecciones_multi_escenario(
            meses_balance,
            data['historical']['revenue_promedio'],
            data['financial']['burn_rate']
        )
        
        balances = generar_balance_multi_escenario(efectivo_actual, proyecciones)
        
        # Gráfico comparativo de balance
        fig = go.Figure()
        
        colores = {
            'Conservador': '#EF4444',
            'Moderado': '#2563EB',
            'Optimista': '#10B981'
        }
        
        for escenario, df_balance in balances.items():
            fig.add_trace(go.Scatter(
                x=[f"Mes {m}" for m in df_balance['mes']],
                y=df_balance['efectivo'],
                mode='lines+markers',
                name=escenario,
                line=dict(color=colores[escenario], width=3),
                marker=dict(size=10),
                hovertemplate=f'<b>{escenario}</b><br>Efectivo: $%{{y:,.0f}}<extra></extra>'
            ))
        
        # Línea de referencia en $0 (punto crítico)
        fig.add_hline(y=0, line_dash="dash", line_color="red", line_width=2,
                     annotation_text="⚠️ Punto Crítico", annotation_position="right")
        
        # Línea efectivo inicial
        fig.add_hline(y=efectivo_actual, line_dash="dot", line_color="gray",
                     annotation_text=f"Efectivo Inicial: ${efectivo_actual:,.0f}", 
                     annotation_position="left")
        
        fig.update_layout(
            height=500,
            hovermode='x unified',
            xaxis_title='Período',
            yaxis_title='Efectivo Disponible (USD)',
            yaxis=dict(tickformat='$,.0f'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            title='Evolución del Efectivo por Escenario'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Análisis de runway
        st.markdown("### ⏱️ Análisis de Runway por Escenario")
        
        cols = st.columns(3)
        
        for idx, (escenario, df_balance) in enumerate(balances.items()):
            with cols[idx]:
                efectivo_final = df_balance.iloc[-1]['efectivo']
                
                if efectivo_final > 0:
                    runway_escenario = efectivo_final / data['financial']['burn_rate']
                    st.success(f"""
                    **{escenario}**
                    
                    Efectivo final: ${efectivo_final:,.0f}
                    
                    Runway: {runway_escenario:.1f} meses
                    
                    ✅ Posición saludable
                    """)
                else:
                    # Encontrar cuándo se quedó sin efectivo
                    meses_sin_efectivo = df_balance[df_balance['efectivo'] < 0]
                    if len(meses_sin_efectivo) > 0:
                        mes_critico = meses_sin_efectivo.iloc[0]['mes']
                        st.error(f"""
                        **{escenario}**
                        
                        Efectivo final: ${efectivo_final:,.0f}
                        
                        ⚠️ Déficit en mes {int(mes_critico)}
                        
                        Requiere financiamiento
                        """)
        
        # Tabla detallada
        st.markdown("#### 📋 Detalle de Balance por Escenario")
        
        cols_table = st.columns(3)
        
        for idx, (escenario, df_balance) in enumerate(balances.items()):
            with cols_table[idx]:
                st.markdown(f"**{escenario}**")
                df_display = df_balance.copy()
                df_display['mes'] = df_display['mes'].apply(lambda x: f"Mes {int(x)}")
                df_display['efectivo'] = df_display['efectivo'].apply(lambda x: f"${x:,.0f}")
                df_display = df_display[['mes', 'efectivo']]
                df_display.columns = ['Período', 'Efectivo']
                st.dataframe(df_display, use_container_width=True, hide_index=True, height=400)

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748B; padding: 2rem 0;'>
    <p><strong>SPT Cash Flow Tool v4.4</strong></p>
    <p>🆕 Con mejoras visuales: Histórico completo + Comparación de escenarios + Balance multi-escenario</p>
    <p>Desarrollado por <a href='https://www.ai-mindnovation.com' target='_blank'>AI-MindNovation</a></p>
    <p>© 2025 AI-MindNovation. Todos los derechos reservados.</p>
</div>
""", unsafe_allow_html=True)
