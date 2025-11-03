"""
SPT CASH FLOW TOOL - Dashboard Streamlit v4.2
==============================================
Dashboard de análisis de flujo de efectivo para SPT Colombia

MEJORAS EN ESTA VERSIÓN:
✅ 1. Autenticación con password
✅ 2. Ingreso manual de efectivo disponible
✅ 4. Revenue por cliente ordenado descendente
✅ 7. Diagrama radar con enero arriba (12 en punto)

Autor: AI-MindNovation
Cliente: SPT Colombia
Fecha: Noviembre 2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =============================================================================
# CONFIGURACIÓN Y AUTENTICACIÓN
# =============================================================================

# Password para acceso (en producción, mover a Streamlit Secrets)
VALID_PASSWORD = "spt2025"  # Cambiar por password real

def check_password():
    """Verifica autenticación del usuario"""
    
    # Si ya está autenticado, retornar True
    if st.session_state.get('authenticated', False):
        return True
    
    # Pantalla de login
    st.markdown("""
    <div style='text-align: center; padding: 3rem 0;'>
        <h1 style='color: #2563EB; font-size: 3rem;'>💰 SPT CASH FLOW TOOL</h1>
        <p style='color: #64748B; font-size: 1.2rem;'>Análisis de Flujo de Efectivo</p>
        <p style='color: #64748B;'>Ingrese la contraseña para acceder</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Centrar el formulario
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

# Verificar autenticación ANTES de mostrar contenido
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
    .logout-btn {
        background-color: #EF4444;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# INICIALIZACIÓN DE SESSION STATE
# =============================================================================

if 'efectivo_disponible' not in st.session_state:
    st.session_state.efectivo_disponible = None

# =============================================================================
# FUNCIONES DE DATOS DEMO
# =============================================================================

def get_historical_data():
    """Retorna datos históricos de demostración"""
    return pd.DataFrame({
        'mes': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        'revenue': [120000, 135000, 128000, 145000, 138000, 152000, 
                   148000, 155000, 162000, 158000, 165000, 172000]
    })

def get_top_clients():
    """Retorna top clientes ordenados descendente"""
    return pd.DataFrame({
        'Cliente': ['Kluane/Aris', 'Explomin', 'Kluane', 'Office', 'SPT Colombia'],
        'Revenue': [549800, 496700, 490575, 481310, 445850]
    }).sort_values('Revenue', ascending=False)  # ✅ Ordenado descendente

def get_seasonal_factors():
    """Retorna factores estacionales"""
    return pd.DataFrame({
        'Mes': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
               'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        'Factor': [1.15, 0.85, 1.05, 0.95, 1.10, 1.20, 
                  1.08, 0.92, 1.03, 1.12, 0.98, 1.18]
    })

# =============================================================================
# HEADER Y SIDEBAR
# =============================================================================

st.markdown('<div class="main-title">💰 SPT CASH FLOW TOOL</div>', unsafe_allow_html=True)
st.markdown(f"**Estado al:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Botón de logout en header
col1, col2, col3 = st.columns([6, 1, 1])
with col3:
    if st.button("🚪 Salir"):
        st.session_state.authenticated = False
        st.session_state.efectivo_disponible = None
        st.rerun()

st.markdown("---")

# =============================================================================
# SIDEBAR CON INPUT DE EFECTIVO
# =============================================================================

with st.sidebar:
    st.markdown("### ⚙️ SPT Colombia")
    st.markdown("**Análisis de Flujo de Efectivo**")
    st.markdown("---")
    
    # ✅ MEJORA 2: Input de Efectivo Disponible
    st.markdown("### 💵 Configuración Financiera")
    
    efectivo_input = st.number_input(
        "Efectivo Disponible Actual (USD):",
        min_value=0,
        value=st.session_state.efectivo_disponible if st.session_state.efectivo_disponible else 80000,
        step=1000,
        format="%d",
        help="Ingrese el monto de efectivo disponible actual en la empresa"
    )
    
    if st.button("💾 Actualizar Efectivo", use_container_width=True):
        st.session_state.efectivo_disponible = efectivo_input
        st.success(f"✅ Efectivo actualizado: ${efectivo_input:,.0f}")
        st.rerun()
    
    # Usar el valor de session state o el input
    efectivo_actual = st.session_state.efectivo_disponible if st.session_state.efectivo_disponible else efectivo_input
    
    st.info(f"💰 **Efectivo actual:** ${efectivo_actual:,.0f}")
    
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
    st.markdown("""
    **Usuario:** Autenticado ✅
    
    **Desarrollado por:**  
    [AI-MindNovation](https://www.ai-mindnovation.com)
    
    **Cliente:**  
    SPT Colombia
    
    **Versión:** 4.2
    """)

# =============================================================================
# PÁGINA: RESUMEN EJECUTIVO
# =============================================================================

if page == "🏠 Resumen Ejecutivo":
    st.markdown("## 🎯 Resumen Ejecutivo")
    
    # Calcular métricas basadas en efectivo actual
    revenue_mensual = 185661
    burn_rate = 87089
    runway = efectivo_actual / burn_rate if burn_rate > 0 else 0
    
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
    
    # Gráfico de tendencia
    st.markdown("### 📈 Tendencia de Revenue")
    
    df = get_historical_data()
    
    fig = px.line(df, x='mes', y='revenue', markers=True)
    fig.update_traces(line_color='#2563EB', line_width=3, marker=dict(size=10))
    fig.update_layout(
        height=400,
        hovermode='x unified',
        xaxis_title="Mes",
        yaxis_title="Revenue (USD)",
        yaxis=dict(tickformat='$,.0f')
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
        
        # Calcular excedente/déficit dinámicamente
        necesidades_3_meses = 30000
        excedente = efectivo_actual - necesidades_3_meses
        
        if excedente > 0:
            st.success(f"""
            **✅ EXCEDENTE DE EFECTIVO**
            
            Basado en el análisis actual:
            - Efectivo disponible: ${efectivo_actual:,.0f}
            - Necesidades próximos 3 meses: ${necesidades_3_meses:,.0f}
            - **Excedente para inversión: ${excedente:,.0f}**
            
            **Recomendaciones:**
            1. Asignar 30% a reserva de emergencia
            2. Invertir 40% en expansión de flota
            3. Usar 30% para pago adelantado de deudas
            """)
        else:
            deficit = abs(excedente)
            st.warning(f"""
            **⚠️ NECESIDAD DE FINANCIAMIENTO**
            
            Basado en el análisis actual:
            - Efectivo disponible: ${efectivo_actual:,.0f}
            - Necesidades próximos 3 meses: ${necesidades_3_meses:,.0f}
            - **Déficit a cubrir: ${deficit:,.0f}**
            
            **Recomendaciones:**
            1. Acelerar cobros de cuentas por cobrar
            2. Negociar extensión de plazos con proveedores
            3. Línea de crédito de corto plazo
            """)

# =============================================================================
# PÁGINA: ANÁLISIS HISTÓRICO
# =============================================================================

elif page == "📈 Análisis Histórico":
    st.markdown("## 📈 Análisis Histórico (2023-2025)")
    
    df = get_historical_data()
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_revenue = df['revenue'].mean()
        st.metric("Revenue Promedio", f"${avg_revenue:,.0f}")
    
    with col2:
        min_revenue = df['revenue'].min()
        st.metric("Revenue Mínimo", f"${min_revenue:,.0f}")
    
    with col3:
        max_revenue = df['revenue'].max()
        st.metric("Revenue Máximo", f"${max_revenue:,.0f}")
    
    # Gráfico histórico
    fig = px.area(df, x='mes', y='revenue',
                  title='Evolución Histórica del Revenue')
    fig.update_traces(line_color='#2563EB', fillcolor='rgba(37, 99, 235, 0.2)')
    fig.update_layout(
        height=400,
        xaxis_title="Mes",
        yaxis_title="Revenue (USD)",
        yaxis=dict(tickformat='$,.0f')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # ✅ MEJORA 4: Top clientes ordenado descendente
    st.markdown("### 👥 Top 5 Clientes Históricos")
    
    df_clients = get_top_clients()
    
    fig = px.bar(df_clients, y='Cliente', x='Revenue', orientation='h',
                 title='Revenue por Cliente (2023-2025)')
    fig.update_traces(marker_color='#2563EB')
    fig.update_layout(
        height=400,
        xaxis_title="Revenue Total (USD)",
        yaxis_title="",
        xaxis=dict(tickformat='$,.0f'),
        yaxis={'categoryorder':'total ascending'}  # ✅ Mayor arriba
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de clientes
    st.markdown("#### 📋 Detalle de Clientes")
    df_clients['Revenue'] = df_clients['Revenue'].apply(lambda x: f"${x:,.0f}")
    st.dataframe(df_clients, use_container_width=True, hide_index=True)

# =============================================================================
# PÁGINA: PROYECCIONES
# =============================================================================

elif page == "💵 Proyecciones":
    st.markdown("## 💵 Proyecciones de Flujo de Efectivo")
    
    st.info("📊 **Nota:** Estas son proyecciones basadas en datos históricos y factores estacionales")
    
    # Parámetros
    col1, col2 = st.columns(2)
    
    with col1:
        meses = st.slider("Meses a proyectar:", 1, 12, 3)
    
    with col2:
        escenario = st.selectbox("Escenario:", ["Conservador", "Moderado", "Optimista"])
    
    # Ajustar proyecciones según escenario
    if escenario == "Conservador":
        factor = 0.9
    elif escenario == "Moderado":
        factor = 1.0
    else:  # Optimista
        factor = 1.1
    
    # Datos de proyección
    df_proj = pd.DataFrame({
        'mes': [f'Mes {i+1}' for i in range(meses)],
        'ingresos': [(180000 + (i * 5000)) * factor for i in range(meses)],
        'gastos': [87000] * meses
    })
    df_proj['flujo_neto'] = df_proj['ingresos'] - df_proj['gastos']
    
    # Gráfico de proyección
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Ingresos', x=df_proj['mes'], y=df_proj['ingresos'],
                         marker_color='#10B981'))
    fig.add_trace(go.Bar(name='Gastos', x=df_proj['mes'], y=df_proj['gastos'],
                         marker_color='#EF4444'))
    fig.add_trace(go.Scatter(name='Flujo Neto', x=df_proj['mes'], y=df_proj['flujo_neto'],
                            mode='lines+markers', line=dict(color='#2563EB', width=3),
                            marker=dict(size=10)))
    
    fig.update_layout(
        title=f'Proyección de Flujo de Efectivo - Escenario {escenario}',
        xaxis_title='Período',
        yaxis_title='Monto (USD)',
        yaxis=dict(tickformat='$,.0f'),
        height=500,
        barmode='group',
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de proyección
    st.markdown("### 📋 Detalle de Proyección")
    df_display = df_proj.copy()
    df_display['ingresos'] = df_display['ingresos'].apply(lambda x: f"${x:,.0f}")
    df_display['gastos'] = df_display['gastos'].apply(lambda x: f"${x:,.0f}")
    df_display['flujo_neto'] = df_display['flujo_neto'].apply(lambda x: f"${x:,.0f}")
    df_display.columns = ['Mes', 'Ingresos Proyectados', 'Gastos Proyectados', 'Flujo Neto']
    st.dataframe(df_display, use_container_width=True, hide_index=True)

# =============================================================================
# PÁGINA: REPORTES DETALLADOS
# =============================================================================

elif page == "📊 Reportes Detallados":
    st.markdown("## 📊 Reportes Detallados")
    
    tabs = st.tabs(["📈 Estacionalidad", "🔥 Burn Rate", "💰 Balance"])
    
    with tabs[0]:
        st.markdown("### 📅 Análisis de Estacionalidad")
        
        df_seasonal = get_seasonal_factors()
        
        # ✅ MEJORA 7: Radar con enero arriba (12 en punto)
        fig = go.Figure(data=go.Scatterpolar(
            r=df_seasonal['Factor'],
            theta=df_seasonal['Mes'],
            fill='toself',
            line=dict(color='#2563EB', width=2),
            marker=dict(size=8, color='#2563EB')
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1.5],
                    tickformat='.2f'
                ),
                angularaxis=dict(
                    rotation=90,  # ✅ Rotar para que enero esté arriba
                    direction='clockwise'  # ✅ Sentido horario
                )
            ),
            title='Factores Estacionales por Mes (1.0 = promedio)',
            height=500,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabla de factores
        st.markdown("#### 📋 Factores Estacionales Detallados")
        df_seasonal_display = df_seasonal.copy()
        df_seasonal_display['Interpretación'] = df_seasonal_display['Factor'].apply(
            lambda x: '📈 Alta actividad' if x > 1.1 else ('📉 Baja actividad' if x < 0.9 else '➡️ Normal')
        )
        st.dataframe(df_seasonal_display, use_container_width=True, hide_index=True)
    
    with tabs[1]:
        st.markdown("### 🔥 Análisis de Burn Rate")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Burn Rate Mensual", "$87,089")
        with col2:
            st.metric("Gastos Fijos", "$65,000")
        with col3:
            st.metric("Costos Variables", "$22,089")
        
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
        st.markdown("### 💰 Balance Proyectado")
        
        balance_data = pd.DataFrame({
            'Mes': ['Nov-25', 'Dic-25', 'Ene-26'],
            'Efectivo Inicial': [efectivo_actual, efectivo_actual + 45000, efectivo_actual + 97000],
            'Ingresos': [185000, 192000, 180000],
            'Gastos': [140000, 140000, 142000]
        })
        balance_data['Efectivo Final'] = balance_data['Efectivo Inicial'] + balance_data['Ingresos'] - balance_data['Gastos']
        
        # Gráfico de balance
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=balance_data['Mes'],
            y=balance_data['Efectivo Final'],
            mode='lines+markers',
            name='Efectivo Final',
            line=dict(color='#2563EB', width=3),
            marker=dict(size=10)
        ))
        fig.update_layout(
            title='Evolución del Efectivo Disponible',
            xaxis_title='Mes',
            yaxis_title='Efectivo (USD)',
            yaxis=dict(tickformat='$,.0f'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabla de balance
        st.markdown("#### 📋 Detalle del Balance")
        balance_display = balance_data.copy()
        for col in ['Efectivo Inicial', 'Ingresos', 'Gastos', 'Efectivo Final']:
            balance_display[col] = balance_display[col].apply(lambda x: f"${x:,.0f}")
        st.dataframe(balance_display, use_container_width=True, hide_index=True)

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748B; padding: 2rem 0;'>
    <p><strong>SPT Cash Flow Tool v4.2</strong></p>
    <p>Desarrollado por <a href='https://www.ai-mindnovation.com' target='_blank'>AI-MindNovation</a></p>
    <p>© 2025 AI-MindNovation. Todos los derechos reservados.</p>
</div>
""", unsafe_allow_html=True)
