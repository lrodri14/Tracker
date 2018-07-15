$(document).on('ready', () => {
    //#region Efectos en SideBar
    $('#side-menu a').removeClass('active');
    $('#aCorporativo').addClass('active');
    $('#aEmpresa').addClass('active');
    $('#sEmpresa2').addClass('active');
    //#endregion

    //#region Librerías
    $('#myTable').DataTable();
    //#endregion
});