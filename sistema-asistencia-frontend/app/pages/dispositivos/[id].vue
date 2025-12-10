<template>
    <div class="dispositivos-detail">
        <div class="container">
            <div class="header">
                <NuxtLink to="/dispositivos" class="back-btn">← Volver</NuxtLink>
                <h1>Detalles del Dispositivo</h1>
            </div>

            <div v-if="loading" class="loading">Cargando...</div>
            
            <div v-else-if="dispositivo" class="content">
                <div class="card">
                    <div class="form-group">
                        <label>ID:</label>
                        <p>{{ dispositivo.id }}</p>
                    </div>
                    <div class="form-group"></div>
                        <label>Nombre:</label>
                        <p>{{ dispositivo.nombre }}</p>
                    </div>
                    <div class="form-group">
                        <label>Tipo:</label>
                        <p>{{ dispositivo.tipo }}</p>
                    </div>
                    <div class="form-group">
                        <label>Estado:</label>
                        <p :class="dispositivo.estado">{{ dispositivo.estado }}</p>
                    </div>
                    <div class="form-group">
                        <label>Última Sincronización:</label>
                        <p>{{ formatDate(dispositivo.ultimaSincronizacion) }}</p>
                    </div>
                </div>

                <div class="actions">
                    <button @click="editarDispositivo" class="btn-primary">Editar</button>
                    <button @click="eliminarDispositivo" class="btn-danger">Eliminar</button>
                </div>
            </div>
        </div>
</template>

<script setup>
definePageMeta({
    middleware: 'auth'
});

const route = useRoute();
const router = useRouter();
const dispositivo = ref(null);
const loading = ref(true);

const id = route.params.id;

onMounted(async () => {
    try {
        const { data } = await $fetch(`/api/dispositivos/${id}`);
        dispositivo.value = data;
    } catch (error) {
        console.error('Error al cargar dispositivo:', error);
    } finally {
        loading.value = false;
    }
});

const formatDate = (date) => {
    return new Date(date).toLocaleDateString('es-ES');
};

const editarDispositivo = () => {
    router.push(`/dispositivos/${id}/editar`);
};

const eliminarDispositivo = async () => {
    if (confirm('¿Está seguro de que desea eliminar este dispositivo?')) {
        try {
            await $fetch(`/api/dispositivos/${id}`, { method: 'DELETE' });
            router.push('/dispositivos');
        } catch (error) {
            console.error('Error al eliminar:', error);
        }
    }
};
</script>

<style scoped>
.dispositivos-detail {
    padding: 20px;
}

.header {
    margin-bottom: 30px;
}

.back-btn {
    color: #0066cc;
    text-decoration: none;
    margin-bottom: 10px;
    display: inline-block;
}

.card {
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    font-weight: bold;
    display: block;
    margin-bottom: 5px;
}

.actions {
    display: flex;
    gap: 10px;
}

.btn-primary,
.btn-danger {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.btn-primary {
    background: #0066cc;
    color: white;
}

.btn-danger {
    background: #dc3545;
    color: white;
}

.loading,
.error {
    text-align: center;
    padding: 20px;
}
</style>