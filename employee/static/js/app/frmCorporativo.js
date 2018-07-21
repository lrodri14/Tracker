$(document).on('ready', () => {
    //#region Efectos en SideBar
    $('#side-menu a').removeClass('active');
    $('#aCorporativo').addClass('active');
    $('#aCorporativo2').addClass('active');
    $('#sCorporativo1').addClass('active');

    //#endregion
    //#region Variables
    var vActivo = 0;
    var id_org = $('input[name="id_org"]'); 
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

    $('#btnCancelar').on('click', (e) => {
        e.preventDefault();
        LimpiarControles();
    });
    $('#btnActualizar').on('click', (e) => {
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

            var url = "/guardar/corporativo/"; // the script where you handle the form input.
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
                            heading: 'Grupo Corporativo',
                            text: 'Se ha registrado un nuevo grupo corporativo.',
                            position: 'top-right',
                            loaderBg: '#ff6849',
                            icon: 'success',
                            hideAfter: 5000,
                            stack: 6
                        });
                        var html = "<tr>"
                        html += "<td>"+ data.grupo.razon +"</td>"
                        html += "<td>"+ data.grupo.nombre +"</td>"
                        html += "<td>"+ data.grupo.activo +"</td>"
                        html += "</tr>"
                        $('tbody').prepend(html);
                        $('#myTable').DataTable();
                        LimpiarControles();
                    }else{
                        $.toast({
                            heading: 'Grupo Corporativo',
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
                        heading: 'Grupo Corporativo',
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

    function ActualizarRegistro(){
        if (validarDatos() != false) {

            if (activo.is(":checked"))
            {
                vActivo = 1;
            }else{
                vActivo = 0;
            }

            var url = "/actualizar/corporativo/"; // the script where you handle the form input.
            $.ajax({
                type: "POST",
                url: url,
                data: {
                    'id': id_org.val(),
                    'razon':razon.val(),
                    'organiz':organizacion.val(),
                    'activo':vActivo,
                    'csrfmiddlewaretoken': token.val(),
                }, // serializes the form's elements.
                success: function(data)
                {
                    if(data.error == false){
                        $.toast({
                            heading: 'Grupo Corporativo',
                            text: 'Se ha actualizado registro en grupo corporativo.',
                            position: 'top-right',
                            loaderBg: '#ff6849',
                            icon: 'success',
                            hideAfter: 5000,
                            stack: 6
                        });
                        LimpiarControles();
                    }else{
                        $.toast({
                            heading: 'Grupo Corporativo',
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
                        heading: 'Grupo Corporativo',
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
        $('input[name="id_org"]').val(null);
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