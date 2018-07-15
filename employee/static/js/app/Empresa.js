$(document).on('ready', () => {
    //#region Efectos en SideBar
    $('#side-menu a').removeClass('active');
    $('#aCorporativo').addClass('active');
    $('#aEmpresa').addClass('active');
    $('#sEmpresa1').addClass('active');

    //#endregion
    //#region Variables
    var vActivo = 0;
    var razon = $('input[name="razonSocial"]');
    var organizacion = $('input[name="nombreComercial"]');
    var activo = $('input[name="activo"]');
    var token = $('input[name="csrfmiddlewaretoken"]');
    //#endregion
    //#region Librerías
    $('#myTable').DataTable();
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

            var url = "/guardar/empresa/"; // the script where you handle the form input.
            $.ajax({
                type: "POST",
                url: url,
                data: {
                    'razon':razon.val(),
                    'organiz':organizacion.val(),
                    'activo':vActivo,
                    'csrfmiddlewaretoken': token.val(),
                }, // serializes the form's elements.
                success: function(data)
                {
                    if(data.error == false){
                        $.toast({
                            heading: 'Empresa',
                            text: 'Se ha registrado una nueva empresa.',
                            position: 'top-right',
                            loaderBg: '#ff6849',
                            icon: 'success',
                            hideAfter: 5000,
                            stack: 6
                        });
                        LimpiarControles();
                    }else{
                        $.toast({
                            heading: 'Empresa',
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
                        heading: 'Empresa',
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

        if(razon.val().length == 0){
            razon.parent().addClass('has-warning');
            return false;
        }
        return true;
    }
    //#endregion
});