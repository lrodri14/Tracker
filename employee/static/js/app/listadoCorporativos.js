$(document).on('ready', () => {
    var control = null;
    var token = $('input[name="csrfmiddlewaretoken"]');
    //#region Efectos en SideBar
    $('#side-menu a').removeClass('active');
    $('#aCorporativo').addClass('active');
    $('#aCorporativo2').addClass('active');
    $('#sCorporativo2').addClass('active');
    //#endregion

    //#region Librerías
    $('#myTable').DataTable();
    //#endregion

    //#region  Variables
    var id_org = $('input[name="id_org"]');
    
    //#endregion

    //#region Eventos Controles
    // $('.acciones a').on("click", function(e) {
    //     e.preventDefault();
    //     control = $(this);
    //     var valor = control.attr('id');
    //     var parent = control.parents('tr').attr('id');
    //     Eliminar(valor, parent);
    // });
    //#endregion

    //#region Funciones
    function Eliminar(id, parent) {
        var url = "/eliminar/corporativo/"; // the script where you handle the form input.
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
                        heading: 'Grupo Corporativo',
                        text: data.mensaje,
                        position: 'top-right',
                        loaderBg: '#ff6849',
                        icon: 'success',
                        hideAfter: 5000,
                        stack: 6
                    });
                    $('#'+parent).toggle(1000);
                    actualizarTabla();
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
    function actualizarTabla(){
        $('#myTable').DataTable({
            "processing": true,
            "serverSide": true,
            "ajax": "/ajax/corporativos/",
            "columns": [
                { "data": "razonSocial" },
                { "data": "nombreComercial" },
                { "data": "active" },
            ]
        } );
    }
    //#endregion
});