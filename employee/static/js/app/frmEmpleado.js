$(document).on('ready', () => {

    //#region Variables
    var activo = 0;
    //#endregion

    //#region Controles
    var chkActivo = $('#chkActivo');
    var pNombre = $('#txtPrimerNombre');
    var sNombre = $('input[name="segundoNombre"]');
    var numExt = $('#txtNoEmpExt');
    var apellido = $('input[name="apellido"]');
    var puesto = $('input[name="jobTitle"]');
    var pos = $('select[name="position"]');
    var telOfi = $('input[name="tel_ofi"]');
    var dept = $('select[name="dept"]');
    var ext = $('input[name="ext"]');
    var suc = $('select[name="sucursal"]');
    var telMov = $('input[name="telMov"]');
    var pag = $('input[name="pager"]');
    var slsP = $('select[name="slsPer"]');
    var fax = $('input[name="fax"]');
    var email = $('input[name="email"]');
    var telCasa = $('input[name="telCasa"]');

    var calle = $('input[name="calle"]');
    var nCalle = $('input[name="nCalle"]');
    var bloque = $('input[name="bloque"]');
    var edif = $('input[name="edif"]');
    var codPost = $('input[name="codPos"]');
    var ciudad = $('input[name="ciudad"]');
    var condado = $('input[name="condado"]');
    var hdept = $('select[name="hdept"]');
    var hpais = $('select[name="hpais"]');

    var wcalle = $('input[name="wcalle"]');
    var wncalle = $('input[name="wncalle"]');
    var wbloque = $('input[name="wbloque"]');
    var wedif = $('input[name="wedif"]');
    var wcodPost = $('input[name="wcodPost"]');
    var wciudad = $('input[name="wciudad"]');
    var wcondado = $('input[name="wcondado"]');
    var wdept = $('select[name="wdept"]');
    var wpais = $('select[name="wpais"]');

    var fechaCont = $('input[name="fechaCont"]');
    var estEmp = $('select[name="estEmp"]');
    var fechaRes = $('input[name="fechaRes"]');
    var term = $('select[name="term"]');

    var sexo = $('select[name="sexo"]');
    var fechaNac = $('input[name="fecNac"]');
    var lugNac = $('select[name="lugNac"]');
    var estadoCivil = $('select[name="estadoCivil"]');
    var cantHijos = $('input[name="cantHijos"]');
    var numID = $('input[name="num_id"]');
    var citiz = $('select[name="citiz"]');
    var numPass = $('input[name="numPass"]');
    var fecPassExt = $('input[name="fecPassExt"]');
    var fecEmis = $('input[name="fecEmis"]');
    var emisor = $('input[name="emisor"]');
    var salario = $('input[name="salario"]');
    var salarioUnd = $('select[name="salaryUnits"]');
    var costEmp = $('input[name="costEmp"]');
    var costEmpUni = $('select[name="costEmpUni"]');
    var banco = $('select[name="banco"]');
    var numCuenta = $('input[name="num_cuenta"]');
    var bankSucursal = $('input[name="bankSucursal"]');
    var comentarios = $('textarea[name="comentarios"]');

    var token = $('input[name="csrfmiddlewaretoken"]');
    //#endregion

    //#region Efectos en SideBar
    $('#side-menu a').removeClass('active');
    $('#aEmp').addClass('active');
    $('#saEmpFrm').addClass('active');
    //#endregion

    //#region Eventos Botones
    $('#btnGuardar').on('click', function(e) {
        e.preventDefault();
        GuardarEmpleado();
    });
    //#endregion

    //#region Funciones
    function GuardarEmpleado() {
        if (validarDatos() != false) {
            if (chkActivo.is(":checked"))
            {
                activo = 1;
            }else{
                activo = 0;
            }
            
            //Petición AJAX para guardar los datos
            var url = "/guardar/empleado/"; // the script where you handle the form input.
            $.ajax({
                type: "POST",
                url: url,
                data: {
                    'pNom':pNombre.val(),
                    'sNom':sNombre.val(),
                    'apellido':apellido.val(),
                    'numExt':numExt.val(),
                    'puesto':puesto.val(),
                    'activo':activo,
                    'pos':pos.val(),
                    'telOf':telOfi.val(),
                    'dept':dept.val(),
                    'telExt':ext.val(),
                    'suc':suc.val(),
                    'telMov':telMov.val(),
                    'pag':pag.val(),
                    'slsP':slsP.val(),
                    'fax':fax.val(),
                    'email':email.val(),
                    'telCasa':telCasa.val(),
                    'calle':calle.val(),
                    'nCalle':nCalle.val(),
                    'bloque':bloque.val(),
                    'edif':edif.val(),
                    'codPos':codPost.val(),
                    'ciudad':ciudad.val(),
                    'condado': condado.val(),
                    'hdept':hdept.val(),
                    'hpais':hpais.val(),
                    'wcalle':wcalle.val(),
                    'wncalle':wncalle.val(),
                    'wbloque':wbloque.val(),
                    'wedif':wedif.val(),
                    'wcodPost':wcodPost.val(),
                    'wciudad':wciudad.val(),
                    'wcondado':wcondado.val(),
                    'wdept':wdept.val(),
                    'wpais':wpais.val(),
                    'fechaCont':fechaCont.val(),
                    'estEmp':estEmp.val(),
                    'fechaRES':fechaRes.val(),
                    'term':term.val(),
                    'sexo':sexo.val(),
                    'fecNac':fechaNac.val(),
                    'lugNac': lugNac.val(),
                    'estCivil': estadoCivil.val(),
                    'cantHijos': cantHijos.val(),
                    'numID': numID.val(),
                    'citiz':citiz.val(),
                    'numPass': numPass.val(),
                    'fecPassExt':fecPassExt.val(),
                    'fecEmis':fecEmis.val(),
                    'emisor':emisor.val(),
                    'salario':salario.val(),
                    'salarioUnd':salarioUnd.val(),
                    'costEmp':costEmp.val(),
                    'costEmpUni':costEmpUni.val(),
                    'banco':banco.val(),
                    'numCuenta':numCuenta.val(),
                    'bankSucursal':bankSucursal.val(),
                    'comentarios':comentarios.val(),
                    'csrfmiddlewaretoken': token.val(),
                }, // serializes the form's elements.
                success: function(data)
                {
                    if(data.error == false){
                        $.toast({
                            heading: 'Empleado',
                            text: 'Se ha registrado un nuevo empleado.',
                            position: 'top-right',
                            loaderBg: '#ff6849',
                            icon: 'success',
                            hideAfter: 5000,
                            stack: 6
                        });
                        LimpiarControles();
                    }else{
                        $.toast({
                            heading: 'Empleado',
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
                        heading: 'Empleado',
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

    //#region Validaciones
    function validarDatos(){
        $('div').removeClass('has-warning');

        // if(pNombre.val().length == 0){
        //     pNombre.parent().addClass('has-warning');
        //     return false;
        // }
        // if (numExt.val().length == 0) {
        //     numExt.parent().addClass('has-warning');
        //     return false;
        // }
        // if (apellido.val().length == 0) {
        //     apellido.parent().addClass('has-warning');
        //     return false;
        // }
        // if (puesto.val().length == 0) {
        //     puesto.parent().addClass('has-warning');
        //     return false;
        // }
        // if (cantHijos.val().length == 0) {
        //     cantHijos.parent('.form-group').addClass('has-warning');
        //     return false;
        // }
        return true;
    }
    //#endregion

    //#region Funciones Librerías
    jQuery('.mydatepicker, #datepicker').datepicker({
        format: 'yyyy-mm-dd',
        autoclose:true,
        todayHighlight: true,
    });
    //#endregion
});