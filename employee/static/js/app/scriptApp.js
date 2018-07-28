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
    }
    //#endregion
});