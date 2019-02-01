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
    var cc_code = $('input[name="cc_codigo"]');
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
                'code': cc_code.val(),
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
                'code': cc_code.val(),
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
    var dept_pais = $('select[name="dept_pais"]');
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
                'pais': dept_pais.val(),
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
                'pais': dept_pais.val(),
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
        if (dept_pais.val() == 0) {
            mensaje("Registro de Departamentos/Estado", "El campo 'País' es un campo obligatorio.", "warning");
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
    var gnr_code = $('input[name="gnr_code"]');
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
                'code': gnr_code.val(),
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
                'code': gnr_code.val(),
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
//#endregion

//#endregion Código para registrar Géneros

//#region Código para registrar Estado Civil

    //#region Variables
    var estcv_desc = $('input[name="estcv_desc"]');
    var estcv_code = $('input[name="estcv_code"]');
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
                'code': estcv_code.val(),
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
                'code': estcv_code.val(),
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
    var parnt_code = $('input[name="parent_codigo"]');
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
                'code': parnt_code.val(),
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
                'code':parnt_code.val(),
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
    var fun_code = $('input[name="fun_code"]');
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
                'desc': fun_desc.val(),
                'code': fun_code.val(),
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
                'code': fun_code.val(),
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
    var eqT_code = $('input[name="eqT_codigo"]');
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
                'code': eqT_code.val(),
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
                'code': eqT_code.val(),
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
    var Au_motivo = $('select[name="au_motivos"]');
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
        // if (Au_motivo.val().length == 0) {
        //     mensaje("Registro de Ausentismo", "El campo 'Motivo' es obligatorio.", "warning");
        //     return false;
        // }

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
    var mAu_code = $('input[name="mau_code"]');
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
        //if (validarmAuDatos() != false) {
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
            'code': mAu_code.val(),
            'pagado': vPagado,
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Motivos de Ausencia");
            
        //}
    });

    $('#btnmAuActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/motivo-ausencia/';
        metodo = 'POST';
        //if (validarmAuDatos() != false) {
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
            'code':mAu_code.val(),
            'desc': mAu_desc.val(),
            'pagado': vPagado,
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Motivo de Ausencia", true, "/listar/motivos-ausencia/");
        //}
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
     var mdes_code = $('input[name="mdes_code"]');
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
                'code': mdes_code.val(),
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
                'code': mdes_code.val(),
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
        if (mdes_code.val().length == 0) {
            mensaje("Registro de Motivos de Despido", "El campo 'Código' es obligatorio.", "warning");
            return false;
        }
        return true;
    }
    //#endregion

//#endregion Código para registrar Motivos de Despido

//#region Código para registrar Motivos de Renuncia

    //#region Variables
    var mre_desc = $('textarea[name="mre_desc"]');
    var mre_code = $('input[name="mre_codigo"]');
    var mre_activo = $('input[name="mre_activo"]');
    //#endregion

     //#region Eventos Controles
     $('#btnmReGuardar').on('click', function(e) {
        e.preventDefault();
        url = '/guardar/motivo-renuncia/';
        metodo = 'POST';
        if (validarmReDatos() != false) {
            if (mre_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'desc': mre_desc.val(),
                'code': mre_code.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Motivos de Renuncia");
            
        }
    });

    $('#btnmReActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/motivo-renuncia/';
        metodo = 'POST';
        if (validarmReDatos() != false) {
            if (mre_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'id': id.val(),
                'desc': mre_desc.val(),
                'code': mre_code.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Motivo de Renuncia", true, "/listar/motivos-renuncia/");
        }
    });

    $('#btnmReCancelar').on('click', function(e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/motivos-renuncia/");
    });
    //#endregion

     //#region Validación
     function validarmReDatos() {
        $('div').removeClass('has-warning');
        if (mre_desc.val().length == 0) {
            mensaje("Registro de Motivos de Renuncia", "El campo 'Descripción' es obligatorio.", "warning");
            return false;
        }
        return true;
    }
    //#endregion

//#endregion Código para registrar Motivos de Renuncia

//#region Código para registrar Clases de Educación

    //#region Variables
    var clsEd_desc = $('textarea[name="clsEd_desc"]');
    var clsEd_code = $('input[name="clsEd_code"]');
    var clsEd_activo = $('input[name="clsEd_activo"]');
    //#endregion

    //#region Eventos Controles
    $('#btnclsEdGuardar').on('click', function(e) {
        e.preventDefault();
        url = '/guardar/clases-educacion/';
        metodo = 'POST';
        if (validarClsEdDatos() != false) {
            if (clsEd_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'code': clsEd_code.val(),
                'desc': clsEd_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Clase de Educación");
            
        }
    });

    $('#btnclsEdActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/clase-educacion/';
        metodo = 'POST';
        if (validarClsEdDatos() != false) {
            if (clsEd_activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }
            data = {
                'id': id.val(),
                'code': clsEd_code.val(),
                'desc': clsEd_desc.val(),
                'activo': vActivo,
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Clase de Educación", true, "/listar/clase-educacion/");
        }
    });

    $('#btnclsEdCancelar').on('click', function(e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/clase-educacion/");
    });
    //#endregion

    //#region Validación
     function validarClsEdDatos() {
        $('div').removeClass('has-warning');
        if (clsEd_code.val().length == 0) {
            mensaje("Registro de Clase de Educación", "El campo 'Código' es obligatorio.", "warning");
            return false;
        }
        if (clsEd_desc.val().length == 0) {
            mensaje("Registro de Clase de Educación", "El campo 'Descripción' es obligatorio.", "warning");
            return false;
        }
        return true;
    }
    //#endregion

//#endregion Código para registrar Clases de Educación

//#region Código para registrar Educación del Empleado

    //#region Variables
    var ed_emp = $('select[name="ed_emp"]');
    var ed_formacion = $('select[name="ed_clsEd"]');
    var ed_desde = $('input[name="ed_desde"]');
    var ed_hasta = $('input[name="ed_hasta"]');
    var ed_entidad = $('input[name="ed_ent"]');
    var ed_asignatura = $('input[name="ed_asig"]');
    var ed_titulo = $('input[name="ed_titulo"]');
    //#endregion

    //#region Eventos Controles
    $('#btnEdGuardar').on('click', function(e) {
        e.preventDefault();
        url = '/guardar/educacion/';
        metodo = 'POST';
        if (validarEdDatos() != false) {
            data = {
                'emp': ed_emp.val(),
                'formacion': ed_formacion.val(),
                'desde': ed_desde.val(),
                'hasta': ed_hasta.val(),
                'entidad': ed_entidad.val(),
                'asignatura': ed_asignatura.val(),
                'titulo': ed_titulo.val(),
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Educación");
        }
    });

    $('#btnEdActualizar').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/educacion/';
        metodo = 'POST';
        if (validarEdDatos() != false) {
            data = {
                'id': id.val(),
                'emp': ed_emp.val(),
                'formacion': ed_formacion.val(),
                'desde': ed_desde.val(),
                'hasta': ed_hasta.val(),
                'entidad': ed_entidad.val(),
                'asignatura': ed_asignatura.val(),
                'titulo': ed_titulo.val(),
                'csrfmiddlewaretoken': token.val(),
            };
            GuardarRegistro(url, metodo, data, "Educación", true, "/listar/educacion/");
        }
    });

    $('#btnEdCancelar').on('click', function(e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/educacion/");
    });
    //#endregion

    //#region Validación
    function validarEdDatos() {
        $('div').removeClass('has-warning');
        if (ed_emp.val() == 0) {
            mensaje("Registro de Educación", "El campo 'Empleado' es obligatorio.", "warning");
            return false;
        }
        if (ed_formacion.val() == 0) {
            mensaje("Registro de Educación", "El campo 'Clase de Formación' es obligatorio.", "warning");
            return false;
        }
        if (ed_desde.val().length == 0) {
            mensaje("Registro de Educación", "El campo 'Desde' es obligatorio.", "warning");
            return false;
        }
        if (ed_hasta.val().length == 0) {
            mensaje("Registro de Educación", "El campo 'Hasta' es obligatorio.", "warning");
            return false;
        }
        if (ed_entidad.val().length == 0) {
            mensaje("Registro de Educación", "El campo 'Institución' es obligatorio.", "warning");
            return false;
        }
        if (ed_asignatura.val().length == 0) {
            mensaje("Registro de Educación", "El campo 'Asignatura Principal' es obligatorio.", "warning");
            return false;
        }
        if (ed_titulo.val().length == 0) {
            mensaje("Registro de Educación", "El campo 'Título' es obligatorio.", "warning");
            return false;
        }
        return true;
    }
    //#endregion


//#endregion Código para registrar Educación del Empleado

//#region Código para registrar las Evaluaciones

//#region Variables
    var ev_emp = $('select[name="eV_emp"]');
    var ev_gerente = $('select[name="eV_gerente"]');
    var ev_fecha = $('input[name="eV_fecha"]');
    var ev_grupo = $('input[name="eV_grpsal"]');
    var ev_desc = $('textarea[name="eV_desc"]');
    var ev_coment = $('textarea[name="eV_coment"]');
//#endregion

    //#region Eventos Controles
    $('#btnEvGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/evaluacion/';
        metodo = 'POST';
        //if (validarEvDatos() != false) {
        data = {
            'emp': ev_emp.val(),
            'gerente': ev_gerente.val(),
            'fecha': ev_fecha.val(),
            'grupo_asal': ev_grupo.val(),
            'desc': ev_desc.val(),
            'coment': ev_coment.val(),
            'csrfmiddlewaretoken': token.val(),
        };     
        GuardarRegistro(url, metodo, data, "Evaluación");
        //}
    });

    $('#btnEvActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/evaluacion/';
        metodo = 'POST';
        //if (validarEvDatos() != false) {
        data = {
            'id': id.val(),
            'emp': ev_emp.val(),
            'gerente': ev_gerente.val(),
            'fecha': ev_fecha.val(),
            'grupo_asal': ev_grupo.val(),
            'desc': ev_desc.val(),
            'coment': ev_coment.val(),
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Evaluación", true, "/listar/evaluaciones/");
        //}
    });

    $('#btnEvCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/evaluaciones/");
    });
    //#endregion

    //#region Validación
    function validarEvDatos() {
        $('div').removeClass('has-warning');
        if (ed_emp.val() == 0) {
            mensaje("Registro de Educación", "El campo 'Empleado' es obligatorio.", "warning");
            return false;
        }
        if (ed_formacion.val() == 0) {
            mensaje("Registro de Educación", "El campo 'Clase de Formación' es obligatorio.", "warning");
            return false;
        }
        if (ed_desde.val().length == 0) {
            mensaje("Registro de Educación", "El campo 'Desde' es obligatorio.", "warning");
            return false;
        }
        if (ed_hasta.val().length == 0) {
            mensaje("Registro de Educación", "El campo 'Hasta' es obligatorio.", "warning");
            return false;
        }
        if (ed_entidad.val().length == 0) {
            mensaje("Registro de Educación", "El campo 'Institución' es obligatorio.", "warning");
            return false;
        }
        if (ed_asignatura.val().length == 0) {
            mensaje("Registro de Educación", "El campo 'Asignatura Principal' es obligatorio.", "warning");
            return false;
        }
        if (ed_titulo.val().length == 0) {
            mensaje("Registro de Educación", "El campo 'Título' es obligatorio.", "warning");
            return false;
        }
        return true;
    }
    //#endregion

//#endregion Código para registrar Evaluaciones

//#region Código para registrar Motivos para Aumento de Sueldo

    //#region Variables
    var mas_code = $('input[name="mAuSal_code"]');
    var mas_desc = $('textarea[name="mAuSal_desc"]');
    var mas_activo = $('input[name="mas_activo"]');
    //#endregion

    //#region Eventos Controles
    $('#btnmasGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/motivo-aumento-sueldo/';
        metodo = 'POST';
        if (mas_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        //if (validarEvDatos() != false) {
        data = {
            'desc': mas_desc.val(),
            'code': mas_code.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Motivos para Aumento de Sueldo");
        //}
    });

    $('#btnmasActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/motivo-aumento-sueldo/';
        metodo = 'POST';
        if (mas_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        //if (validarEvDatos() != false) {
        data = {
            'id': id.val(),
            'code': mas_code.val(),
            'desc': mas_desc.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Motivos para Aumento de Sueldo", true, "/listar/motivos-aumento-sueldo/");
        //}
    });

    $('#btnmasCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/motivos-aumento-sueldo/");
    });
    //#endregion

//#endregion Código para registrar Motivos para Aumento de Sueldo

//#region Código para registrar Motivos para Rescisión de Contrato

    //#region Variables
    var mReCon_id = $('input[name="mReCon_id"]');
    var mReCon_nombre = $('input[name="mReCon_nombre"]');
    var mReCon_desc = $('textarea[name="mReCon_desc"]');
    var mReCon_activo = $('input[name="mReCon_activo"]');
    //#endregion

    //#region Eventos Controles
    $('#btnReConGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/motivo-rescision-contrato/';
        metodo = 'POST';
        if (mReCon_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        //if (validarEvDatos() != false) {
        data = {
            'nombre': mReCon_nombre.val(),
            'desc': mReCon_desc.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Motivos para Rescisión de Contrato");
        //}
    });

    $('#btnReConActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/motivo-rescision-contrato/';
        metodo = 'POST';
        if (mReCon_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        //if (validarEvDatos() != false) {
        data = {
            'id': mReCon_id.val(),
            'nombre': mReCon_nombre.val(),
            'desc': mReCon_desc.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Motivos para Rescisión de Contrato", true, "/listar/motivo-rescision-contrato/");
        //}
    });

    $('#btnReConCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/motivo-rescision-contrato/");
    });
    //#endregion

//#endregion Código para registrar Motivos para Rescisión de Contrato

//#region Código para registar empleos anteriores

    //#region Variables
    var empAnt_id = $('input[name="empAnt_id"]');
    var empAnt_emp = $('select[name="empAnt_emp"]');
    var empAnt_desde = $('input[name="empAnt_desde"]');
    var empAnt_hasta = $('input[name="empAnt_hasta"]');
    var empAnt_empresa = $('input[name="empAnt_empr"]');
    var empAnt_posicion = $('input[name="empAnt_pos"]');
    var empAnt_comentario = $('textarea[name="empAnt_com"]');
    var empAnt_activo = $('input[name="empAnt_activo"]');
    //#endregion

    //#region Eventos Controles
    $('#btnempAntGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/empleo-anterior/';
        metodo = 'POST';
        if (empAnt_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'emp': empAnt_emp.val(),
            'desde': empAnt_desde.val(),
            'hasta': empAnt_hasta.val(),
            'empresa': empAnt_empresa.val(),
            'posicion': empAnt_posicion.val(),
            'comentario': empAnt_comentario.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Empleo Anterior");
    });

    $('#btnempAntActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/empleo-anterior/';
        metodo = 'POST';
        //if (validarEvDatos() != false) {
        if (empAnt_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'id': empAnt_id.val(),
            'emp': empAnt_emp.val(),
            'desde': empAnt_desde.val(),
            'hasta': empAnt_hasta.val(),
            'empresa': empAnt_empresa.val(),
            'posicion': empAnt_posicion.val(),
            'comentario': empAnt_comentario.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Empleo Anterior", true, "/listar/empleo-anterior/");
        //}
    });

    $('#btnempAntCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/empleo-anterior/");
    });
    //#endregion

//#endregion Códigp para registrar empleos anteriores

//#region Código para registrar Grupo de Comisiones

    //#region Variables
    var grpCom_id = $("input[name='grpCom_id'");
    var grpCom_desc = $('textarea[name="grpCom_desc"]');
    var grpCom_code = $('input[name="grpCom_code"]');
    var grpCom_activo = $('input[name="grpCom_activo"]');
    //#endregion

    //#region Eventos Controles
    $('#btngrpcomGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/grupo-comision/';
        metodo = 'POST';
        if (grpCom_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'desc': grpCom_desc.val(),
            'code': grpCom_code.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Grupo de Comisión");
    });

    $('#btngrpcomActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/grupo-comision/';
        metodo = 'POST';
        //if (validarestEmDatos() != false) {
        if (grpCom_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'id': grpCom_id.val(),
            'desc': grpCom_desc.val(),
            'code': grpCom_code.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Grupo de Comisión", true, "/listar/grupo-comision/");
        //}
    });

    $('#btngrpcomCancelar').on('click', function(e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/grupo-comision/");
    });
    //#endregion

//#endregion Código para registrar Grupo de Comisiones

//#region Código para registrar Vendedor

    //#region Variables
    var vnd_id = $("input[name='vnd_id'");
    var vnd_nombre = $("input[name='ven_nombre'");
    var vnd_grpcom = $('select[name="vend_grpcom"]');
    var vnd_porcen = $('input[name="ven_porc"]');
    var vnd_emplea = $('select[name="vend_emp"]');
    var vnd_telefo = $('input[name="vend_tel"]');
    var vnd_telmov = $('input[name="vend_movil"]');
    var vnd_correo = $('input[name="vend_correo"]');
    var vnd_coment = $('textarea[name="vend_com"]');
    var vnd_activo = $('input[name="vend_activo"]');
    //#endregion

    //#region Eventos Controles

    $('#btnVendGuardar').on('click', function(e) {
        e.preventDefault();
        url = '/guardar/vendedor/';
        metodo = 'POST';
        //if (validarcddDatos() != false) {
        if (vnd_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'nombre': vnd_nombre.val(),
            'grupo_com': vnd_grpcom.val(),
            'porcentaje': vnd_porcen.val(),
            'emp': vnd_emplea.val(),
            'tel': vnd_telefo.val(),
            'movil':vnd_telmov.val(),
            'correo': vnd_correo.val(),
            'coment':vnd_coment.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Vendedor");
        //}
    });

    $('#btnVendActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/vendedor/';
        metodo = 'POST';
        //if (validarcddDatos() != false) {
        if (vnd_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'id': vnd_id.val(),
            'nombre': vnd_nombre.val(),
            'grupo_com': vnd_grpcom.val(),
            'porcentaje': vnd_porcen.val(),
            'emp': vnd_emplea.val(),
            'tel': vnd_telefo.val(),
            'movil': vnd_telmov.val(),
            'correo': vnd_correo.val(),
            'coment': vnd_coment.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Vendedor", true, "/listar/vendedor/");
        //}
    });

    $('#btnVendCancelar').on('click', function(e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/vendedor/");
    });

//#endregion

//#endregion Código para registrar Vendedor

//#region Código para registrar Feriado.

    //#region Variables
    var fer_id = $("input[name='fer_id'");
    var fer_fecha = $("input[name='fer_fecha'");
    var fer_rate = $('input[name="fer_rate"]');
    var fer_comment = $('textarea[name="fer_coment"]');
    var fer_activo = $('input[name="fer_activo"]');
    //#endregion

    //#region Eventos Controles
    $('#btnFerGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/feriado/';
        metodo = 'POST';
        //if (validarEdDatos() != false) {
        if (fer_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'fecha': fer_fecha.val(),
            'rate': fer_rate.val(),
            'comentario': fer_comment.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Feriado");
        //}
    });

    $('#btnFerActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/feriado/';
        metodo = 'POST';
        if (fer_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        //if (validarEdDatos() != false) {
        data = {
            'id': fer_id.val(),
            'fecha': fer_fecha.val(),
            'rate': fer_rate.val(),
            'comentario': fer_comment.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Feriado", true, "/listar/feriado/");
        //}
    });

    $('#btnFerCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/feriado/");
    });
    //#endregion

//#endregion Código para registrar Feriado.

//#region Código para registrar Activos Asignados

    //#region Variables
    var act_asig_id = $("input[name='act_asig_id'");
    var act_asig_desc = $("textarea[name='act_asig_desc'");
    var act_asig_activo = $('input[name="act_asig_activo"]');
    //#endregion

    //#region Eventos Controles
    $('#btnActAsignGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/activo-asignado/';
        metodo = 'POST';
        //if (validarEdDatos() != false) {
        if (act_asig_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'desc': act_asig_desc.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Activo Asignado");
        //}
    });

    $('#btnActAsignActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/activo-asignado/';
        metodo = 'POST';
        if (act_asig_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        //if (validarEdDatos() != false) {
        data = {
            'id': act_asig_id.val(),
            'desc': act_asig_desc.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Activo Asignado", true, "/listar/activo-asignado/");
        //}
    });

    $('#btnActAsignCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/activo-asignado/");
    });
    //#endregion

//#endregion Código para registra Activos Asignados

//#region Código para registrar Tipo de Salario

    //#region Variables
    var tipoSalario_id = $("input[name='tipoSalario_id'");
    var tipoSalario_desc = $("textarea[name='tipoSalario_desc'");
    var tipoSalario_nombre = $("input[name='tipoSalario_nombre'");
    var tipoSalario_dias = $("input[name='tipoSalario_salariosDias'");
    var tipoSalario_activo = $('input[name="tipoSalario_activo"]');
    //#endregion

    //#region Eventos Controles
    $('#btnTipoSalarioGuardar').on('click', function (e) {
        e.preventDefault();
        var resp = $.isNumeric(tipoSalario_dias.val());
        if (!resp) {
            mensaje("Tipo de Salario", "El campo 'Días de salario' es numérico.", "warning", 3500);
            return;
        }
        url = '/guardar/tipo-salario/';
        metodo = 'POST';
        //if (validarEdDatos() != false) {
        if (tipoSalario_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'nombre': tipoSalario_nombre.val(),
            'desc': tipoSalario_desc.val(),
            'dias': tipoSalario_dias.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Tipo de Salario");
        //}
    });

    $('#btnTipoSalarioActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/tipo-salario/';
        metodo = 'POST';
        if (tipoSalario_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        //if (validarEdDatos() != false) {
        data = {
            'id': tipoSalario_id.val(),
            'nombre': tipoSalario_nombre.val(),
            'desc': tipoSalario_desc.val(),
            'dias': tipoSalario_dias.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Tipo de Salario", true, "/listar/tipo-salario/");
        //}
    });

    $('#btnTipoSalarioCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/tipo-salario/");
    });
    //#endregion

//#endregion Código para registrar Tipo de Salario

//#region Código para registrar Tipo Costo Empleado

    //#region Variables
    var empCosto_id = $("input[name='costoEmp_id'");
    var empCosto_desc = $("textarea[name='costoEmp_desc'");
    var empCosto_nombre = $("input[name='costoEmp_nombre'");
    var empCosto_activo = $('input[name="costoEmp_activo"]');
    //#endregion
    
    //#region Eventos Controles
    $('#btncostoEmpGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/costo-empleado-unidades/';
        metodo = 'POST';
        //if (validarEdDatos() != false) {
        if (empCosto_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'nombre': empCosto_nombre.val(),
            'desc': empCosto_desc.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Unidades Costo Empleado");
        //}
    });

    $('#btncostoEmpActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/costo-empleado-unidades/';
        metodo = 'POST';
        if (empCosto_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        //if (validarEdDatos() != false) {
        data = {
            'id': empCosto_id.val(),
            'nombre': empCosto_nombre.val(),
            'desc': empCosto_desc.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Unidades Costo de Empleado", true, "/listar/costo-empleado/");
        //}
    });

    $('#btncostoEmpCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/costo-empleado/");
    });
    //#endregion

//#endregion Código para registrar Tipo Costo Empleado

//#region Código para registrar Banco

    //#region Variables
    var banco_id = $("input[name='banco_id'");
    var banco_desc = $("textarea[name='banco_desc'");
    var banco_nombre = $("input[name='banco_nombre'");
    var banco_activo = $('input[name="banco_activo"]');
    //#endregion

    //#region Eventos Controles
    $('#btnbancoGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/banco/';
        metodo = 'POST';
        //if (validarEdDatos() != false) {
        if (banco_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'nombre': banco_nombre.val(),
            'desc': banco_desc.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Banco");
        //}
    });

    $('#btnbancoActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/banco/';
        metodo = 'POST';
        if (banco_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        //if (validarEdDatos() != false) {
        data = {
            'id': banco_id.val(),
            'nombre': banco_nombre.val(),
            'desc': banco_desc.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Banco", true, "/listar/banco/");
        //}
    });

    $('#btnbancoCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/banco/");
    });
    //#endregion

//#endregion Código para registrar Banco

//#region Código para registrar Empresa por usuario

    //#region Variables
    var empUs_id = $("input[name='id'");
    var empUs_usuario = $("select[name='userEmp_usuario'");
    var empUs_empresa = $("select[name='userEmp_empresa'");
    var empUs_activo = $("input[name='userEmp_activo'");
    //#endregion

    //#region Eventos Controles
    $('#btnempUserGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/empresa-usuario/';
        metodo = 'POST';
        //if (validarEdDatos() != false) {
        if (empUs_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'empresa': empUs_empresa.val(),
            'usuario': empUs_usuario.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Asignar empresa a usuario");
        //}
    });

    $('#btnempUserActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/empresa-usuario/';
        metodo = 'POST';
        if (empUs_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        //if (validarEdDatos() != false) {
        data = {
            'id': empUs_id.val(),
            'empresa': empUs_empresa.val(),
            'usuario': empUs_usuario.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Asignar empresa a usuario", true, "/listar/empresas-usuario/");
        //}
    });

    $('#btnempUserCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/empresas-usuario/");
    });
    //#endregion

//#endregion

//#region Código para Editar Fotografía
    var archivo = $('input[name="imagen"]');
    var fileArchivo = $('.dropify').dropify();
    fileArchivo.init();

    $('#frmImagenEmp').submit(function(e) {
        e.preventDefault();
        $form = $(this);
        var formData = new FormData(this);
        var token = $('input[name="csrfmiddlewaretoken"]');
        if (archivo[0].files.length == 0) {
            mensaje("Perfíl de usuario", "Aún no se ha seleccionado la fotografía.", "warning", 3500);
            return;
        }
        $.ajax({
            url: '/guardar/foto-perfil/',
            type: 'POST',
            data: formData,
            success: function (response) {
                $('.error').remove();
                console.log(response);
                if (response.error) {
                    mensaje("Perfíl de usuario", "No se pudo registrar la actualización.", "warning", 3500);
                    console.log(response.mensaje)
                    // $.each(response.errors, function (name, error) {
                    //     error = '<small class="text-muted error">' + error + '</small>';
                    //     $form.find('[name=' + name + ']').after(error);
                    // });
                }
                else {
                    //alert(response.message);
                    console.log(response);
                    $('#imgPerfilUsuario').html(response);
                    // $('input[type="text"], input[type="file"]').val(null);
                    // $('select').val(null);
                    // token.val(token.val());
                    fileArchivo = fileArchivo.data('dropify');
                    fileArchivo.resetPreview();
                    fileArchivo.clearElement(); 
                    mensaje("Perfíl de usuario", "Se ha actualizado la foto del usuario.", "ok", 3500);
                }
            },
            cache: false,
            contentType: false,
            processData: false,
        });
    });

    // fileFoto.on('click', function(e) {
    //     e.preventDefault();
    //     if (archivo[0].files.length == 0) {
    //         console.log("No tiene foto");
    //     } else {
    //         console.log("Cargando foto");
    //     }
    // });
//#endregion

//#region Código para Enviar Sucursal

    var btnSelSuc = $('.btnSelSuc');

    var idSucursal = 0;

    btnSelSuc.on('click', function (e) {
        e.preventDefault();
        idSucursal = $(this).attr('data-suc');

        seleccionaUnaSucursal()
    });

    function seleccionaUnaSucursal() {
        $.ajax({
            type: "GET",
            url: '/enviar/sucursal/',
            data: {
                'idSucursal': idSucursal
            }, // serializes the form's elements.
            success: function (data) {
                if (data.error == false) {
                    window.location.replace(dns + "/");
                } else {
                    mensaje("Seleccionar sucursal", data.mensaje, "error", 3500);
                }
            },
            error: function (data) {
                mensaje("Seleccionar sucursal", data.statusText, "error", 3500);
            },
            typeData: 'json'
        });
    }

//#endregion

//#region Código para Empleado
var emp_cboTipoSalario = $('#frmEmpleado select[name="salaryUnits"]');
var emp_txtSalario = $('#frmEmpleado input[name="salario"]');
var emp_txtSalarioDiario = $('#frmEmpleado input[name="txtSalarioDiario"]');
var emp_dias_salario = 0;

$(document).ready(function () {
   if (emp_cboTipoSalario.val() > 0) {
    $.ajax({
        type: "GET",
        url: '/obtener/dias-salario/',
        data: {
            'id': emp_cboTipoSalario.val(),
        }, // serializes the form's elements.
        success: function (data) {
            if (data.error == false) {
                emp_dias_salario = data.dias_salario;
                if (emp_dias_salario > 0) {
                    if (emp_txtSalario.val() > 0) {
                        sal_dia = parseFloat(emp_txtSalario.val() / emp_dias_salario).toFixed(2);
                        emp_txtSalarioDiario.val(formatNumber.new(sal_dia));
                    }
                }
            } else {
                mensaje("Seleccionar sucursal", data.mensaje, "error", 3500);
            }
        },
        error: function (data) {
            mensaje("Seleccionar sucursal", data.statusText, "error", 3500);
        },
        typeData: 'json'
    });
   }
});

emp_txtSalario.on('change', function() {
    if (emp_dias_salario > 0) {
        if (emp_txtSalario.val() > 0) {
            sal_dia = parseFloat(emp_txtSalario.val() / emp_dias_salario).toFixed(2);
            emp_txtSalarioDiario.val(formatNumber.new(sal_dia));
        }
    }
});

emp_cboTipoSalario.on('change', function() {
    $.ajax({
        type: "GET",
        url: '/obtener/dias-salario/',
        data: {
            'id': emp_cboTipoSalario.val(),
        }, // serializes the form's elements.
        success: function (data) {
            if (data.error == false) {
                emp_dias_salario = data.dias_salario;
                if (emp_dias_salario > 0) {
                    if (emp_txtSalario.val() > 0) {
                        sal_dia = parseFloat(emp_txtSalario.val() / emp_dias_salario).toFixed(2);
                        emp_txtSalarioDiario.val(formatNumber.new(sal_dia));
                    }
                }
            } else {
                mensaje("Seleccionar sucursal", data.mensaje, "error", 3500);
            }
        },
        error: function (data) {
            mensaje("Seleccionar sucursal", data.statusText, "error", 3500);
        },
        typeData: 'json'
    });
})
//#endregion

//#region Código para Aumento de Sueldo
    var cboEmpleado = $('.aumento-salario select[name="empleado"]');
    var txtFechaIncremento = $('.aumento-salario input[name="fecha_incremento"]');
    var motivo_aumento = $('.aumento-salario select[name="motivo_aumento"]');
    var txtSalarioAnterior = $('.aumento-salario input[name="salario_anterior"]');
    var txtIncremento = $('.aumento-salario input[name="incremento"]');
    var txtNuevoSalario = $('.aumento-salario input[name="nuevo_salario"]');
    var txtComentarios = $('.aumento-salario textarea[name="comentarios"]');

    $('#aumento-salario-listado .btnVerRegistroAumentoSalario').on('click', function(e) {
        e.preventDefault();
        url = '/ver-registro/aumento-salario/';
        metodo = 'GET';
        data = {'id': $(this).attr('data')};
        $.ajax({
            type: metodo,
            url: url,
            data: data,
            success: function (data) {
                $('#aumento-salario-modal').html(data);
            },
            error: function (data) {
                console.log(data);
            },
            dataType: 'html'
        });
        $('#responsive-modal').modal('toggle');
    });

    $('#btnIncGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/enviar/aumento-salario/';
        metodo = 'POST';
        data = {
            'empleado_fk': cboEmpleado.val(),
            'fecha_incremento': txtFechaIncremento.val(),
            'motivo_aumento': motivo_aumento.val(),
            'salario_anterior': (txtSalarioAnterior.val().replace(",", "")),
            'incremento': (txtIncremento.val().replace(",", "")),
            'nuevo_salario': (txtNuevoSalario.val().replace(",", "")),
            'comentarios': txtComentarios.val(),
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Aumento de salario");      
    });

    $('#btnIncActualizar').on('click', function(e) {
        e.preventDefault();
        var novo_saldo = parseFloat(txtNuevoSalario.val().replace(",", "")).toFixed(2)
        url = '/actualizar/aumento-salario/';
        metodo = 'POST';
        data = {
            'id': id.val(),
            'motivo': motivo_aumento.val(),
            'fecha_incremento': txtFechaIncremento.val(),
            'incremento': txtIncremento.val(),
            'nuevo_salario': novo_saldo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Aumento de salario", true, "/listar/aumento-salario/");
    });

    $('#btnIncCancelar').on('click', function(e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/aumento-salario/");
    });

    cboEmpleado.on('change', function() {
        obtener_ultimo_salario(cboEmpleado.val())
    });

    txtIncremento.on('change', function() {
        calcular_nuevo_sueldo();
        txtIncremento.val(formatNumber.new(txtIncremento.val()));
    });

    function calcular_nuevo_sueldo(){
        salario_anterior = 0;
        incremento = 0;
        nuevo_salario = 0;
        var salant = 0;
        var inc = 0;
        var nuevo_sal = 0;
        if (txtSalarioAnterior.val().length > 0) {
            salant = $('input[name="salario_anterior"]').val().replace(",", "");
            salario_anterior = Number($('input[name="salario_anterior"]').val());
        }
        if (txtIncremento.val().length > 0) {
            inc = parseFloat($('input[name="incremento"]').val()).toFixed(2);
            incremento = Number($('input[name="incremento"]').val());
        }
        nuevo_sal = Number(salant) + Number(inc);
        nuevo_sal = parseFloat(nuevo_sal).toFixed(2);
        txtNuevoSalario.val(formatNumber.new(nuevo_sal));
    }

    function obtener_ultimo_salario(codEmpleado) {
        $.ajax({
            type: 'GET',
            url: '/obtener/salario-ultimo/',
            data: {'idEmpleado': codEmpleado},
            success: function (data) {
                if (data.error == false) {
                    
                    $('.aumento-salario input[name="salario_anterior"]').val(formatNumber.new(parseFloat(Number(data.salario_anterior)).toFixed(2)));
                    calcular_nuevo_sueldo();
                } else {
                    mensaje("Aumento de salario", data.mensaje, "error", 3500);
                }
            },
            error: function (data) {
                mensaje("Aumento de salario", data.statusText, "error", 3500);
            }
        });
    }

//#endregion

//#region Código para Planilla

    var btnPlGuardar = $('#frmPlanilla #btnGuardar');
    var btnPlActualizar = $('#frmPlanilla #btnActualizar');
    var btnPlCancelar = $('#frmPlanilla #btnCancelar');
    var btnPlVerRegistro = $('#planilla-listado #btnVerRegistro');
    var cboPlTipoPlanilla = $('#frmPlanilla select[name="tipo_planilla"]');
    var cboPlTipoPago = $('#frmPlanilla select[name="tipo_pago"]');
    var txtPlFechaPago = $('#frmPlanilla input[name="fecha_pago"]');
    var txtPlFechaInicio = $('#frmPlanilla input[name="fecha_inicio"]');
    var txtPlFechaFin = $('#frmPlanilla input[name="fecha_fin"]');
    var txtPlFechaPago = $('#frmPlanilla input[name="fecha_pago"]');
    var txtPlDescripcion = $('#frmPlanilla textarea[name="descripcion"]');

    var btnGenerar = $('.planilla-generar #btnGenerar');

    btnPlGuardar.on('click', function(e) {
        e.preventDefault();
        url = '/guardar/planilla/';
        metodo = 'POST';
        data = {
            'tipo_planilla': cboPlTipoPlanilla.val(),
            'tipo_pago': cboPlTipoPago.val(),
            'fecha_pago': txtPlFechaPago.val(),
            'fecha_inicio': txtPlFechaInicio.val(),
            'fecha_fin': txtPlFechaFin.val(),
            'descripcion': txtPlDescripcion.val(),
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Planilla");
    });

    btnPlActualizar.on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/planilla/';
        metodo = 'POST';
        data = {
            'id': id.val(),
            'tipo_planilla': cboPlTipoPlanilla.val(),
            'tipo_pago': cboPlTipoPago.val(),
            'fecha_pago': txtPlFechaPago.val(),
            'fecha_inicio': txtPlFechaInicio.val(),
            'fecha_fin': txtPlFechaFin.val(),
            'descripcion': txtPlDescripcion.val(),
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Planilla", true, "/listar/planilla/");
    });

    btnPlCancelar.on('click', function(e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/planilla/");
    });

    btnPlVerRegistro.on('click', function(e) {
        e.preventDefault();
        url = '/ver-registro/planilla/';
        metodo = 'GET';
        data = { 'id': $(this).attr('data') };
        $.ajax({
            type: metodo,
            url: url,
            data: data,
            success: function (data) {
                $('#planilla-modal').html(data);
            },
            error: function (data) {
                console.log(data);
            },
            dataType: 'html'
        });
        $('#responsive-modal').modal('toggle');
    });

    valor = 0;
    var cboPlanillas = $('.planilla-generar #cboPlanillas');
    btnGenerar.on('click', function(e) {
        e.preventDefault();
        // var valor_porc = $('#loader-bar').attr('style');
        // console.log(valor_porc);
        // valor_porc = valor_porc.replace("%;","");
        // valor_porc = valor_porc.substring(7);
        // valor = parseInt(valor_porc);
        // valor = parseFloat(valor + 5);
        // if (valor > 100) {
        //     valor = 0;
        //     $('#loader-bar').attr('style', 'width: '+valor+'%;');
        // }else{
        //     $('#loader-bar').attr('style', 'width: '+valor+'%;');
        // }
        // $('#loader-bar').text(valor+'%');
        // console.log(valor);
        url = '/obtener/empleados-planilla/';
        metodo = 'GET';
        data = {'id':cboPlanillas.val()};
        $.ajax({
            type: metodo,
            url: url,
            data: data,
            success: function (data) {
                if (data.error) {
                    console.log(data);
                } else {
                    var ldatos = data.empleados;
                    console.log(ldatos.length);
                    ldatos.forEach(item => {
                        url = "/calcular/planilla-empleado/";
                        metodo = 'POST';
                        data = {
                            'empleado_id': item.ID,
                            'planilla_id': cboPlanillas.val(),
                            'csrfmiddlewaretoken': token.val(),
                        }
                        $.ajax({
                            type: metodo,
                            url: url,
                            data: data,
                            success: function(data){
                                if (data.error) {
                                    alert(data.mensaje);
                                }else{
                                    alert(data.mensaje);
                                };
                            },
                            error: function(data){
                                console.log("Error: " + data);
                            },
                            dataType: 'json'
                        });

                        console.log(item.ID);
                    });
                }
            },
            error: function (data) {
                console.log(data);
            },
            dataType: 'json'
        });
    });


//#endregion

//#region Código para Tipo de Contrato

var tc_id = $('#tipo_contrato input[name="tipo_contrato_id"]');
var tc_txtTipoContrato = $('#tipo_contrato input[name="txtTipoContrato"]');
var tc_txtDescripcion = $('#tipo_contrato textarea[name="txtDescripcion"]');
var tc_chkActivo =  $('#tipo_contrato input[name="chkActivo"]');

$('#tipo_contrato #btnGuardar').on('click', function(e) {
    e.preventDefault();
    if (tc_chkActivo.is(":checked")) {
        vActivo = 1;
    } else {
        vActivo = 0;
    }
    url = '/guardar/tipo-contrato/';
    metodo = 'POST';
    data = {
        'tipo_contrato': tc_txtTipoContrato.val(),
        'descripcion': tc_txtDescripcion.val(),
        'activo': vActivo,
        'csrfmiddlewaretoken': token.val(),
    };
    GuardarRegistro(url, metodo, data, "Tipo de contrato");
});

$('#tipo_contrato #btnActualizar').on('click', function(e) {
    e.preventDefault();
    if (tc_chkActivo.is(":checked")) {
        vActivo = 1;
    } else {
        vActivo = 0;
    }
    url = '/actualizar/tipo-contrato/';
    metodo = 'POST';
    data = {
        'id': tc_id.val(),
        'tipo_contrato': tc_txtTipoContrato.val(),
        'descripcion': tc_txtDescripcion.val(),
        'activo': vActivo,
        'csrfmiddlewaretoken': token.val(),
    };
    GuardarRegistro(url, metodo, data, "Tipo de contrato");
});

$('#tipo_contrato #btnCancelar').on('click', function(e) {
    e.preventDefault();
    window.location.replace(dns + "/listar/tipo-contrato/");
});

//#endregion

//#region Código para Tipo Nómina

var tn_id = $('#tipo_nomina input[name="tipoSalario_id"]');
var tn_txtTipoNomina = $('#tipo_nomina input[name="txtTipoNomina"]');
var tn_txtDescripcion = $('#tipo_nomina textarea[name="txtDescripcion"]');
var tn_chkActivo = $('#tipo_nomina input[name="tipoNomina_activo"]');

$('#tipo_nomina #btnTipoNominaGuardar').on('click', function(e) {
    e.preventDefault();
    if (tn_chkActivo.is(":checked")) {
        vActivo = 1;
    } else {
        vActivo = 0;
    }
    url = '/guardar/tipo-nomina/';
    metodo = 'POST';
    data = {
        'tipo_nomina': tn_txtTipoNomina.val(),
        'descripcion': tn_txtDescripcion.val(),
        'activo': vActivo,
        'csrfmiddlewaretoken': token.val(),
    };
    GuardarRegistro(url, metodo, data, "Tipo de nómina");
});

$('#tipo_nomina #btnTipoNominaActualizar').on('click', function(e) {
    e.preventDefault();
        url = '/actualizar/tipo-nomina/';
        metodo = 'POST';
        if (tn_chkActivo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'id': tn_id.val(),
            'tipo_nomina': tn_txtTipoNomina.val(),
            'descripcion': tn_txtDescripcion.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Tipo de Nómina", true, "/listar/tipo-nomina/");
});

$('#tipo_nomina #btnTipoNominaCancelar').on('click', function(e) {
    e.preventDefault();
    window.location.replace(dns + "/listar/tipo-nomina/");
});

//#endregion

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
                    console.log(data.mensaje);
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
        $('input[type="number"]').val(null);
        $('input[type="checkbox"]').removeAttr('checked');
        $('select').val(0);
        $('textarea').val(null);
        $('.select2').select2('val', '0');
    }

    var formatNumber = {
        separador: ",", // separador para los miles
        sepDecimal: '.', // separador para los decimales
        formatear: function (num) {
            num += '';
            var splitStr = num.split('.');
            var splitLeft = splitStr[0];
            var splitRight = splitStr.length > 1 ? this.sepDecimal + splitStr[1] : '';
            var regx = /(\d+)(\d{3})/;
            while (regx.test(splitLeft)) {
                splitLeft = splitLeft.replace(regx, '$1' + this.separador + '$2');
            }
            return this.simbol + splitLeft + splitRight;
        },
        new: function (num, simbol) {
            this.simbol = simbol || '';
            return this.formatear(num);
        }
    }
//#endregion
});