import streamlit as st
import numpy as np
import pandas as pd
import math

st.set_page_config(
    page_title="Plataforma UCE - Álgebra Lineal & Métodos Numéricos",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; color: #1F4E79; font-weight: 700; text-align: center; margin-bottom: 0px; }
    .author-header { font-size: 1.25rem; color: #0D5C75; font-weight: 600; text-align: center; margin-top: 5px; margin-bottom: 5px; }
    .sub-header { font-size: 1.05rem; color: #595959; text-align: center; margin-bottom: 25px; }
    .stButton>button { font-weight: bold; border-radius: 6px; }
    div[data-testid="stSidebar"] button { text-align: left; margin-bottom: 2px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🏛️ Universidad Central del Ecuador</p>', unsafe_allow_html=True)
st.markdown('<p class="author-header">Autor: MSc. Luis Guerra</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Facultad de Ingeniería y Ciencias Aplicadas — Carrera de Ingeniería Civil<br><b>Plataforma Evaluativa y Generativa de Ejercicios</b></p>', unsafe_allow_html=True)

st.sidebar.title("🏛️ UCE - Ing. Civil")
st.sidebar.markdown("**Autor:** MSc. Luis Guerra")
asignatura = st.sidebar.radio("📚 Seleccione Asignatura:", ["Álgebra Lineal", "Métodos Numéricos"])

def matrix_to_latex(arr):
    if arr.ndim == 1:
        elems = " \\\\ ".join([f"{x:.4f}".rstrip('0').rstrip('.') for x in arr])
        return r"\begin{bmatrix}" + elems + r"\end{bmatrix}"
    lines = []
    for row in arr:
        lines.append(" & ".join([f"{x:.4f}".rstrip('0').rstrip('.') for x in row]))
    return r"\begin{bmatrix}" + " \\\\ ".join(lines) + r"\end{bmatrix}"

def generar_matriz_con_dos_ceros_fuera_diag():
    while True:
        m = np.random.randint(-4, 5, size=(3, 3))
        np.fill_diagonal(m, np.random.randint(1, 5, size=3) * np.random.choice([-1, 1], size=3))
        off_diag_indices = [(0,1), (0,2), (1,0), (1,2), (2,0), (2,1)]
        zeros_idx = np.random.choice(len(off_diag_indices), size=2, replace=False)
        for idx in zeros_idx:
            r, c = off_diag_indices[idx]
            m[r, c] = 0
        if int(round(np.linalg.det(m))) != 0:
            return m.astype(float)

# Función auxiliar para obtener coeficientes del polinomio característico P(λ) = det(A - λI) = -λ³ + c₂λ² + c₁λ + c₀
def calcular_coeficientes_pc(A):
    # det(λI - A) = λ³ - c₂λ² - c₁λ - c₀ => P(λ) = det(A - λI) = -λ³ + c₂λ² + c₁λ + c₀
    c2 = float(np.trace(A))
    c0 = float(np.linalg.det(A))
    # c1 = 1/2 * (tr(A)^2 - tr(A^2)) en la forma det(λI-A) = λ³ - c2 λ² + c1 λ - c0... 
    # Para det(A - λI) = -λ³ + c2 λ² + c1 λ + c0:
    # Coeficiente de λ: c1 = - (M11 + M22 + M33) donde Mii son los menores principales de 2x2.
    m11 = A[1,1]*A[2,2] - A[1,2]*A[2,1]
    m22 = A[0,0]*A[2,2] - A[0,2]*A[2,0]
    m33 = A[0,0]*A[1,1] - A[0,1]*A[1,0]
    c1 = -(m11 + m22 + m33)
    return c2, c1, c0

# ==========================================
# ÁLGEBRA LINEAL
# ==========================================
if asignatura == "Álgebra Lineal":
    temas_al_lista = [
        "Vectores en el Plano",
        "Vectores en el Espacio",
        "Suma de Matrices",
        "Multiplicación de Matrices",
        "Determinantes",
        "Matriz Inversa",
        "Método de Gauss-Jordán",
        "Regla de Cramer",
        "Factorización LU por Doolittle",
        "Método de Gauss-Seidel",
        "Independencia Lineal",
        "Polinomio Característico"
    ]
    
    if "tema_al" not in st.session_state:
        st.session_state.tema_al = temas_al_lista[0]
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Seleccione un Tema:")
    for t in temas_al_lista:
        btn_label = f"👉 {t}" if st.session_state.tema_al == t else t
        if st.sidebar.button(btn_label, key=f"btn_al_{t}", use_container_width=True):
            st.session_state.tema_al = t
            st.rerun()
            
    tema_al = st.session_state.tema_al
    st.markdown(f"## 📐 Álgebra Lineal — {tema_al}")
    
    # 1. Vectores Plano
    if tema_al == "Vectores en el Plano":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "al_v2d_u" not in st.session_state:
            st.session_state.al_v2d_u = np.random.randint(-6, 7, size=2)
            st.session_state.al_v2d_v = np.random.randint(-6, 7, size=2)
            while np.all(st.session_state.al_v2d_v == 0):
                st.session_state.al_v2d_v = np.random.randint(-6, 7, size=2)
            st.rerun()
            
        u = st.session_state.al_v2d_u
        v = st.session_state.al_v2d_v
        
        st.info("💡 **Instrucción:** Dados los vectores en 2D $\\vec{u}$ y $\\vec{v}$, determine el producto punto $\\vec{u} \\cdot \\vec{v}$ y los componentes de la proyección vectorial $\\text{proj}_{\\vec{v}}(\\vec{u})$.")
        st.latex(rf"\vec{{u}} = \begin{{bmatrix}} {u[0]} \\ {u[1]} \end{{bmatrix}}, \quad \vec{{v}} = \begin{{bmatrix}} {v[0]} \\ {v[1]} \end{{bmatrix}}")
        
        p_punto = int(np.dot(u, v))
        proj = (np.dot(u, v) / np.dot(v, v)) * v
        
        r_dot = st.number_input("1. Producto Punto (u · v):", value=0.0, step=1.0)
        c1, c2 = st.columns(2)
        with c1: r_px = st.number_input("2. Proyección Componente X:", value=0.0000, format="%.4f")
        with c2: r_py = st.number_input("3. Proyección Componente Y:", value=0.0000, format="%.4f")
            
        if st.button("Comprobar Respuesta"):
            if int(r_dot) == p_punto and abs(r_px - proj[0]) < 0.05 and abs(r_py - proj[1]) < 0.05:
                st.success(f"¡Respuesta Correcta! 🎉\n- Producto Punto: {p_punto}\n- Proyección: ({proj[0]:.4f}, {proj[1]:.4f})")
            else:
                st.error(f"Respuesta Incorrecta. ❌\n- Producto Punto exacto: {p_punto}\n- Proyección exacta: ({proj[0]:.4f}, {proj[1]:.4f})")

    # 2. Vectores Espacio
    elif tema_al == "Vectores en el Espacio":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "al_v3d_u" not in st.session_state:
            st.session_state.al_v3d_u = np.random.randint(-5, 6, size=3)
            st.session_state.al_v3d_v = np.random.randint(-5, 6, size=3)
            while np.all(st.session_state.al_v3d_v == 0):
                st.session_state.al_v3d_v = np.random.randint(-5, 6, size=3)
            st.rerun()
            
        u = st.session_state.al_v3d_u
        v = st.session_state.al_v3d_v
        
        st.info("💡 **Instrucción:** Dados los vectores en 3D $\\vec{u}$ y $\\vec{v}$, calcule el producto cruz $\\vec{u} \\times \\vec{v}$ y la proyección vectorial $\\text{proj}_{\\vec{v}}(\\vec{u})$.")
        st.latex(rf"\vec{{u}} = \begin{{bmatrix}} {u[0]} \\ {u[1]} \\ {u[2]} \end{{bmatrix}}, \quad \vec{{v}} = \begin{{bmatrix}} {v[0]} \\ {v[1]} \\ {v[2]} \end{{bmatrix}}")
        
        cruz = np.cross(u, v)
        proj = (np.dot(u, v) / np.dot(v, v)) * v
        
        st.write("### 1. Componentes del Producto Cruz $\\vec{u} \\times \\vec{v}$:")
        cx1, cx2, cx3 = st.columns(3)
        with cx1: r_cx = st.number_input("Cruz Componente X:", value=0.0000, format="%.4f", key="cx")
        with cx2: r_cy = st.number_input("Cruz Componente Y:", value=0.0000, format="%.4f", key="cy")
        with cx3: r_cz = st.number_input("Cruz Componente Z:", value=0.0000, format="%.4f", key="cz")
            
        st.write("### 2. Componentes de la Proyección $\\text{proj}_{\\vec{v}}(\\vec{u})$:")
        px1, px2, px3 = st.columns(3)
        with px1: r_px = st.number_input("Proyección Componente X:", value=0.0000, format="%.4f", key="px")
        with px2: r_py = st.number_input("Proyección Componente Y:", value=0.0000, format="%.4f", key="py")
        with px3: r_pz = st.number_input("Proyección Componente Z:", value=0.0000, format="%.4f", key="pz")
        
        if st.button("Comprobar Respuesta"):
            user_cruz = np.array([r_cx, r_cy, r_cz])
            user_proj = np.array([r_px, r_py, r_pz])
            
            ok_cruz = np.allclose(user_cruz, cruz, atol=0.05)
            ok_proj = np.allclose(user_proj, proj, atol=0.05)
            
            if ok_cruz and ok_proj:
                st.success(f"¡Respuesta Correcta! 🎉\n- Producto Cruz exacto: [{cruz[0]}, {cruz[1]}, {cruz[2]}]\n- Proyección exacta: [{proj[0]:.4f}, {proj[1]:.4f}, {proj[2]:.4f}]")
            else:
                st.error(f"Respuesta Incorrecta. ❌\n- Producto Cruz exacto: [{cruz[0]}, {cruz[1]}, {cruz[2]}]\n- Proyección exacta: [{proj[0]:.4f}, {proj[1]:.4f}, {proj[2]:.4f}]")

    # 3. Suma de Matrices
    elif tema_al == "Suma de Matrices":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "al_m_a_sum" not in st.session_state:
            st.session_state.al_m_a_sum = np.random.randint(-5, 6, size=(3, 3))
            st.session_state.al_m_b_sum = np.random.randint(-5, 6, size=(3, 3))
            st.rerun()
            
        A = st.session_state.al_m_a_sum
        B = st.session_state.al_m_b_sum
        
        st.info("💡 **Instrucción:** Dadas las matrices $A$ y $B$ de $3 \\times 3$, ingrese la **matriz respuesta completa** $S = A + B$.")
        st.latex(rf"A = {matrix_to_latex(A)}, \quad B = {matrix_to_latex(B)}")
        
        S = A + B
        user_S = np.zeros((3, 3))
        st.write("### Ingrese los 9 elementos de la Matriz Suma $S$:")
        for i in range(3):
            cols = st.columns(3)
            for j in range(3):
                with cols[j]:
                    user_S[i, j] = st.number_input(f"S[{i+1},{j+1}]", value=0.0, step=1.0, key=f"sum_{i}_{j}")
        
        if st.button("Comprobar Matriz Suma Completa"):
            if np.array_equal(user_S, S):
                st.success(f"¡Excelente! 🎉 Toda la Matriz Suma es correcta:\n{S}")
            else:
                st.error("Incorrecto. ❌ Verifique los elementos ingresados.")
                st.latex(rf"S_{{\text{{exacta}}}} = {matrix_to_latex(S)}")

    # 4. Multiplicación de Matrices
    elif tema_al == "Multiplicación de Matrices":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "al_m_a_mult" not in st.session_state:
            st.session_state.al_m_a_mult = np.random.randint(-4, 5, size=(3, 3))
            st.session_state.al_m_b_mult = np.random.randint(-4, 5, size=(3, 3))
            st.rerun()
            
        A = st.session_state.al_m_a_mult
        B = st.session_state.al_m_b_mult
        
        st.info("💡 **Instrucción:** Dadas las matrices $A$ y $B$ de $3 \\times 3$, ingrese la **matriz producto completa** $P = A \\times B$.")
        st.latex(rf"A = {matrix_to_latex(A)}, \quad B = {matrix_to_latex(B)}")
        
        P = np.dot(A, B)
        user_P = np.zeros((3, 3))
        st.write("### Ingrese los 9 elementos de la Matriz Producto $P$:")
        for i in range(3):
            cols = st.columns(3)
            for j in range(3):
                with cols[j]:
                    user_P[i, j] = st.number_input(f"P[{i+1},{j+1}]", value=0.0, step=1.0, key=f"mult_{i}_{j}")
        
        if st.button("Comprobar Matriz Producto Completa"):
            if np.array_equal(user_P, P):
                st.success(f"¡Excelente! 🎉 Toda la Matriz Producto es correcta:\n{P}")
            else:
                st.error("Incorrecto. ❌ Verifique los elementos ingresados.")
                st.latex(rf"P_{{\text{{exacta}}}} = {matrix_to_latex(P)}")

    # 5. Determinantes
    elif tema_al == "Determinantes":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "al_det4" not in st.session_state:
            st.session_state.al_det4 = np.random.randint(-3, 4, size=(4, 4))
            st.rerun()
            
        M = st.session_state.al_det4
        st.info("💡 **Instrucción:** Calcule el determinante de la matriz $A$ de dimensión $4 \\times 4$.")
        st.latex(rf"A = {matrix_to_latex(M)}")
        
        det_exacto = int(round(np.linalg.det(M)))
        r_det = st.number_input("Valor de det(A):", value=0.0, step=1.0)
        
        if st.button("Comprobar Determinante"):
            if int(r_det) == det_exacto:
                st.success(f"¡Excelente! 🎉 det(A) = {det_exacto}")
            else:
                st.error(f"Incorrecto. ❌ El determinante exacto es {det_exacto}")

    # 6. Matriz Inversa
    elif tema_al == "Matriz Inversa":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "al_inv3" not in st.session_state:
            while True:
                m = np.random.randint(-3, 4, size=(3, 3))
                if int(round(np.linalg.det(m))) != 0:
                    st.session_state.al_inv3 = m
                    break
            st.rerun()
            
        A = st.session_state.al_inv3
        st.info("💡 **Instrucción:** Para la matriz $A$ de $3 \\times 3$, calcule su matriz inversa $A^{-1}$ e ingrese los 9 elementos con 4 decimales.")
        st.latex(rf"A = {matrix_to_latex(A)}")
        
        invA = np.linalg.inv(A)
        user_inv = np.zeros((3, 3))
        st.write("### Ingrese la Matriz Inversa $A^{-1}$ completa:")
        for i in range(3):
            cols = st.columns(3)
            for j in range(3):
                with cols[j]:
                    user_inv[i, j] = st.number_input(f"A⁻¹[{i+1},{j+1}]", value=0.0000, format="%.4f", key=f"inv_{i}_{j}")
        
        if st.button("Comprobar Matriz Inversa Completa"):
            if np.allclose(user_inv, invA, atol=0.05):
                st.success("¡Excelente! 🎉 Toda la Matriz Inversa es correcta.")
                st.latex(rf"A^{{-1}} = {matrix_to_latex(invA)}")
            else:
                st.error("Incorrecto. ❌ Matriz Inversa exacta:")
                st.latex(rf"A^{{-1}} = {matrix_to_latex(invA)}")

    # 7. Gauss-Jordán
    elif tema_al == "Método de Gauss-Jordán":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "al_gj_a" not in st.session_state:
            while True:
                a = np.random.randint(-4, 5, size=(3, 3))
                b = np.random.randint(-10, 11, size=3)
                if int(round(np.linalg.det(a))) != 0:
                    st.session_state.al_gj_a = a
                    st.session_state.al_gj_b = b
                    break
            st.rerun()
            
        A, b = st.session_state.al_gj_a, st.session_state.al_gj_b
        st.info("💡 **Instrucción:** Resuelva el sistema por Gauss-Jordán. Ingrese la matriz resultante de la eliminación gaussiana (triangulada superior con el término independiente en la 4ta columna) y la solución final $(x, y, z)$.")
        st.latex(rf"\begin{{cases}} {A[0,0]}x + {A[0,1]}y + {A[0,2]}z = {b[0]} \\ {A[1,0]}x + {A[1,1]}y + {A[1,2]}z = {b[1]} \\ {A[2,0]}x + {A[2,1]}y + {A[2,2]}z = {b[2]} \end{{cases}}")
        
        Aug = np.column_stack((A.astype(float), b.astype(float)))
        for i in range(3):
            for j in range(i+1, 3):
                factor = Aug[j, i] / Aug[i, i]
                Aug[j, i:] -= factor * Aug[i, i:]
                
        sol = np.linalg.solve(A, b)
        
        st.write("### 1. Ingrese la Matriz Triangulada Superior Aumentada $[U | d]$:")
        user_aug = np.zeros((3, 4))
        for i in range(3):
            cols = st.columns(4)
            for j in range(4):
                with cols[j]:
                    user_aug[i, j] = st.number_input(f"U[{i+1},{j+1}]", value=0.00, format="%.2f", key=f"gj_aug_{i}_{j}")
                    
        st.write("### 2. Ingrese las Respuestas del Sistema $(x, y, z)$:")
        c1, c2, c3 = st.columns(3)
        with c1: rx = st.number_input("x:", value=0.00, format="%.2f", key="gj_rx")
        with c2: ry = st.number_input("y:", value=0.00, format="%.2f", key="gj_ry")
        with c3: rz = st.number_input("z:", value=0.00, format="%.2f", key="gj_rz")
        
        if st.button("Comprobar Gauss-Jordán"):
            ok_mat = np.allclose(user_aug, Aug, atol=0.1)
            ok_res = np.allclose([rx, ry, rz], sol, atol=0.1)
            if ok_mat and ok_res:
                st.success(f"¡Excelente! 🎉 Matriz triangulada y solución (x={sol[0]:.2f}, y={sol[1]:.2f}, z={sol[2]:.2f}) correctas.")
            else:
                st.error("Incorrecto. ❌ Revisa la matriz triangulada o las respuestas:")
                st.latex(rf"[U | d] = {matrix_to_latex(Aug)}")
                st.write(f"Solución exacta: x = {sol[0]:.2f}, y = {sol[1]:.2f}, z = {sol[2]:.2f}")

    # 8. Regla de Cramer
    elif tema_al == "Regla de Cramer":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "al_cr_a" not in st.session_state:
            while True:
                a = np.random.randint(-4, 5, size=(3, 3))
                b = np.random.randint(-10, 11, size=3)
                det = int(round(np.linalg.det(a)))
                if det != 0:
                    st.session_state.al_cr_a = a
                    st.session_state.al_cr_b = b
                    break
            st.rerun()
            
        A, b = st.session_state.al_cr_a, st.session_state.al_cr_b
        st.info("💡 **Instrucción:** Resuelva el sistema mediante Regla de Cramer. Determine $\\Delta$ y la incógnita $y = \\frac{\\Delta_y}{\\Delta}$.")
        st.latex(rf"\begin{{cases}} {A[0,0]}x + {A[0,1]}y + {A[0,2]}z = {b[0]} \\ {A[1,0]}x + {A[1,1]}y + {A[1,2]}z = {b[1]} \\ {A[2,0]}x + {A[2,1]}y + {A[2,2]}z = {b[2]} \end{{cases}}")
        
        det_sys = int(round(np.linalg.det(A)))
        sol = np.linalg.solve(A, b)
        
        r_det = st.number_input("Determinante del Sistema (Δ):", value=0.0, step=1.0)
        r_y = st.number_input("Valor de y:", value=0.00, format="%.2f")
        
        if st.button("Comprobar Regla de Cramer"):
            if int(r_det) == det_sys and abs(r_y - sol[1]) < 0.1:
                st.success(f"¡Correcto! 🎉 Δ = {det_sys}, y = {sol[1]:.2f}")
            else:
                st.error(f"Incorrecto. ❌ Valores exactos: Δ = {det_sys}, y = {sol[1]:.2f}")

    # 9. Factorización LU por Doolittle
    elif tema_al == "Factorización LU por Doolittle":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "al_doolittle_a" not in st.session_state:
            while True:
                m = np.random.randint(1, 5, size=(3, 3))
                b = np.random.randint(-10, 11, size=3)
                if int(round(np.linalg.det(m))) != 0 and m[0,0] != 0:
                    st.session_state.al_doolittle_a = m.astype(float)
                    st.session_state.al_doolittle_b = b.astype(float)
                    break
            st.rerun()
            
        A = st.session_state.al_doolittle_a
        b = st.session_state.al_doolittle_b
        st.info("💡 **Instrucción:** En la Factorización LU por Doolittle ($A = L \\cdot U$), donde la diagonal de $L$ tiene unos ($L_{i,i} = 1$), ingrese las matrices $L$ y $U$ completas y la solución $(x, y, z)$.")
        st.latex(rf"A = {matrix_to_latex(A)}, \quad b = {matrix_to_latex(b)}")
        
        L = np.eye(3)
        U = A.copy()
        for i in range(3):
            for j in range(i+1, 3):
                factor = U[j, i] / U[i, i]
                L[j, i] = factor
                U[j, i:] -= factor * U[i, i:]
                
        sol = np.linalg.solve(A, b)
        
        st.write("### 1. Ingrese la Matriz L (Doolittle):")
        user_L = np.zeros((3, 3))
        for i in range(3):
            cols = st.columns(3)
            for j in range(3):
                with cols[j]:
                    user_L[i, j] = st.number_input(f"L[{i+1},{j+1}]", value=0.00, format="%.2f", key=f"dool_L_{i}_{j}")
                    
        st.write("### 2. Ingrese la Matriz U (Doolittle):")
        user_U = np.zeros((3, 3))
        for i in range(3):
            cols = st.columns(3)
            for j in range(3):
                with cols[j]:
                    user_U[i, j] = st.number_input(f"U[{i+1},{j+1}]", value=0.00, format="%.2f", key=f"dool_U_{i}_{j}")
                    
        st.write("### 3. Ingrese las Respuestas del Sistema $(x, y, z)$:")
        c1, c2, c3 = st.columns(3)
        with c1: rx = st.number_input("x:", value=0.00, format="%.2f", key="dool_rx")
        with c2: ry = st.number_input("y:", value=0.00, format="%.2f", key="dool_ry")
        with c3: rz = st.number_input("z:", value=0.00, format="%.2f", key="dool_rz")
        
        if st.button("Verificar Doolittle LU y Respuestas"):
            ok_L = np.allclose(user_L, L, atol=0.1)
            ok_U = np.allclose(user_U, U, atol=0.1)
            ok_sol = np.allclose([rx, ry, rz], sol, atol=0.1)
            if ok_L and ok_U and ok_sol:
                st.success("¡Excelente! 🎉 Descomposición Doolittle L, U y respuestas totalmente correctas.")
            else:
                st.error("Incorrecto. ❌ Matrices exactas y solución:")
                st.latex(rf"L = {matrix_to_latex(L)}, \quad U = {matrix_to_latex(U)}")
                st.write(f"Solución exacta: x = {sol[0]:.2f}, y = {sol[1]:.2f}, z = {sol[2]:.2f}")

    # 10. Gauss-Seidel
    elif tema_al == "Método de Gauss-Seidel":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "al_gs3_a" not in st.session_state:
            st.session_state.al_gs3_a = np.array([[12, -2, 1], [-1, 10, -2], [2, -1, 11]], dtype=float)
            st.session_state.al_gs3_b = np.random.randint(-15, 16, size=3).astype(float)
            st.rerun()
            
        A, b = st.session_state.al_gs3_a, st.session_state.al_gs3_b
        st.info("💡 **Instrucción:** Partiendo de $(x^{(0)}, y^{(0)}, z^{(0)}) = (0,0,0)$, realice **3 iteraciones** del Método de Gauss-Seidel e ingrese los valores de $(x^{(3)}, y^{(3)}, z^{(3)})$.")
        st.latex(rf"\begin{{cases}} {int(A[0,0])}x {int(A[0,1]):+}y {int(A[0,2]):+}z = {int(b[0])} \\ {int(A[1,0])}x {int(A[1,1]):+}y {int(A[1,2]):+}z = {int(b[1])} \\ {int(A[2,0])}x {int(A[2,1]):+}y {int(A[2,2]):+}z = {int(b[2])} \end{{cases}}")
        
        x_k, y_k, z_k = 0.0, 0.0, 0.0
        for _ in range(3):
            x_k = (b[0] - A[0,1]*y_k - A[0,2]*z_k) / A[0,0]
            y_k = (b[1] - A[1,0]*x_k - A[1,2]*z_k) / A[1,1]
            z_k = (b[2] - A[2,0]*x_k - A[2,1]*y_k) / A[2,2]
            
        c1, c2, c3 = st.columns(3)
        with c1: rx3 = st.number_input("Valor de x^(3):", value=0.0000, format="%.4f")
        with c2: ry3 = st.number_input("Valor de y^(3):", value=0.0000, format="%.4f")
        with c3: rz3 = st.number_input("Valor de z^(3):", value=0.0000, format="%.4f")
        
        if st.button("Comprobar 3ra Iteración de Gauss-Seidel"):
            if abs(rx3 - x_k) < 0.01 and abs(ry3 - y_k) < 0.01 and abs(rz3 - z_k) < 0.01:
                st.success(f"¡Excelente! 🎉 Valores correctos en la 3ra iteración: x^(3) = {x_k:.4f}, y^(3) = {y_k:.4f}, z^(3) = {z_k:.4f}")
            else:
                st.error(f"Incorrecto. ❌ Valores exactos en la 3ra iteración: x^(3) = {x_k:.4f}, y^(3) = {y_k:.4f}, z^(3) = {z_k:.4f}")

    # 11. Independencia Lineal
    elif tema_al == "Independencia Lineal":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "al_ind_v" not in st.session_state:
            st.session_state.al_ind_v = [np.random.randint(-4, 5, size=3) for _ in range(3)]
            st.rerun()
            
        v1, v2, v3 = st.session_state.al_ind_v
        st.info("💡 **Instrucción:** Determine si el conjunto de tres vectores en $\\mathbb{R}^3$ es Linealmente Independiente (LI) o Dependiente (LD).")
        st.latex(rf"\vec{{v}}_1 = \begin{{bmatrix}} {v1[0]} \\ {v1[1]} \\ {v1[2]} \end{{bmatrix}}, \quad \vec{{v}}_2 = \begin{{bmatrix}} {v2[0]} \\ {v2[1]} \\ {v2[2]} \end{{bmatrix}}, \quad \vec{{v}}_3 = \begin{{bmatrix}} {v3[0]} \\ {v3[1]} \\ {v3[2]} \end{{bmatrix}}")
        
        mat = np.column_stack((v1, v2, v3))
        det = round(float(np.linalg.det(mat)), 2)
        es_li = "Linealmente Independiente (LI)" if det != 0 else "Linealmente Dependiente (LD)"
        
        r_li = st.selectbox("¿Es LI o LD?", ["Seleccione...", "Linealmente Independiente (LI)", "Linealmente Dependiente (LD)"])
        
        if st.button("Comprobar Independencia"):
            if r_li == es_li:
                st.success(f"¡Correcto! 🎉 det(M) = {det}. El conjunto es {es_li}.")
            else:
                st.error(f"Incorrecto. ❌ det(M) = {det}. La respuesta correcta es {es_li}.")

    # 12. Polinomio Característico
    else:
        if st.button("🔄 Generar nuevos datos del ejercicio") or "al_pc_mat" not in st.session_state:
            st.session_state.al_pc_mat = generar_matriz_con_dos_ceros_fuera_diag()
            st.rerun()
            
        A = st.session_state.al_pc_mat
        st.info("💡 **Instrucción:** Para la matriz $A$ de $3 \\times 3$, determine el Polinomio Característico completo $P(\\lambda) = -\\lambda^3 + c_2 \\lambda^2 + c_1 \\lambda + c_0 = 0$ (verificando $c_2, c_1, c_0$) y el **autovector normalizado (unitario)** correspondiente al mayor eigenvalor $\\lambda_{\\max}$.")
        st.latex(rf"A = {matrix_to_latex(A)}")
        
        c2, c1, c0 = calcular_coeficientes_pc(A)
        vals, vecs = np.linalg.eig(A)
        
        # Seleccionar mayor eigenvalor real / módulo
        idx_max = np.argmax(np.real(vals))
        lambda_max = float(np.real(vals[idx_max]))
        vec_max = np.real(vecs[:, idx_max])
        vec_max = vec_max / np.linalg.norm(vec_max) # Normalizado unitario
        
        st.write("### 1. Coeficientes del Polinomio Característico $P(\\lambda) = -\\lambda^3 + c_2 \\lambda^2 + c_1 \\lambda + c_0$:")
        cc1, cc2, cc3 = st.columns(3)
        with cc1: r_c2 = st.number_input("Coeficiente c2 (Traza):", value=0.0000, format="%.4f", key="al_pc_c2")
        with cc2: r_c1 = st.number_input("Coeficiente c1:", value=0.0000, format="%.4f", key="al_pc_c1")
        with cc3: r_c0 = st.number_input("Término c0 (Determinante):", value=0.0000, format="%.4f", key="al_pc_c0")
        
        st.write(f"### 2. Eigenvector (Autovector Unitario) del Mayor Eigenvalor (λ_max ≈ {lambda_max:.4f}):")
        ev1, ev2, ev3 = st.columns(3)
        with ev1: r_v1 = st.number_input("v1 (Componente X):", value=0.0000, format="%.4f", key="al_ev1")
        with ev2: r_v2 = st.number_input("v2 (Componente Y):", value=0.0000, format="%.4f", key="al_ev2")
        with ev3: r_v3 = st.number_input("v3 (Componente Z):", value=0.0000, format="%.4f", key="al_ev3")
        
        if st.button("Verificar Polinomio Característico y Eigenvector"):
            ok_c2 = abs(r_c2 - c2) < 0.05
            ok_c1 = abs(r_c1 - c1) < 0.05
            ok_c0 = abs(r_c0 - c0) < 0.05
            
            user_v = np.array([r_v1, r_v2, r_v3])
            ok_v = np.allclose(user_v, vec_max, atol=0.08) or np.allclose(user_v, -vec_max, atol=0.08)
            
            if ok_c2 and ok_c1 and ok_c0 and ok_v:
                st.success(f"¡Verificación Correcta! 🎉\n- Coeficientes: c2 = {c2:.4f}, c1 = {c1:.4f}, c0 = {c0:.4f}\n- Eigenvalor Máximo: λ_max = {lambda_max:.4f}\n- Eigenvector Unitario: [{vec_max[0]:.4f}, {vec_max[1]:.4f}, {vec_max[2]:.4f}]")
            else:
                st.error(f"Incorrecto. ❌ Valores exactos:\n- Coeficientes: c2 = {c2:.4f}, c1 = {c1:.4f}, c0 = {c0:.4f}\n- Eigenvalor Máximo: λ_max = {lambda_max:.4f}\n- Eigenvector Unitario: [{vec_max[0]:.4f}, {vec_max[1]:.4f}, {vec_max[2]:.4f}] (o con signo opuesto)")

# ==========================================
# MÉTODOS NUMÉRICOS
# ==========================================
else:
    temas_mn_lista = [
        "Series Numéricas",
        "Serie de Taylor",
        "Concepto de Errores",
        "Registro de Computadora IEEE 754",
        "Método de Bisección",
        "Método de Falsa Posición",
        "Método de Falsa Posición Modificada",
        "Método de Newton",
        "Método de la Secante",
        "Método de Gauss-Jordán",
        "Descomposición LU",
        "Matriz Inversa",
        "Polinomio Característico",
        "Iteración Matricial",
        "Regresión Lineal",
        "Regresión Cuadrática",
        "Regresión Exponencial",
        "Interpolación Polinómica Única",
        "Sistema No Lineal por Newton-Raphson",
        "Aproximación de Integrales por Simpson",
        "EDO - Método de Euler Modificado",
        "EDO - Método de Taylor",
        "EDO - Runge-Kutta 4to Orden"
    ]
    
    if "tema_mn" not in st.session_state:
        st.session_state.tema_mn = temas_mn_lista[0]
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Seleccione un Tema:")
    for t in temas_mn_lista:
        btn_label = f"👉 {t}" if st.session_state.tema_mn == t else t
        if st.sidebar.button(btn_label, key=f"btn_mn_{t}", use_container_width=True):
            st.session_state.tema_mn = t
            st.rerun()
            
    tema_mn = st.session_state.tema_mn
    st.markdown(f"## 🔢 Métodos Numéricos — {tema_mn}")
    
    # 1. Series numéricas
    if tema_mn == "Series Numéricas":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_s5_deg" not in st.session_state:
            st.session_state.mn_s5_deg = int(np.random.randint(10, 360))
            st.session_state.mn_s5_tipo = str(np.random.choice(["seno", "coseno"]))
            st.rerun()
            
        deg = st.session_state.mn_s5_deg
        tipo = st.session_state.mn_s5_tipo
        rad = math.radians(deg)
        
        st.info(f"💡 **Instrucción:** Dado el ángulo $\\theta = {deg}^\\circ$ (${rad:.4f}$ rad), evalúe los primeros 5 términos (5ta iteración de Maclaurin) de la función **{tipo.upper()}**.")
        
        if tipo == "seno":
            st.latex(rf"\sin(x) \approx x - \frac{{x^3}}{{3!}} + \frac{{x^5}}{{5!}} - \frac{{x^7}}{{7!}} + \frac{{x^9}}{{9!}}")
            s5 = rad - (rad**3)/6.0 + (rad**5)/120.0 - (rad**7)/5040.0 + (rad**9)/362880.0
        else:
            st.latex(rf"\cos(x) \approx 1 - \frac{{x^2}}{{2!}} + \frac{{x^4}}{{4!}} - \frac{{x^6}}{{6!}} + \frac{{x^8}}{{8!}}")
            s5 = 1 - (rad**2)/2.0 + (rad**4)/24.0 - (rad**6)/720.0 + (rad**8)/40320.0
            
        r_s5 = st.number_input(f"Valor aproximado en la 5ta iteración para {tipo}({deg}°):", value=0.0000, format="%.6f")
        
        if st.button("Comprobar Serie (5ta Iteración)"):
            if abs(r_s5 - s5) < 0.0005:
                st.success(f"¡Correcto! 🎉 Valor en la 5ta iteración = {s5:.6f}")
            else:
                st.error(f"Incorrecto. ❌ El valor exacto en la 5ta iteración es {s5:.6f}")

    # 2. Serie de Taylor
    elif tema_mn == "Serie de Taylor":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_tay_func" not in st.session_state:
            st.session_state.mn_tay_func = str(np.random.choice(["ln", "geometrica"]))
            st.session_state.mn_tay_x = round(float(np.random.uniform(0.1, 0.5)), 2)
            st.rerun()
            
        func_tipo = st.session_state.mn_tay_func
        x_val = st.session_state.mn_tay_x
        
        if func_tipo == "ln":
            st.info(f"💡 **Instrucción (Logaritmo Natural):** Evalúe el polinomio de Taylor de 4to grado para $f(x) = \\ln(1+x)$ en $x = {x_val}$.")
            st.latex(rf"P_4(x) = x - \frac{{x^2}}{{2}} + \frac{{x^3}}{{3}} - \frac{{x^4}}{{4}}")
            p4 = x_val - (x_val**2)/2.0 + (x_val**3)/3.0 - (x_val**4)/4.0
        else:
            st.info(f"💡 **Instrucción (Serie Geométrica):** Evalúe la serie geométrica de 4to grado para $f(x) = \\frac{{1}}{{1-x}}$ en $x = {x_val}$.")
            st.latex(rf"P_4(x) = 1 + x + x^2 + x^3 + x^4")
            p4 = 1 + x_val + x_val**2 + x_val**3 + x_val**4
            
        r_p4 = st.number_input(f"Valor aproximado P4({x_val}):", value=0.0000, format="%.4f")
        if st.button("Comprobar Serie de Taylor"):
            if abs(r_p4 - p4) < 0.001:
                st.success(f"¡Correcto! 🎉 P4({x_val}) = {p4:.4f}")
            else:
                st.error(f"Incorrecto. ❌ El valor exacto es {p4:.4f}")

    # 3. Errores
    elif tema_mn == "Concepto de Errores":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_err_v" not in st.session_state:
            st.session_state.mn_err_v = round(float(np.random.uniform(15.0, 45.0)), 2)
            st.session_state.mn_err_ap = round(st.session_state.mn_err_v + float(np.random.uniform(-1.5, 1.5)), 2)
            st.rerun()
        vt, va = st.session_state.mn_err_v, st.session_state.mn_err_ap
        st.info(f"💡 **Instrucción:** Dado $V_{{\\text{{verdadero}}}} = {vt}$ y $V_{{\\text{{aprox}}}} = {va}$, calcule el Error Absoluto y el Error Relativo Porcentual.")
        st.latex(rf"E_a = |V - V_{{\text{{ap}}}}|, \quad E_r = \frac{{|V - V_{{\text{{ap}}}}|}}{{V}} \times 100\%")
        
        ea = abs(vt - va)
        er = (ea / vt) * 100
        
        r_ea = st.number_input("Error Absoluto (Ea):", value=0.0000, format="%.4f")
        r_er = st.number_input("Error Relativo Porcentual (% Er):", value=0.0000, format="%.4f")
        
        if st.button("Comprobar Errores"):
            if abs(r_ea - ea) < 0.01 and abs(r_er - er) < 0.05:
                st.success(f"¡Correcto! 🎉 Ea = {ea:.4f}, Er = {er:.4f}%")
            else:
                st.error(f"Incorrecto. ❌ Ea = {ea:.4f}, Er = {er:.4f}%")

    # 4. IEEE 754
    elif tema_mn == "Registro de Computadora IEEE 754":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_ieee_val" not in st.session_state:
            st.session_state.mn_ieee_val = float(np.random.choice([-12.5, 6.25, -0.75, 18.5, 4.125]))
            st.rerun()
        v = st.session_state.mn_ieee_val
        st.info(f"💡 **Instrucción:** Para el número decimal **{v}**, indique el bit de signo (1=negativo, 0=positivo) y el exponente sesgado $E = e + 127$ (IEEE 754).")
        
        signo = 1 if v < 0 else 0
        exp_bias = math.floor(math.log2(abs(v))) + 127
        
        r_s = st.selectbox("Bit de Signo:", [0, 1])
        r_exp = st.number_input("Exponente sesgado E (base 10):", value=0, step=1)
        
        if st.button("Comprobar Registro IEEE 754"):
            if r_s == signo and r_exp == exp_bias:
                st.success(f"¡Excelente! 🎉 Signo = {signo}, Exponente Sesgado E = {exp_bias}")
            else:
                st.error(f"Incorrecto. ❌ Signo = {signo}, Exponente Sesgado E = {exp_bias}")

    # 5. Bisección
    elif tema_mn == "Método de Bisección":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_bis_k" not in st.session_state:
            st.session_state.mn_bis_k = int(np.random.randint(1, 5))
            st.rerun()
        k = st.session_state.mn_bis_k
        st.info(f"💡 **Instrucción (Ecuación Mixta Polinómica-Trigonométrica):** Para $f(x) = x^3 - \\cos(x) - {k} = 0$ en $[0, 2]$, calcule las **3 primeras aproximaciones del punto medio** ($x_{{r1}}, x_{{r2}}, x_{{r3}}$) con 4 decimales.")
        st.latex(rf"f(x) = x^3 - \cos(x) - {k} = 0")
        
        def f_bis(x):
            return x**3 - math.cos(x) - k
            
        xl, xu = 0.0, 2.0
        xr_vals = []
        for _ in range(3):
            xr = (xl + xu) / 2.0
            xr_vals.append(xr)
            fl = f_bis(xl)
            fr = f_bis(xr)
            if fl * fr < 0:
                xu = xr
            else:
                xl = xr
                
        c1, c2, c3 = st.columns(3)
        with c1: rx1 = st.number_input("xr1 (1ra Iteración):", value=0.0000, format="%.4f")
        with c2: rx2 = st.number_input("xr2 (2da Iteración):", value=0.0000, format="%.4f")
        with c3: rx3 = st.number_input("xr3 (3ra Iteración):", value=0.0000, format="%.4f")
        
        if st.button("Comprobar 3 Aproximaciones de Bisección"):
            if abs(rx1 - xr_vals[0]) < 0.001 and abs(rx2 - xr_vals[1]) < 0.001 and abs(rx3 - xr_vals[2]) < 0.001:
                st.success(f"¡Correcto! 🎉 xr1={xr_vals[0]:.4f}, xr2={xr_vals[1]:.4f}, xr3={xr_vals[2]:.4f}")
            else:
                st.error(f"Incorrecto. ❌ Valores exactos: xr1={xr_vals[0]:.4f}, xr2={xr_vals[1]:.4f}, xr3={xr_vals[2]:.4f}")

    # 6. Falsa Posición
    elif tema_mn == "Método de Falsa Posición":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_fp_k" not in st.session_state:
            st.session_state.mn_fp_k = int(np.random.randint(1, 5))
            st.rerun()
        k = st.session_state.mn_fp_k
        st.info(f"💡 **Instrucción (Ecuación Mixta Polinómica-Trigonométrica):** Para $f(x) = x^3 - \\sin(x) - {k} = 0$ en $[1, 2]$, calcule las **3 primeras aproximaciones** ($x_{{r1}}, x_{{r2}}, x_{{r3}}$) por Falsa Posición.")
        st.latex(rf"f(x) = x^3 - \sin(x) - {k} = 0")
        
        def f_fp(x):
            return x**3 - math.sin(x) - k
            
        xl, xu = 1.0, 2.0
        xr_vals = []
        for _ in range(3):
            fl = f_fp(xl)
            fu = f_fp(xu)
            xr = xu - (fu * (xl - xu)) / (fl - fu)
            xr_vals.append(xr)
            fr = f_fp(xr)
            if fl * fr < 0:
                xu = xr
            else:
                xl = xr
                
        c1, c2, c3 = st.columns(3)
        with c1: rx1 = st.number_input("xr1 (1ra Iteración):", value=0.0000, format="%.4f", key="fp1")
        with c2: rx2 = st.number_input("xr2 (2da Iteración):", value=0.0000, format="%.4f", key="fp2")
        with c3: rx3 = st.number_input("xr3 (3ra Iteración):", value=0.0000, format="%.4f", key="fp3")
        
        if st.button("Comprobar 3 Aproximaciones de Falsa Posición"):
            if abs(rx1 - xr_vals[0]) < 0.002 and abs(rx2 - xr_vals[1]) < 0.002 and abs(rx3 - xr_vals[2]) < 0.002:
                st.success(f"¡Excelente! 🎉 xr1={xr_vals[0]:.4f}, xr2={xr_vals[1]:.4f}, xr3={xr_vals[2]:.4f}")
            else:
                st.error(f"Incorrecto. ❌ Valores exactos: xr1={xr_vals[0]:.4f}, xr2={xr_vals[1]:.4f}, xr3={xr_vals[2]:.4f}")

    # 7. Falsa Posición Modificada
    elif tema_mn == "Método de Falsa Posición Modificada":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_fpm_k" not in st.session_state:
            st.session_state.mn_fpm_k = int(np.random.randint(1, 5))
            st.rerun()
        k = st.session_state.mn_fpm_k
        st.info(f"💡 **Instrucción (Ecuación Mixta Polinómica-Trigonométrica):** Para $f(x) = x^3 - \\cos(x) - {k} = 0$ en $[0, 2]$, aplique Falsa Posición Modificada y verifique $x_{{r1}}, x_{{r2}}, x_{{r3}}$.")
        st.latex(rf"f(x) = x^3 - \cos(x) - {k} = 0")
        
        def f_fpm(x):
            return x**3 - math.cos(x) - k
            
        xl, xu = 0.0, 2.0
        fl = f_fpm(xl)
        fu = f_fpm(xu)
        xr_vals = []
        l_count, u_count = 0, 0
        for _ in range(3):
            xr = xu - (fu * (xl - xu)) / (fl - fu)
            xr_vals.append(xr)
            fr = f_fpm(xr)
            if fl * fr < 0:
                xu = xr
                fu = fr
                u_count = 0
                l_count += 1
                if l_count >= 2: fl /= 2.0
            else:
                xl = xr
                fl = fr
                l_count = 0
                u_count += 1
                if u_count >= 2: fu /= 2.0
                
        c1, c2, c3 = st.columns(3)
        with c1: rx1 = st.number_input("xr1 (1ra Iteración):", value=0.0000, format="%.4f", key="fpm1")
        with c2: rx2 = st.number_input("xr2 (2da Iteración):", value=0.0000, format="%.4f", key="fpm2")
        with c3: rx3 = st.number_input("xr3 (3ra Iteración):", value=0.0000, format="%.4f", key="fpm3")
        
        if st.button("Comprobar 3 Aproximaciones (Falsa Posición Modificada)"):
            if abs(rx1 - xr_vals[0]) < 0.002 and abs(rx2 - xr_vals[1]) < 0.002 and abs(rx3 - xr_vals[2]) < 0.002:
                st.success(f"¡Excelente! 🎉 xr1={xr_vals[0]:.4f}, xr2={xr_vals[1]:.4f}, xr3={xr_vals[2]:.4f}")
            else:
                st.error(f"Incorrecto. ❌ Valores exactos: xr1={xr_vals[0]:.4f}, xr2={xr_vals[1]:.4f}, xr3={xr_vals[2]:.4f}")

    # 8. Newton
    elif tema_mn == "Método de Newton":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_nw_k" not in st.session_state:
            st.session_state.mn_nw_k = int(np.random.randint(1, 5))
            st.session_state.mn_nw_x0 = round(float(np.random.uniform(1.2, 2.0)), 2)
            st.rerun()
        k = st.session_state.mn_nw_k
        x0 = st.session_state.mn_nw_x0
        st.info(f"💡 **Instrucción (Ecuación Mixta Polinómica-Trigonométrica):** Para $f(x) = x^3 - \\sin(x) - {k} = 0$ partiendo de $x_0 = {x0}$, calcule las **3 primeras iteraciones** de Newton-Raphson ($x_1, x_2, x_3$).")
        st.latex(rf"f(x) = x^3 - \sin(x) - {k} = 0, \quad f'(x) = 3x^2 - \cos(x)")
        
        x_k = x0
        x_vals = []
        for _ in range(3):
            f_k = x_k**3 - math.sin(x_k) - k
            df_k = 3*(x_k**2) - math.cos(x_k)
            x_k = x_k - f_k / df_k
            x_vals.append(x_k)
            
        c1, c2, c3 = st.columns(3)
        with c1: rx1 = st.number_input("x1 (1ra Iteración):", value=0.0000, format="%.4f", key="nw1")
        with c2: rx2 = st.number_input("x2 (2da Iteración):", value=0.0000, format="%.4f", key="nw2")
        with c3: rx3 = st.number_input("x3 (3ra Iteración):", value=0.0000, format="%.4f", key="nw3")
        
        if st.button("Comprobar 3 Aproximaciones de Newton"):
            if abs(rx1 - x_vals[0]) < 0.002 and abs(rx2 - x_vals[1]) < 0.002 and abs(rx3 - x_vals[2]) < 0.002:
                st.success(f"¡Correcto! 🎉 x1={x_vals[0]:.4f}, x2={x_vals[1]:.4f}, x3={x_vals[2]:.4f}")
            else:
                st.error(f"Incorrecto. ❌ Valores exactos: x1={x_vals[0]:.4f}, x2={x_vals[1]:.4f}, x3={x_vals[2]:.4f}")

    # 9. Secante
    elif tema_mn == "Método de la Secante":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_sec_c" not in st.session_state:
            st.session_state.mn_sec_c = int(np.random.randint(1, 5))
            st.rerun()
        c = st.session_state.mn_sec_c
        st.info(f"💡 **Instrucción (Ecuación Mixta Polinómica-Trigonométrica):** Para $f(x) = x^3 - \\cos(x) - {c} = 0$ con puntos iniciales $x_0 = 0.5$ y $x_1 = 1.5$, calcule las **3 primeras iteraciones** ($x_2, x_3, x_4$).")
        st.latex(rf"f(x) = x^3 - \cos(x) - {c} = 0")
        
        def f_sec(x):
            return x**3 - math.cos(x) - c
            
        x0, x1 = 0.5, 1.5
        x_vals = []
        for _ in range(3):
            f0 = f_sec(x0)
            f1 = f_sec(x1)
            x2 = x1 - (f1 * (x0 - x1)) / (f0 - f1)
            x_vals.append(x2)
            x0, x1 = x1, x2
            
        c1, c2, c3 = st.columns(3)
        with c1: rx2 = st.number_input("x2 (1ra Iteración):", value=0.0000, format="%.4f", key="sec1")
        with c2: rx3 = st.number_input("x3 (2da Iteración):", value=0.0000, format="%.4f", key="sec2")
        with c3: rx4 = st.number_input("x4 (3ra Iteración):", value=0.0000, format="%.4f", key="sec3")
        
        if st.button("Comprobar 3 Aproximaciones de la Secante"):
            if abs(rx2 - x_vals[0]) < 0.002 and abs(rx3 - x_vals[1]) < 0.002 and abs(rx4 - x_vals[2]) < 0.002:
                st.success(f"¡Correcto! 🎉 x2={x_vals[0]:.4f}, x3={x_vals[1]:.4f}, x4={x_vals[2]:.4f}")
            else:
                st.error(f"Incorrecto. ❌ Valores exactos: x2={x_vals[0]:.4f}, x3={x_vals[1]:.4f}, x4={x_vals[2]:.4f}")

    # 10. Gauss-Jordán (MN)
    elif tema_mn == "Método de Gauss-Jordán":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_gj_a" not in st.session_state:
            while True:
                a = np.random.randint(-4, 5, size=(3, 3))
                b = np.random.randint(-10, 11, size=3)
                if int(round(np.linalg.det(a))) != 0:
                    st.session_state.mn_gj_a = a
                    st.session_state.mn_gj_b = b
                    break
            st.rerun()
            
        A, b = st.session_state.mn_gj_a, st.session_state.mn_gj_b
        st.info("💡 **Instrucción:** Resuelva el sistema por eliminación gaussiana e ingrese la matriz triangulada superior aumentada $[U | d]$ y las soluciones $(x, y, z)$.")
        st.latex(rf"\begin{{cases}} {A[0,0]}x + {A[0,1]}y + {A[0,2]}z = {b[0]} \\ {A[1,0]}x + {A[1,1]}y + {A[1,2]}z = {b[1]} \\ {A[2,0]}x + {A[2,1]}y + {A[2,2]}z = {b[2]} \end{{cases}}")
        
        Aug = np.column_stack((A.astype(float), b.astype(float)))
        for i in range(3):
            for j in range(i+1, 3):
                factor = Aug[j, i] / Aug[i, i]
                Aug[j, i:] -= factor * Aug[i, i:]
                
        sol = np.linalg.solve(A, b)
        
        st.write("### 1. Ingrese la Matriz Triangulada Superior Aumentada $[U | d]$:")
        user_aug = np.zeros((3, 4))
        for i in range(3):
            cols = st.columns(4)
            for j in range(4):
                with cols[j]:
                    user_aug[i, j] = st.number_input(f"U[{i+1},{j+1}]", value=0.00, format="%.2f", key=f"mn_gj_aug_{i}_{j}")
                    
        st.write("### 2. Ingrese las Respuestas del Sistema $(x, y, z)$:")
        c1, c2, c3 = st.columns(3)
        with c1: rx = st.number_input("x:", value=0.00, format="%.2f", key="mn_gj_rx")
        with c2: ry = st.number_input("y:", value=0.00, format="%.2f", key="mn_gj_ry")
        with c3: rz = st.number_input("z:", value=0.00, format="%.2f", key="mn_gj_rz")
        
        if st.button("Comprobar Gauss-Jordán (MN)"):
            ok_mat = np.allclose(user_aug, Aug, atol=0.1)
            ok_res = np.allclose([rx, ry, rz], sol, atol=0.1)
            if ok_mat and ok_res:
                st.success(f"¡Excelente! 🎉 Matriz triangulada y solución (x={sol[0]:.2f}, y={sol[1]:.2f}, z={sol[2]:.2f}) correctas.")
            else:
                st.error("Incorrecto. ❌ Matriz triangulada exacta y solución:")
                st.latex(rf"[U | d] = {matrix_to_latex(Aug)}")
                st.write(f"Solución exacta: x = {sol[0]:.2f}, y = {sol[1]:.2f}, z = {sol[2]:.2f}")

    # 11. Descomposición LU
    elif tema_mn == "Descomposición LU":
        metodo_lu = st.selectbox("📌 Seleccione Variación de Factorización LU:", ["Doolittle (Diag L = 1)", "Crout (Diag U = 1)"])
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_lu_a" not in st.session_state:
            while True:
                m = np.random.randint(1, 5, size=(3, 3))
                b = np.random.randint(-10, 11, size=3)
                if int(round(np.linalg.det(m))) != 0 and m[0,0] != 0:
                    st.session_state.mn_lu_a = m.astype(float)
                    st.session_state.mn_lu_b = b.astype(float)
                    break
            st.rerun()
            
        A, b = st.session_state.mn_lu_a, st.session_state.mn_lu_b
        st.info(f"💡 **Instrucción:** Halle la Factorización LU por **{metodo_lu}**. Ingrese las matrices $L$, $U$ completas y las respuestas $(x, y, z)$.")
        st.latex(rf"A = {matrix_to_latex(A)}, \quad b = {matrix_to_latex(b)}")
        
        if "Doolittle" in metodo_lu:
            L = np.eye(3)
            U = A.copy()
            for i in range(3):
                for j in range(i+1, 3):
                    factor = U[j, i] / U[i, i]
                    L[j, i] = factor
                    U[j, i:] -= factor * U[i, i:]
        else:
            L = np.zeros((3, 3))
            U = np.eye(3)
            for i in range(3):
                for j in range(i, 3):
                    L[j, i] = A[j, i] - sum(L[j, k] * U[k, i] for k in range(i))
                for j in range(i + 1, 3):
                    U[i, j] = (A[i, j] - sum(L[i, k] * U[k, j] for k in range(i))) / L[i, i]
                    
        sol = np.linalg.solve(A, b)
        
        st.write("### 1. Ingrese la Matriz L:")
        user_L = np.zeros((3, 3))
        for i in range(3):
            cols = st.columns(3)
            for j in range(3):
                with cols[j]:
                    user_L[i, j] = st.number_input(f"L[{i+1},{j+1}]", value=0.00, format="%.2f", key=f"mn_lu_L_{i}_{j}")
                    
        st.write("### 2. Ingrese la Matriz U:")
        user_U = np.zeros((3, 3))
        for i in range(3):
            cols = st.columns(3)
            for j in range(3):
                with cols[j]:
                    user_U[i, j] = st.number_input(f"U[{i+1},{j+1}]", value=0.00, format="%.2f", key=f"mn_lu_U_{i}_{j}")
                    
        st.write("### 3. Ingrese las Respuestas del Sistema $(x, y, z)$:")
        c1, c2, c3 = st.columns(3)
        with c1: rx = st.number_input("x:", value=0.00, format="%.2f", key="mn_lu_rx")
        with c2: ry = st.number_input("y:", value=0.00, format="%.2f", key="mn_lu_ry")
        with c3: rz = st.number_input("z:", value=0.00, format="%.2f", key="mn_lu_rz")
        
        if st.button("Verificar LU y Respuestas (MN)"):
            ok_L = np.allclose(user_L, L, atol=0.1)
            ok_U = np.allclose(user_U, U, atol=0.1)
            ok_sol = np.allclose([rx, ry, rz], sol, atol=0.1)
            if ok_L and ok_U and ok_sol:
                st.success("¡Excelente! 🎉 Matrices L, U y solución verificadas con éxito.")
            else:
                st.error("Incorrecto. ❌ Matrices exactas y solución:")
                st.latex(rf"L = {matrix_to_latex(L)}, \quad U = {matrix_to_latex(U)}")
                st.write(f"Solución exacta: x = {sol[0]:.2f}, y = {sol[1]:.2f}, z = {sol[2]:.2f}")

    # 12. Inversión Matriz 3x3 (MN)
    elif tema_mn == "Matriz Inversa":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_inv3" not in st.session_state:
            while True:
                m = np.random.randint(-3, 4, size=(3, 3))
                if int(round(np.linalg.det(m))) != 0:
                    st.session_state.mn_inv3 = m
                    break
            st.rerun()
            
        A = st.session_state.mn_inv3
        st.info("💡 **Instrucción:** Halle la matriz inversa $A^{-1}$ completa para la matriz $A$ de $3 \\times 3$.")
        st.latex(rf"A = {matrix_to_latex(A)}")
        
        invA = np.linalg.inv(A)
        user_inv = np.zeros((3, 3))
        st.write("### Ingrese la Matriz Inversa $A^{-1}$ completa:")
        for i in range(3):
            cols = st.columns(3)
            for j in range(3):
                with cols[j]:
                    user_inv[i, j] = st.number_input(f"A⁻¹[{i+1},{j+1}]", value=0.0000, format="%.4f", key=f"mn_inv_{i}_{j}")
        
        if st.button("Comprobar Matriz Inversa Completa (MN)"):
            if np.allclose(user_inv, invA, atol=0.05):
                st.success("¡Excelente! 🎉 Toda la Matriz Inversa es correcta.")
                st.latex(rf"A^{{-1}} = {matrix_to_latex(invA)}")
            else:
                st.error("Incorrecto. ❌ Matriz Inversa exacta:")
                st.latex(rf"A^{{-1}} = {matrix_to_latex(invA)}")

    # 13. Polinomio Característico (MN)
    elif tema_mn == "Polinomio Característico":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_pc_m" not in st.session_state:
            st.session_state.mn_pc_m = generar_matriz_con_dos_ceros_fuera_diag()
            st.rerun()
            
        A = st.session_state.mn_pc_m
        st.info("💡 **Instrucción:** Para la matriz $A$ de $3 \\times 3$, determine todos los coeficientes del Polinomio Característico $P(\\lambda) = -\\lambda^3 + c_2 \\lambda^2 + c_1 \\lambda + c_0 = 0$ y el **autovector normalizado (unitario)** correspondiente al mayor eigenvalor $\\lambda_{\\max}$.")
        st.latex(rf"A = {matrix_to_latex(A)}")
        
        c2, c1, c0 = calcular_coeficientes_pc(A)
        vals, vecs = np.linalg.eig(A)
        
        idx_max = np.argmax(np.real(vals))
        lambda_max = float(np.real(vals[idx_max]))
        vec_max = np.real(vecs[:, idx_max])
        vec_max = vec_max / np.linalg.norm(vec_max)
        
        st.write("### 1. Coeficientes del Polinomio Característico $P(\\lambda) = -\\lambda^3 + c_2 \\lambda^2 + c_1 \\lambda + c_0$:")
        cc1, cc2, cc3 = st.columns(3)
        with cc1: r_c2 = st.number_input("Coeficiente c2 (Traza):", value=0.0000, format="%.4f", key="mn_pc_c2")
        with cc2: r_c1 = st.number_input("Coeficiente c1:", value=0.0000, format="%.4f", key="mn_pc_c1")
        with cc3: r_c0 = st.number_input("Término c0 (Determinante):", value=0.0000, format="%.4f", key="mn_pc_c0")
        
        st.write(f"### 2. Eigenvector (Autovector Unitario) del Mayor Eigenvalor (λ_max ≈ {lambda_max:.4f}):")
        ev1, ev2, ev3 = st.columns(3)
        with ev1: r_v1 = st.number_input("v1 (Componente X):", value=0.0000, format="%.4f", key="mn_ev1")
        with ev2: r_v2 = st.number_input("v2 (Componente Y):", value=0.0000, format="%.4f", key="mn_ev2")
        with ev3: r_v3 = st.number_input("v3 (Componente Z):", value=0.0000, format="%.4f", key="mn_ev3")
        
        if st.button("Verificar Polinomio Característico y Eigenvector (MN)"):
            ok_c2 = abs(r_c2 - c2) < 0.05
            ok_c1 = abs(r_c1 - c1) < 0.05
            ok_c0 = abs(r_c0 - c0) < 0.05
            
            user_v = np.array([r_v1, r_v2, r_v3])
            ok_v = np.allclose(user_v, vec_max, atol=0.08) or np.allclose(user_v, -vec_max, atol=0.08)
            
            if ok_c2 and ok_c1 and ok_c0 and ok_v:
                st.success(f"¡Verificación Correcta! 🎉\n- Coeficientes: c2 = {c2:.4f}, c1 = {c1:.4f}, c0 = {c0:.4f}\n- Eigenvalor Máximo: λ_max = {lambda_max:.4f}\n- Eigenvector Unitario: [{vec_max[0]:.4f}, {vec_max[1]:.4f}, {vec_max[2]:.4f}]")
            else:
                st.error(f"Incorrecto. ❌ Valores exactos:\n- Coeficientes: c2 = {c2:.4f}, c1 = {c1:.4f}, c0 = {c0:.4f}\n- Eigenvalor Máximo: λ_max = {lambda_max:.4f}\n- Eigenvector Unitario: [{vec_max[0]:.4f}, {vec_max[1]:.4f}, {vec_max[2]:.4f}] (o con signo opuesto)")

    # 14. Iteración Matricial 5x5
    elif tema_mn == "Iteración Matricial":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_pot5" not in st.session_state:
            m = np.random.randint(1, 4, size=(5, 5))
            st.session_state.mn_pot5 = (m + m.T).astype(float)
            st.rerun()
            
        A = st.session_state.mn_pot5
        st.info("💡 **Instrucción:** Para $X^{(0)} = [1, 1, 1, 1, 1]^T$, calcule $Y^{(1)} = A \\cdot X^{(0)}$ e ingrese su componente máximo.")
        st.latex(rf"A = {matrix_to_latex(A)}")
        
        x0 = np.ones(5)
        y1 = np.dot(A, x0)
        max_y1 = max(y1, key=abs)
        
        r_m = st.number_input("Valor máximo de Y^(1):", value=0.00, format="%.2f")
        if st.button("Comprobar Iteración Matricial"):
            if abs(r_m - max_y1) < 0.1:
                st.success(f"¡Excelente! 🎉 Factor máximo = {max_y1:.2f}\n Y^(1) = {list(y1)}")
            else:
                st.error(f"Incorrecto. ❌ Valor máximo exacto = {max_y1:.2f}")

    # 15. Regresión Lineal
    elif tema_mn == "Regresión Lineal":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_reg_x" not in st.session_state:
            st.session_state.mn_reg_x = np.array([1, 2, 3, 4, 5], dtype=float)
            st.session_state.mn_reg_y = np.array([2.1, 3.8, 6.2, 7.9, 10.1], dtype=float) + np.random.uniform(-0.3, 0.3, size=5)
            st.rerun()
            
        x, y = st.session_state.mn_reg_x, st.session_state.mn_reg_y
        st.info("💡 **Instrucción:** Ajuste el modelo de Regresión Lineal $y = a_1 x + a_0$ e ingrese **ambos coeficientes** ($a_1$ y $a_0$) con 4 decimales.")
        st.dataframe(pd.DataFrame({"x": x, "y": y}), use_container_width=True)
        
        a1, a0 = np.polyfit(x, y, 1)
        c1, c2 = st.columns(2)
        with c1: r_a1 = st.number_input("Pendiente (a1):", value=0.0000, format="%.4f")
        with c2: r_a0 = st.number_input("Intersección / Término Independiente (a0):", value=0.0000, format="%.4f")
        
        if st.button("Verificar Todos los Coeficientes (Regresión Lineal)"):
            ok_a1 = abs(r_a1 - a1) < 0.05
            ok_a0 = abs(r_a0 - a0) < 0.05
            if ok_a1 and ok_a0:
                st.success(f"¡Excelente! 🎉 Todos los coeficientes son correctos:\n- a1 = {a1:.4f}\n- a0 = {a0:.4f}\nEcuación: y = {a1:.4f} x + {a0:.4f}")
            else:
                st.error(f"Incorrecto. ❌ Coeficientes exactos:\n- a1 (Pendiente) = {a1:.4f}\n- a0 (Intersección) = {a0:.4f}")

    # 16. Regresión Cuadrática
    elif tema_mn == "Regresión Cuadrática":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_rc_x" not in st.session_state:
            st.session_state.mn_rc_x = np.array([1, 2, 3, 4, 5], dtype=float)
            st.session_state.mn_rc_y = 0.5 * (st.session_state.mn_rc_x**2) + np.random.uniform(-0.2, 0.2, size=5)
            st.rerun()
            
        x, y = st.session_state.mn_rc_x, st.session_state.mn_rc_y
        st.info("💡 **Instrucción:** Ajuste la parábola de Regresión Cuadrática $y = a_2 x^2 + a_1 x + a_0$ e ingrese **todos los coeficientes** ($a_2, a_1, a_0$) con 4 decimales.")
        st.dataframe(pd.DataFrame({"x": x, "y": y}), use_container_width=True)
        
        a2, a1, a0 = np.polyfit(x, y, 2)
        c1, c2, c3 = st.columns(3)
        with c1: r_a2 = st.number_input("Coeficiente cuadrático (a2):", value=0.0000, format="%.4f")
        with c2: r_a1 = st.number_input("Coeficiente lineal (a1):", value=0.0000, format="%.4f")
        with c3: r_a0 = st.number_input("Término independiente (a0):", value=0.0000, format="%.4f")
        
        if st.button("Verificar Todos los Coeficientes (Regresión Cuadrática)"):
            ok_a2 = abs(r_a2 - a2) < 0.05
            ok_a1 = abs(r_a1 - a1) < 0.05
            ok_a0 = abs(r_a0 - a0) < 0.05
            if ok_a2 and ok_a1 and ok_a0:
                st.success(f"¡Excelente! 🎉 Todos los coeficientes son correctos:\n- a2 = {a2:.4f}\n- a1 = {a1:.4f}\n- a0 = {a0:.4f}\nEcuación: y = {a2:.4f} x² + {a1:.4f} x + {a0:.4f}")
            else:
                st.error(f"Incorrecto. ❌ Coeficientes exactos:\n- a2 = {a2:.4f}\n- a1 = {a1:.4f}\n- a0 = {a0:.4f}")

    # 17. Regresión Exponencial
    elif tema_mn == "Regresión Exponencial":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_re_x" not in st.session_state:
            st.session_state.mn_re_x = np.array([1, 2, 3, 4, 5], dtype=float)
            st.session_state.mn_re_y = 2.0 * np.exp(0.4 * st.session_state.mn_re_x) + np.random.uniform(-0.1, 0.1, size=5)
            st.rerun()
            
        x, y = st.session_state.mn_re_x, st.session_state.mn_re_y
        st.info("💡 **Instrucción:** Ajuste el modelo de Regresión Exponencial $y = A \\cdot e^{B x}$ mediante linealización $\\ln(y) = \\ln(A) + B x$. Ingrese **todos los coeficientes del modelo final** ($A$ y $B$) con 4 decimales.")
        st.dataframe(pd.DataFrame({"x": x, "y": y}), use_container_width=True)
        
        B, lnA = np.polyfit(x, np.log(y), 1)
        A_val = np.exp(lnA)
        
        c1, c2 = st.columns(2)
        with c1: r_A = st.number_input("Coeficiente de Amplitud (A):", value=0.0000, format="%.4f")
        with c2: r_B = st.number_input("Tasa Exponencial (B):", value=0.0000, format="%.4f")
        
        if st.button("Verificar Todos los Coeficientes (Regresión Exponencial)"):
            ok_A = abs(r_A - A_val) < 0.05
            ok_B = abs(r_B - B) < 0.05
            if ok_A and ok_B:
                st.success(f"¡Excelente! 🎉 Todos los coeficientes son correctos:\n- A = {A_val:.4f}\n- B = {B:.4f}\nEcuación: y = {A_val:.4f} · e^({B:.4f} x)")
            else:
                st.error(f"Incorrecto. ❌ Coeficientes exactos:\n- A (Amplitud) = {A_val:.4f}\n- B (Tasa) = {B:.4f}")

    # 18. Interpolación Polinómica Única
    elif tema_mn == "Interpolación Polinómica Única":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_pu5_x" not in st.session_state:
            st.session_state.mn_pu5_x = np.array([0, 1, 2, 3, 4], dtype=float)
            st.session_state.mn_pu5_y = np.array([2, 1, 4, 3, 6], dtype=float) + np.random.randint(-1, 2, size=5)
            st.rerun()
            
        x, y = st.session_state.mn_pu5_x, st.session_state.mn_pu5_y
        st.info("💡 **Instrucción:** Dados los 5 puntos experimentales, determine el único polinomio interpolador de 4to grado: $P_4(x) = a_4 x^4 + a_3 x^3 + a_2 x^2 + a_1 x + a_0$ e ingrese todos sus coeficientes.")
        st.dataframe(pd.DataFrame({"x": x, "y": y}), use_container_width=True)
        
        coeffs = np.polyfit(x, y, 4)
        a4, a3, a2, a1, a0 = coeffs
        
        c1, c2, c3 = st.columns(3)
        with c1: r_a4 = st.number_input("a4 (x^4):", value=0.0000, format="%.4f")
        with c2: r_a3 = st.number_input("a3 (x^3):", value=0.0000, format="%.4f")
        with c3: r_a2 = st.number_input("a2 (x^2):", value=0.0000, format="%.4f")
        
        c4, c5 = st.columns(2)
        with c4: r_a1 = st.number_input("a1 (x^1):", value=0.0000, format="%.4f")
        with c5: r_a0 = st.number_input("a0 (término indep.):", value=0.0000, format="%.4f")
        
        if st.button("Verificar Coeficientes del Polinomio Interpolador"):
            user_coeffs = np.array([r_a4, r_a3, r_a2, r_a1, r_a0])
            if np.allclose(user_coeffs, coeffs, atol=0.05):
                st.success(f"¡Polinomio Verificado! 🎉 P_4(x) = {a4:.4f}x⁴ + {a3:.4f}x³ + {a2:.4f}x² + {a1:.4f}x + {a0:.4f}")
            else:
                st.error(f"Incorrecto. ❌ Coeficientes exactos: a4={a4:.4f}, a3={a3:.4f}, a2={a2:.4f}, a1={a1:.4f}, a0={a0:.4f}")

    # 19. Sistema No Lineal
    elif tema_mn == "Sistema No Lineal por Newton-Raphson":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_nl_c" not in st.session_state:
            st.session_state.mn_nl_c = int(np.random.randint(4, 9))
            st.rerun()
        c = st.session_state.mn_nl_c
        
        st.info("💡 **Instrucción:** Realice 3 iteraciones de Newton-Raphson partiendo de $(x_0, y_0) = (1.5, 1.5)$ y verifique el par $(x_3, y_3)$.")
        st.latex(rf"\begin{{cases}} f_1(x, y) = x^2 + y^2 - {c} = 0 \\ f_2(x, y) = x - y^2 = 0 \end{{cases}}")
        
        x_k, y_k = 1.5, 1.5
        iter_data = []
        for i in range(1, 4):
            f1 = x_k**2 + y_k**2 - c
            f2 = x_k - y_k**2
            J = np.array([[2*x_k, 2*y_k], [1, -2*y_k]])
            F = np.array([f1, f2])
            delta = np.linalg.solve(J, -F)
            x_k += delta[0]
            y_k += delta[1]
            iter_data.append({"Iteración": i, "x": round(x_k, 4), "y": round(y_k, 4), "f1(x,y)": round(x_k**2 + y_k**2 - c, 5), "f2(x,y)": round(x_k - y_k**2, 5)})
            
        c1, c2 = st.columns(2)
        with c1: rx3 = st.number_input("Valor x3 (3ra iteración):", value=0.0000, format="%.4f")
        with c2: ry3 = st.number_input("Valor y3 (3ra iteración):", value=0.0000, format="%.4f")
            
        if st.button("Verificar Par (x, y) en 3ra Iteración"):
            if abs(rx3 - x_k) < 0.05 and abs(ry3 - y_k) < 0.05:
                st.success(f"¡Verificación Correcta! 🎉 Par (x3, y3) = ({x_k:.4f}, {y_k:.4f})")
                st.markdown("**Tabla de Verificación Iterativa:**")
                st.dataframe(pd.DataFrame(iter_data), use_container_width=True)
            else:
                st.error(f"Incorrecto. ❌ En la 3ra iteración el par exacto es (x3, y3) = ({x_k:.4f}, {y_k:.4f})")

    # 20. Simpson (Mixta Polinómica y Trigonométrica)
    elif tema_mn == "Aproximación de Integrales por Simpson":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_simp_k" not in st.session_state:
            st.session_state.mn_simp_k = int(np.random.randint(1, 6))
            st.session_state.mn_simp_n = int(np.random.choice([4, 6, 8]))
            st.rerun()
            
        k_val = st.session_state.mn_simp_k
        n_sub = st.session_state.mn_simp_n
        a_val, b_val = 0.0, 3.0
        h = (b_val - a_val) / n_sub
        
        st.info(f"💡 **Instrucción (Radicando Polinómico-Trigonométrico):** Evalúe la integral $\\int_0^3 \\sqrt{{x^2 + \\cos(x) + {k_val}}} \\, dx$ aplicando la Regla de Simpson 1/3 Compuesta con $n = {n_sub}$ subintervalos ($h = {h:.4f}$).")
        st.latex(rf"\int_0^3 \sqrt{{x^2 + \cos(x) + {k_val}}} \, dx")
        
        f_func = lambda x: np.sqrt(x**2 + np.cos(x) + k_val)
            
        x_pts = np.linspace(a_val, b_val, n_sub + 1)
        f_pts = f_func(x_pts)
        simp_val = (h/3.0) * (f_pts[0] + f_pts[-1] + 4*sum(f_pts[1:-1:2]) + 2*sum(f_pts[2:-1:2]))
        
        r_s = st.number_input("Valor de la integral por Simpson 1/3:", value=0.0000, format="%.4f")
        if st.button("Comprobar Simpson 1/3"):
            if abs(r_s - simp_val) < 0.01:
                st.success(f"¡Excelente! 🎉 Integral por Simpson 1/3 = {simp_val:.4f}")
            else:
                st.error(f"Incorrecto. ❌ El valor exacto por Simpson 1/3 es {simp_val:.4f}")

    # 21. EDO Euler Modificado
    elif tema_mn == "EDO - Método de Euler Modificado":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_eul_params" not in st.session_state:
            st.session_state.mn_eul_params = {
                "h": 0.05,
                "x0": 0.0,
                "y0": round(float(np.random.uniform(0.5, 1.5)), 2)
            }
            st.rerun()
            
        p = st.session_state.mn_eul_params
        h, y0, x0 = p["h"], p["y0"], p["x0"]
        x_target = round(x0 + h, 2)
        
        def f_edo(x, y):
            return 4*x + 5*y - 3*(x**2) + 4*(y**2) - np.exp(2*x)
            
        st.info(f"💡 **Instrucción:** Para la EDO no lineal con condición inicial $y({x0}) = {y0}$ y tamaño de paso $h = {h}$, aplique el Método de Euler Modificado (Heun) para aproximar $y({x_target})$.")
        st.latex(rf"\frac{{dy}}{{dx}} = 4x + 5y - 3x^2 + 4y^2 - e^{{2x}}")
        
        f0 = f_edo(x0, y0)
        y_pred = y0 + h * f0
        f1 = f_edo(x_target, y_pred)
        y1 = y0 + (h/2.0) * (f0 + f1)
        
        r_y1 = st.number_input(f"Valor aproximado de y({x_target}):", value=0.0000, format="%.4f")
        if st.button("Comprobar Euler Modificado"):
            if abs(r_y1 - y1) < 0.005:
                st.success(f"¡Correcto! 🎉 y({x_target}) = {y1:.4f}")
            else:
                st.error(f"Incorrecto. ❌ El valor exacto por Euler Modificado es y({x_target}) = {y1:.4f}")

    # 22. EDO Taylor
    elif tema_mn == "EDO - Método de Taylor":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_tay_params" not in st.session_state:
            st.session_state.mn_tay_params = {
                "h": 0.1,
                "x0": 0.0,
                "y0": round(float(np.random.uniform(0.5, 2.0)), 2)
            }
            st.rerun()
            
        p = st.session_state.mn_tay_params
        h, x0, y0 = p["h"], p["x0"], p["y0"]
        x_target = round(x0 + h, 2)
        
        st.info(f"💡 **Instrucción:** Para la EDO con $y({x0}) = {y0}$ y paso $h = {h}$, aplique el Método de Taylor de Orden 2: $y_1 = y_0 + h y'_0 + \\frac{{h^2}}{{2}} y''_0$ para aproximar $y({x_target})$.")
        st.latex(rf"\frac{{dy}}{{dx}} = 4x + 5y")
        
        yp0 = 4*x0 + 5*y0
        ypp0 = 4 + 5*yp0
        y1 = y0 + h*yp0 + (h**2 / 2.0)*ypp0
        
        r_yt = st.number_input(f"Valor de y({x_target}):", value=0.0000, format="%.4f")
        if st.button("Comprobar Taylor Orden 2"):
            if abs(r_yt - y1) < 0.005:
                st.success(f"¡Excelente! 🎉 y({x_target}) = {y1:.4f}")
            else:
                st.error(f"Incorrecto. ❌ El valor exacto es y({x_target}) = {y1:.4f}")

    # 23. EDO RK4
    else:
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_rk4_params" not in st.session_state:
            st.session_state.mn_rk4_params = {
                "h": 0.05,
                "x0": 0.0,
                "y0": round(float(np.random.uniform(0.5, 1.5)), 2)
            }
            st.rerun()
            
        p = st.session_state.mn_rk4_params
        h, x0, y0 = p["h"], p["x0"], p["y0"]
        x_target = round(x0 + h, 2)
        
        def f_edo(x, y):
            return 4*x + 5*y - 3*(x**2) + 4*(y**2) - np.exp(2*x)
            
        st.info(f"💡 **Instrucción:** Para la EDO no lineal con condición inicial $y({x0}) = {y0}$ y paso $h = {h}$, aplique Runge-Kutta de 4to Orden (RK4) para aproximar $y({x_target})$.")
        st.latex(rf"\frac{{dy}}{{dx}} = 4x + 5y - 3x^2 + 4y^2 - e^{{2x}}")
        
        k1 = f_edo(x0, y0)
        k2 = f_edo(x0 + 0.5*h, y0 + 0.5*h*k1)
        k3 = f_edo(x0 + 0.5*h, y0 + 0.5*h*k2)
        k4 = f_edo(x0 + h, y0 + h*k3)
        
        y1 = y0 + (h/6.0)*(k1 + 2*k2 + 2*k3 + k4)
        
        r_rk4 = st.number_input(f"Valor de y({x_target}):", value=0.0000, format="%.4f")
        if st.button("Comprobar RK4"):
            if abs(r_rk4 - y1) < 0.002:
                st.success(f"¡Excelente! 🎉 y({x_target}) = {y1:.4f}")
            else:
                st.error(f"Incorrecto. ❌ El valor exacto por RK4 es y({x_target}) = {y1:.4f}")
