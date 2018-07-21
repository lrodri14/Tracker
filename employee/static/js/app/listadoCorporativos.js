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
    $('.acciones .btnEliminar').on("click", function(e) {
        e.preventDefault();
        control = $(this);
        //var parent = control.parents('tr').attr('id');
        var valor = control.attr('id');
        Eliminar(valor);
    });
    //#endregion

    //#region Funciones
    function Eliminar(id) {
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
                        hideAfter: 2000,
                        stack: 6
                    });
                    setTimeout(function () {
                        location.reload();
                    }, 2000);
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
    //#endregion
});