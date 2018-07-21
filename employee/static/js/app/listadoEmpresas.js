$(document).on('ready', () => {
    //#region Efectos en SideBar
    $('#side-menu a').removeClass('active');
    $('#aCorporativo').addClass('active');
    $('#aEmpresa').addClass('active');
    $('#sEmpresa2').addClass('active');
    //#endregion

    //#region Controles
     var btnCanc = $('#btnCancelar');
    //#endregion

    //#region Librerías
    $('#myTable').DataTable();
    //#endregion

    //#region Evento Controles
    btnCanc.on('click', function(e) {
       e.preventDefault();
        
    });
    //#endregion
});