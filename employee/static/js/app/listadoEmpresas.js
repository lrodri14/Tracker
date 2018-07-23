$(document).on('ready', () => {
    var token = $('input[name="csrfmiddlewaretoken"]');
    //#region Efectos en SideBar
    $('#side-menu a').removeClass('active');
    $('#aCorporativo').addClass('active');
    $('#aEmpresa').addClass('active');
    $('#sEmpresa2').addClass('active');
    //#endregion

    //#region Controles
    //#endregion

    //#region Librerías
    //#endregion

    //#region Evento Controles
    $('.acciones .btnEliminar').on('click', function(e) {
        e.preventDefault();
        var id = $(this).attr('data');
        Eliminar(id);
    });
    //#endregion

    //#region Funciones
    function Eliminar(id) {
        var url = "/eliminar/empresa/"; // the script where you handle the form input.
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
                        heading: 'Empresas',
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
                        heading: 'Empresas',
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
                    heading: 'Empresas',
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