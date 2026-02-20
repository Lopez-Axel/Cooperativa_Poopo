<template>
    <div class="detalle-cooperativista-page">
        <!-- Breadcrumb -->
        <nav class="breadcrumb-nav">
            <NuxtLink to="/cooperativistas" class="breadcrumb-link">
                <i class="mdi mdi-arrow-left"></i>
                Volver a Cooperativistas
            </NuxtLink>
        </nav>

        <div v-if="loading" class="loading-container">
            <div class="loader"></div>
            <p>Cargando información...</p>
        </div>

        <div v-else-if="cooperativista" class="detalle-container">
            <!-- Credencial del Cooperativista -->
            <div
                class="credencial-cooperativista"
                :class="{ 'is-jefe': esCargoEspecial }"
            >
                <!-- Header de la Credencial -->
                <div class="credencial-header">
                    <div class="header-bg"></div>
                    <div class="logo-section">
                        <div class="logo-circle">
                            <i class="mdi mdi-hammer-wrench"></i>
                        </div>
                        <h2 class="cooperativa-nombre">
                            Cooperativa Minera Poopó R.L.
                        </h2>
                    </div>
                </div>

                <!-- Foto y QR -->
                <div class="foto-qr-section">
                    <div class="foto-container">
                        <img
                            v-if="cooperativista.ci_foto_url"
                            :src="cooperativista.ci_foto_url"
                            alt="Foto CI"
                            class="foto-ci"
                        />
                        <div v-else class="foto-placeholder">
                            <i class="mdi mdi-account-circle"></i>
                        </div>
                    </div>

                    <div class="qr-container">
                        <QRCodeVue3
                            :value="cooperativista.qr_code"
                            :width="180"
                            :height="180"
                            :margin="2"
                            :corner-square-options="{
                                type: 'square',
                                color: '#038730',
                            }"
                            :corner-dot-options="{
                                type: 'square',
                                color: '#feea01',
                            }"
                            :dots-options="{ type: 'square', color: '#1a2e1a' }"
                            :background-options="{ color: '#ffffff' }"
                            image="/logo.png"
                            :image-options="{
                                hideBackgroundDots: true,
                                imageSize: 0.5,
                                margin: 2,
                            }"
                        />
                    </div>
                </div>

                <!-- Información Principal -->
                <div class="info-principal">
                    <h1 class="nombre-completo">
                        {{ cooperativista.nombres }}
                        {{ cooperativista.apellido_paterno }}
                        {{ cooperativista.apellido_materno }}
                    </h1>
                </div>

                <!-- Badge de Cargo Especial -->
                <div v-if="cooperativista.rol_cuadrilla" class="cargo-especial">
                    <i class="mdi mdi-star"></i>
                    <span>{{ cooperativista.rol_cuadrilla }}</span>
                </div>

                <!-- Datos Personales -->
                <div class="seccion-datos">
                    <h3 class="seccion-titulo">
                        <i class="mdi mdi-card-account-details"></i>
                        Datos Personales
                    </h3>
                    <div class="datos-grid">
                        <div class="dato-item">
                            <span class="dato-label">CI:</span>
                            <span class="dato-valor">{{
                                cooperativista.ci || "No registrado"
                            }}</span>
                        </div>
                        <div
                            class="dato-item"
                            v-if="cooperativista.ci_expedido"
                        >
                            <span class="dato-label">Expedido:</span>
                            <span class="dato-valor">{{
                                cooperativista.ci_expedido
                            }}</span>
                        </div>
                        <div
                            class="dato-item"
                            v-if="cooperativista.fecha_nacimiento"
                        >
                            <span class="dato-label">Fecha Nacimiento:</span>
                            <span class="dato-valor">{{
                                formatearFecha(cooperativista.fecha_nacimiento)
                            }}</span>
                        </div>
                        <div class="dato-item" v-if="edad">
                            <span class="dato-label">Edad:</span>
                            <span class="dato-valor">{{ edad }} años</span>
                        </div>
                        <div class="dato-item" v-if="cooperativista.email">
                            <span class="dato-label">Email:</span>
                            <span class="dato-valor">{{
                                cooperativista.email
                            }}</span>
                        </div>
                        <div class="dato-item" v-if="cooperativista.telefono">
                            <span class="dato-label">Teléfono:</span>
                            <span class="dato-valor">{{
                                cooperativista.telefono
                            }}</span>
                        </div>
                    </div>
                </div>

                <!-- Información Laboral -->
                <div class="seccion-datos">
                    <h3 class="seccion-titulo">
                        <i class="mdi mdi-briefcase"></i>
                        Información Laboral
                    </h3>
                    <div class="datos-grid">
                        <div class="dato-item">
                            <span class="dato-label">Sección:</span>
                            <span class="dato-valor">{{ seccionName }}</span>
                        </div>
                        <div class="dato-item">
                            <span class="dato-label">Cuadrilla:</span>
                            <span class="dato-valor">{{ cuadrillaName }}</span>
                        </div>
                        <div
                            class="dato-item"
                            v-if="cooperativista.rol_cuadrilla"
                        >
                            <span class="dato-label">Rol en Cuadrilla:</span>
                            <span class="dato-valor cargo-badge">{{
                                cooperativista.rol_cuadrilla
                            }}</span>
                        </div>
                        <div class="dato-item" v-if="cooperativista.ocupacion">
                            <span class="dato-label">Ocupación:</span>
                            <span class="dato-valor ocupacion">{{
                                cooperativista.ocupacion
                            }}</span>
                        </div>
                        <div
                            class="dato-item"
                            v-if="cooperativista.fecha_ingreso"
                        >
                            <span class="dato-label">Fecha Ingreso:</span>
                            <span class="dato-valor">{{
                                formatearFecha(cooperativista.fecha_ingreso)
                            }}</span>
                        </div>
                        <div class="dato-item" v-if="antiguedad">
                            <span class="dato-label">Antigüedad:</span>
                            <span class="dato-valor">{{ antiguedad }}</span>
                        </div>
                    </div>
                </div>

                <!-- Información de Seguro -->
                <div
                    class="seccion-datos"
                    v-if="cooperativista.codigo_asegurado || cooperativista.cua"
                >
                    <h3 class="seccion-titulo">
                        <i class="mdi mdi-shield-check"></i>
                        Información de Seguro
                    </h3>
                    <div class="datos-grid">
                        <div
                            class="dato-item"
                            v-if="cooperativista.codigo_asegurado"
                        >
                            <span class="dato-label">Código Asegurado:</span>
                            <span class="dato-valor">{{
                                cooperativista.codigo_asegurado
                            }}</span>
                        </div>
                        <div class="dato-item" v-if="cooperativista.cua">
                            <span class="dato-label">CUA:</span>
                            <span class="dato-valor">{{
                                cooperativista.cua
                            }}</span>
                        </div>
                        <div
                            class="dato-item"
                            v-if="cooperativista.estado_asegurado"
                        >
                            <span class="dato-label">Estado:</span>
                            <span class="dato-valor">{{
                                cooperativista.estado_asegurado
                            }}</span>
                        </div>
                    </div>
                </div>

                <!-- Información de Gestora con Protección -->
                <div
                    class="seccion-datos seccion-protegida"
                    v-if="
                        cooperativista.usuario_gestora ||
                        cooperativista.password_gestora
                    "
                >
                    <div class="seccion-header-protegida">
                        <h3 class="seccion-titulo">
                            <i class="mdi mdi-shield-lock"></i>
                            Información de Gestora
                            <span class="tag-protegido">Protegido</span>
                        </h3>
                    </div>

                    <!-- Verificación de Contraseña -->
                    <div v-if="!gestoraDesbloqueada" class="bloqueo-gestora">
                        <div class="icono-bloqueo">
                            <i class="mdi mdi-lock-outline"></i>
                        </div>
                        <p class="texto-bloqueo">
                            Ingresa tu contraseña actual para acceder a la
                            información de gestora
                        </p>
                        <div class="field-verificacion">
                            <div class="control has-icons-left">
                                <input
                                    v-model="passwordVerificacion"
                                    class="input input-verificacion"
                                    type="password"
                                    placeholder="Tu contraseña actual"
                                    @keyup.enter="verificarPassword"
                                />
                                <span class="icon is-left">
                                    <i class="mdi mdi-key"></i>
                                </span>
                            </div>
                            <button
                                class="button-desbloquear"
                                @click="verificarPassword"
                                :disabled="!passwordVerificacion"
                            >
                                <i class="mdi mdi-lock-open-variant"></i>
                                Desbloquear
                            </button>
                            <p v-if="errorVerificacion" class="help is-danger">
                                {{ errorVerificacion }}
                            </p>
                        </div>
                    </div>

                    <!-- Campos de Gestora (visibles solo si está desbloqueado) -->
                    <div v-else class="campos-gestora-desbloqueados">
                        <div class="estado-desbloqueado">
                            <i class="mdi mdi-lock-open-check-outline"></i>
                            <span>Acceso autorizado</span>
                            <button
                                class="button-bloquear"
                                @click="bloquearGestora"
                            >
                                <i class="mdi mdi-lock"></i>
                                Bloquear
                            </button>
                        </div>

                        <div class="datos-grid">
                            <div
                                class="dato-item dato-protegido"
                                v-if="cooperativista.usuario_gestora"
                            >
                                <span class="dato-label">
                                    <i class="mdi mdi-account-key"></i>
                                    Usuario Gestora:
                                </span>
                                <span class="dato-valor">{{
                                    cooperativista.usuario_gestora
                                }}</span>
                            </div>
                            <div
                                class="dato-item dato-protegido"
                                v-if="cooperativista.password_gestora"
                            >
                                <span class="dato-label">
                                    <i
                                        class="mdi mdi-form-textbox-password"
                                    ></i>
                                    Contraseña:
                                </span>
                                <span class="dato-valor dato-password">
                                    <span v-if="!mostrarPasswordGestora">
                                        {{
                                            "•".repeat(
                                                cooperativista.password_gestora
                                                    .length,
                                            )
                                        }}
                                    </span>
                                    <span v-else>
                                        {{ cooperativista.password_gestora }}
                                    </span>
                                    <button
                                        class="toggle-password"
                                        @click="
                                            mostrarPasswordGestora =
                                                !mostrarPasswordGestora
                                        "
                                    >
                                        <i
                                            class="mdi"
                                            :class="
                                                mostrarPasswordGestora
                                                    ? 'mdi-eye-off'
                                                    : 'mdi-eye'
                                            "
                                        ></i>
                                    </button>
                                </span>
                            </div>
                        </div>

                        <div class="nota-seguridad">
                            <i class="mdi mdi-information-outline"></i>
                            <span
                                >Estas credenciales son independientes del
                                sistema</span
                            >
                        </div>
                    </div>
                </div>

                <!-- Documentos -->
                <div class="seccion-datos">
                    <h3 class="seccion-titulo">
                        <i class="mdi mdi-file-document"></i>
                        Documentos
                    </h3>
                    <div class="documentos-grid">
                        <div class="documento-item">
                            <span class="documento-label">Foto CI:</span>
                            <div class="documento-preview">
                                <a
                                    v-if="cooperativista.ci_foto_url"
                                    :href="cooperativista.ci_foto_url"
                                    target="_blank"
                                    class="documento-link"
                                >
                                    <i class="mdi mdi-image"></i>
                                    Ver Foto
                                </a>
                                <div v-else class="documento-vacio">
                                    <i class="mdi mdi-image-outline"></i>
                                    <span>No disponible</span>
                                </div>
                            </div>
                        </div>
                        <div class="documento-item">
                            <span class="documento-label">Documento ABC:</span>
                            <div class="documento-preview">
                                <a
                                    v-if="cooperativista.documento_abc_url"
                                    :href="cooperativista.documento_abc_url"
                                    target="_blank"
                                    class="documento-link"
                                >
                                    <i class="mdi mdi-file-pdf-box"></i>
                                    Ver Documento
                                </a>
                                <div v-else class="documento-vacio">
                                    <i
                                        class="mdi mdi-file-document-outline"
                                    ></i>
                                    <span>No disponible</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Footer de Credencial -->
                <div class="credencial-footer">
                    <p class="fecha-emision">
                        Fecha de emisión: {{ fechaActual }}
                    </p>
                    <div
                        class="estado-badge"
                        :class="{
                            activo: cooperativista.is_active,
                            inactivo: !cooperativista.is_active,
                        }"
                    >
                        <i
                            class="mdi"
                            :class="
                                cooperativista.is_active
                                    ? 'mdi-check-circle'
                                    : 'mdi-close-circle'
                            "
                        ></i>
                        {{ cooperativista.is_active ? "ACTIVO" : "INACTIVO" }}
                    </div>
                </div>
            </div>

            <!-- Panel de Acciones -->
            <div class="acciones-panel">
                <h3 class="panel-titulo">Acciones</h3>

                <button
                    class="action-button editar"
                    @click="editarCooperativista"
                >
                    <i class="mdi mdi-pencil"></i>
                    <span>Editar Información</span>
                </button>

                <button
                    class="action-button asistencias"
                    @click="verAsistencias"
                >
                    <i class="mdi mdi-calendar-check"></i>
                    <span>Ver Asistencias</span>
                </button>

                <button
                    class="action-button desactivar"
                    @click="toggleEstado"
                    v-if="cooperativista.is_active"
                >
                    <i class="mdi mdi-account-off"></i>
                    <span>Desactivar Cooperativista</span>
                </button>

                <button
                    class="action-button activar"
                    @click="toggleEstado"
                    v-else
                >
                    <i class="mdi mdi-account-check"></i>
                    <span>Activar Cooperativista</span>
                </button>

                <button
                    class="action-button generar-pdf"
                    @click="generarPerfil"
                >
                    <i class="mdi mdi-file-pdf-box"></i>
                    <span>Generar Perfil PDF</span>
                </button>
            </div>
        </div>

        <!-- Modal de Edición -->
        <FormularioCooperativista
            v-if="cooperativista"
            :isOpen="mostrarFormularioEdicion"
            :esEdicion="true"
            :datosIniciales="cooperativista"
            :secciones="seccionesStore.secciones"
            :cuadrillas="cuadrillasStore.cuadrillas"
            :ocupaciones="store.ocupaciones"
            :estadosAsegurado="store.estadosAsegurado"
            :cooperativistaId="cooperativistaId"
            :cargando="guardando"
            @close="mostrarFormularioEdicion = false"
            @guardar="handleGuardarEdicion"
        />
    </div>
</template>

<script setup>
import { defineAsyncComponent } from "vue";
import { generarPerfilCooperativista } from "../../utils/reporteCooperativista";
import FormularioCooperativista from "~/components/FormularioCooperativista.vue";

definePageMeta({
    layout: "dashboard",
    middleware: "auth",
});

const route = useRoute();
const router = useRouter();
const store = useCooperativistasStore();
const cuadrillasStore = useCuadrillasStore();
const seccionesStore = useSeccionesStore();
const authStore = useAuthStore();

const cooperativista = ref(null);
const loading = ref(true);
const mostrarConfirmacion = ref(false);
const mostrarFormularioEdicion = ref(false);
const cooperativistaEdicion = ref(null);

// Variables para gestora protegida
const gestoraDesbloqueada = ref(false);
const passwordVerificacion = ref("");
const errorVerificacion = ref("");
const mostrarPasswordGestora = ref(false);

const cooperativistaId = computed(() => parseInt(route.params.id));
const guardando = ref(false);

const QRCodeVue3 = defineAsyncComponent(() => import("qrcode-vue3"));

onMounted(async () => {
    try {
        // Cargar stores si están vacíos
        await Promise.all([
            cuadrillasStore.cuadrillas.length === 0
                ? cuadrillasStore.fetchCuadrillas()
                : Promise.resolve(),
            seccionesStore.secciones.length === 0
                ? seccionesStore.fetchSecciones()
                : Promise.resolve(),
        ]);

        // Cargar cooperativista
        cooperativista.value = await store.obtenerCooperativista(
            cooperativistaId.value,
        );
    } catch (error) {
        alert("Error al cargar cooperativista: " + error.message);
        router.push("/cooperativistas");
    } finally {
        loading.value = false;
    }
});

// Computed para obtener nombre de cuadrilla
const cuadrillaName = computed(() => {
    if (!cooperativista.value?.id_cuadrilla) return "Sin Cuadrilla";
    const cuadrilla = cuadrillasStore.cuadrillas.find(
        (c) => c.id === cooperativista.value.id_cuadrilla,
    );
    return cuadrilla ? cuadrilla.nombre : "N/A";
});

// Computed para obtener nombre de sección (a través de cuadrilla)
const seccionName = computed(() => {
    if (!cooperativista.value?.id_cuadrilla) return "Sin Sección";
    const cuadrilla = cuadrillasStore.cuadrillas.find(
        (c) => c.id === cooperativista.value.id_cuadrilla,
    );
    if (!cuadrilla || !cuadrilla.id_seccion) return "N/A";

    const seccion = seccionesStore.secciones.find(
        (s) => s.id === cuadrilla.id_seccion,
    );
    return seccion ? seccion.nombre : "N/A";
});

// Determinar si tiene cargo especial
const esCargoEspecial = computed(() => {
    if (!cooperativista.value?.rol_cuadrilla) return false;
    const rol = cooperativista.value.rol_cuadrilla.toLowerCase();
    return (
        rol.includes("jefe") ||
        rol.includes("tesorero") ||
        rol.includes("delegado")
    );
});

// Calcular edad
const edad = computed(() => {
    if (!cooperativista.value?.fecha_nacimiento) return null;
    const hoy = new Date();
    const nacimiento = new Date(cooperativista.value.fecha_nacimiento);
    let edad = hoy.getFullYear() - nacimiento.getFullYear();
    const mes = hoy.getMonth() - nacimiento.getMonth();
    if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
        edad--;
    }
    return edad;
});

// Calcular antigüedad
const antiguedad = computed(() => {
    if (!cooperativista.value?.fecha_ingreso) return null;
    const hoy = new Date();
    const ingreso = new Date(cooperativista.value.fecha_ingreso);

    let años = hoy.getFullYear() - ingreso.getFullYear();
    let meses = hoy.getMonth() - ingreso.getMonth();

    if (meses < 0) {
        años--;
        meses += 12;
    }

    if (años > 0 && meses > 0) {
        return `${años} años y ${meses} meses`;
    } else if (años > 0) {
        return `${años} ${años === 1 ? "año" : "años"}`;
    } else {
        return `${meses} ${meses === 1 ? "mes" : "meses"}`;
    }
});

const fechaActual = computed(() => {
    return new Date().toLocaleDateString("es-BO", {
        year: "numeric",
        month: "long",
        day: "numeric",
    });
});

const formatearFecha = (fecha) => {
    if (!fecha) return "";
    return new Date(fecha).toLocaleDateString("es-BO", {
        year: "numeric",
        month: "long",
        day: "numeric",
    });
};

const editarCooperativista = () => {
    mostrarFormularioEdicion.value = true;
};

const handleGuardarEdicion = async (datos) => {
    try {
        guardando.value = true;

        await store.actualizarCooperativista(cooperativistaId.value, datos);

        alert("Cooperativista actualizado exitosamente");
        mostrarFormularioEdicion.value = false;

        cooperativista.value = await store.obtenerCooperativista(
            cooperativistaId.value,
        );
    } catch (error) {
        console.error("Error:", error);
        alert("Error al actualizar: " + error.message);
    } finally {
        guardando.value = false;
    }
};

const verAsistencias = () => {
    router.push(`/asistencias?cooperativista=${cooperativistaId.value}`);
};

const toggleEstado = async () => {
    const nuevoEstado = !cooperativista.value.is_active;
    const mensaje = nuevoEstado ? "activar" : "desactivar";

    if (!confirm(`¿Está seguro que desea ${mensaje} este cooperativista?`))
        return;

    try {
        await store.toggleActivacion(cooperativistaId.value, nuevoEstado);
        cooperativista.value.is_active = nuevoEstado;
        alert(`Cooperativista ${mensaje}do exitosamente`);
    } catch (error) {
        alert("Error al cambiar estado: " + error.message);
    }
};

const generarPerfil = async () => {
    try {
        loading.value = true;
        await generarPerfilCooperativista(
            cooperativista.value,
            cuadrillaName.value,
            seccionName.value,
        );
        alert("Perfil PDF generado exitosamente");
    } catch (error) {
        console.error("Error generando PDF:", error);
        alert("Error al generar el PDF: " + error.message);
    } finally {
        loading.value = false;
    }
};

// Funciones para gestora protegida
const verificarPassword = async () => {
    errorVerificacion.value = "";

    if (!passwordVerificacion.value) {
        errorVerificacion.value = "Ingresa tu contraseña";
        return;
    }

    try {
        const response = await $fetch(`${authStore.apiUrl}/api/auth/login`, {
            method: "POST",
            body: {
                username: authStore.user.username,
                password: passwordVerificacion.value,
            },
        });

        if (response.access_token) {
            gestoraDesbloqueada.value = true;
            passwordVerificacion.value = "";
            errorVerificacion.value = "";
        }
    } catch (error) {
        errorVerificacion.value = "Contraseña incorrecta";
    }
};

const bloquearGestora = () => {
    gestoraDesbloqueada.value = false;
    passwordVerificacion.value = "";
    errorVerificacion.value = "";
    mostrarPasswordGestora.value = false;
};

useHead({
    title: cooperativista.value
        ? `${cooperativista.value.nombres} ${cooperativista.value.apellido_paterno}`
        : "Detalles Cooperativista",
});
</script>

<style scoped>
.detalle-cooperativista-page {
    min-height: calc(100vh - 200px);
    padding: 2rem;
    margin: -2rem -1.5rem;
    background: linear-gradient(135deg, #0a1a0a 0%, #0f1f0f 50%, #0a1a0a 100%);
}

.breadcrumb-nav {
    margin-bottom: 2rem;
}

.breadcrumb-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    color: #a5d6a7;
    font-weight: 600;
    transition: all 0.3s ease;
    text-decoration: none;
}

.breadcrumb-link:hover {
    color: #ffd700;
    transform: translateX(-4px);
}

.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    color: #a5d6a7;
}

.loader {
    width: 50px;
    height: 50px;
    border: 4px solid rgba(255, 215, 0, 0.2);
    border-top-color: #ffd700;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.detalle-container {
    display: grid;
    grid-template-columns: 1fr 350px;
    gap: 2rem;
}

.credencial-cooperativista {
    background: linear-gradient(
        135deg,
        rgba(26, 46, 26, 0.9),
        rgba(15, 31, 15, 0.9)
    );
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 10px 50px rgba(0, 0, 0, 0.5);
    border: 3px solid transparent;
    border-image: linear-gradient(135deg, #2e7d32, #9e9d24, #ffd700) 1;
    position: relative;
}

.credencial-cooperativista.is-jefe {
    border-image: linear-gradient(135deg, #ffd700, #ff9800, #f44336) 1;
}

.credencial-header {
    position: relative;
    height: 200px;
    background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 50%, #0d3d14 100%);
    overflow: hidden;
}

.header-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: repeating-linear-gradient(
        45deg,
        rgba(255, 215, 0, 0.05),
        rgba(255, 215, 0, 0.05) 10px,
        transparent 10px,
        transparent 20px
    );
}

.logo-section {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    gap: 1rem;
}

.logo-circle {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ffd700, #ff9800);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    color: #1a2e1a;
    box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4);
    border: 3px solid rgba(255, 255, 255, 0.3);
}

.cooperativa-nombre {
    color: #ffd700;
    font-size: 1.5rem;
    font-weight: 800;
    text-align: center;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    letter-spacing: 1px;
}

.foto-qr-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    padding: 2rem;
    border-bottom: 1px solid rgba(255, 215, 0, 0.2);
}

.foto-container {
    display: flex;
    justify-content: center;
    align-items: center;
}

.foto-ci {
    width: 200px;
    height: 200px;
    object-fit: cover;
    border-radius: 12px;
    border: 3px solid #ffd700;
    box-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
}

.foto-placeholder {
    width: 180px;
    height: 180px;
    border-radius: 12px;
    background: linear-gradient(
        135deg,
        rgba(46, 125, 50, 0.3),
        rgba(26, 46, 26, 0.3)
    );
    border: 3px dashed rgba(255, 215, 0, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 5rem;
    color: rgba(255, 215, 0, 0.4);
}

.qr-container {
    width: 200px;
    height: 200px;
    padding: 4px;
    border: 2px solid #038730;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #ffffff;
}

.qr-code-text {
    color: #ffd700;
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: 1px;
    margin: 0;
    padding: 0.5rem 1rem;
    background: rgba(255, 215, 0, 0.1);
    border-radius: 6px;
    border: 1px solid rgba(255, 215, 0, 0.3);
}

.info-principal {
    padding: 2rem 2rem 1rem;
    text-align: center;
}

.nombre-completo {
    background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2rem;
    font-weight: 800;
    margin: 0;
    line-height: 1.2;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.cargo-especial {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    margin: 0 2rem 1.5rem;
    background: linear-gradient(
        135deg,
        rgba(255, 215, 0, 0.2),
        rgba(255, 152, 0, 0.2)
    );
    border: 2px solid #ffd700;
    border-radius: 50px;
    color: #ffd700;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.cargo-especial i {
    font-size: 1.5rem;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%,
    100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.1);
    }
}

.seccion-datos {
    padding: 1.5rem 2rem;
    border-bottom: 1px solid rgba(255, 215, 0, 0.1);
}

.seccion-datos:last-of-type {
    border-bottom: none;
}

.seccion-titulo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #e0f2f1;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(255, 215, 0, 0.3);
}

.seccion-titulo i {
    font-size: 1.5rem;
    background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.datos-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
}

.dato-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.dato-label {
    color: #a5d6a7;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.dato-valor {
    color: #e0f2f1;
    font-size: 1rem;
    font-weight: 600;
}

.dato-valor.ocupacion {
    background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}

.dato-valor.cargo-badge {
    background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
    text-transform: uppercase;
}

.documentos-grid {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.documento-item {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.documento-label {
    color: #a5d6a7;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
}

.documento-preview {
    display: flex;
    align-items: center;
}

.documento-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    background: linear-gradient(
        135deg,
        rgba(255, 215, 0, 0.1),
        rgba(158, 157, 36, 0.1)
    );
    border: 2px solid rgba(255, 215, 0, 0.3);
    border-radius: 8px;
    color: #ffd700;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
}

.documento-link:hover {
    background: linear-gradient(
        135deg,
        rgba(255, 215, 0, 0.2),
        rgba(158, 157, 36, 0.2)
    );
    border-color: #ffd700;
    transform: translateX(4px);
}

.documento-link i {
    font-size: 1.5rem;
}

.documento-vacio {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    background: rgba(255, 255, 255, 0.05);
    border: 2px dashed rgba(255, 215, 0, 0.2);
    border-radius: 8px;
    color: rgba(255, 215, 0, 0.4);
    font-style: italic;
}

.documento-vacio i {
    font-size: 1.5rem;
}

.credencial-footer {
    background: linear-gradient(
        135deg,
        rgba(26, 46, 26, 0.6),
        rgba(15, 31, 15, 0.6)
    );
    padding: 1.5rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(255, 215, 0, 0.2);
}

.fecha-emision {
    color: #a5d6a7;
    font-size: 0.875rem;
    margin: 0;
}

.estado-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 50px;
    font-weight: 700;
    font-size: 0.875rem;
}

.estado-badge.activo {
    background: linear-gradient(
        135deg,
        rgba(76, 175, 80, 0.3),
        rgba(46, 125, 50, 0.3)
    );
    border: 2px solid #4caf50;
    color: #4caf50;
}

.estado-badge.inactivo {
    background: linear-gradient(
        135deg,
        rgba(244, 67, 54, 0.3),
        rgba(211, 47, 47, 0.3)
    );
    border: 2px solid #f44336;
    color: #f44336;
}

.acciones-panel {
    background: linear-gradient(
        135deg,
        rgba(26, 46, 26, 0.8),
        rgba(15, 31, 15, 0.8)
    );
    border-radius: 16px;
    padding: 1.5rem;
    border: 3px solid transparent;
    border-image: linear-gradient(135deg, #2e7d32, #9e9d24, #ffd700) 1;
    height: fit-content;
    position: sticky;
    top: 2rem;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
}

.panel-titulo {
    background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 1.25rem;
    font-weight: 800;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 3px solid #ffd700;
}

.action-button {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.875rem 1rem;
    margin-bottom: 0.75rem;
    border: 2px solid rgba(255, 215, 0, 0.3);
    border-radius: 10px;
    background: linear-gradient(
        135deg,
        rgba(26, 46, 26, 0.6),
        rgba(15, 31, 15, 0.6)
    );
    color: #e0f2f1;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.action-button:hover {
    transform: translateX(8px);
    box-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
    background: linear-gradient(
        135deg,
        rgba(46, 125, 50, 0.3),
        rgba(158, 157, 36, 0.2)
    );
}

.action-button i {
    font-size: 1.5rem;
    transition: all 0.3s ease;
}

.action-button:hover i {
    transform: scale(1.2);
}

.action-button.editar:hover {
    border-color: #ffd700;
    color: #ffd700;
}

.action-button.dispositivos:hover {
    border-color: #4caf50;
    color: #4caf50;
}

.action-button.asistencias:hover {
    border-color: #ff9800;
    color: #ff9800;
}

.action-button.desactivar:hover {
    border-color: #ff5722;
    color: #ff5722;
}

.action-button.activar:hover {
    border-color: #4caf50;
    color: #4caf50;
}

.action-button.eliminar:hover {
    border-color: #f44336;
    color: #f44336;
}

/* Modal Styles */
.modal-large .modal-card {
    width: 90%;
    max-width: 900px;
}

.modal-card-head {
    background: linear-gradient(135deg, #1a2e1a 0%, #0f1f0f 100%);
    border-bottom: 2px solid #ffd700;
}

.modal-card-title {
    background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #9e9d24 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
}

.modal-card-body {
    background: linear-gradient(
        135deg,
        rgba(26, 46, 26, 0.9),
        rgba(15, 31, 15, 0.9)
    );
    color: #e0f2f1;
    max-height: 80vh;
    overflow-y: auto;
}

.modal-card-foot {
    background: linear-gradient(
        135deg,
        rgba(26, 46, 26, 0.8),
        rgba(15, 31, 15, 0.8)
    );
    border-top: 1px solid rgba(255, 215, 0, 0.3);
}

.button.is-danger {
    background: linear-gradient(135deg, #f44336, #d32f2f);
    color: white;
    border: none;
    font-weight: 600;
}

.button.is-danger:hover {
    background: linear-gradient(135deg, #d32f2f, #c62828);
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(244, 67, 54, 0.4);
}

.button {
    background: linear-gradient(
        135deg,
        rgba(255, 215, 0, 0.2),
        rgba(158, 157, 36, 0.3)
    );
    border: 2px solid rgba(255, 215, 0, 0.4);
    color: #ffd700;
    font-weight: 600;
    transition: all 0.3s ease;
}

.button:hover {
    background: linear-gradient(
        135deg,
        rgba(255, 215, 0, 0.3),
        rgba(158, 157, 36, 0.4)
    );
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}

@media screen and (max-width: 1023px) {
    .detalle-container {
        grid-template-columns: 1fr;
    }

    .acciones-panel {
        position: static;
    }

    .datos-grid {
        grid-template-columns: 1fr;
    }

    .foto-qr-section {
        grid-template-columns: 1fr;
    }
}

@media screen and (max-width: 768px) {
    .detalle-cooperativista-page {
        padding: 1rem;
        margin: -1.5rem -1rem;
    }

    .credencial-header {
        height: 150px;
    }

    .logo-circle {
        width: 60px;
        height: 60px;
        font-size: 2rem;
    }

    .cooperativa-nombre {
        font-size: 1.2rem;
    }

    .nombre-completo {
        font-size: 1.4rem;
    }
}

/* Estilos para Sección Protegida de Gestora */
.seccion-protegida {
    background: linear-gradient(
        135deg,
        rgba(255, 215, 0, 0.08) 0%,
        rgba(158, 157, 36, 0.08) 100%
    );
    border: 2px solid rgba(255, 215, 0, 0.4) !important;
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.15);
}

.seccion-header-protegida {
    display: flex;
    align-items: center;
    margin-bottom: 1.5rem;
}

.seccion-header-protegida .seccion-titulo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-grow: 1;
}

.tag-protegido {
    background: linear-gradient(135deg, #ff9800, #ff6f00);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    box-shadow: 0 2px 8px rgba(255, 152, 0, 0.3);
}

.bloqueo-gestora {
    text-align: center;
    padding: 2rem;
}

.icono-bloqueo {
    font-size: 4rem;
    color: rgba(255, 215, 0, 0.6);
    margin-bottom: 1rem;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%,
    100% {
        opacity: 0.6;
        transform: scale(1);
    }
    50% {
        opacity: 1;
        transform: scale(1.1);
    }
}

.texto-bloqueo {
    color: #c8e6c9;
    margin-bottom: 1.5rem;
    font-size: 1rem;
}

.field-verificacion {
    max-width: 400px;
    margin: 0 auto;
}

.control {
    position: relative;
}

.control.has-icons-left .input {
    padding-left: 2.5rem;
}

.control.has-icons-left .icon {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
}

.icon {
    color: rgba(255, 215, 0, 0.6);
}

.input-verificacion {
    background: rgba(15, 31, 15, 0.7);
    border: 2px solid rgba(255, 215, 0, 0.3);
    color: #e0f2f1;
    font-size: 1rem;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    width: 100%;
    text-align: center;
}

.input-verificacion:focus {
    outline: none;
    border-color: #ffd700;
    box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
}

.button-desbloquear {
    margin-top: 1rem;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: linear-gradient(135deg, #ffd700 0%, #ff9800 50%, #ff6f00 100%);
    color: #0d1b0d;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4);
}

.button-desbloquear:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(255, 215, 0, 0.6);
}

.button-desbloquear:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.help.is-danger {
    color: #ff5252;
    font-weight: 600;
    text-align: center;
    margin-top: 0.5rem;
}

.campos-gestora-desbloqueados {
    animation: fadeIn 0.4s ease-in-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.estado-desbloqueado {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
    padding: 0.75rem;
    background: linear-gradient(
        135deg,
        rgba(76, 175, 80, 0.15),
        rgba(56, 142, 60, 0.15)
    );
    border: 2px solid rgba(76, 175, 80, 0.4);
    border-radius: 8px;
    color: #81c784;
    font-weight: 600;
}

.estado-desbloqueado i {
    font-size: 1.5rem;
    color: #66bb6a;
}

.button-bloquear {
    background: rgba(255, 215, 0, 0.1);
    color: #ffd700;
    border: 1px solid rgba(255, 215, 0, 0.3);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
}

.button-bloquear:hover {
    background: rgba(255, 215, 0, 0.2);
    border-color: #ffd700;
}

.dato-protegido {
    background: linear-gradient(
        135deg,
        rgba(255, 215, 0, 0.05),
        rgba(158, 157, 36, 0.05)
    );
    border-left: 3px solid rgba(255, 215, 0, 0.5);
}

.dato-password {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: "Courier New", monospace;
}

.toggle-password {
    background: rgba(255, 215, 0, 0.1);
    border: 1px solid rgba(255, 215, 0, 0.3);
    color: #ffd700;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
}

.toggle-password:hover {
    background: rgba(255, 215, 0, 0.2);
    border-color: #ffd700;
    transform: scale(1.1);
}

.nota-seguridad {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    margin-top: 1rem;
    padding: 0.75rem;
    background: rgba(33, 150, 243, 0.1);
    border-left: 3px solid rgba(33, 150, 243, 0.5);
    border-radius: 4px;
    color: #90caf9;
    font-size: 0.875rem;
}

.nota-seguridad i {
    font-size: 1.25rem;
    margin-top: 0.1rem;
    flex-shrink: 0;
}
</style>
