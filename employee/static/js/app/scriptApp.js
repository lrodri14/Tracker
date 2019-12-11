$(document).on('ready', () => {
    //#region Variables App
    var vActivo = 0;
    var url = '';
    var metodo = '';
    var data = {};
    var token = $('input[name="csrfmiddlewaretoken"]');
    var dns = window.location.protocol + "//" + window.location.host;
    var id = $('input[name="id"]');
    //#endregion

    //#region Botones
    var botonVerRegistro;
    var botonGuardar;
    //#endregion

    //#region Código para Puestos de Trabajo
    //#region Variables
    var pt_nombre = $('input[name="pt_nombre"]');
    var pt_desc = $('textarea[name="pt_descripcion"]');
    var pt_fun = $('select[name="pt_funcion_operativa"]');
    var pt_activo = $('input[name="pt_activo"]');

    //var token = $('input[name="csrfmiddlewaretoken"]');
    //#endregion
    //#region Eventos Controles
    $('#btnptGuardar').on('click', (e) => {
        e.preventDefault();
        url = '/guardar/puesto/';
        metodo = 'POST';
        if (pt_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'nombre': pt_nombre.val(),
            'descripcion': pt_desc.val(),
            'funcion_operativa': pt_fun.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Puesto de Trabajo", false, '');
    });

    $('#btnptActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/puesto/';
        metodo = 'POST';
        if (pt_activo.is(":checked")) {
            console.log("Verdadero");
            vActivo = 1;
        } else {
            console.log("Falso");
            vActivo = 0;
        }
        data = {
            'id': id.val(),
            'nombre': pt_nombre.val(),
            'desc': pt_desc.val(),
            'funcion_operativa': pt_fun.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Puesto de Trabajo", true, "/listar/puestos-trabajo/");
    });
    $('#btnptCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/puestos-trabajo/");
    });
    //#endregion
    //#region Validación
    // function validarptDatos() {
    //     $('div').removeClass('has-warning');

    //     if (pt_nombre.val().length == 0) {
    //         mensaje("Registro de Puesto de trabajo", "El campo 'Nombre' es obligatorio.", "warning");
    //         return false;
    //     }
    //     return true;
    // }
    //#endregion
    //#endregion Fin código de Puestos de Trabajo

    //#region Código para Centros de Costos

    //#region Variables
    var cc_desc = $('input[name="cc_descripcion"]');
    var cc_activo = $('input[name="cc_activo"]');
    var cc_code = $('input[name="cc_codigo"]');
    //#endregion

    //#region Eventos Controles
    $('#btnccGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/centro-costo/';
        metodo = 'POST';
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
    });

    $('#btnccActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/centro-costo/';
        metodo = 'POST';
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
    });


    $('#btnccCancelar').on('click', function (e) {
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
        // if (validarpDatos() != false) {
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
        // }
    });

    $('#btnpActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/pais/';
        metodo = 'POST';
        if (p_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'id': id.val(),
            'nombre': p_nombre.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Países", true, "/listar/paises/");
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
    });

    $('#btndeptActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/deptos-pais/';
        metodo = 'POST';
        if (dept_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'id': id.val(),
            'nombre': dept_nombre.val(),
            'pais': dept_pais.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Departamento/Estado", true, "/listar/deptos-estados/");
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

    $('#btncddActualizar').on('click', function (e) {
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
        // if (validargnrDatos() != false) {
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
        // }
    });

    $('#btngnrActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/genero/';
        metodo = 'POST';
        // if (validargnrDatos() != false) {
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
        // }
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
    $('#btnestcvGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/estado-civil/';
        metodo = 'POST';
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
    });

    $('#btnestcvActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/estado-civil/';
        metodo = 'POST';
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
    $('#btnparentGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/parentesco/';
        metodo = 'POST';
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
    });

    $('#btnparentActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/parentesco/';
        metodo = 'POST';
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
    var fun_desc = $('input[name="fun_desc"]');
    var fun_activo = $('input[name="fun_activo"]');
    var fun_code = $('input[name="fun_code"]');
    //#endregion

    //#region Eventos Controles
    $('#btnfunGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/funcion/';
        metodo = 'POST';
        // if (validarfunDatos() != false) {
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
        // }
    });

    $('#btnfunActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/funcion/';
        metodo = 'POST';
        // if (validarfunDatos() != false) {
        if (fun_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'id': id.val(),
            'desc': fun_desc.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Función de Trabajo", true, "/listar/funciones/");
        // }
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
    $('#btneqTGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/equipo/';
        metodo = 'POST';
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
    });

    $('#btneqTActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/equipo/';
        metodo = 'POST';
        if (eqT_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'id': id.val(),
            'desc': eqT_desc.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Equipos de Trabajo", true, "/listar/equipos/");
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
    $('#btnestEmGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/estatus-empleado/';
        metodo = 'POST';
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
    });

    $('#btnestEmActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/estatus-empleado/';
        metodo = 'POST';
        if (estEm_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'id': id.val(),
            'desc': estEm_desc.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Estados de Empleado", true, "/listar/estatus-empleado/");
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
    $('#btnAuGuardar').on('click', function (e) {
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

    $('#btnAuActualizar').on('click', function (e) {
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

    $('#btnAuCancelar').on('click', function (e) {
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
    $('#btnmAuGuardar').on('click', function (e) {
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

    $('#btnmAuActualizar').on('click', function (e) {
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
            'desc': mAu_desc.val(),
            'pagado': vPagado,
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Motivo de Ausencia", true, "/listar/motivos-ausencia/");
        //}
    });

    $('#btnmAuCancelar').on('click', function (e) {
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
    $('#btnmDesGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/motivo-despido/';
        metodo = 'POST';
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
    });

    $('#btnmDesActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/motivo-despido/';
        metodo = 'POST';
        if (mdes_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'id': id.val(),
            'desc': mdes_desc.val(),
            'pagado': vPagado,
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Motivo de Despido", true, "/listar/motivos-despido/");
    });

    $('#btnmDesCancelar').on('click', function (e) {
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
    $('#btnmReGuardar').on('click', function (e) {
        e.preventDefault();
        url = '/guardar/motivo-renuncia/';
        metodo = 'POST';
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
    });

    $('#btnmReActualizar').on('click', function (e) {
        e.preventDefault();
        url = '/actualizar/motivo-renuncia/';
        metodo = 'POST';
        if (mre_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        data = {
            'id': id.val(),
            'desc': mre_desc.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Motivo de Renuncia", true, "/listar/motivos-renuncia/");
    });

    $('#btnmReCancelar').on('click', function (e) {
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
    $('#btnclsEdGuardar').on('click', function (e) {
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

    $('#btnclsEdActualizar').on('click', function (e) {
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

    $('#btnclsEdCancelar').on('click', function (e) {
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
    $('#btnEdGuardar').on('click', function (e) {
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

    $('#btnEdActualizar').on('click', function (e) {
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

    $('#btnEdCancelar').on('click', function (e) {
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
        data = {
            'id': id.val(),
            'desc': mas_desc.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Motivos para Aumento de Sueldo", true, "/listar/motivos-aumento-sueldo/");
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

    $('#btngrpcomCancelar').on('click', function (e) {
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
    var vnd_telefo = $('input[name="vend_tel"]');
    var vnd_telmov = $('input[name="vend_movil"]');
    var vnd_correo = $('input[name="vend_correo"]');
    var vnd_coment = $('textarea[name="vend_com"]');
    var vnd_activo = $('input[name="vend_activo"]');
    //#endregion

    //#region Eventos Controles

    $('#btnVendGuardar').on('click', function (e) {
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
            'tel': vnd_telefo.val(),
            'movil': vnd_telmov.val(),
            'correo': vnd_correo.val(),
            'coment': vnd_coment.val(),
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

    $('#btnVendCancelar').on('click', function (e) {
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
    var act_asig_code = $("input[name='act_asig_code'");
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
            'code': act_asig_code.val(),
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
            'code': act_asig_code.val(),
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
        $(this).addClass('disabled');
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
        $(this).addClass('disabled');
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
        data = {
            'id': empUs_id.val(),
            'empresa': empUs_empresa.val(),
            'usuario': empUs_usuario.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Asignar empresa a usuario", true, "/listar/empresas-usuario/");
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

    $('#frmImagenEmp').submit(function (e) {
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
    //#endregion

    //#region Código para Aumento de Sueldo
    var cboEmpleado = $('#frmGuardarDatoSalario select[name="empleado"]');
    var txtFechaIncremento = $('#frmGuardarDatoSalario input[name="fecha_incremento"]');
    var motivo_aumento = $('#frmGuardarDatoSalario select[name="motivo_aumento"]');
    var txtSalarioAnterior = $('#frmGuardarDatoSalario input[name="salario_anterior"]');
    var txtIncremento = $('#frmGuardarDatoSalario input[name="incremento"]');
    var txtNuevoSalario = $('#frmGuardarDatoSalario input[name="nuevo_salario"]');
    var txtComentarios = $('#frmGuardarDatoSalario textarea[name="comentarios"]');


    var theadDatosSalario = $('#tablaDatosSalario thead tr').clone(true);
    theadDatosSalario.appendTo( '#tablaDatosSalario thead' );
    $('#tablaDatosSalario thead tr:eq(1) th').each( function (i) {
        var title = $(this).text();
        if (title != "Acciones") {
            $(this).html( '<input type="text" class="form-control" placeholder="Buscar '+title+'" />' );
        }else{
            "";
        }
        $( 'input', this ).on( 'keyup change', function () {
            if ( tableDatosSalario.column(i).search() !== this.value ) {
                tableDatosSalario
                    .column(i)
                    .search( this.value )
                    .draw();
            }
        } );
    });
    theadDatosSalario.find("#thAcciones").html("");

    var tableDatosSalario = $('#tablaDatosSalario').DataTable({
        "ajax": "/obtener/datos-salarios/",
        "processing": true,
        "columnDefs": [
            {
                "targets": 5,
                "className": "text-center",
            },
            {
                "targets": 4,
                "className": "text-center",
                "width": "8%",
            },
            {
                "targets": 3,
                "width": "12%",
            },
            {
                "targets": 1,
                "width": "15%",
            },
            {
                "targets": 0,
                "width": "13%",
            }
        ],
        "columns": [
            {"data": "codigo"},
            {"data": "identidad"},
            {"data": "empleado"},
            {"data": "fecha"},
            {
                "data": "es_salario_actual",
                render: function(data, type, row) {
                    if (data) {
                        return "SI"
                    }else{
                        return "NO"
                    }
                }
            },
            {
                "data": "id",
                render : function(data, type, row) {
                    html = '<a href="#" class="btnEliminar" data="'+data+'" data-tooltip="Eliminar el registro" data-toggle="tooltip" data-original-title="Eliminar"> <i class="fa fa-close text-danger m-r-10"></i></a> ';
                    html += '<a href="#" class="btnEditarDatosSalario" data-toggle="tooltip" data="'+data+'" data-original-title="Editar"><i class="fa fa-pencil text-inverse m-r-10"></i></a> ';
                    html += '<a href="#" data-original-title="Ver registro" class="btnVerRegistroAumentoSalario" data="'+data+'"><i class="fa fa-search text-success m-r-10"></i></a>'
                    return html;
                }
            }
        ],
        orderCellsTop: true,
        fixedHeader: true,
        "language": {
            "lengthMenu": "Mostrar _MENU_ registros por página",
            "zeroRecords": "No se encontraron datos.",
            "info": "Página _PAGE_ de _PAGES_",
            "infoEmpty": "No existen registros",
            "infoFiltered": "(resultado de _MAX_ registros en total)",
            "paginate": {
                "first": "Primer registro",
                "last": "Último registro",
                "next": "Siguiente",
                "previous": "Anterior",
            },
            "search": "Buscar:",
            "loadingRecords": "Cargando datos...",
            "processing": "Procesando datos...",
        }
    });

    $('#aumento-salario-listado').on('click', '.btnEliminar', function(e) {
        e.preventDefault();
        var id = $(this).attr('data');
        Eliminar(id);
    });

    function Eliminar(id) {
        var Encabezado = 'Aumento de sueldo';
        var url = "/eliminar/aumento-salario/"; // the script where you handle the form input.
        $.ajax({
            type: "POST",
            url: url,
            data: {
                'id': id,
                'csrfmiddlewaretoken': token.val(),
            }, // serializes the form's elements.
            success: function(data)
            {
                if(data.error == false){
                    $.toast({
                        heading: Encabezado,
                        text: data.mensaje,
                        position: 'top-right',
                        loaderBg: '#ff6849',
                        icon: 'success',
                        hideAfter: 2000,
                        stack: 6
                    });
                    // setTimeout(function () {
                    //     location.reload();
                    // }, 2000);
                    tableDatosSalario.ajax.reload();
                }else{
                    $.toast({
                        heading: Encabezado,
                        text: data.mensaje,
                        position: 'top-right',
                        loaderBg: '#ff6849',
                        icon: 'error',
                        hideAfter: 5000,
                        stack: 6
                    });
                }
            },
            error: function(data) {
                console.log(data);
                $.toast({
                    heading: Encabezado,
                    text: data.status + ' - ' + data.statusText,
                    position: 'top-right',
                    loaderBg: '#ff6849',
                    icon: 'error',
                    hideAfter: 5000,
                    stack: 6
                });
            }
        });
    }

    $('#aumento-salario-listado').on('click', '.btnVerRegistroAumentoSalario', function (e) {
        e.preventDefault();
        url = '/ver-registro/aumento-salario/';
        metodo = 'GET';
        data = { 'id': $(this).attr('data') };
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

    $('#aumento-salario-listado #btnAgregar').on('click', function(e) {
        e.preventDefault();
        $('#frmGuardarDatoSalario').modal('toggle');
    });

    $('#aumento-salario-listado #btnRefrescar').on('click', function(e) {
        e.preventDefault();
        tableDatosSalario.ajax.reload();
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

    $('#frmGuardarDatoSalario #btnCancelar').on('click', function(e) {
        e.preventDefault();
    });

    $('#frmGuardarDatoSalario #btnGF_DS').on('click', function(e) {
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
        tableDatosSalario.ajax.reload();
    });

    $('#btnIncActualizar').on('click', function (e) {
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
        $('#frmEditarDatoSalario').modal('toggle');
    });

    $('#btnIncCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/aumento-salario/");
    });

    $('#aumento-salario-listado').on('click', '.btnEditarDatosSalario', function(e) {
        e.preventDefault();
        url = '/obtener/dato-salario/';
        metodo = 'GET';
        data = { 'id': $(this).attr('data') };
        $.ajax({
            type: metodo,
            url: url,
            data: data,
            success: function (data) {
                if (data.error === false) {
                    $('#reg_id').val(data.data.pk);
                    //$('#cboDSEmp').val(data.data.empleado).trigger('change');
                    $('#txtDS_NE').val(data.data.nombre_empleado);
                    $('#cboDSMotivo').val(data.data.motivo_aumento).trigger('change');
                    $('#txtDSFecha').datepicker('setDate',data.data.fecha_incremento);
                    $('#txtDS_SA').val(data.data.salario_anterior);
                    $('#txtDS_I').val(data.data.incremento);
                    $('#txtDS_NS').val(data.data.nuevo_salario);
                    $('#txtDS_C').text(data.data.comentarios);
                    $('#frmEditarDatoSalario').modal('toggle');
                }
            },
            error: function (data) {
                console.log(data);
            },
            dataType: 'json'
        });
    });

    $('#btnA_DS').on('click', function(e) {
        
    });

    $('#btnG_DS').on('click', function(e) {
        e.preventDefault();
        url = '/actualizar/aumento-salario/';
        metodo = 'POST';
        data = {
            'reg_id': $('#reg_id').val(),
            'motivo': $('#cboDSMotivo').val(),
            'incremento': $('#txtDS_I').val().replace(",", ""),
            'comentarios': $('#txtDS_C').val(),
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Aumento de salario", true, null);
        $('#frmEditarDatoSalario').modal('toggle');
    });

    $('#txtDS_I').on('change', function() {
        calcular_nuevo_sueldo2();
    });

    cboEmpleado.on('change', function () {
        obtener_ultimo_salario(cboEmpleado.val())
    });

    txtIncremento.on('change', function () {
        calcular_nuevo_sueldo();
        txtIncremento.val(formatNumber.new(txtIncremento.val()));
    });

    function calcular_nuevo_sueldo() {
        salario_anterior = 0;
        incremento = 0;
        nuevo_salario = 0;
        var salant = 0;
        var inc = 0;
        var nuevo_sal = 0;
        if (txtSalarioAnterior.val().length > 0) {
            salant = $('#frmGuardarDatoSalario  input[name="salario_anterior"]').val().replace(",", "");
            salario_anterior = Number($('#frmGuardarDatoSalario input[name="salario_anterior"]').val());
        }
        if (txtIncremento.val().length > 0) {
            inc = parseFloat($('#frmGuardarDatoSalario  input[name="incremento"]').val()).toFixed(4);
            incremento = Number($('#frmGuardarDatoSalario  input[name="incremento"]').val());
        }
        nuevo_sal = Number(salant) + Number(inc);
        nuevo_sal = parseFloat(nuevo_sal).toFixed(4);
        txtNuevoSalario.val(formatNumber.new(nuevo_sal));
    }

    function calcular_nuevo_sueldo2(){
        salario_anterior = 0;
        incremento = 0;
        nuevo_salario = 0;
        var salant = 0;
        var inc = 0;
        var nuevo_sal = 0;
        if ($('#txtDS_SA').val().length > 0) {
            salant = $('#txtDS_SA').val().replace(",", "");
            salario_anterior = Number($('#txtDS_SA').val());
        }
        if ($('#txtDS_I').val().length > 0) {
            salant = $('#txtDS_I').val().replace(",", "");
            salario_anterior = Number($('#txtDS_I').val());
        }
        nuevo_sal = Number(salant) + Number(inc);
        nuevo_sal = parseFloat(nuevo_sal).toFixed(4);
        $('#txtDS_NS').val(formatNumber.new(nuevo_sal));
    }

    function obtener_ultimo_salario(codEmpleado) {
        $.ajax({
            type: 'GET',
            url: '/obtener/salario-ultimo/',
            data: { 'idEmpleado': codEmpleado },
            success: function (data) {
                if (data.error == false) {

                    $('#frmGuardarDatoSalario input[name="salario_anterior"]').val(formatNumber.new(parseFloat(Number(data.salario_anterior)).toFixed(4)));
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

    //#region Código para Deducción General

    var dg_id = $('#deduccion_general input[name="id"]');
    var dg_deduccion = $('#deduccion_general input[name="deduccion"]');
    var dg_tipodeduccion = $('#deduccion_general select[name="tipo_deduccion"]');
    var dg_chkActivo = $('#deduccion_general input[name="activo"]');

    $('#deduccion_general #btnGuardar').on('click', function (e) {
        e.preventDefault();
        if (dg_chkActivo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/guardar/deduccion-general/';
        metodo = 'POST';
        data = {
            'tipo_deduccion': dg_tipodeduccion.val(),
            'deduccion': dg_deduccion.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Deducción General");
    });

    $('#deduccion_general #btnActualizar').on('click', function (e) {
        e.preventDefault();
        if (dg_chkActivo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/actualizar/deduccion-general/';
        metodo = 'POST';
        data = {
            'id': dg_id.val(),
            'tipo_deduccion': dg_tipodeduccion.val(),
            'deduccion': dg_deduccion.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Deducción General", true, "/listar/deduccion-general/");
    });

    $('#deduccion_general #btnCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/deduccion-general/");
    });
    //#endregion

    //#region Código para Deducción General Detalle

    var dgd_id = $('#deduccion_general_detalle input[name="id"]');
    var dgd_deduccion = $('#deduccion_general_detalle select[name="deduccion"]');
    var dgd_nomina = $('#deduccion_general_detalle select[name="planilla"]');
    var dgd_tipo_pago = $('#deduccion_general_detalle select[name="tipo_pago"]');
    var dgd_tipo_contrato = $('#deduccion_general_detalle select[name="tipo_contrato"]');
    var dgd_valor = $('#deduccion_general_detalle input[name="valor"]');
    var dgd_fecha = $('#deduccion_general_detalle input[name="fecha"]');
    var dgd_activo = $('#deduccion_general_detalle input[name="activo"]');

    $('#deduccion_general_detalle #btnGuardar').on('click', function (e) {
        e.preventDefault();
        if (dgd_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/guardar/deduccion-general-detalle/';
        metodo = 'POST';
        data = {
            'deduccion': dgd_deduccion.val(),
            'nomina': dgd_nomina.val(),
            'tipo_pago': dgd_tipo_pago.val(),
            'tipo_contrato': dgd_tipo_contrato.val(),
            'valor': dgd_valor.val(),
            'fecha': dgd_fecha.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Detalles de Deducción General");
    });

    $('#deduccion_general_detalle #btnActualizar').on('click', function (e) {
        e.preventDefault();
        if (dgd_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/actualizar/deduccion-general-detalle/';
        metodo = 'POST';
        data = {
            'id': dgd_id.val(),
            'deduccion': dgd_deduccion.val(),
            'nomina': dgd_nomina.val(),
            'tipo_pago': dgd_tipo_pago.val(),
            'tipo_contrato': dgd_tipo_contrato.val(),
            'valor': dgd_valor.val(),
            'fecha': dgd_fecha.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Detalles de Deducción General", true, "/listar/deduccion-general-detalle/");
    });

    $('#deduccion_general_detalle #btnCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/deduccion-general-detalle/");
    });

    //#endregion

    //#region Código para Deducción Individual

    var di_id = $('#deduccion_individual input[name="id"]');
    var di_deduccion = $('#deduccion_individual input[name="deduccion"]');
    var di_tipodeduccion = $('#deduccion_individual select[name="tipo_deduccion"]');
    var di_controlasaldo = $('#deduccion_individual input[name="controla_saldo"]');
    var di_chkActivo = $('#deduccion_individual input[name="activo"]');

    $('#deduccion_individual #btnGuardar').on('click', function (e) {
        e.preventDefault();
        if (di_controlasaldo.is(":checked")) {
            vControlaSaldo = 1;
        } else {
            vControlaSaldo = 0;
        }
        if (di_chkActivo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/guardar/deduccion-individual/';
        metodo = 'POST';
        data = {
            'tipo_deduccion': di_tipodeduccion.val(),
            'deduccion': di_deduccion.val(),
            'controla_saldo': vControlaSaldo,
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Deducción Individual");
    });

    $('#deduccion_individual #btnActualizar').on('click', function (e) {
        e.preventDefault();
        if (di_controlasaldo.is(":checked")) {
            vControlaSaldo = 1;
        } else {
            vControlaSaldo = 0;
        }
        if (di_chkActivo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/actualizar/deduccion-individual/';
        metodo = 'POST';
        data = {
            'id': di_id.val(),
            'tipo_deduccion': di_tipodeduccion.val(),
            'deduccion': di_deduccion.val(),
            'controla_saldo': vControlaSaldo,
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Deducción Individual", true, "/listar/deduccion-individual/");
    });

    $('#deduccion_individual #btnCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/deduccion-individual/");
    });

    //#endregion

    //#region Código para Deducción Individual Detalle

    var did_id = $('#deduccion_individual_detalle input[name="id"]');
    var did_deduccion = $('#deduccion_individual_detalle select[name="deduccion"]');
    var did_empleado = $('#deduccion_individual_detalle select[name="empleado"]');
    var did_valor = $('#deduccion_individual_detalle input[name="valor"]');
    var did_fecha = $('#deduccion_individual_detalle input[name="fecha"]');
    var did_activo = $('#deduccion_individual_detalle input[name="activo"]');

    $('#deduccion_individual_detalle #btnGuardar').on('click', function (e) {
        e.preventDefault();
        if (did_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/guardar/deduccion-individual-detalle/';
        metodo = 'POST';
        data = {
            'deduccion': did_deduccion.val(),
            'empleado': did_empleado.val(),
            'valor': did_valor.val(),
            'fecha': did_fecha.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Detalles de Deducción Individual");
    });

    $('#deduccion_individual_detalle #btnActualizar').on('click', function (e) {
        e.preventDefault();
        if (did_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/actualizar/deduccion-individual-detalle/';
        metodo = 'POST';
        data = {
            'id': did_id.val(),
            'deduccion': did_deduccion.val(),
            'empleado': did_empleado.val(),
            'valor': did_valor.val(),
            'fecha': did_fecha.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Detalle de Deducción Individual", true, "/listar/deduccion-individual-detalle/");
    });

    $('#deduccion_individual_detalle #btnCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/deduccion-individual-detalle/");
    });

    //#endregion

    //#region Código para Deducción Individual Planilla

    var dip_id = $('#deduccion_individual_planilla input[name="id"]');
    var dip_deduccion = $('#deduccion_individual_planilla select[name="deduccion"]');
    var dip_empleado = $('#deduccion_individual_planilla select[name="empleado"]');
    var dip_valor = $('#deduccion_individual_planilla input[name="valor"]');
    var dip_planilla = $('#deduccion_individual_planilla select[name="planilla"]');
    var dip_activo = $('#deduccion_individual_planilla input[name="activo"]');

    $('#deduccion_individual_planilla #btnGuardar').on('click', function (e) {
        e.preventDefault();
        if (dip_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/guardar/deduccion-individual-planilla/';
        metodo = 'POST';
        data = {
            'deduccion': dip_deduccion.val(),
            'empleado': dip_empleado.val(),
            'valor': dip_valor.val(),
            'planilla': dip_planilla.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Deducción Individual ");
    });

    $('#deduccion_individual_planilla #btnActualizar').on('click', function (e) {
        e.preventDefault();
        if (dip_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/actualizar/deduccion-individual-planilla/';
        metodo = 'POST';
        data = {
            'id': dip_id.val(),
            'deduccion': dip_deduccion.val(),
            'empleado': dip_empleado.val(),
            'valor': dip_valor.val(),
            'planilla': dip_planilla.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Deducción Individual en Planilla", true, "/listar/deduccion-individual-planilla/");
    });

    $('#deduccion_individual_planilla #btnCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/deduccion-individual-planilla/");
    });

    //#endregion

    //#region Código para Horas Extras

    var he_id = $('#horaextra input[name="id"]');
    var he_jornada = $('#horaextra input[name="jornada"]');
    var he_horaini = $('#horaextra input[name="horaini"]');
    var he_horafin = $('#horaextra input[name="horafin"]');
    var he_horasdiarias = $('#horaextra input[name="horasDiarias"]');
    var he_horassemanas = $('#horaextra input[name="horasSemana"]');
    var he_noexede = $('#horaextra input[name="noExedeNocturno"]');
    var he_horaextra = $('#horaextra input[name="horaExtra"]');
    var he_activo = $('#horaextra input[name="activo"]');

    $('#horaextra #btnGuardar').on('click', function (e) {
        e.preventDefault();
        if (he_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/guardar/he/';
        metodo = 'POST';
        data = {
            'jornada': he_jornada.val(),
            'horaini': he_horaini.val(),
            'horafin': he_horafin.val(),
            'horasDiarias': he_horasdiarias.val(),
            'horasSemana': he_horassemanas.val(),
            'noexede': he_noexede.val(),
            'horaextra': he_horaextra.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Horas Extras");
    });

    $('#horaextra #btnActualizar').on('click', function (e) {
        e.preventDefault();
        if (he_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/actualizar/he/';
        metodo = 'POST';
        data = {
            'id': he_id.val(),
            'jornada': he_jornada.val(),
            'horaini': he_horaini.val(),
            'horafin': he_horafin.val(),
            'horasDiarias': he_horasdiarias.val(),
            'horasSemana': he_horassemanas.val(),
            'noexede': he_noexede.val(),
            'horaextra': he_horaextra.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Horas Extras", true, "/listar/he/");
    });

    $('#horaextra #btnCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/he/");
    });

    //#endregion

    //#region Código para ISR

    var isr_id = $('#isr input[name="id"]');
    var isr_desde = $('#isr input[name="desde"]');
    var isr_hasta = $('#isr input[name="hasta"]');
    var isr_prcnt = $('#isr input[name="porcentaje"]');
    var isr_activo = $('#isr input[name="activo"]');

    $('#isr #btnGuardar').on('click', function (e) {
        e.preventDefault();
        if (isr_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/guardar/isr/';
        metodo = 'POST';
        data = {
            'desde': isr_desde.val(),
            'hasta': isr_hasta.val(),
            'porcentaje': isr_prcnt.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Impuesto sobre renta");
    });
    $('#isr #btnActualizar').on('click', function (e) {
        e.preventDefault();
        if (isr_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/actualizar/isr/';
        metodo = 'POST';
        data = {
            'id': isr_id.val(),
            'desde': isr_desde.val(),
            'hasta': isr_hasta.val(),
            'porcentaje': isr_prcnt.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Impuesto sobre renta", true, "/listar/isr/");
    });

    $('#isr #btnCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/isr/");
    });

    //#endregion

    //#region Código para ISR Encabezado
    botonGuardar = $('#formEncabezadoISR #btnGuardar');
    botonGuardarDetalleISR = $('#formAgregarDetalle #btnGuardarDetalleISR');
    var isr_desde = $('#formAgregarDetalle input[name="desde"]');
    var isr_hasta = $('#formAgregarDetalle input[name="hasta"]');
    var isr_prcnt = $('#formAgregarDetalle input[name="porcentaje"]');

    textCodigo = $('#formEncabezadoISR input[name="txtCodigo"]');
    textFecha = $('#formEncabezadoISR input[name="fecha_vigencia"]');
    textDeducible = $('#formEncabezadoISR input[name="txtDeducible"]');
    textValor = $('#formEncabezadoISR input[name="txtValor"]');
    textDeducible1 = $('#formEncabezadoISR input[name="txtDeducible1"]');
    textValor1 = $('#formEncabezadoISR input[name="txtValor1"]');
    textDeducible2 = $('#formEncabezadoISR input[name="txtDeducible2"]');
    textValor2 = $('#formEncabezadoISR input[name="txtValor2"]');

    botonVerRegistro = $('#frmEncabezadoISR #btnVerRegistro');
    botonRefrescar = $('#frmEncabezadoISR #btnRefrescar');

    botonGuardar.on('click', function (e) {
        e.preventDefault();
        url = '/guardar/isr-encabezado/';
        metodo = 'POST';
        data = {
            'codigo': textCodigo.val(),
            'fecha': textFecha.val(),
            'deducible': textDeducible.val(),
            'valor': textValor.val(),
            'deducible1': textDeducible1.val(),
            'valor1': textValor1.val(),
            'deducible2': textDeducible2.val(),
            'valor2': textValor2.val(),
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Impuesto Sobre Renta");
    });

    botonGuardarDetalleISR.on('click', function (e) {
        e.preventDefault();
        url = '/guardar/isr-detalle/';
        metodo = 'POST';
        data = {
            'desde': isr_desde.val(),
            'hasta': isr_hasta.val(),
            'porcentaje': isr_prcnt.val(),
            'isr_enc': $('input[name="isr_enc_pk"]').val(),
            'csrfmiddlewaretoken': token.val(),
        };
        $.ajax({
            type: metodo,
            url: "/guardar/isr/",
            data: data,
            success: function (data) {
                if (data.error === false) {
                    isr_desde.val('');
                    isr_hasta.val('');
                    isr_prcnt.val('');
                    mensaje("Impuesto Sobre Renta - Detalle", "Se ha creado el registro", "ok", 3500);
                    var html = '<tr>';
                    html += '<td class="text-right">' + data.dato.desde + '</td>';
                    html += '<td class="text-right">' + data.dato.hasta + '</td>';
                    html += '<td class="text-right">' + data.dato.porcentaje + '</td>';
                    html += '<td class="text-center"><a href="#" class="btnEliminarDetalleISR" data="' + data.dato.pk + '">Eliminar</a></td>';
                    html += '</tr>';
                    $('#formularioModalVerRegistro #contenido-modal tbody').prepend(html);
                    $('#formAgregarDetalle').modal('hide');
                } else {
                    mensaje("Impuesto Sobre Renta - Detalle", data.mensaje, "error", 3500);
                }
            },
            error: function (data) {
                console.log(data);
            },
            dataType: 'json'
        }).done(function (data) {

        });
    });

    $('#formularioModalVerRegistro').on('click', "#btnAgregarDetalle", function (e) {
        $('#formAgregarDetalle').modal({
            show: 'true',
        });
    });

    $('#formularioModalVerRegistro').on('click', '.btnEliminarDetalleISR', function (e) {
        e.preventDefault();
        url = '/eliminar/isr/';
        metodo = 'POST';
        var registro_id = $(this).attr('data');
        var elemento = $(this).parents('tr');
        data = {
            'id': registro_id,
            'csrfmiddlewaretoken': token.val(),
        };
        $.ajax({
            type: metodo,
            url: url,
            data: data,
            success: function (data) {
                if (data.error === false) {
                    mensaje("Impuesto Sobre Renta - Detalle", data.mensaje, "ok", 3500);
                    elemento.hide();
                    //$('#formAgregarDetalle').modal('hide');
                } else {
                    mensaje("Impuesto Sobre Renta - Detalle", data.mensaje, "error", 3500);
                }
            },
            error: function (data) {
                console.log(data);
            },
            dataType: 'json'
        }).done(function (data) {

        });
    });

    botonVerRegistro.on('click', function (e) {
        e.preventDefault();
        BloquearPantalla();
        var idregistro = $(this).attr('data');
        $.ajax({
            type: "GET",
            url: "/obtener/isr-encabezado/",
            data: { 'Id': idregistro },
            success: function (data) {
                $('#contenido-modal').html(data);
                $('input[name="isr_enc_pk"]').val(idregistro);
            },
            error: function (data) {
                errores = errores + 1;
                console.log("Error: " + data);
            },
            dataType: 'html'
        }).done(function () {
            DesbloquearPantalla();
            $('#formularioModalVerRegistro').modal({
                show: 'true',
            });
        });
    });
    //#endregion

    //#region Código para Impuesto Vecinal

    var iv_id = $('#impuestovecinal input[name="id"]');
    var iv_desde = $('#impuestovecinal input[name="desde"]');
    var iv_hasta = $('#impuestovecinal input[name="hasta"]');
    var iv_porcentaje = $('#impuestovecinal input[name="porcentaje"]');
    var iv_activo = $('#impuestovecinal input[name="activo"]');

    $('#impuestovecinal #btnGuardar').on('click', function (e) {
        e.preventDefault();
        if (iv_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/guardar/impuesto-vecinal/';
        metodo = 'POST';
        data = {
            'desde': iv_desde.val(),
            'hasta': iv_hasta.val(),
            'porcentaje': iv_porcentaje.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Impuesto Vecinal");
    });

    $('#impuestovecinal #btnActualizar').on('click', function (e) {
        e.preventDefault();
        if (iv_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/actualizar/impuesto-vecinal/';
        metodo = 'POST';
        data = {
            'id': iv_id.val(),
            'desde': iv_desde.val(),
            'hasta': iv_hasta.val(),
            'porcentaje': iv_porcentaje.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Impuesto Vecinal", true, "/listar/impuesto-vecinal/");
    });

    $('#impuestovecinal #btnCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/impuesto-vecinal/");
    });

    //#endregion

    //#region Código para Ingreso General


    var ing_id = $('#ingreso_general input[name="id"]');
    var ing_txtIngreso = $('#ingreso_general input[name="txtIngresoG"]');
    var ing_cboTipoIngreso = $('#ingreso_general select[name="cboTipoIngreso"]');
    var ing_chkGravable = $('#ingreso_general input[name="ingresog_gravable"]');
    var ing_chkActivo = $('#ingreso_general input[name="chkActivo"]');
    var ing_btnGuardar = $('#ingreso_general #btnGuardar');
    var ing_btnActualizar = $('#ingreso_general #btnActualizar');
    var ing_btnCancelar = $('#ingreso_general #btnCancelar');

    ing_btnGuardar.on('click', function (e) {
        e.preventDefault();
        if (ing_chkGravable.is(":checked")) {
            vGravable = 1;
        } else {
            vGravable = 0;
        }
        if (ing_chkActivo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/guardar/ingreso-general/';
        metodo = 'POST';
        data = {
            'ingreso_g': ing_txtIngreso.val(),
            'tipo_ingreso': ing_cboTipoIngreso.val(),
            'gravable': vGravable,
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Ingreso General");
    });

    ing_btnActualizar.on('click', function (e) {
        e.preventDefault();
        if (ing_chkActivo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        if (ing_chkGravable.is(":checked")) {
            vGravable = 1;
        } else {
            vGravable = 0;
        }
        url = '/actualizar/ingreso-general/';
        metodo = 'POST';
        data = {
            'id': ing_id.val(),
            'ingreso_g': ing_txtIngreso.val(),
            'tipo_ingreso': ing_cboTipoIngreso.val(),
            'gravable': vGravable,
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Ingreso General", true, "/listar/ingreso-general/");
    });

    ing_btnCancelar.on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/ingreso-general/");
    });

    //#endregion

    //#region  Código para Ingreso General Detalle

    var igd_id = $('#ingreso_general_detalle input[name="id"]');
    var igd_ingreso = $('#ingreso_general_detalle select[name="ingreso"]');
    var igd_nomina = $('#ingreso_general_detalle select[name="nomina"]');
    var igd_tipo_pago = $('#ingreso_general_detalle select[name="tipo_pago"]');
    var igd_tipo_contrato = $('#ingreso_general_detalle select[name="tipo_contrato"]');
    var igd_valor = $('#ingreso_general_detalle input[name="valor"]');
    var igd_fecha = $('#ingreso_general_detalle input[name="fecha"]');
    var igd_activa = $('#ingreso_general_detalle input[name="activo"]');

    $('#ingreso_general_detalle #btnGuardar').on('click', function (e) {
        e.preventDefault();
        if (igd_activa.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/guardar/ingreso-general-detalle/';
        metodo = 'POST';
        data = {
            'ingreso': igd_ingreso.val(),
            'nomina': igd_nomina.val(),
            'tipo_pago': igd_tipo_pago.val(),
            'tipo_contrato': igd_tipo_contrato.val(),
            'valor': igd_valor.val(),
            'fecha': igd_fecha.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Ingreso General Detalle");
    });

    $('#ingreso_general_detalle #btnActualizar').on('click', function (e) {
        e.preventDefault();
        if (igd_activa.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/actualizar/ingreso-general-detalle/';
        metodo = 'POST';
        data = {
            'id': igd_id.val(),
            'ingreso': igd_ingreso.val(),
            'nomina': igd_nomina.val(),
            'tipo_pago': igd_tipo_pago.val(),
            'tipo_contrato': igd_tipo_contrato.val(),
            'valor': igd_valor.val(),
            'fecha': igd_fecha.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Detalle de Ingreso General", true, "/listar/ingreso-general-detalle/");
    });

    $('#ingreso_general_detalle #btnCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/ingreso-general-detalle/");
    });

    //#endregion

    //#region Código para Ingreso Individual

    var ini_id = $('#ingreso_individual input[name="id"]');
    var ini_txtIngresoI = $('#ingreso_individual input[name="txtIngresoI"]');
    var ini_cboTipoI = $('#ingreso_individual select[name="cboTipoIngreso"]');
    var ini_chkGravable = $('#ingreso_individual input[name="ingresoi_gravable"]');
    var ini_chkActivo = $('#ingreso_individual input[name="chkActivo"]');
    var ini_btnGuardar = $('#ingreso_individual #btnGuardar');
    var ini_btnActualizar = $('#ingreso_individual #btnActualizar');
    var ini_btnCancelar = $('#ingreso_individual #btnCancelar');
    var vGravable = 0;


    ini_btnGuardar.on('click', function (e) {
        e.preventDefault();
        if (ini_chkGravable.is(":checked")) {
            vGravable = 1;
        } else {
            vGravable = 0;
        }
        if (ini_chkActivo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/guardar/ingreso-individual/';
        metodo = 'POST';
        data = {
            'ingreso_i': ini_txtIngresoI.val(),
            'tipo_ingreso': ini_cboTipoI.val(),
            'gravable': vGravable,
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Ingreso Individual");
    });

    ini_btnActualizar.on('click', function (e) {
        e.preventDefault();
        if (ini_chkActivo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        if (ini_chkGravable.is(":checked")) {
            vGravable = 1;
        } else {
            vGravable = 0;
        }
        url = '/actualizar/ingreso-individual/';
        metodo = 'POST';
        data = {
            'id': ini_id.val(),
            'ingreso_i': ini_txtIngresoI.val(),
            'tipo_ingreso': ini_cboTipoI.val(),
            'gravable': vGravable,
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Ingreso Individual", true, "/listar/ingreso-individual/");
    });

    ini_btnCancelar.on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/ingreso-individual/");
    });


    //#endregion

    //#region Código pára Ingreso Individual Detalle

    var iid_id = $('#ingreso_individual_detalle input[name="id"]');
    var iid_ingreso = $('#ingreso_individual_detalle select[name="ingreso"]');
    var iid_empleado = $('#ingreso_individual_detalle select[name="empleado"]');
    var iid_valor = $('#ingreso_individual_detalle input[name="valor"]');
    var iid_fecha = $('#ingreso_individual_detalle input[name="fecha"]');
    var iid_activo = $('#ingreso_individual_detalle input[name="activo"]');

    $('#ingreso_individual_detalle #btnGuardar').on('click', function (e) {
        e.preventDefault();
        if (iid_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/guardar/ingreso-individual-detalle/';
        metodo = 'POST';
        data = {
            'ingreso': iid_ingreso.val(),
            'empleado': iid_empleado.val(),
            'valor': iid_valor.val(),
            'fecha': iid_fecha.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Detalles de Ingreso Individual");
    });

    $('#ingreso_individual_detalle #btnActualizar').on('click', function (e) {
        e.preventDefault();
        if (iid_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/actualizar/ingreso-individual-detalle/';
        metodo = 'POST';
        data = {
            'id': iid_id.val(),
            'ingreso': iid_ingreso.val(),
            'empleado': iid_empleado.val(),
            'valor': iid_valor.val(),
            'fecha': iid_fecha.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Detalle de Ingreso Individual", true, "/listar/ingreso-individual-detalle/");
    });

    $('#ingreso_individual_detalle #btnCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/ingreso-individual-detalle/");
    });

    //#endregion

    //#region Código para Ingreo Individual Planilla

    var iip_id = $('#ingreso_individual_planilla input[name="id"]');
    var iip_ingreso = $('#ingreso_individual_planilla select[name="ingreso"]');
    var iip_planilla = $('#ingreso_individual_planilla select[name="planilla"]');
    var iip_empleado = $('#ingreso_individual_planilla select[name="empleado"]');
    var iip_valor = $('#ingreso_individual_planilla input[name="valor"]');
    var iip_activo = $('#ingreso_individual_planilla input[name="activo"]');

    $('#ingreso_individual_planilla #btnGuardar').on('click', function (e) {
        e.preventDefault();
        if (iip_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/guardar/ingreso-individual-planilla/';
        metodo = 'POST';
        data = {
            'ingreso': iip_ingreso.val(),
            'empleado': iip_empleado.val(),
            'planilla': iip_planilla.val(),
            'valor': iip_valor.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Ingreso Individual en Planilla");
    });

    $('#ingreso_individual_planilla #btnActualizar').on('click', function (e) {
        e.preventDefault();
        if (iip_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/actualizar/ingreso-individual-planilla/';
        metodo = 'POST';
        data = {
            'id': iip_id.val(),
            'ingreso': iip_ingreso.val(),
            'empleado': iip_empleado.val(),
            'planilla': iip_planilla.val(),
            'valor': iip_valor.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Ingreso Individual en Planilla", true, "/listar/ingreso-individual-planilla/");
    });

    $('#ingreso_individual_planilla #btnCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/ingreso-individual-planilla/");
    });

    //#endregion

    //#region Código para Planilla

    var btnPlGuardar = $('#frmPlanilla #btnGuardar');
    var btnPlActualizar = $('#frmPlanilla #btnActualizar');
    var btnPlCancelar = $('#frmPlanilla #btnCancelar');
    var btnPlVerRegistro = $('#planilla-listado #btnVerRegistro');
    var cboPlTipoPlanilla = $('#frmPlanilla select[name="tipo_planilla"]');
    var cboPlTipoContrato = $('#frmPlanilla select[name="tipo_contrato"]');
    var cboPlTipoPago = $('#frmPlanilla select[name="tipo_pago"]');
    var txtPlFechaPago = $('#frmPlanilla input[name="fecha_pago"]');
    var txtPlFechaInicio = $('#frmPlanilla input[name="fecha_inicio"]');
    var txtPlFechaFin = $('#frmPlanilla input[name="fecha_fin"]');
    var txtPlFechaPago = $('#frmPlanilla input[name="fecha_pago"]');
    var txtPlDescripcion = $('#frmPlanilla textarea[name="descripcion"]');
    var btnBuscarPlanilla = $('#planilla-reporte-general #btnBuscar');
    var cboDepartamentoRep = $('#planilla-reporte-general #cboDepartamento');
    var cboTipoContrato = $('#planilla-reporte-general #cboTipoContrato');
    var cboTipoPlanilla = $('#planilla-reporte-general #cboTipoPlanilla');
    var cboFrecuenciaPago = $('#planilla-reporte-general #cboFrecuenciaPago');
    var cboDesde = $('#planilla-reporte-general #txtDesde');
    var cboHasta = $('#planilla-reporte-general #txtHasta');

    var btnGenerar = $('.planilla-generar #btnGenerar');
    var btnGenerar2 = $('.planilla-generar #btnGenerar2');
    var columnas = [];

    $('#tablaProbando').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    });

    $('#example23').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    });
    $('.buttons-copy, .buttons-csv, .buttons-print, .buttons-pdf, .buttons-excel').addClass('btn btn-primary m-r-10');

    btnPlGuardar.on('click', function (e) {
        e.preventDefault();
        url = '/guardar/planilla/';
        metodo = 'POST';
        data = {
            'tipo_planilla': cboPlTipoPlanilla.val(),
            'tipo_pago': cboPlTipoPago.val(),
            'tipo_contrato': cboPlTipoContrato.val(),
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
            'tipo_contrato': cboPlTipoContrato.val(),
            'fecha_pago': txtPlFechaPago.val(),
            'fecha_inicio': txtPlFechaInicio.val(),
            'fecha_fin': txtPlFechaFin.val(),
            'descripcion': txtPlDescripcion.val(),
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Planilla", true, "/listar/planilla/");
    });

    btnPlCancelar.on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/planilla/");
    });

    btnPlVerRegistro.on('click', function (e) {
        // e.preventDefault();
        // url = '/ver-registro/planilla/';
        // metodo = 'GET';
        // data = { 'id': $(this).attr('data') };
        // $.ajax({
        //     type: metodo,
        //     url: url,
        //     data: data,
        //     success: function (data) {
        //         $('#planilla-modal').html(data);
        //     },
        //     error: function (data) {
        //         console.log(data);
        //     },
        //     dataType: 'html'
        // });
        // $('#responsive-modal').modal('toggle');
    });

    valor = 0;
    var cboPlanillas = $('.planilla-generar #cboPlanillas');

    var prog = 0;
    var prog2 = 0;
    var errores = 0;
    var requests = [];
    var totalD = 0;
    var ldatos;
    var htmlencabezado = "";
    var htmldetalle = "";
    var datosreporte = [];

    btnGenerar.on('click', function (e) {
        e.preventDefault();
        url = '/obtener/empleados-planilla/';
        metodo = 'GET';
        data = { 'id': cboPlanillas.val() };
        $.ajax({
            type: metodo,
            url: url,
            data: data,
            success: function (data) {
                if (data.error) {
                    console.log(data);
                } else {
                    if (data.error) {
                        mensaje("Generar Planilla", data.mensaje, "warning", 3500);
                    } else {
                        ldatos = data.empleados;
                        totalID = ldatos.length;
                    }
                }
            },
            error: function (data) {
                console.log(data);
            },
            dataType: 'json'
        }).done(function () {
            enviar(0);
        });

        function enviar(indice) {
            if (indice < ldatos.length) {
                url = "/calcular/planilla-empleado/";
                metodo = 'POST';
                data = {
                    'empleado_id': ldatos[indice].ID,
                    'planilla_id': cboPlanillas.val(),
                    'csrfmiddlewaretoken': token.val(),
                }
                $.ajax({
                    type: metodo,
                    url: url,
                    data: data,
                    success: function (data) {
                        if (data.error) {
                            alert(data.mensaje);
                            errores = errores + 1;
                        } else {
                            prog2 = ((indice + 1) / ldatos.length) * 100;
                            $('#loader-bar').attr("style", "width: " + prog2 + "%");
                            $('#loader-bar').html(prog2 + "%");
                        };
                    },
                    error: function (data) {
                        errores = errores + 1;
                        console.log("Error: " + data);
                    },
                    dataType: 'json'
                }).done(function () {
                    enviar(indice + 1);
                });
            } else {
                $('#registros_procesados_planilla').text(indice);
                $('#registros_planilla_error').text(errores);
                obtener_planilla_generada(cboPlanillas.val());
            }
        }
    });

    btnGenerar2.on('click', function (e) {
        $('div.block5').block({
            message: '<h4><img src="../../static/plugins/images/busy.gif" /> Espere un momento...</h4>',
            css: {
                border: '1px solid #fff',
            }
        });
        e.preventDefault();
        url = '/generar/planilla2/';
        metodo = 'POST';
        data = { 'id': cboPlanillas.val(), 'csrfmiddlewaretoken': token.val() };

        $.ajax({
            type: metodo,
            url: url,
            data: data,
            success: function (data) {
                if (data.error != true) {
                    obtener_planilla_generada(cboPlanillas.val());
                };
            },
            error: function (data) {
                console.log(data);
            },
            dataType: 'json'
        }).done(function () {
            $('div.block5').unblock();
        });
    });

    function obtener_planilla_generada(Id_Planilla) {
        $.ajax({
            type: "GET",
            url: "/obtener/planilla-generada/",
            data: { 'Id': Id_Planilla },
            success: function (data) {
                if (data.error) {
                    console.log(data.mensaje);
                } else {
                    $('.lista-empleados').html(data);
                };
            },
            error: function (data) {
                errores = errores + 1;
                console.log("Error: " + data);
            },
            dataType: 'html'
        }).done(function () {

        });
    }

    btnBuscarPlanilla.on('click', function (e) {
        // e.preventDefault();
        // url = '/generar/reporte-general/planilla/';
        // metodo = 'GET';
        // data = {
        //     'departamento_id': cboDepartamentoRep.val(),
        //     'tipo_contrato_id': cboTipoContrato.val(),
        //     'tipo_planilla_id': cboTipoPlanilla.val(),
        //     'frecuencia_pago_id': cboFrecuenciaPago.val(),
        //     'desde': cboDesde.val(),
        //     'hasta': cboHasta.val(),
        // };

        // $.ajax({
        //     type: metodo,
        //     url: url,
        //     data: data,
        //     success: function (data) {
        //         if (data.error != true) {
        //             $('#tablaProbando').DataTable({
        //                 dom: 'Bfrtip',
        //                 buttons: [
        //                     'copy', 'csv', 'excel', 'pdf', 'print'
        //                 ],
        //                 //"data": details,
        //                 "columns": data.columns,
        //                 "data": data.data,
        //                 "destroy": true,
        //             });
        //         };
        //     },
        //     error: function (data) {
        //         console.log(mensaje);
        //     },
        //     dataType: 'json'
        // }).done(function () {
        //     $('div.block5').unblock();
        // });
    });
    //#endregion

    //#region Código para Perfil Empleado
    $('#detalle-deducciones').on('click', '#btnAgregarEmpleadoDeduccion', function () {
        var $radios = $('input:radio[name=radio]');
        $('select[name="cbodeduccion"]').val("0");
        $radios.filter('[value=0]').prop('checked', false);
        $radios.filter('[value=1]').prop('checked', true);
        $('select[name="cboperiodopago"]').val("0");
        $('#chkActivoDedEmp').prop('checked', false);
        $('#btnActualizarEmplDed').addClass('hide');
        $('#btnGuardarEmplDed').removeClass('hide');
        $('#ctrl-chkActivo').addClass('hide');
        $('.cbo-periodo').removeClass('hide');
    });

    $('#btnGuardarEmplDed').on('click', function (e) {
        $('select[name="cbodeduccion"]')
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/guardar/deduccion-empleado/",
            data: {
                'deduccion': $('select[name="cbodeduccion"]').val(),
                'tipo_periodo': $("input[name='radio']:checked").val(),
                'periodo': $('select[name="cboperiodopago"]').val(),
                'activo': $('#chkActivoDedEmp').prop('checked'),
                'empleado': $('input[name="empleado"]').val(),
                'csrfmiddlewaretoken': token.val(),
            },
            success: function (data) {
                if (data.error === false) {
                    swal("Registrado!", data.mensaje, "success");
                    $('#form-empleado-deduccion').modal('hide');
                    obtenerDeduccionesEmpleado();
                } else {
                    swal("¡Cancelado!", data.mensaje, "error");
                }
            },
            error: function (data) {
                swal("¡Cancelado!", data.mensaje, "error");
                console.log(data)
            },
            dataType: "json",
        });
    });
    var registro_id;
    $('#btnActualizarEmplDed').on('click', function (e) {
        e.preventDefault();
        var pActivo;
        if ($('#chkActivoDedEmp').is(':checked')) {
            pActivo = true;
        } else {
            pActivo = false;
        }
        $.ajax({
            type: "POST",
            url: "/actualizar/deduccion-empleado/",
            data: {
                'id': registro_id,
                'deduccion': $('select[name="cbodeduccion"]').val(),
                'tipo_periodo': $("input[name='radio']:checked").val(),
                'periodo': $('select[name="cboperiodopago"]').val(),
                'activo': pActivo,
                'empleado': $('input[name="empleado"]').val(),
                'csrfmiddlewaretoken': token.val(),
            },
            success: function (data) {
                if (data.error === false) {
                    swal("Actualizado!", data.mensaje, "success");
                    $('#form-empleado-deduccion').modal('hide');
                    obtenerDeduccionesEmpleado();
                } else {
                    swal("¡Cancelado!", data.mensaje, "error");
                }
            },
            error: function (data) {
                swal("¡Cancelado!", data.mensaje, "error");
            },
            dataType: "json",
        });
    });

    function obtenerDeduccionesEmpleado() {
        $.ajax({
            type: "GET",
            url: "/obtener/deducciones-empleado/",
            data: { 'empleado_id': $('input[name="empleado"]').val() },
            success: function (data) {
                $('#detalle-deducciones').html(data);
            },
            error: function (data) {
                console.log("Error: " + data);
            },
            dataType: 'html'
        }).done(function () {

        });
    }

    $('#detalle-deducciones').on('click', '.btnEditarDeduccionEmp', function (e) {
        e.preventDefault();
        registro_id = $(this).attr('data');
        var $radios = $('input:radio[name=radio]');
        $('#btnActualizarEmplDed').removeClass('hide');
        $('#btnGuardarEmplDed').addClass('hide');
        $('#ctrl-chkActivo').removeClass('hide');

        $.ajax({
            type: "GET",
            url: "/obtener/deduccion-empleado/",
            data: { 'id': registro_id },
            success: function (data) {
                if (data.error == false) {
                    $('select[name="cbodeduccion"]').val("" + data.deduccion + "");
                    if (data.deduccion_parcial === false) {
                        $radios.filter('[value=0]').prop('checked', true);
                        $('.cbo-periodo').addClass('hide');
                    } else {
                        $radios.filter('[value=1]').prop('checked', true);
                        $('.cbo-periodo').removeClass('hide');
                    }
                    if (data.activo === true) {
                        $('#chkActivoDedEmp').prop('checked', true);
                    } else {
                        $('#chkActivoDedEmp').prop('checked', false);
                    }
                    $('select[name="cboperiodopago"]').val("" + data.periodo + "");
                } else {
                    console.log(data.mensaje);
                }
            },
            error: function (data) {
                swal("¡Cancelado!", "El proceso no se ha realizado.", "error");
                console.log(data.mensaje);
            }
        });
    });


    $('input[type=radio][name=radio]').change(function () {
        if ($(this).val() === "0") {
            $('.cbo-periodo').addClass('hide');
        }
        else {
            console.log("Entro aqui");
            $('.cbo-periodo').removeClass('hide');
        }
    })

    //#endregion

    //#region Código para Salario Minimo

    var sm_id = $('#salariominimo input[name="id"]');
    var sm_salariominimo = $('#salariominimo input[name="salariominimo"]');
    var sm_forzar = $('#salariominimo input[name="forzar_salario"]');
    var sm_activo = $('#salariominimo input[name="activo"]');

    $('#salariominimo #btnGuardar').on('click', function (e) {
        e.preventDefault();
        if (sm_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        if (sm_forzar.is(":checked")) {
            vForzar = 1;
        } else {
            vForzar = 0;
        }
        url = '/guardar/salario-minimo/';
        metodo = 'POST';
        data = {
            'salario_minimo': sm_salariominimo.val(),
            'forzar_salario': vForzar,
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Salario Mínimo");
    });

    $('#salariominimo #btnCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/salario-minimo/");
    });


    //#endregion

    //#region Código para Seguro Social

    var ss_id = $('#segurosocial input[name="id"]');
    var ss_tipo = $('#segurosocial input[name="tipo"]');
    var ss_techo = $('#segurosocial input[name="techo"]');
    var ss_prcnt_e = $('#segurosocial input[name="porcentaje_e"]');
    var ss_valor_e = $('#segurosocial input[name="valor_e"]');
    var ss_prcnt_p = $('#segurosocial input[name="porcentaje_p"');
    var ss_valor_p = $('#segurosocial input[name="valor_e"]');
    var ss_activo = $('#segurosocial input[name="activo"]');


    $('#segurosocial #btnGuardar').on('click', function (e) {
        e.preventDefault();
        if (ss_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/guardar/seguro-social/';
        metodo = 'POST';
        data = {
            'tipo': ss_tipo.val(),
            'techo': ss_techo.val(),
            'porcentaje_e': ss_prcnt_e.val(),
            'porcentaje_p': ss_prcnt_p.val(),
            'valor_e': ss_valor_e.val(),
            'valor_p': ss_valor_p.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Seguro Social");
    });

    $('#segurosocial #btnActualizar').on('click', function (e) {
        e.preventDefault();
        if (ss_activo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/actualizar/seguro-social/';
        metodo = 'POST';
        data = {
            'id': ss_id.val(),
            'tipo': ss_tipo.val(),
            'techo': ss_techo.val(),
            'porcentaje_e': ss_prcnt_e.val(),
            'porcentaje_p': ss_prcnt_p.val(),
            'valor_e': ss_valor_e.val(),
            'valor_p': ss_valor_p.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Seguro Social", true, "/listar/seguro-social/");
    });

    $('#segurosocial #btnCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/seguro-social/");
    });

    //#endregion

    //#region Código para Tipo de Contrato

    var tc_id = $('#tipo_contrato input[name="tipo_contrato_id"]');
    var tc_txtTipoContrato = $('#tipo_contrato input[name="txtTipoContrato"]');
    var tc_txtDescripcion = $('#tipo_contrato textarea[name="txtDescripcion"]');
    var tc_chkActivo = $('#tipo_contrato input[name="chkActivo"]');

    $('#tipo_contrato #btnGuardar').on('click', function (e) {
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

    $('#tipo_contrato #btnActualizar').on('click', function (e) {
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

    $('#tipo_contrato #btnCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/tipo-contrato/");
    });

    //#endregion

    //#region Código para Tipo de Deducción

    var td_id = $('#tipo_deduccion input[name="id"]');
    var td_tipoDeduccion = $('#tipo_deduccion input[name="txtTipoDeduccion"]');
    var td_txtDescripcion = $('#tipo_deduccion textarea[name="txtDescripcion"]');
    var td_chkActivo = $('#tipo_deduccion input[name="tipoDeduccion_activo"]');

    $('#tipo_deduccion #btnGuardar').on('click', function (e) {
        e.preventDefault();
        if (td_chkActivo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/guardar/tipo-deduccion/';
        metodo = 'POST';
        data = {
            'tipo_deduccion': td_tipoDeduccion.val(),
            'descripcion': td_txtDescripcion.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Tipo de Deducción");
    });

    $('#tipo_deduccion #btnActualizar').on('click', function (e) {
        e.preventDefault();
        if (td_chkActivo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/actualizar/tipo-deduccion/';
        metodo = 'POST';
        data = {
            'id': td_id.val(),
            'tipo_deduccion': td_tipoDeduccion.val(),
            'descripcion': td_txtDescripcion.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Tipo de Deducción", true, "/listar/tipo-deduccion/");
    });

    $('#tipo_deduccion #btnCancelar').on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/tipo-deduccion/");
    });

    //#endregion

    //#region Código para Tipo de Ingreso

    var ti_id = $('#tipo_ingreso input[name="id"]');
    var ti_txtTipoIngreso = $('#tipo_ingreso input[name="txtTipoIngreso"]');
    var ti_txtDescripcion = $('#tipo_ingreso textarea[name="txtDescripcion"]');
    var ti_txtOrden = $('#tipo_ingreso input[name="txtIngresoOrden"]');
    var ti_chkActivo = $('#tipo_ingreso input[name="tipoIngreso_activo"]');
    var ti_btnGuardar = $('#tipo_ingreso #btnGuardar');
    var ti_btnCancelar = $('#tipo_ingreso #btnCancelar');
    var ti_btnActualizar = $('#tipo_ingreso #btnActualizar');

    ti_btnGuardar.on('click', function (e) {
        e.preventDefault();
        if (ti_chkActivo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/guardar/tipo-ingreso/';
        metodo = 'POST';
        data = {
            'tipo_ingreso': ti_txtTipoIngreso.val(),
            'descripcion': ti_txtDescripcion.val(),
            'orden': ti_txtOrden.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Tipo de Ingreso");
    });

    ti_btnActualizar.on('click', function (e) {
        e.preventDefault();
        if (ti_chkActivo.is(":checked")) {
            vActivo = 1;
        } else {
            vActivo = 0;
        }
        url = '/actualizar/tipo-ingreso/';
        metodo = 'POST';
        data = {
            'id': ti_id.val(),
            'tipo_ingreso': ti_txtTipoIngreso.val(),
            'descripcion': ti_txtDescripcion.val(),
            'orden': ti_txtOrden.val(),
            'activo': vActivo,
            'csrfmiddlewaretoken': token.val(),
        };
        GuardarRegistro(url, metodo, data, "Tipo de Ingreso", true, "/listar/tipo-ingreso/");
    });

    ti_btnCancelar.on('click', function (e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/tipo-ingreso/");
    });

    //#endregion

    //#region Código para Tipo Nómina

    var tn_id = $('#tipo_nomina input[name="tipoSalario_id"]');
    var tn_txtTipoNomina = $('#tipo_nomina input[name="txtTipoNomina"]');
    var tn_txtDescripcion = $('#tipo_nomina textarea[name="txtDescripcion"]');
    var tn_chkActivo = $('#tipo_nomina input[name="tipoNomina_activo"]');

    $('#tipo_nomina #btnTipoNominaGuardar').on('click', function (e) {
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

    $('#tipo_nomina #btnTipoNominaActualizar').on('click', function (e) {
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

    $('#tipo_nomina #btnTipoNominaCancelar').on('click', function (e) {
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
                        if (urlRedirect) {
                            setTimeout(function () {
                                window.location.replace(dns + urlRedirect);
                            }, tiempo);    
                        }else{
                            LimpiarControles();
                        }
                    } else {
                        LimpiarControles();
                    }
                } else {
                    mensaje(encabezado, data.mensaje, "error", tiempo);
                    console.log(data.mensaje);
                }
                if (editar != true) {
                    $(".btn").removeClass("disabled");
                }
            },
            error: function (data) {
                mensaje(encabezado, data.statusText, "error", tiempo);
                if (editar != true) {
                    $(".btn").removeClass("disabled");
                }
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

    function BloquearPantalla() {
        $('.pagina-contenido').block({
            message: '<h4><img src="../../static/plugins/images/busy.gif" /> Espere un momento...</h4>',
            css: {
                border: '1px solid #fff',
            }
        });
    }

    function DesbloquearPantalla() {
        $('.pagina-contenido').unblock();
    }
    //#endregion
});