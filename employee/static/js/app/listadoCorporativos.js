$(document).on('ready', () => {
    //#region Efectos en SideBar
    $('#side-menu a').removeClass('active');
    $('#aCorporativo').addClass('active');
    $('#aCorporativo2').addClass('active');
    $('#sCorporativo2').addClass('active');
    //#endregion

    //#region Librerías
    $('#myTable').DataTable();
    //#endregion
});