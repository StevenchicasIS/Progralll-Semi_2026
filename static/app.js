async function login() {
    const u = document.getElementById('u').value;
    const p = document.getElementById('p').value;
    const res = await fetch('/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({usuario: u, clave: p})
    });
    const data = await res.json();
    if (data.status === 'success') window.location.href = data.url;
    else document.getElementById('err-msg').innerText = data.msj;
}

async function save() {
    const id = document.getElementById('e-id').value;
    const obj = {
        usuario: document.getElementById('f-user').value,
        clave: document.getElementById('f-pass').value,
        nombre: document.getElementById('f-name').value,
        direccion: document.getElementById('f-dir').value,
        telefono: document.getElementById('f-tel').value
    };

    if(!obj.usuario || !obj.clave || !obj.nombre) {
        alert("Por favor, llena los campos de Usuario, Clave y Nombre.");
        return;
    }

    const url = id ? `/api/update/${id}` : '/api/add';
    const method = id ? 'PUT' : 'POST';
    
    try {
        const res = await fetch(url, { 
            method: method, 
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify(obj) 
        });
        
        const data = await res.json();
        
        if (res.ok && data.ok) { 
            alert(id ? "Usuario actualizado correctamente" : "Usuario guardado con éxito");
            reset(); 
            load(); 
        } else {
            alert("Error al guardar: " + (data.error || "Revisa la consola de Python"));
        }
    } catch (error) {
        console.error("Error de red:", error);
        alert("Error de conexión con el servidor.");
    }
}

async function load() {
    const q = document.getElementById('search').value;
    try {
        const res = await fetch(`/api/get?q=${q}`);
        if (!res.ok) return; 
        
        const arr = await res.json();
        const tb = document.getElementById('tb');
        tb.innerHTML = '';
        
        arr.forEach(x => {
            // Escapamos comillas para evitar errores si el nombre tiene ' (ej. O'Brian)
            const safeUser = x.usuario.replace(/'/g, "\\'");
            const safePass = x.clave.replace(/'/g, "\\'");
            const safeName = x.nombre.replace(/'/g, "\\'");
            const safeDir = (x['dirección'] || '').replace(/'/g, "\\'");
            const safeTel = (x['teléfono'] || '').replace(/'/g, "\\'");

            tb.innerHTML += `
                <tr>
                    <td>${x.idUsuario}</td>
                    <td>${x.usuario}</td>
                    <td>${x.nombre}</td>
                    <td>${x['dirección'] || ''}</td>
                    <td>${x['teléfono'] || ''}</td>
                    <td class="action-btns">
                        <button onclick="edit(${x.idUsuario}, '${safeUser}', '${safePass}', '${safeName}', '${safeDir}', '${safeTel}')">Editar</button>
                        <button onclick="del(${x.idUsuario})" class="btn-danger">Eliminar</button>
                    </td>
                </tr>`;
        });
    } catch (error) {
        console.error("Error al cargar los datos:", error);
    }
}

async function del(id) {
    if (!confirm('¿Estás seguro de eliminar este usuario?')) return;
    await fetch(`/api/del/${id}`, { method: 'DELETE' });
    load();
}

function edit(id, u, p, n, d, t) {
    document.getElementById('e-id').value = id;
    document.getElementById('f-user').value = u;
    document.getElementById('f-pass').value = p;
    document.getElementById('f-name').value = n;
    document.getElementById('f-dir').value = d;
    document.getElementById('f-tel').value = t;
    document.getElementById('btn-cancel').classList.remove('hide');
}

function reset() {
    document.getElementById('e-id').value = '';
    document.getElementById('f-user').value = '';
    document.getElementById('f-pass').value = '';
    document.getElementById('f-name').value = '';
    document.getElementById('f-dir').value = '';
    document.getElementById('f-tel').value = '';
    document.getElementById('btn-cancel').classList.add('hide');
}


if (document.getElementById('v-panel') && !document.getElementById('v-panel').classList.contains('hide')) {
    load();
}