const placeholders = {
    "text/plain": "Hola Mundo",
    "application/json": JSON.stringify({
        nombre: "Franciel",
        framework: "MiniHTTP"
    }, null, 4),
    "application/x-www-form-urlencoded": "nombre=Franciel&framework=MiniHTTP"
};

document.addEventListener("DOMContentLoaded", () => {

    cambiarPlaceholder();

    document.getElementById("endpoint")
        .addEventListener("input", actualizarInspector);

    document.getElementById("body-content")
        .addEventListener("input", actualizarInspector);

});

function obtenerContentTypeSeleccionado(){

    return document.querySelector(
        'input[name="content-type"]:checked'
    ).value;

}

function cambiarPlaceholder(){

    const tipo = obtenerContentTypeSeleccionado();

    const textarea = document.getElementById("body-content");

    textarea.placeholder = placeholders[tipo];

    actualizarInspector();

}

function actualizarInspector(){

    let endpoint = document.getElementById("endpoint").value.trim();

    if(endpoint === "")
        endpoint = "/";

    if(!endpoint.startsWith("/"))
        endpoint = "/" + endpoint;

    const body = document.getElementById("body-content").value;

    const tipo = obtenerContentTypeSeleccionado();

    const inspector = document.getElementById("raw-request");

    inspector.textContent =
`POST ${endpoint} HTTP/1.1
Host: ${location.host}
Content-Type: ${tipo}
Content-Length: ${new Blob([body]).size}

${body}`;
}

async function enviarPOST() {
    const endpointInput = document.getElementById("endpoint");
    const errorSpan = document.getElementById("endpoint-error");
    const warningSpan = document.getElementById("body-warning");
    const submitBtn = document.getElementById("btn-submit");
    
    const endpoint = endpointInput.value.trim();
    const selectedType = obtenerContentTypeSeleccionado();
    const bodyContent = document.getElementById("body-content").value;

    // Validación de Endpoint vacío
    if (!endpoint) {
        errorSpan.innerText = "Debe ingresar una ruta.";
        endpointInput.focus();
        return;
    } else {
        errorSpan.innerText = "";
    }

    // Validación de Body vacío (No bloqueante)
    if (!bodyContent) {
        warningSpan.innerText = "Se enviará un Body vacío.";
    } else {
        warningSpan.innerText = "";
    }

    // Interfaz en modo de carga
    submitBtn.innerText = "Enviando...";
    submitBtn.disabled = true;

    // --- AQUÍ SE DEFINE LA VARIABLE QUE FALTABA ---
    const startTime = performance.now();

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": selectedType
            },
            body: bodyContent || null
        });

        const endTime = performance.now();
        const duration = Math.round(endTime - startTime);

        // Comprobación de cabecera para descargas
        const contentDisposition = response.headers.get("content-disposition");
        
        if (contentDisposition && contentDisposition.includes("attachment")) {
            let nombreArchivo = "archivo_descargado";
            const match = contentDisposition.match(/filename="?([^"]+)"?/);
            if (match && match[1]) nombreArchivo = match[1];

            const blob = await response.blob();
            const urlTemporal = window.URL.createObjectURL(blob);
            const enlaceInvisible = document.createElement("a");
            enlaceInvisible.href = urlTemporal;
            enlaceInvisible.download = nombreArchivo;
            
            document.body.appendChild(enlaceInvisible);
            enlaceInvisible.click();
            enlaceInvisible.remove();
            window.URL.revokeObjectURL(urlTemporal);

            mostrarRespuesta(response, `[Archivo descargado con éxito: ${nombreArchivo}]`, duration);
        } else {
            const responseBody = await response.text();
            mostrarRespuesta(response, responseBody, duration);
        }

        agregarLog(endpoint, response.status, response.statusText);

    } catch (error) {
        const endTime = performance.now();
        const duration = Math.round(endTime - startTime);
        mostrarError(error, duration);
        agregarLog(endpoint, "ERR", "Network Error");
    } finally {
        submitBtn.innerText = "Enviar POST";
        submitBtn.disabled = false;
    }
}

function mostrarRespuesta(response,body,tiempo){

    document.getElementById("res-status").textContent =
        `${response.status} ${response.statusText}`;

    document.getElementById("res-time").textContent =
        `${tiempo} ms`;

    document.getElementById("res-type").textContent =
        response.headers.get("Content-Type") || "--";

    document.getElementById("res-body").textContent =
        body;

}

function mostrarError(error){

    document.getElementById("res-status").textContent =
        "ERROR";

    document.getElementById("res-time").textContent =
        "--";

    document.getElementById("res-type").textContent =
        "--";

    document.getElementById("res-body").textContent =
        error.message;

}

function agregarLog(endpoint,status,text){

    const consola =
        document.getElementById("console-log");

    const hora =
        new Date().toLocaleTimeString();

    consola.innerHTML +=

`<div class="log-line">
${hora} |
<strong>POST</strong> |
${endpoint} |
${status} ${text}
</div>`;

    consola.scrollTop = consola.scrollHeight;

}

function limpiarFormulario(){

    document.getElementById("tester-form").reset();

    document.getElementById("res-status").textContent="--";
    document.getElementById("res-time").textContent="0 ms";
    document.getElementById("res-type").textContent="--";
    document.getElementById("res-body").textContent="Esperando petición...";

    document.getElementById("endpoint-error").textContent="";
    document.getElementById("body-warning").textContent="";

    cambiarPlaceholder();

}

async function copiarRespuesta(){

    await navigator.clipboard.writeText(
        document.getElementById("res-body").textContent
    );

    console.log("Respuesta copiada");

}