$(document).on('ready', () => {
    //#region Efectos en SideBar
    $('#side-menu a').removeClass('active');
    $('#aCorporativo').addClass('active');
    $('#aDepartamentos').addClass('active');
    $('#sDepartamentos1').addClass('active');
    //#endregion
    //#region Variables
    var vActivo = 0;
    var nombre = $('input[name="nombre"]');
    var descripcion = $('input[name="descripcion"]');
    var activo = $('input[name="activo"]');
    var token = $('input[name="csrfmiddlewaretoken"]');
    //#endregion
    //#region Eventos Controles
    $('#btnGuardar').on('click', (e) => {
        e.preventDefault();
        GuardarRegistro();
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

            var url = "/guardar/departamento/"; // the script where you handle the form input.
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
                            heading: 'Departamentos',
                            text: 'Se ha registrado un nuevo Departamento de la Empresa.',
                            position: 'top-right',
                            loaderBg: '#ff6849',
                            icon: 'success',
                            hideAfter: 5000,
                            stack: 6
                        });
                        LimpiarControles();
                    }else{
                        $.toast({
                            heading: 'Departamentos',
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
                        heading: 'Departamentos',
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
            $.toast({
                heading: 'Registro de Departamento de la Empresa',
                text: 'El campo "Nombre" es obligatorio.',
                position: 'top-right',
                loaderBg: '#ff6849',
                icon: 'warning',
                hideAfter: 3500,
                stack: 6
            });
            return false;
        }
        if(descripcion.val().length == 0){
            $.toast({
                heading: 'Registro de Departamento de la Empresa',
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