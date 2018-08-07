$(document).on('ready', () => {
    //#region Variables App
    var vActivo = 0;
    var url = '';
    var metodo = '';
    var data = {};
    var token = $('input[name="csrfmiddlewaretoken"]');
    var dns = window.location.protocol+"//"+window.location.host;
    var id = $('input[name="id"]');
    //#endregion

    //#region Código para Puestos de Trabajo
    //#region Variables
    var pt_nombre = $('input[name="pt_nombre"]');
    var pt_desc = $('input[name="pt_descripcion"]');
    var pt_activo = $('input[name="pt_activo"]');
    //var token = $('input[name="csrfmiddlewaretoken"]');
    //#endregion
    //#region Eventos Controles
    $('#btnptGuardar').on('click', (e) => {
        e.preventDefault();
        url = '/guardar/puesto/';
        metodo = 'POST';
        if (validarptDatos() != false) {
            if (pt_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'nombre':pt_nombre.val(),
                'descripcion': pt_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Puesto de Trabajo", false, '');
        }
    });

    $('#btnptActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/puesto/';
        metodo = 'POST';
        if (validarptDatos() != false) {
            if (pt_activo.is(":checked")) {
                console.log("Verdadero");
                vActivo = 1;
            } else {
                console.log("Falso");
                vActivo = 0;
            }
            data = {
                'id': id.val(),
                'nombre':pt_nombre.val(),
                'desc': pt_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Puesto de Trabajo", true, "/listar/puestos-trabajo/");
        }
    });
    $('#btnptCancelar').on('click', function(e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/puestos-trabajo/");
    });
    //#endregion
    //#region Validación
    function validarptDatos() {
        $('div').removeClass('has-warning');

        if (pt_nombre.val().length == 0) {
            mensaje("Registro de Puesto de trabajo", "El campo 'Nombre' es obligatorio.", "warning");
            return false;
        }
        if (pt_desc.val().length == 0) {
            mensaje("Registro de Puesto de trabajo", "El campo 'Descripción' es obligatorio.", "warning");
            return false;
        }
        return true;
    }
    //#endregion
    //#endregion Fin código de Puestos de Trabajo
    
//#region Código para Centros de Costos

    //#region Variables
    var cc_desc = $('input[name="cc_descripcion"]');
    var cc_activo = $('input[name="cc_activo"]');
    //#endregion

    //#region Eventos Controles
    $('#btnccGuardar').on('click', (e) => {
        e.preventDefault();
        url = '/guardar/centro-costo/';
        metodo = 'POST';
        if (validarccDatos() != false) {
            if (cc_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'descripcion': cc_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Centro de Costos");
        }
    });

    $('#btnccActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/centro-costo/';
        metodo = 'POST';
        if (validarccDatos() != false) {
            if (cc_activo.is(":checked")) {
                console.log("Verdadero");
                vActivo = 1;
            } else {
                console.log("Falso");
                vActivo = 0;
            }
            data = {
                'id': id.val(),
                'desc': cc_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Centro de Costos", true, "/listar/centro-costos/");
        }
    });
    

    $('#btnccCancelar').on('click', (e) => {
        e.preventDefault();
        window.location.replace(dns + "/listar/centro-costos/");
    });
    //#endregion

    //#region Validación
    function validarccDatos() {
        $('div').removeClass('has-warning');

        if (cc_desc.val().length == 0) {
            mensaje("Registro de Centro de Costos", "El campo 'Descripción' es obligatorio.", "warning");
            return false;
        }
        if (cc_desc.val().length > 250) {
            mensaje("Registro de Centro de Costos", "El campo 'Descripción' solo es de 250 caracteres.", "warning");
            return false;
        }
        return true;
    }
    //#endregion

//#endregion Fin código para Centros de Costos

//#region Código para registro de Países

    //#region Variables
    var p_codigo = $('input[name="p_codigo"]');
    var p_nombre = $('input[name="p_nombre"]');
    var p_activo = $('input[name="p_activo"]');
    //#endregion

    //#region Eventos Controles
    $('#btnpGuardar').on('click', (e) => {
        e.preventDefault();
        url = '/guardar/pais/';
        metodo = 'POST';
        if (validarpDatos() != false) {
            if (p_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'codigo': p_codigo.val(),
                'nombre': p_nombre.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "País");
        }
    });

    $('#btnpActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/pais/';
        metodo = 'POST';
        if (validarpDatos() != false) {
            if (p_activo.is(":checked")) {
                console.log("Verdadero");
                vActivo = 1;
            } else {
                console.log("Falso");
                vActivo = 0;
            }
            data = {
                'id': id.val(),
                'codigo': p_codigo.val(),
                'nombre': p_nombre.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Países", true, "/listar/paises/");
        }
    });

    $('#btnpCancelar').on('click', (e) => {
        e.preventDefault();
        window.location.replace(dns + "/listar/paises/");
    });
    //#endregion

    //#region Validación
    function validarpDatos() {
        $('div').removeClass('has-warning');

        if (p_codigo.val().length == 0) {
            mensaje("Registro de Centro de Costos", "El campo 'Código' es obligatorio.", "warning");
            return false;
        }
        if (p_nombre.val().length == 0) {
            mensaje("Registro de Centro de Costos", "El campo 'Nombre' es obligatorio.", "warning");
            return false;
        }
        if (p_codigo.val().length > 5) {
            mensaje("Registro de Centro de Costos", "El campo 'Código' solo es de 5 caracteres.", "warning");
            return false;
        }
        if (p_nombre.val().length > 150) {
            mensaje("Registro de Centro de Costos", "El campo 'Nombre' solo es de 5 caracteres.", "warning");
            return false;
        }
        return true;
    }
    //#endregion

//#endregion Fin código para registro de Países

//#region Código para registro de Departamentos / Estados

//#region Variables
    var dept_codigo = $('input[name="dept_codigo"]');
    var dept_nombre = $('input[name="dept_nombre"]');
    var dept_activo = $('input[name="dept_activo"]');
//#endregion

//#region Eventos Controles

    $('#btndeptGuardar').on('click', (e) => {
        e.preventDefault();
        url = '/guardar/depto-pais/';
        metodo = 'POST';
        if (validardeptDatos() != false) {
            if (dept_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'codigo': dept_codigo.val(),
                'nombre': dept_nombre.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Departamento/Estado");
        }
    });

    $('#btndeptActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/deptos-pais/';
        metodo = 'POST';
        if (validardeptDatos() != false) {
            if (dept_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'id': id.val(),
                'codigo': dept_codigo.val(),
                'nombre': dept_nombre.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Departamento/Estado", true, "/listar/deptos-estados/");
        }
    });

    $('#btndeptCancelar').on('click', (e) => {
        e.preventDefault();
        window.location.replace(dns + "/listar/deptos-estados/");
    });
//#endregion

//#region Validación
    function validardeptDatos() {
        $('div').removeClass('has-warning');
        if (dept_codigo.val().length == 0) {
            mensaje("Registro de Departamentos/Estado", "El campo 'Código' es obligatorio.", "warning");
            return false;
        }
        if (dept_nombre.val().length == 0) {
            mensaje("Registro de Departamentos/Estado", "El campo 'Nombre' es obligatorio.", "warning");
            return false;
        }
        if (dept_codigo.val().length > 5) {
            mensaje("Registro de Departamentos/Estado", "El campo 'Código' solo es de 5 caracteres.", "warning");
            return false;
        }
        if (dept_nombre.val().length > 150) {
            mensaje("Registro de Departamentos/Estado", "El campo 'Nombre' solo es de 5 caracteres.", "warning");
            return false;
        }
        return true;
    }
//#endregion

//#endregion

//#region Código para registro de Ciudades

//#region Variables
    var cdd_ID = $('input[name="cdd_ID"]');
    var cdd_nombre = $('input[name="cdd_nombre"]');
    var cdd_activo = $('input[name="cdd_activo"]');
//#endregion

//#region Eventos Controles

    $('#btncddGuardar').on('click', (e) => {
        e.preventDefault();
        url = '/guardar/ciudad/';
        metodo = 'POST';
        if (validarcddDatos() != false) {
            if (cdd_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'ID': cdd_ID.val(),
                'nombre': cdd_nombre.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Ciudades");
        }
    });

    $('#btncddActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/ciudad/';
        metodo = 'POST';
        if (validarcddDatos() != false) {
            if (cdd_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'id': id.val(),
                'ID': cdd_ID.val(),
                'nombre': cdd_nombre.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Ciudades", true, "/listar/ciudades/");
        }
    });

    $('#btncddCancelar').on('click', (e) => {
        e.preventDefault();
        window.location.replace(dns + "/listar/ciudades/");
    });

//#endregion

//#region Validación
function validarcddDatos() {
    $('div').removeClass('has-warning');
    if (cdd_ID.val().length == 0) {
        mensaje("Registro de Departamentos/Estado", "El campo 'Código' es obligatorio.", "warning");
        return false;
    }
    if (cdd_nombre.val().length == 0) {
        mensaje("Registro de Departamentos/Estado", "El campo 'Nombre' es obligatorio.", "warning");
        return false;
    }
    if (cdd_ID.val().length > 5) {
        mensaje("Registro de Departamentos/Estado", "El campo 'Código' solo es de 5 caracteres.", "warning");
        return false;
    }
    if (cdd_nombre.val().length > 150) {
        mensaje("Registro de Departamentos/Estado", "El campo 'Nombre' solo es de 5 caracteres.", "warning");
        return false;
    }
    return true;
}
//#endregion

//#endregion Código para registro de Ciudades

//#region Código para registrar Géneros

//#region Variables
    var gnr_desc = $('input[name="gnr_desc"]');
    var gnr_activo = $('input[name="gnr_activo"]');
//#endregion

//#region Eventos Controles

    $('#btngnrGuardar').on('click', (e) => {
        e.preventDefault();
        url = '/guardar/genero/';
        metodo = 'POST';
        if (validargnrDatos() != false) {
            if (gnr_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'desc': gnr_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Géneros");
        }
    });

    $('#btngnrActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/genero/';
        metodo = 'POST';
        if (validargnrDatos() != false) {
            if (gnr_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'id': id.val(),
                'desc': gnr_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Géneros", true, "/listar/generos/");
        }
    });

    $('#btngnrCancelar').on('click', (e) => {
        e.preventDefault();
        window.location.replace(dns + "/listar/generos/");
    });

//#endregion Eventos Controles

//#region Validación
function validargnrDatos() {
    $('div').removeClass('has-warning');
    if (gnr_desc.val().length == 0) {
        mensaje("Registro de Géneros", "El campo 'Descripción' es obligatorio.", "warning");
        return false;
    }
    if (gnr_desc.val().length > 25) {
        mensaje("Registro de Géneros", "El campo 'Código' solo es de 5 caracteres.", "warning");
        return false;
    }
    return true;
}

//#endregion Código para registrar Géneros

//#region Código para registrar Estado Civil

    //#region Variables
    var estcv_desc = $('input[name="estcv_desc"]');
    var estcv_activo = $('input[name="estcv_activo"]');
    //#endregion

    //#region Eventos Controles
    $('#btnestcvGuardar').on('click', function(e) {
        e.preventDefault();
        url = '/guardar/estado-civil/';
        metodo = 'POST';
        if (validarestcvDatos() != false) {
            if (estcv_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'desc': estcv_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Estado Civil");
        }
    });

    $('#btnestcvActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/estado-civil/';
        metodo = 'POST';
        if (validarestcvDatos() != false) {
            if (estcv_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'id': id.val(),
                'desc': estcv_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Estado Civil", true, "/listar/estado-civil/");
        }
    });

    $('#btnestcvCancelar').on('click', (e) => {
        e.preventDefault();
        window.location.replace(dns + "/listar/estado-civil/");
    });
    //#endregion

    //#region Validación
    function validarestcvDatos() {
        $('div').removeClass('has-warning');
        if (estcv_desc.val().length == 0) {
            mensaje("Registro de Estado Civil", "El campo 'Descripción' es obligatorio.", "warning");
            return false;
        }
        if (estcv_desc.val().length > 50) {
            mensaje("Registro de Estado Civil", "El campo 'Descripción' solo es de 50 caracteres.", "warning");
            return false;
        }
        return true;
    }
    //#endregion

//#endregion Código para registrar Estado Civil

//#region Código para registrar Parentesco

    //#region Variables
    var parnt_desc = $('input[name="parent_desc"]');
    var parnt_activo = $('input[name="parent_activo"]');
    //#endregion

    //#region Eventos Controles
    $('#btnparentGuardar').on('click', function(e) {
        e.preventDefault();
        url = '/guardar/parentesco/';
        metodo = 'POST';
        if (validarparntDatos() != false) {
            if (parnt_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'desc': parnt_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Parentesco");
        }
    });

    $('#btnparentActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/parentesco/';
        metodo = 'POST';
        if (validarparntDatos() != false) {
            if (parnt_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'id': id.val(),
                'desc': parnt_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Parentesco", true, "/listar/parentesco/");
        }
    });

    $('#btnparentCancelar').on('click', (e) => {
        e.preventDefault();
        window.location.replace(dns + "/listar/parentesco/");
    });
    //#endregion

    //#region Validación
    function validarparntDatos() {
        $('div').removeClass('has-warning');
        if (parnt_desc.val().length == 0) {
            mensaje("Registro de Parentesco", "El campo 'Descripción' es obligatorio.", "warning");
            return false;
        }
        if (parnt_desc.val().length > 50) {
            mensaje("Registro de Parentesco", "El campo 'Descripción' solo es de 50 caracteres.", "warning");
            return false;
        }
        return true;
    }
    //#endregion

//#endregion

//#region Código para registra Función de Trabajo

    //#region Variables
    var fun_nombre = $('input[name="fun_desc"]');
    var fun_desc = $('input[name="fun_desc"]');
    var fun_activo = $('input[name="fun_activo"]');
    //#endregion

    //#region Eventos Controles
    $('#btnfunGuardar').on('click', function(e) {
        e.preventDefault();
        url = '/guardar/funcion/';
        metodo = 'POST';
        if (validarfunDatos() != false) {
            if (fun_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'nombre': fun_nombre.val(),
                'desc': fun_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Función de Trabajo");
        }
    });

    $('#btnfunActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/funcion/';
        metodo = 'POST';
        if (validarfunDatos() != false) {
            if (fun_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'id': id.val(),
                'nombre': fun_nombre.val(),
                'desc': fun_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Función de Trabajo", true, "/listar/funciones/");
        }
    });

    $('#btnfunCancelar').on('click', (e) => {
        e.preventDefault();
        window.location.replace(dns + "/listar/funciones/");
    });
    //#endregion

    //#region Validación
    function validarfunDatos() {
        $('div').removeClass('has-warning');
        if (fun_nombre.val().length == 0) {
            mensaje("Registro de Función de Trabajo", "El campo 'Nombre' es obligatorio.", "warning");
            return false;
        }
        if (fun_nombre.val().length > 50) {
            mensaje("Registro de Función de Trabajo", "El campo 'Nombre' solo es de 50 caracteres.", "warning");
            return false;
        }
        if (fun_desc.val().length == 0) {
            mensaje("Registro de Función de Trabajo", "El campo 'Descripción' es obligatorio.", "warning");
            return false;
        }
        if (fun_desc.val().length > 150) {
            mensaje("Registro de Función de Trabajo", "El campo 'Descripción' solo es de 150 caracteres.", "warning");
            return false;
        }
        return true;
    }
    //#endregion

//#endregion

//#region Código para registro de Equipo de Trabajo

    //#region Variables
    var eqT_nombre = $('input[name="eqT_desc"]');
    var eqT_desc = $('input[name="eqT_desc"]');
    var eqT_activo = $('input[name="eqT_activo"]');
    //#endregion

    //#region Eventos Controles
    $('#btneqTGuardar').on('click', function(e) {
        e.preventDefault();
        url = '/guardar/equipo/';
        metodo = 'POST';
        if (validareqDatos() != false) {
            if (eqT_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'nombre': eqT_nombre.val(),
                'desc': eqT_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Equipos de Trabajo");
        }
    });

    $('#btneqTActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/equipo/';
        metodo = 'POST';
        if (validareqDatos() != false) {
            if (eqT_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'id': id.val(),
                'nombre': eqT_nombre.val(),
                'desc': eqT_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Equipos de Trabajo", true, "/listar/equipos/");
        }
    });

    $('#btneqTCancelar').on('click', (e) => {
        e.preventDefault();
        window.location.replace(dns + "/listar/equipos/");
    });
    //#endregion

    //#region Validación
    function validareqDatos() {
        $('div').removeClass('has-warning');
        if (eqT_nombre.val().length == 0) {
            mensaje("Registro de Equipo de Trabajo", "El campo 'Nombre' es obligatorio.", "warning");
            return false;
        }
        if (eqT_nombre.val().length > 50) {
            mensaje("Registro de Equipo de Trabajo", "El campo 'Nombre' solo es de 50 caracteres.", "warning");
            return false;
        }
        if (eqT_desc.val().length == 0) {
            mensaje("Registro de Equipo de Trabajo", "El campo 'Descripción' es obligatorio.", "warning");
            return false;
        }
        if (eqT_desc.val().length > 150) {
            mensaje("Registro de Equipo de Trabajo", "El campo 'Descripción' solo es de 150 caracteres.", "warning");
            return false;
        }
        return true;
    }
    //#endregion

//#endregion Codigo para registro de Equipo de Trabajo

//#region Código para registrar Estatus Empleado

    //#region Variables
    var estEm_nombre = $('input[name="estEm_nombre"]');
    var estEm_desc = $('input[name="estEm_desc"]');
    var estEm_activo = $('input[name="estEm_activo"]');
    //#endregion

    //#region Eventos Controles
    $('#btnestEmGuardar').on('click', function(e) {
        e.preventDefault();
        url = '/guardar/estatus-empleado/';
        metodo = 'POST';
        if (validarestEmDatos() != false) {
            if (estEm_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'nombre': estEm_nombre.val(),
                'desc': estEm_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Estados de Empleado");
        }
    });

    $('#btnestEmActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/estatus-empleado/';
        metodo = 'POST';
        if (validarestEmDatos() != false) {
            if (estEm_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'id': id.val(),
                'nombre': estEm_nombre.val(),
                'desc': estEm_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Estados de Empleado", true, "/listar/estatus-empleado/");
        }
    });

    $('#btnestEmCancelar').on('click', (e) => {
        e.preventDefault();
        window.location.replace(dns + "/listar/estatus-empleado/");
    });
    //#endregion

    //#region Validación
    function validarestEmDatos() {
        $('div').removeClass('has-warning');
        if (estEm_nombre.val().length == 0) {
            mensaje("Registro de Estatus de Empleado", "El campo 'Nombre' es obligatorio.", "warning");
            return false;
        }
        if (estEm_nombre.val().length > 150) {
            mensaje("Registro de Estatus de Empleado", "El campo 'Nombre' solo es de 150 caracteres.", "warning");
            return false;
        }
        return true;
    }
    //#endregion

//#endregion Código para registrar Estatus Empleado

//#region Código para registrar Ausentismo

    //#region Variables
    var Au_emp = $('select[name="au_emp"]');
    var Au_desde = $('input[name="au_desde"]');
    var Au_hasta = $('input[name="au_hasta"]');
    var Au_motivo = $('textarea[name="au_motivos"]');
    var Au_aprobo = $('select[name="au_aprobo"]');
    var Au_activo = $('input[name="au_activo"]');
    //#endregion

    //#region Eventos Controles
    $('#btnAuGuardar').on('click', function(e) {
        e.preventDefault();
        url = '/guardar/ausentismo/';
        metodo = 'POST';
        if (validarAuDatos() != false) {
            if (Au_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'emp': Au_emp.val(),
                'desde': Au_desde.val(),
                'hasta': Au_hasta.val(),
                'motivo': Au_motivo.val(),
                'aprobo': Au_aprobo.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Ausentismo");
            
        }
    });

    $('#btnAuActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/ausentismo/';
        metodo = 'POST';
        if (validarAuDatos() != false) {
            if (Au_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'id': id.val(),
                'emp': Au_emp.val(),
                'desde': Au_desde.val(),
                'hasta': Au_hasta.val(),
                'motivo': Au_motivo.val(),
                'aprobo': Au_aprobo.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Ausentismo", true, "/listar/ausentismo/");
        }
    });

    $('#btnAuCancelar').on('click', function(e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/ausentismo/");
    });
    //#endregion

    //#region Validación
    function validarAuDatos() {
        $('div').removeClass('has-warning');
        // if (Au_emp.val() == 0) {
        //     mensaje("Registro de Ausentismo", "El campo 'Empleado' es obligatorio.", "warning");
        //     return false;
        // }
        if (Au_desde.val().length == 0) {
            mensaje("Registro de Ausentismo", "El campo 'Desde' es obligatorio.", "warning");
            return false;
        }
        if (Au_hasta.val().length == 0) {
            mensaje("Registro de Ausentismo", "El campo 'Hasta' es obligatorio.", "warning");
            return false;
        }
        if (Au_motivo.val().length == 0) {
            mensaje("Registro de Ausentismo", "El campo 'Motivo' es obligatorio.", "warning");
            return false;
        }

        // if (Au_aprobo.val() == 0) {
        //     mensaje("Registro de Ausentismo", "El campo 'Aprobó' es obligatorio.", "warning");
        //     return false;
        // }
        return true;
    }
    //#endregion

//#endregion Código para registrar Ausentismo

//#region Código para registrar Motivos de Ausencia

    //#region Variables
    var mAu_desc = $('input[name="mau_desc"]');
    var mAu_pagado = $('input[name="mau_pagado"]');
    var mAu_activo = $('input[name="mau_activo"]');
    var vPagado = 0;
    //#endregion

    //#region Eventos Controles
    $('#btnmAuGuardar').on('click', function(e) {
        e.preventDefault();
        url = '/guardar/motivo-ausencia/';
        metodo = 'POST';
        if (validarmAuDatos() != false) {
            if (mAu_pagado.is(":checked")) {
                vPagado = 1;
            } else {
                vPagado = 0;
            }
            if (mAu_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'desc': mAu_desc.val(),
                'pagado': vPagado,
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Motivos de Ausencia");
            
        }
    });

    $('#btnmAuActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/motivo-ausencia/';
        metodo = 'POST';
        if (validarmAuDatos() != false) {
            if (mAu_pagado.is(":checked")) {
                vPagado = 1;
            } else {
                vPagado = 0;
            }
            if (mAu_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'id': id.val(),
                'desc': mAu_desc.val(),
                'pagado': vPagado,
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Motivo de Ausencia", true, "/listar/motivos-ausencia/");
        }
    });

    $('#btnmAuCancelar').on('click', function(e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/motivos-ausencia/");
    });
    //#endregion

     //#region Validación
     function validarmAuDatos() {
        $('div').removeClass('has-warning');
        if (mAu_desc.val().length == 0) {
            mensaje("Registro de Motivos de Ausencia", "El campo 'Descripción' es obligatorio.", "warning");
            return false;
        }
        return true;
    }
    //#endregion

//#endregion Código para registrar Motivos de Ausencia

//#region Código para registrar Motivos de Despido

     //#region Variables
     var mdes_desc = $('textarea[name="mdes_desc"]');
     var mdes_nombre = $('input[name="mdes_nombre"]');
     var mdes_activo = $('input[name="mdes_activo"]');

     //#endregion

     //#region Eventos Controles
    $('#btnmDesGuardar').on('click', function(e) {
        e.preventDefault();
        url = '/guardar/motivo-despido/';
        metodo = 'POST';
        if (validarmAuDatos() != false) {
            if (mdes_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'desc': mdes_desc.val(),
                'nombre': mdes_nombre.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Motivos de Despido");
            
        }
    });

    $('#btnmDesActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/motivo-despido/';
        metodo = 'POST';
        if (validarmAuDatos() != false) {
            if (mdes_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'id': id.val(),
                'desc': mdes_desc.val(),
                'nombre': mdes_nombre.val(),
                'pagado': vPagado,
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Motivo de Despido", true, "/listar/motivos-despido/");
        }
    });

    $('#btnmDesCancelar').on('click', function(e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/motivos-despido/");
    });
    //#endregion

     //#region Validación
     function validarmAuDatos() {
        $('div').removeClass('has-warning');
        if (mdes_nombre.val().length == 0) {
            mensaje("Registro de Motivos de Despido", "El campo 'Nombre' es obligatorio.", "warning");
            return false;
        }
        return true;
    }
    //#endregion

//#endregion Código para registrar Motivos de Despido



    //#region Funciones Generales
    function GuardarRegistro(url, metodo, data, encabezado, editar, urlRedirect) {
        var texto = 'Se ha creado un nuevo registro.';
        var tiempo = 3500;
        if (editar) {
            texto = 'Se ha actualizado el registro.';
            tiempo = 2500;
        }
        $.ajax({
            type: metodo,
            url: url,
            data: data,
            success: function (data) {
                if (data.error == false) {
                    mensaje(encabezado, texto, "ok", tiempo);
                    if (editar) {
                        setTimeout(function () {
                            window.location.replace(dns + urlRedirect);
                        }, tiempo);
                    }else{
                        LimpiarControles();
                    }
                } else {
                    mensaje(encabezado, data.mensaje, "error", tiempo);
                }
            },
            error: function (data) {
                mensaje(encabezado, data.statusText, "error", tiempo);
            }
        });
    }

    function mensaje(encabezado, texto, tipomsj, tiempo) {
        vicon = "warning";
        if (tipomsj == "warning") {
            vicon = "warning";
        } else if (tipomsj == "ok") {
            vicon = "success";
        } else if (tipomsj == "error") {
            vicon = "error";
        }
        $.toast({
            heading: encabezado,
            text: texto,
            position: 'top-right',
            loaderBg: '#ff6849',
            icon: vicon,
            hideAfter: tiempo,
            stack: 6
        });
    }
    function LimpiarControles() {
        $('input[type="text"]').val(null);
        $('input[type="checkbox"]').removeAttr('checked');
        $('select').val(0);
        $('textarea').val(null);
        $('.select2').select2('val', '0');
    }
    //#endregion
});