document.addEventListener('DOMContentLoaded', () => {

    // --- Elementos del DOM ---
    const capacidadInput = document.getElementById('capacidad');
    const proyectosContainer = document.getElementById('proyectos-container');
    const addProyectoBtn = document.getElementById('add-proyecto');
    const calcularBtn = document.getElementById('calcular-btn');
    const limpiarBtn = document.getElementById('limpiar-btn');
    const resultadoContainer = document.getElementById('resultado-container');
    const resultadoContenido = document.getElementById('resultado-contenido');

    const API_URL = 'http://127.0.0.1:8000/optimizar';

    let proyectoIdCounter = 0;

    // --- Funciones ---

    /**
     * Agrega un nuevo conjunto de campos para un proyecto de inversión.
     */
    const agregarProyecto = () => {
        proyectoIdCounter++;
        const proyectoDiv = document.createElement('div');
        proyectoDiv.classList.add('proyecto-item');
        proyectoDiv.innerHTML = `
            <input type="text" placeholder="Nombre (Ej: Fondo A)" class="proyecto-nombre" value="Proyecto ${proyectoIdCounter}">
            <input type="number" placeholder="Costo" class="proyecto-peso">
            <input type="number" placeholder="Ganancia" class="proyecto-ganancia">
            <button class="btn btn-remove-proyecto">Eliminar</button>
        `;
        proyectosContainer.appendChild(proyectoDiv);

        // Event listener para el botón de eliminar
        proyectoDiv.querySelector('.btn-remove-proyecto').addEventListener('click', () => {
            proyectoDiv.remove();
        });
    };

    /**
     * Recoge los datos del formulario, los valida y los envía a la API.
     */
    const calcularOptimizacion = async () => {
        const capacidad = parseInt(capacidadInput.value, 10);

        if (isNaN(capacidad) || capacidad <= 0) {
            alert('Por favor, ingresa una capacidad (presupuesto) válida y positiva.');
            return;
        }

        const objetos = [];
        const proyectoItems = proyectosContainer.querySelectorAll('.proyecto-item');

        for (const item of proyectoItems) {
            const nombre = item.querySelector('.proyecto-nombre').value;
            const peso = parseInt(item.querySelector('.proyecto-peso').value, 10);
            const ganancia = parseInt(item.querySelector('.proyecto-ganancia').value, 10);

            if (!nombre || isNaN(peso) || isNaN(ganancia) || peso <= 0 || ganancia <= 0) {
                alert(`Datos inválidos en el proyecto "${nombre || 'sin nombre'}". Todos los campos son obligatorios y los valores numéricos deben ser positivos.`);
                return;
            }
            objetos.push({ nombre, peso, ganancia });
        }

        if (objetos.length === 0) {
            alert('Agrega al menos un proyecto de inversión.');
            return;
        }

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ capacidad, objetos }),
            });

            if (!response.ok) {
                // Intenta leer el error del cuerpo de la respuesta
                const errorData = await response.json();
                throw new Error(errorData.detail || `Error del servidor: ${response.status}`);
            }

            const resultado = await response.json();
            mostrarResultados(resultado);

        } catch (error) {
            alert(`Error al conectar con la API: ${error.message}`);
            console.error('Error en la petición fetch:', error);
        }
    };

    /**
     * Muestra los resultados de la optimización en la página.
     * @param {object} data - Los datos recibidos de la API.
     */
    const mostrarResultados = (data) => {
        resultadoContenido.innerHTML = `
            <p><strong>Proyectos Seleccionados:</strong> <span>${data.seleccionados.join(', ') || 'Ninguno'}</span></p>
            <p><strong>Ganancia Total:</strong> <span>${data.ganancia_total.toLocaleString()}</span></p>
            <p><strong>Costo Total:</strong> <span>${data.peso_total.toLocaleString()}</span></p>
        `;
        resultadoContainer.classList.remove('hidden');
    };

    /**
     * Limpia todos los campos de entrada y los resultados.
     */
    const limpiarTodo = () => {
        capacidadInput.value = '';
        proyectosContainer.innerHTML = '';
        resultadoContainer.classList.add('hidden');
        proyectoIdCounter = 0;
        agregarProyecto(); // Agrega un campo vacío para empezar
    };

    // --- Event Listeners ---
    addProyectoBtn.addEventListener('click', agregarProyecto);
    calcularBtn.addEventListener('click', calcularOptimizacion);
    limpiarBtn.addEventListener('click', limpiarTodo);

    // --- Inicialización ---
    agregarProyecto(); // Agrega el primer campo de proyecto al cargar la página
});
