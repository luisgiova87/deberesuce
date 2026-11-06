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

# ==========================================
# ÁLGEBRA LINEAL
# ==========================================
if asignatura == "Álgebra Lineal":
    st.sidebar.markdown("---")
    tema_al = st.sidebar.selectbox("Seleccione Tema de Álgebra Lineal:", [
        "Vectores en el plano (Punto y Proyecciones)",
        "Vectores en el espacio (Cruz y Proyecciones)",
        "Suma de Matrices (≥ 9 elementos)",
        "Multiplicación de Matrices (≥ 7 elementos)",
        "Determinantes (Tamaño mínimo 4x4)",
        "Cálculo de la Matriz Inversa a través de la Adjunta (≥ 3x3)",
        "Método de Gauss-Jordán (Sistema 3x3)",
        "Regla de Cramer (Sistema 3x3)",
        "Factorización LU por Crout (Sistema 3x3)",
        "Método Gauss-Seidel (Sistema 3x3)",
        "Independencia Lineal (Subespacios)",
        "Método del Polinomio Característico (≥ 3x3)"
    ])
    
    st.markdown(f"## 📐 Álgebra Lineal — {tema_al}")
    
    # 1. Vectores Plano
    if tema_al == "Vectores en el plano (Punto y Proyecciones)":
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
    elif tema_al == "Vectores en el espacio (Cruz y Proyecciones)":
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
    elif tema_al == "Suma de Matrices (≥ 9 elementos)":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "al_m_a_sum" not in st.session_state:
            st.session_state.al_m_a_sum = np.random.randint(-5, 6, size=(3, 3))
            st.session_state.al_m_b_sum = np.random.randint(-5, 6, size=(3, 3))
            st.rerun()
            
        A = st.session_state.al_m_a_sum
        B = st.session_state.al_m_b_sum
        
        st.info("💡 **Instrucción:** Dadas las matrices $A$ y $B$ de $3 \\times 3$, calcule la suma $S = A + B$ e ingrese los elementos indicados.")
        st.latex(rf"A = {matrix_to_latex(A)}, \quad B = {matrix_to_latex(B)}")
        
        S = A + B
        c1, c2 = st.columns(2)
        with c1: r_s11 = st.number_input("Elemento S[1,1]:", value=0.0, step=1.0)
        with c2: r_s33 = st.number_input("Elemento S[3,3]:", value=0.0, step=1.0)
        
        if st.button("Comprobar Suma"):
            if int(r_s11) == S[0,0] and int(r_s33) == S[2,2]:
                st.success(f"¡Correcto! 🎉 Matriz Suma S:\n {S}")
            else:
                st.error(f"Incorrecto. ❌ S[1,1] exacto = {S[0,0]}, S[3,3] exacto = {S[2,2]}")

    # 4. Multiplicación de Matrices
    elif tema_al == "Multiplicación de Matrices (≥ 7 elementos)":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "al_m_a_mult" not in st.session_state:
            st.session_state.al_m_a_mult = np.random.randint(-4, 5, size=(3, 3))
            st.session_state.al_m_b_mult = np.random.randint(-4, 5, size=(3, 3))
            st.rerun()
            
        A = st.session_state.al_m_a_mult
        B = st.session_state.al_m_b_mult
        
        st.info("💡 **Instrucción:** Dadas las matrices $A$ y $B$ de $3 \\times 3$, determine el producto $P = A \\times B$. Ingrese $P_{1,1}$ y $P_{2,3}$.")
        st.latex(rf"A = {matrix_to_latex(A)}, \quad B = {matrix_to_latex(B)}")
        
        P = np.dot(A, B)
        c1, c2 = st.columns(2)
        with c1: r_p11 = st.number_input("Elemento P[1,1]:", value=0.0, step=1.0)
        with c2: r_p23 = st.number_input("Elemento P[2,3]:", value=0.0, step=1.0)
        
        if st.button("Comprobar Multiplicación"):
            if int(r_p11) == P[0,0] and int(r_p23) == P[1,2]:
                st.success(f"¡Excelente! 🎉 Producto P:\n{P}")
            else:
                st.error(f"Incorrecto. ❌ P[1,1] = {P[0,0]}, P[2,3] = {P[1,2]}")

    # 5. Determinantes 4x4
    elif tema_al == "Determinantes (Tamaño mínimo 4x4)":
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
    elif tema_al == "Cálculo de la Matriz Inversa a través de la Adjunta (≥ 3x3)":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "al_inv3" not in st.session_state:
            while True:
                m = np.random.randint(-3, 4, size=(3, 3))
                if int(round(np.linalg.det(m))) != 0:
                    st.session_state.al_inv3 = m
                    break
            st.rerun()
            
        A = st.session_state.al_inv3
        st.info("💡 **Instrucción:** Para la matriz $A$ de $3 \\times 3$, calcule su inversa mediante $A^{-1} = \\frac{1}{\\det(A)} \\text{Adj}(A)$. Ingrese $\\det(A)$ y el elemento $A^{-1}_{1,1}$.")
        st.latex(rf"A = {matrix_to_latex(A)}")
        
        detA = int(round(np.linalg.det(A)))
        invA = np.linalg.inv(A)
        
        c1, c2 = st.columns(2)
        with c1: r_det = st.number_input("Determinante det(A):", value=0.0, step=1.0)
        with c2: r_inv11 = st.number_input("Elemento A^(-1)[1,1]:", value=0.0000, format="%.4f")
        
        if st.button("Comprobar Inversa"):
            if int(r_det) == detA and abs(r_inv11 - invA[0,0]) < 0.05:
                st.success(f"¡Correcto! 🎉 det(A) = {detA}.\n Matriz Inversa A^(-1):\n {invA.round(4)}")
            else:
                st.error(f"Incorrecto. ❌ det(A) = {detA}, A^(-1)[1,1] exacto = {invA[0,0]:.4f}")

    # 7. Gauss-Jordán 3x3
    elif tema_al == "Método de Gauss-Jordán (Sistema 3x3)":
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
        st.info("💡 **Instrucción:** Resuelva el sistema de ecuaciones lineales $3 \\times 3$ por Gauss-Jordán e ingrese $(x, y, z)$.")
        st.latex(rf"\begin{{cases}} {A[0,0]}x + {A[0,1]}y + {A[0,2]}z = {b[0]} \\ {A[1,0]}x + {A[1,1]}y + {A[1,2]}z = {b[1]} \\ {A[2,0]}x + {A[2,1]}y + {A[2,2]}z = {b[2]} \end{{cases}}")
        
        sol = np.linalg.solve(A, b)
        c1, c2, c3 = st.columns(3)
        with c1: rx = st.number_input("Valor de x:", value=0.00, format="%.2f")
        with c2: ry = st.number_input("Valor de y:", value=0.00, format="%.2f")
        with c3: rz = st.number_input("Valor de z:", value=0.00, format="%.2f")
        
        if st.button("Comprobar Gauss-Jordán"):
            if abs(rx - sol[0]) < 0.1 and abs(ry - sol[1]) < 0.1 and abs(rz - sol[2]) < 0.1:
                st.success(f"¡Excelente! 🎉 Solución: x = {sol[0]:.2f}, y = {sol[1]:.2f}, z = {sol[2]:.2f}")
            else:
                st.error(f"Incorrecto. ❌ Solución exacta: x = {sol[0]:.2f}, y = {sol[1]:.2f}, z = {sol[2]:.2f}")

    # 8. Regla de Cramer 3x3
    elif tema_al == "Regla de Cramer (Sistema 3x3)":
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

    # 9. Factorización LU por Crout
    elif tema_al == "Factorización LU por Crout (Sistema 3x3)":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "al_crout_a" not in st.session_state:
            while True:
                m = np.random.randint(1, 5, size=(3, 3))
                if int(round(np.linalg.det(m))) != 0 and m[0,0] != 0:
                    st.session_state.al_crout_a = m.astype(float)
                    break
            st.rerun()
            
        A = st.session_state.al_crout_a
        st.info("💡 **Instrucción:** En la Factorización LU de Crout ($A = L \\cdot U$), donde la diagonal de $U$ son unos ($U_{i,i} = 1$), verifique las matrices $L$ y $U$ e ingrese $L_{2,1}$ y $U_{1,2}$.")
        st.latex(rf"A = {matrix_to_latex(A)}")
        
        L = np.zeros((3, 3))
        U = np.eye(3)
        for i in range(3):
            for j in range(i, 3):
                L[j, i] = A[j, i] - sum(L[j, k] * U[k, i] for k in range(i))
            for j in range(i + 1, 3):
                U[i, j] = (A[i, j] - sum(L[i, k] * U[k, j] for k in range(i))) / L[i, i]
                
        r_l21 = st.number_input("Elemento L[2,1] (L_21):", value=0.00, format="%.2f")
        r_u12 = st.number_input("Elemento U[1,2] (U_12):", value=0.00, format="%.2f")
        
        if st.button("Verificar Crout LU"):
            if abs(r_l21 - L[1,0]) < 0.1 and abs(r_u12 - U[0,1]) < 0.1:
                st.success("¡Excelente! 🎉 Descomposición Crout Verificada.")
                st.latex(rf"L = {matrix_to_latex(L)}, \quad U = {matrix_to_latex(U)}")
            else:
                st.error(f"Incorrecto. ❌ Valores exactos: L_21 = {L[1,0]:.2f}, U_12 = {U[0,1]:.2f}")
                st.latex(rf"L = {matrix_to_latex(L)}, \quad U = {matrix_to_latex(U)}")

    # 10. Gauss-Seidel 3x3
    elif tema_al == "Método Gauss-Seidel (Sistema 3x3)":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "al_gs_a" not in st.session_state:
            st.session_state.al_gs_a = np.array([[12, -2, 1], [-1, 10, -2], [2, -1, 11]], dtype=float)
            st.session_state.al_gs_b = np.random.randint(-15, 16, size=3).astype(float)
            st.rerun()
            
        A, b = st.session_state.al_gs_a, st.session_state.al_gs_b
        st.info("💡 **Instrucción:** Verifique la condición de diagonal dominante. Partiendo de $(x^{(0)}, y^{(0)}, z^{(0)}) = (0,0,0)$, calcule $x^{(1)}$ en la primera iteración.")
        st.latex(rf"\begin{{cases}} {int(A[0,0])}x {int(A[0,1]):+}y {int(A[0,2]):+}z = {int(b[0])} \\ {int(A[1,0])}x {int(A[1,1]):+}y {int(A[1,2]):+}z = {int(b[1])} \\ {int(A[2,0])}x {int(A[2,1]):+}y {int(A[2,2]):+}z = {int(b[2])} \end{{cases}}")
        
        x1 = (b[0] - A[0,1]*0 - A[0,2]*0) / A[0,0]
        r_x1 = st.number_input("Valor de x^(1):", value=0.0000, format="%.4f")
        
        if st.button("Comprobar Gauss-Seidel"):
            if abs(r_x1 - x1) < 0.01:
                st.success(f"¡Excelente! 🎉 El sistema es convergente. x^(1) = {x1:.4f}")
            else:
                st.error(f"Incorrecto. ❌ El valor exacto de x^(1) es {x1:.4f}")

    # 11. Independencia Lineal
    elif tema_al == "Independencia Lineal (Subespacios)":
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
            m = np.random.randint(-2, 3, size=(3, 3))
            st.session_state.al_pc_mat = (m + m.T).astype(float)
            st.rerun()
            
        A = st.session_state.al_pc_mat
        st.info("💡 **Instrucción:** Para la matriz simétrica $A$ de $3 \\times 3$, encuentre su polinomio característico $\\det(A - \\lambda I) = 0$ e ingrese el valor propio dominante $\\lambda_{\\text{max}}$.")
        st.latex(rf"A = {matrix_to_latex(A)}")
        
        vals = np.linalg.eigvals(A)
        max_eig = max(vals, key=abs)
        
        r_eig = st.number_input("Eigenvalor dominante (λ_max):", value=0.00, format="%.2f")
        
        if st.button("Comprobar Polinomio Característico"):
            if abs(r_eig - max_eig) < 0.15:
                st.success(f"¡Correcto! 🎉 Eigenvalores: {[round(x,2) for x in vals]}. Dominante = {max_eig:.2f}")
            else:
                st.error(f"Incorrecto. ❌ Eigenvalores exactos: {[round(x,2) for x in vals]}. Dominante = {max_eig:.2f}")

# ==========================================
# MÉTODOS NUMÉRICOS
# ==========================================
else:
    st.sidebar.markdown("---")
    tema_mn = st.sidebar.selectbox("Seleccione Tema de Métodos Numéricos:", [
        "Series Numéricas (Seno / Coseno - 5ta iteración)",
        "Serie de Taylor (Polinomio de 3er Grado)",
        "Concepto de Errores y Sus Tipos",
        "Cambio de Registro de Computadora de 32 bits a Decimal",
        "Método de Bisección (Polinómica y Trigonométrica)",
        "Método de Falsa Posición y Falsa Posición Modificada",
        "Método de Newton (Polinómica y Trigonométrica)",
        "Método de la Secante (Polinómica y Trigonométrica)",
        "Método de Gauss-Jordán (Sistema 3x3)",
        "Método de Descomposición A-LU (Matriz U y Respuestas)",
        "Inversión de Matriz (Tamaño 3x3)",
        "Método del Polinomio Característico (≥ 3x3)",
        "Método de Iteración Matricial (Tamaño 5x5)",
        "Regresión Lineal (5 datos)",
        "Regresión Cuadrática (5 datos)",
        "Regresión Exponencial (5 datos)",
        "Interpolación por Lagrange (4 datos)",
        "Interpolación por Polinomio Único (5 datos)",
        "Sistema No Lineal por Newton-Raphson (Verificación 3ra Iteración)",
        "Aproximación de Integrales (Simpson Compuesto)",
        "EDO - Método de Euler Modificado",
        "EDO - Método de Taylor",
        "EDO - Runge-Kutta Orden 4"
    ])
    
    st.markdown(f"## 🔢 Métodos Numéricos — {tema_mn}")
    
    # 1. Series numéricas (5ta iteración)
    if tema_mn == "Series Numéricas (Seno / Coseno - 5ta iteración)":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_s5_x" not in st.session_state:
            st.session_state.mn_s5_x = round(float(np.random.uniform(0.3, 1.2)), 2)
            st.rerun()
        x_val = st.session_state.mn_s5_x
        st.info(f"💡 **Instrucción:** Evalúe los primeros 5 términos (5ta iteración) de la serie de Maclaurin para $\\sin({x_val})$.")
        st.latex(rf"\sin(x) \approx x - \frac{{x^3}}{{3!}} + \frac{{x^5}}{{5!}} - \frac{{x^7}}{{7!}} + \frac{{x^9}}{{9!}}")
        
        s5 = x_val - (x_val**3)/6.0 + (x_val**5)/120.0 - (x_val**7)/5040.0 + (x_val**9)/362880.0
        r_s5 = st.number_input("Valor de la serie en la 5ta iteración:", value=0.0000, format="%.6f")
        
        if st.button("Comprobar Serie (5ta Iteración)"):
            if abs(r_s5 - s5) < 0.0001:
                st.success(f"¡Correcto! 🎉 Valor aproximado en la 5ta iteración = {s5:.6f}")
            else:
                st.error(f"Incorrecto. ❌ El valor exacto en la 5ta iteración es {s5:.6f}")

    # 2. Serie de Taylor (3er Grado)
    elif tema_mn == "Serie de Taylor (Polinomio de 3er Grado)":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_tay3_a" not in st.session_state:
            st.session_state.mn_tay3_a = round(float(np.random.uniform(0.5, 2.0)), 2)
            st.rerun()
        a_val = st.session_state.mn_tay3_a
        st.info(f"💡 **Instrucción:** Para $f(x) = e^x$ alrededor de $x = 0$, evalúe $P_3({a_val})$ usando el polinomio de 3er grado.")
        st.latex(rf"P_3(x) = 1 + x + \frac{{x^2}}{{2!}} + \frac{{x^3}}{{3!}}")
        
        p3 = 1 + a_val + (a_val**2)/2.0 + (a_val**3)/6.0
        r_p3 = st.number_input(f"Valor de P3({a_val}):", value=0.0000, format="%.4f")
        
        if st.button("Comprobar Polinomio de Taylor"):
            if abs(r_p3 - p3) < 0.001:
                st.success(f"¡Correcto! 🎉 P3({a_val}) = {p3:.4f}")
            else:
                st.error(f"Incorrecto. ❌ El valor exacto es {p3:.4f}")

    # 3. Errores
    elif tema_mn == "Concepto de Errores y Sus Tipos":
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
    elif tema_mn == "Cambio de Registro de Computadora de 32 bits a Decimal":
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
    elif tema_mn == "Método de Bisección (Polinómica y Trigonométrica)":
        tipo_eq = st.selectbox("📌 Seleccione Tipo de Ecuación:", ["Polinómica", "Trigonométrica"])
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_bis_k" not in st.session_state:
            st.session_state.mn_bis_k = int(np.random.randint(2, 7))
            st.rerun()
        k = st.session_state.mn_bis_k
        
        if tipo_eq == "Polinómica":
            st.info(f"💡 **Instrucción (Polinómica):** Halle el punto medio $x_r$ en la 1ra iteración en $[1, 2]$.")
            st.latex(rf"f(x) = x^3 - {k}x - 1 = 0")
            xl, xu = 1.0, 2.0
            xr = (xl + xu) / 2.0
        else:
            st.info(f"💡 **Instrucción (Trigonométrica):** Halle el punto medio $x_r$ en la 1ra iteración en $[0, 1.5]$.")
            st.latex(rf"f(x) = \cos(x) - {k/10.0:.1f}x = 0")
            xl, xu = 0.0, 1.5
            xr = (xl + xu) / 2.0
            
        r_xr = st.number_input("Punto medio xr:", value=0.0000, format="%.4f")
        if st.button("Comprobar Bisección"):
            if abs(r_xr - xr) < 0.01:
                st.success(f"¡Correcto! 🎉 xr = {xr:.4f}")
            else:
                st.error(f"Incorrecto. ❌ xr exacto = {xr:.4f}")

    # 6. Falsa Posición
    elif tema_mn == "Método de Falsa Posición y Falsa Posición Modificada":
        tipo_eq = st.selectbox("📌 Seleccione Tipo de Ecuación:", ["Polinómica", "Trigonométrica"])
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_fp_k" not in st.session_state:
            st.session_state.mn_fp_k = int(np.random.randint(2, 6))
            st.rerun()
        k = st.session_state.mn_fp_k
        
        if tipo_eq == "Polinómica":
            st.info(f"💡 **Instrucción (Polinómica):** Halle $x_r$ en la 1ra iteración por Falsa Posición en $[1, 2]$.")
            st.latex(rf"f(x) = x^3 - {k} = 0")
            xl, xu = 1.0, 2.0
            fl, fu = xl**3 - k, xu**3 - k
        else:
            st.info(f"💡 **Instrucción (Trigonométrica):** Halle $x_r$ en la 1ra iteración por Falsa Posición en $[1, 2]$.")
            st.latex(rf"f(x) = \sin(x) - {k/10.0:.1f}x = 0")
            xl, xu = 1.0, 2.0
            fl, fu = math.sin(xl) - (k/10.0)*xl, math.sin(xu) - (k/10.0)*xu
            
        xr = xu - (fu * (xl - xu)) / (fl - fu)
        r_xr = st.number_input("Valor de xr:", value=0.0000, format="%.4f")
        if st.button("Comprobar Falsa Posición"):
            if abs(r_xr - xr) < 0.02:
                st.success(f"¡Excelente! 🎉 xr = {xr:.4f}")
            else:
                st.error(f"Incorrecto. ❌ El valor exacto es xr = {xr:.4f}")

    # 7. Newton
    elif tema_mn == "Método de Newton (Polinómica y Trigonométrica)":
        tipo_eq = st.selectbox("📌 Seleccione Tipo de Ecuación:", ["Polinómica", "Trigonométrica"])
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_nw_k" not in st.session_state:
            st.session_state.mn_nw_k = round(float(np.random.uniform(1.2, 2.2)), 2)
            st.rerun()
        x0 = st.session_state.mn_nw_k
        
        if tipo_eq == "Polinómica":
            st.info(f"💡 **Instrucción (Polinómica):** Para $x_0 = {x0}$, halle $x_1$ mediante Newton-Raphson.")
            st.latex(rf"f(x) = x^3 - 2x - 5 = 0")
            f0 = x0**3 - 2*x0 - 5
            df0 = 3*(x0**2) - 2
        else:
            st.info(f"💡 **Instrucción (Trigonométrica):** Para $x_0 = {x0}$, halle $x_1$ mediante Newton-Raphson.")
            st.latex(rf"f(x) = \sin(x) - \frac{{x}}{{2}} = 0")
            f0 = math.sin(x0) - x0/2.0
            df0 = math.cos(x0) - 0.5
            
        x1 = x0 - f0/df0
        r_x1 = st.number_input("Valor de x_1:", value=0.0000, format="%.4f")
        if st.button("Comprobar Newton"):
            if abs(r_x1 - x1) < 0.02:
                st.success(f"¡Correcto! 🎉 x_1 = {x1:.4f}")
            else:
                st.error(f"Incorrecto. ❌ El valor exacto es x_1 = {x1:.4f}")

    # 8. Secante
    elif tema_mn == "Método de la Secante (Polinómica y Trigonométrica)":
        tipo_eq = st.selectbox("📌 Seleccione Tipo de Ecuación:", ["Polinómica", "Trigonométrica"])
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_sec_k" not in st.session_state:
            st.session_state.mn_sec_k = int(np.random.randint(3, 8))
            st.rerun()
        c = st.session_state.mn_sec_k
        
        if tipo_eq == "Polinómica":
            st.info(f"💡 **Instrucción (Polinómica):** Para $x_0 = 1$ y $x_1 = 2$, calcule $x_2$.")
            st.latex(rf"f(x) = x^3 - {c} = 0")
            x0, x1 = 1.0, 2.0
            f0, f1 = x0**3 - c, x1**3 - c
        else:
            st.info(f"💡 **Instrucción (Trigonométrica):** Para $x_0 = 0.5$ y $x_1 = 1.0$, calcule $x_2$.")
            st.latex(rf"f(x) = \cos(x) - x = 0")
            x0, x1 = 0.5, 1.0
            f0, f1 = math.cos(x0) - x0, math.cos(x1) - x1
            
        x2 = x1 - (f1 * (x0 - x1)) / (f0 - f1)
        r_x2 = st.number_input("Valor de x_2:", value=0.0000, format="%.4f")
        if st.button("Comprobar Secante"):
            if abs(r_x2 - x2) < 0.02:
                st.success(f"¡Correcto! 🎉 x_2 = {x2:.4f}")
            else:
                st.error(f"Incorrecto. ❌ El valor exacto es x_2 = {x2:.4f}")

    # 9. Gauss-Jordán 3x3
    elif tema_mn == "Método de Gauss-Jordán (Sistema 3x3)":
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
        st.info("💡 **Instrucción:** Resuelva el sistema por Gauss-Jordán y determine $z$.")
        st.latex(rf"\begin{{cases}} {A[0,0]}x + {A[0,1]}y + {A[0,2]}z = {b[0]} \\ {A[1,0]}x + {A[1,1]}y + {A[1,2]}z = {b[1]} \\ {A[2,0]}x + {A[2,1]}y + {A[2,2]}z = {b[2]} \end{{cases}}")
        
        sol = np.linalg.solve(A, b)
        r_z = st.number_input("Valor de z:", value=0.00, format="%.2f")
        if st.button("Comprobar z"):
            if abs(r_z - sol[2]) < 0.1:
                st.success(f"¡Excelente! 🎉 z = {sol[2]:.2f}")
            else:
                st.error(f"Incorrecto. ❌ z exacto = {sol[2]:.2f}")

    # 10. Descomposición LU (MN)
    elif tema_mn == "Método de Descomposición A-LU (Matriz U y Respuestas)":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_lu_a" not in st.session_state:
            st.session_state.mn_lu_a = np.array([[2, 1, -1], [4, 4, 1], [-2, 3, 1]], dtype=float)
            st.session_state.mn_lu_b = np.array([1, 11, 4], dtype=float)
            st.rerun()
            
        A, b = st.session_state.mn_lu_a, st.session_state.mn_lu_b
        st.info("💡 **Instrucción:** Halle la descomposición Doolittle $A = L \\cdot U$ y determine la matriz superior $U$ y la solución $X$.")
        st.latex(rf"A = {matrix_to_latex(A)}, \quad B = {matrix_to_latex(b)}")
        
        L = np.eye(3)
        U = A.copy()
        for i in range(3):
            for j in range(i+1, 3):
                factor = U[j, i] / U[i, i]
                L[j, i] = factor
                U[j, i:] -= factor * U[i, i:]
                
        sol = np.linalg.solve(A, b)
        
        c1, c2 = st.columns(2)
        with c1: r_u11 = st.number_input("Pivote U[2,2] (U_22):", value=0.00, format="%.2f")
        with c2: r_x0 = st.number_input("Solución x_1:", value=0.00, format="%.2f")
        
        if st.button("Verificar Matriz U y Respuestas"):
            if abs(r_u11 - U[1,1]) < 0.1 and abs(r_x0 - sol[0]) < 0.1:
                st.success("¡Correcto! 🎉 Matriz U y Vector Respuestas verificados.")
                st.latex(rf"U = {matrix_to_latex(U)}, \quad X = {matrix_to_latex(sol)}")
            else:
                st.error("Incorrecto. ❌ Verifique la matriz U y la solución.")
                st.latex(rf"U = {matrix_to_latex(U)}, \quad X = {matrix_to_latex(sol)}")

    # 11. Inversión Matriz 3x3
    elif tema_mn == "Inversión de Matriz (Tamaño 3x3)":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_inv3" not in st.session_state:
            while True:
                m = np.random.randint(-3, 4, size=(3, 3))
                if int(round(np.linalg.det(m))) != 0:
                    st.session_state.mn_inv3 = m
                    break
            st.rerun()
            
        A = st.session_state.mn_inv3
        st.info("💡 **Instrucción:** Halle la matriz inversa $A^{-1}$ e ingrese la traza $\\text{tr}(A^{-1})$.")
        st.latex(rf"A = {matrix_to_latex(A)}")
        
        invA = np.linalg.inv(A)
        traza_inv = float(np.trace(invA))
        
        r_tr = st.number_input("Traza de A^(-1):", value=0.0000, format="%.4f")
        if st.button("Comprobar Inversión"):
            if abs(r_tr - traza_inv) < 0.05:
                st.success(f"¡Excelente! 🎉 Traza de A^(-1) = {traza_inv:.4f}")
                st.latex(rf"A^{{-1}} = {matrix_to_latex(invA)}")
            else:
                st.error(f"Incorrecto. ❌ Traza exacta = {traza_inv:.4f}")

    # 12. Polinomio Característico
    elif tema_mn == "Método del Polinomio Característico (≥ 3x3)":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_pc_m" not in st.session_state:
            m = np.random.randint(-2, 3, size=(3, 3))
            st.session_state.mn_pc_m = (m + m.T).astype(float)
            st.rerun()
            
        A = st.session_state.mn_pc_m
        st.info("💡 **Instrucción:** Determine la traza $\\text{tr}(A)$ coincidente con la suma de los autovalores.")
        st.latex(rf"A = {matrix_to_latex(A)}")
        
        traza = int(np.trace(A))
        r_tr = st.number_input("Traza tr(A):", value=0.0, step=1.0)
        if st.button("Comprobar Traza"):
            if int(r_tr) == traza: st.success(f"¡Excelente! 🎉 traza(A) = {traza}")
            else: st.error(f"Incorrecto. ❌ La traza exacta es {traza}")

    # 13. Iteración Matricial 5x5
    elif tema_mn == "Método de Iteración Matricial (Tamaño 5x5)":
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

    # 14. Regresión Lineal
    elif tema_mn == "Regresión Lineal (5 datos)":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_reg_x" not in st.session_state:
            st.session_state.mn_reg_x = np.array([1, 2, 3, 4, 5], dtype=float)
            st.session_state.mn_reg_y = np.array([2.1, 3.8, 6.2, 7.9, 10.1], dtype=float) + np.random.uniform(-0.3, 0.3, size=5)
            st.rerun()
            
        x, y = st.session_state.mn_reg_x, st.session_state.mn_reg_y
        st.info("💡 **Instrucción:** Ajuste la recta $y = P_1(x) = a_1 x + a_0$ y verifique los coeficientes $(a_1, a_0)$.")
        st.dataframe(pd.DataFrame({"x": x, "y": y}), use_container_width=True)
        
        a1, a0 = np.polyfit(x, y, 1)
        c1, c2 = st.columns(2)
        with c1: r_a1 = st.number_input("Pendiente a1:", value=0.0000, format="%.4f")
        with c2: r_a0 = st.number_input("Intersección a0:", value=0.0000, format="%.4f")
        
        if st.button("Verificar Polinomio Lineal"):
            if abs(r_a1 - a1) < 0.05 and abs(r_a0 - a0) < 0.05:
                st.success(f"¡Polinomio Verificado! 🎉 P_1(x) = {a1:.4f} x + {a0:.4f}")
            else:
                st.error(f"Incorrecto. ❌ Polinomio exacto: P_1(x) = {a1:.4f} x + {a0:.4f}")

    # 15. Regresión Cuadrática
    elif tema_mn == "Regresión Cuadrática (5 datos)":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_rc_x" not in st.session_state:
            st.session_state.mn_rc_x = np.array([1, 2, 3, 4, 5], dtype=float)
            st.session_state.mn_rc_y = 0.5 * (st.session_state.mn_rc_x**2) + np.random.uniform(-0.2, 0.2, size=5)
            st.rerun()
            
        x, y = st.session_state.mn_rc_x, st.session_state.mn_rc_y
        st.info("💡 **Instrucción:** Ajuste la parábola $y = P_2(x) = a_2 x^2 + a_1 x + a_0$ y verifique el coeficiente cuadrático $a_2$.")
        st.dataframe(pd.DataFrame({"x": x, "y": y}), use_container_width=True)
        
        a2, a1, a0 = np.polyfit(x, y, 2)
        r_a2 = st.number_input("Coeficiente cuadrático a2:", value=0.0000, format="%.4f")
        if st.button("Verificar Polinomio Cuadrático"):
            if abs(r_a2 - a2) < 0.05:
                st.success(f"¡Polinomio Verificado! 🎉 P_2(x) = {a2:.4f} x^2 + {a1:.4f} x + {a0:.4f}")
            else:
                st.error(f"Incorrecto. ❌ a2 exacto = {a2:.4f}")

    # 16. Regresión Exponencial
    elif tema_mn == "Regresión Exponencial (5 datos)":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_re_x" not in st.session_state:
            st.session_state.mn_re_x = np.array([1, 2, 3, 4, 5], dtype=float)
            st.session_state.mn_re_y = 2.0 * np.exp(0.4 * st.session_state.mn_re_x) + np.random.uniform(-0.1, 0.1, size=5)
            st.rerun()
            
        x, y = st.session_state.mn_re_x, st.session_state.mn_re_y
        st.info("💡 **Instrucción:** Ajuste el modelo $y = A \\cdot e^{B x}$ mediante $\\ln(y) = \\ln(A) + B x$ y verifique la tasa $B$.")
        st.dataframe(pd.DataFrame({"x": x, "y": y}), use_container_width=True)
        
        B, lnA = np.polyfit(x, np.log(y), 1)
        r_b = st.number_input("Tasa Exponencial B:", value=0.0000, format="%.4f")
        if st.button("Verificar Modelo Exponencial"):
            if abs(r_b - B) < 0.05:
                st.success(f"¡Modelo Verificado! 🎉 y = {np.exp(lnA):.4f} * e^({B:.4f} x)")
            else:
                st.error(f"Incorrecto. ❌ B exacto = {B:.4f}")

    # 17. Interpolación Lagrange
    elif tema_mn == "Interpolación por Lagrange (4 datos)":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_lag_x" not in st.session_state:
            st.session_state.mn_lag_x = np.array([0, 1, 2, 3], dtype=float)
            st.session_state.mn_lag_y = np.array([1, 3, 0, 5], dtype=float) + np.random.randint(-1, 2, size=4)
            st.rerun()
            
        x, y = st.session_state.mn_lag_x, st.session_state.mn_lag_y
        st.info("💡 **Instrucción:** Para los 4 datos, halle $P_3(x) = c_3 x^3 + c_2 x^2 + c_1 x + c_0$ y verifique el término independiente $c_0$.")
        st.dataframe(pd.DataFrame({"x": x, "y": y}), use_container_width=True)
        
        coeffs = np.polyfit(x, y, 3)
        c0 = coeffs[-1]
        
        r_c0 = st.number_input("Término independiente c0:", value=0.0000, format="%.4f")
        if st.button("Verificar Coeficientes de Lagrange"):
            if abs(r_c0 - c0) < 0.05:
                st.success(f"¡Coeficiente Verificado! 🎉 c0 = {c0:.4f}\n Polinomio: {[round(k,4) for k in coeffs]}")
            else:
                st.error(f"Incorrecto. ❌ c0 exacto = {c0:.4f}")

    # 18. Interpolación Polinomio Único
    elif tema_mn == "Interpolación por Polinomio Único (5 datos)":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_pu_x" not in st.session_state:
            st.session_state.mn_pu_x = np.array([0, 1, 2, 3, 4], dtype=float)
            st.session_state.mn_pu_y = np.array([2, 1, 4, 3, 6], dtype=float) + np.random.randint(-1, 2, size=5)
            st.rerun()
            
        x, y = st.session_state.mn_pu_x, st.session_state.mn_pu_y
        st.info("💡 **Instrucción:** Mediante Vandermonde $5 \\times 5$, determine $P_4(x) = a_4 x^4 + a_3 x^3 + a_2 x^2 + a_1 x + a_0$ y verifique $a_0$.")
        st.dataframe(pd.DataFrame({"x": x, "y": y}), use_container_width=True)
        
        coeffs = np.polyfit(x, y, 4)
        a0 = coeffs[-1]
        
        r_a0 = st.number_input("Término independiente a0:", value=0.0000, format="%.4f")
        if st.button("Verificar Polinomio Único"):
            if abs(r_a0 - a0) < 0.05:
                st.success(f"¡Coeficiente Verificado! 🎉 a0 = {a0:.4f}\n Coeficientes [a4..a0]: {[round(k,4) for k in coeffs]}")
            else:
                st.error(f"Incorrecto. ❌ a0 exacto = {a0:.4f}")

    # 19. Sistema No Lineal
    elif tema_mn == "Sistema No Lineal por Newton-Raphson (Verificación 3ra Iteración)":
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

    # 20. Simpson Compuesto
    elif tema_mn == "Aproximación de Integrales (Simpson Compuesto)":
        if st.button("🔄 Generar nuevos datos del ejercicio") or "mn_simp_n" not in st.session_state:
            st.session_state.mn_simp_n = int(np.random.choice([4, 6, 8]))
            st.rerun()
        n_sub = st.session_state.mn_simp_n
        b_val = 2.0
        h = b_val / n_sub
        st.info(f"💡 **Instrucción:** Evalúe la integral aplicando la Regla de Simpson 1/3 Compuesta con $n = {n_sub}$ subintervalos ($h = {h:.4f}$).")
        st.latex(rf"\int_0^2 x^3 \, dx")
        
        x_pts = np.linspace(0, b_val, n_sub + 1)
        f_pts = x_pts**3
        simp_val = (h/3.0) * (f_pts[0] + f_pts[-1] + 4*sum(f_pts[1:-1:2]) + 2*sum(f_pts[2:-1:2]))
        
        r_s = st.number_input("Valor de la integral por Simpson:", value=0.0000, format="%.4f")
        if st.button("Comprobar Simpson 1/3"):
            if abs(r_s - simp_val) < 0.01:
                st.success(f"¡Excelente! 🎉 Integral = {simp_val:.4f}")
            else:
                st.error(f"Incorrecto. ❌ El valor exacto por Simpson 1/3 es {simp_val:.4f}")

    # 21. EDO Euler Modificado (CORREGIDO AL ESTILO dy/dx = 4x + 5y - 3x^2 + 4y^2 - e^(2x))
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

    # 22. EDO Taylor (CORREGIDO AL ESTILO dy/dx = 4x + 5y)
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
        
        # dy/dx = 4x + 5y -> y' = 4x + 5y
        # y'' = d/dx(4x + 5y) = 4 + 5y' = 4 + 5(4x + 5y)
        yp0 = 4*x0 + 5*y0
        ypp0 = 4 + 5*yp0
        y1 = y0 + h*yp0 + (h**2 / 2.0)*ypp0
        
        r_yt = st.number_input(f"Valor de y({x_target}):", value=0.0000, format="%.4f")
        if st.button("Comprobar Taylor Orden 2"):
            if abs(r_yt - y1) < 0.005:
                st.success(f"¡Excelente! 🎉 y({x_target}) = {y1:.4f}")
            else:
                st.error(f"Incorrecto. ❌ El valor exacto es y({x_target}) = {y1:.4f}")

    # 23. EDO RK4 (CORREGIDO AL ESTILO dy/dx = 4x + 5y - 3x^2 + 4y^2 - e^(2x))
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
