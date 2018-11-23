$(document).on('ready', () => {
    var dns = window.location.protocol+"//"+window.location.host;
    //#region Efectos en SideBar
    $('#side-menu a').removeClass('active');
    $('#aCorporativo').addClass('active');
    $('#aDivision').addClass('active');
    $('#sDivision1').addClass('active');
    //#endregion
    //#region Variables
    var vActivo = 0;
    var id = $('input[name="id"]');
    var code = $('input[name="codigo"]');
    var descripcion = $('input[name="descripcion"]');
    var activo = $('input[name="activo"]');
    var token = $('input[name="csrfmiddlewaretoken"]');
    //#endregion
    //#region Eventos Controles
    $('#btnGuardar').on('click', (e) => {
        e.preventDefault();
        GuardarRegistro();
    });

    $('#btnActualizar').on('click', function(e) {
        e.preventDefault();
        ActualizarRegistro();
    });

    $('#btnCancelar').on('click', function(e) {
        e.preventDefault();
        window.location.replace(dns + "/listar/divisiones/");
    });
    //#region Funciones
    function GuardarRegistro(){
        
        if (validarDatos() != false) {

            if (activo.is(":checked"))
            {
                vActivo = 1;
            }else{
                vActivo = 0;
            }

            var url = "/guardar/division/"; // the script where you handle the form input.
            $.ajax({
                type: "POST",
                url: url,
                data: {
                    'code': code.val(),
                    'descripcion':descripcion.val(),
                    'activo':vActivo,
                    'csrfmiddlewaretoken': token.val(),
                }, // serializes the form's elements.
                success: function(data)
                {
                    if(data.error == false){
                        $.toast({
                            heading: 'División',
                            text: 'Se ha registrado una nueva División.',
                            position: 'top-right',
                            loaderBg: '#ff6849',
                            icon: 'success',
                            hideAfter: 5000,
                            stack: 6
                        });
                        LimpiarControles();
                    }else{
                        $.toast({
                            heading: 'División',
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
                        heading: 'División',
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

            var url = "/actualizar/division/"; // the script where you handle the form input.
            $.ajax({
                type: "POST",
                url: url,
                data: {
                    'id': id.val(),
                    'code': code.val(),
                    'desc': descripcion.val(),
                    'activo': vActivo,
                    'csrfmiddlewaretoken': token.val(),
                }, // serializes the form's elements.
                success: function (data) {
                    if (data.error == false) {
                        $.toast({
                            heading: 'Divisiones',
                            text: 'Se ha actualizado el registro.',
                            position: 'top-right',
                            loaderBg: '#ff6849',
                            icon: 'success',
                            hideAfter: 2500,
                            stack: 6
                        });
                        setTimeout(function () {
                            window.location.replace(dns +"/listar/divisiones/");
                        }, 2500);
                        //LimpiarControles();
                    } else {
                        $.toast({
                            heading: 'Divisiones',
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
                        heading: 'Divisiones',
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

        if(descripcion.val().length == 0){
            $.toast({
                heading: 'Registro de División',
                text: 'El campo "Descripción" es obligatorio.',
                position: 'top-right',
                loaderBg: '#ff6849',
                icon: 'warning',
                hideAfter: 3500,
                stack: 6
            });
            return false;
        }
        return true;
    }
    //#endregion
});