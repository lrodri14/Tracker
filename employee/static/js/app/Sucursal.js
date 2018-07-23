$(document).on('ready', () => {
    var dns = window.location.protocol+"//"+window.location.host;
    //#region Efectos en SideBar
    $('#side-menu a').removeClass('active');
    $('#aCorporativo').addClass('active');
    $('#aSucursal').addClass('active');
    $('#sSucursal1').addClass('active');

    //#endregion
    //#region Variables
    var vActivo = 0;
    var id = $('input[name="id"]');
    var nombre = $('input[name="nombre"]');
    var descripcion = $('textarea[name="descripcion"]');
    var activo = $('input[name="activo"]');
    var token = $('input[name="csrfmiddlewaretoken"]');
    //#endregion
    //#region Librerías
    //#endregion
    //#region Eventos Controles
    $('#btnGuardar').on('click', function(e) {
        e.preventDefault();
        GuardarRegistro();
    });
    $('#btnCancelar').on('click', function(e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/sucursales/");
       //LimpiarControles(); 
    });
    $('#btnActualizar').on('click', function(e) {
        e.preventDefault();
        ActualizarRegistro();
    });
    //#endregion
    //#region Funciones
    function GuardarRegistro(){
        
        if (validarDatos() != false) {

            if (activo.is(":checked"))
            {
                vActivo = 1;
            }else{
                vActivo = 0;
            }

            var url = "/guardar/sucursal/"; // the script where you handle the form input.
            $.ajax({
                type: "POST",
                url: url,
                data: {
                    'nombre':nombre.val(),
                    'descripcion':descripcion.val(),
                    'activo':vActivo,
                    'csrfmiddlewaretoken': token.val(),
                }, // serializes the form's elements.
                success: function(data)
                {
                    if(data.error == false){
                        $.toast({
                            heading: 'Sucursal',
                            text: 'Se ha registrado una nueva sucursal.',
                            position: 'top-right',
                            loaderBg: '#ff6849',
                            icon: 'success',
                            hideAfter: 5000,
                            stack: 6
                        });
                        LimpiarControles();
                    }else{
                        $.toast({
                            heading: 'Sucursal',
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
                        heading: 'Sucursal',
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
    }

    function ActualizarRegistro() {
        if (validarDatos() != false) {

            if (activo.is(":checked")) {
                vActivo = 1;
            } else {
                vActivo = 0;
            }

            var url = "/actualizar/sucursal/"; // the script where you handle the form input.
            $.ajax({
                type: "POST",
                url: url,
                data: {
                    'id': id.val(),
                    'nombre': nombre.val(),
                    'desc': descripcion.val(),
                    'activo': vActivo,
                    'csrfmiddlewaretoken': token.val(),
                }, // serializes the form's elements.
                success: function (data) {
                    if (data.error == false) {
                        $.toast({
                            heading: 'Sucursales',
                            text: 'Se ha actualizado registro en Sucursales.',
                            position: 'top-right',
                            loaderBg: '#ff6849',
                            icon: 'success',
                            hideAfter: 2500,
                            stack: 6
                        });
                        setTimeout(function () {
                            window.location.replace(dns +"/listar/sucursales/");
                        }, 2500);
                        //LimpiarControles();
                    } else {
                        $.toast({
                            heading: 'Sucursales',
                            text: data.mensaje,
                            position: 'top-right',
                            loaderBg: '#ff6849',
                            icon: 'error',
                            hideAfter: 5000,
                            stack: 6
                        });
                    }
                },
                error: function (data) {
                    console.log(data);
                    $.toast({
                        heading: 'Sucursales',
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
    }

    function LimpiarControles() {
        $('input[type="text"]').val(null);
        $('input[type="checkbox"]').removeAttr('checked');
        $('select').val(0);
        $('textarea').val(null);
    }
    //#endregion
    //#region Validación


    function validarDatos(){
        $('div').removeClass('has-warning');

        if(nombre.val().length == 0){
            nombre.parent().addClass('has-warning');
            return false;
        }
        return true;
    }
    //#endregion
});