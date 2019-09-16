"""employee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
#from django.contrib.auth.views import logout
from django.contrib.auth import views as auth_views
from worksheet import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^form/iniciar-sesion/$', views.inicia_sesion, name="iniciar-sesion"),
    url(r'^ingresar/$', views.ingresar, name="ingresar"),
    url(r'^seleccionar/sucursal/$', views.seleccionar_sucursal, name="selecciona_sucursal"),
    url(r'^recibir/sucursal/$', views.recibir_sucursal, name="recibir_sucursal"),
    url(r'^salir/$', auth_views.LogoutView.as_view(), name='salir'),
    #url(r'^salir/$', logout, name="salir", kwargs={'next_page': '/'}),
    url(r'^login/$', views.login, name="login"),

    url(r'^forms/empleado/$', views.empleado_form, name="empleados-form"),
    url(r'^editar/empleado/(?P<id>\w+)/$', views.empleado_editar, name="empleado_editar"),
    url(r'^perfil/empleado/(?P<id>\w+)/$', views.empleado_perfil, name="empleado-perfil"),
    url(r'^listar/empleados/$', views.empleado_listado, name="empleados-listado"),
    url(r'^corporativo/$', views.corporativo, name="corporativo"),
    url(r'^editar/corporativo/(?P<reg_id>\w+)/$', views.corporativo_editar, name="corporativo_editar"),
    url(r'^listar/corporativos/$', views.listadoCorporativo, name="listado_corporativos"),
    url(r'^empresa/$', views.empresa, name="empresa"),
    url(r'^editar/empresa/(?P<emp_id>\w+)/$', views.empresa_editar, name="empresa_editar"),
    url(r'^listar/empresas/$', views.listadoEmpresa, name="listado_empresas"),
    url(r'^sucursal/$', views.sucursal, name="sucursal"),
    url(r'^editar/sucursal/(?P<id>\w+)/$', views.sucursal_editar, name="sucursal_editar"),
    url(r'^listar/sucursales/$', views.listadoSucursal, name="listado_sucursal"),
    url(r'^divisiones/$', views.divisiones, name="divisiones"),
    url(r'^editar/division/(?P<id>\w+)/$', views.division_editar, name="division_editar"),
    url(r'^listar/divisiones/$', views.listadoDivisiones, name="listado_divisiones"),
    url(r'^departamentos/$', views.departamentos, name="departamentos"),
    url(r'^editar/departamento/(?P<id>\w+)/$', views.departamento_editar, name="departamento_editar"),
    url(r'^listar/departamentos/$', views.listadoDepartamentos, name="listado_departamentos"),
    url(r'^puesto-trabajo/$', views.puestoTrabajo, name="puestoTrabajo"),
    url(r'^editar/puesto/(?P<id>\w+)/$', views.puesto_editar, name="puesto_editar"),
    url(r'^listar/puestos-trabajo/$', views.listadoPuestoTrabajo, name="listado_puestos"),
    url(r'^centro-costos/$', views.centro_costos, name="centro_costos"),
    url(r'^editar/centro-costos/(?P<id>\w+)/$', views.centro_costo_editar, name="centro_costo_editar"),
    url(r'^listar/centro-costos/$', views.listadoCentroCostos, name="listado_ccostos"),
    url(r'^paises/$', views.paises, name="paises"),
    url(r'^editar/pais/(?P<id>\w+)/$', views.paises_editar, name="paises_editar"),
    url(r'^listar/paises/$', views.listadoPaises, name="listado_paises"),
    url(r'^deptos-estados/$', views.deptos_pais, name="deptos_pais"),
    url(r'^editar/deptos-pais/(?P<id>\w+)/$', views.deptos_pais_editar, name="deptos_pais_editar"),
    url(r'^listar/deptos-estados/$', views.deptos_pais_listado, name="listado_deptos"),
    url(r'^ciudad/$', views.ciudad, name="ciudad"),
    url(r'^editar/ciudad/(?P<id>\w+)/$', views.ciudad_editar, name="ciudad_editar"),
    url(r'^listar/ciudades/$', views.ciudades_listado, name="ciudades_listado"),
    url(r'^genero/$', views.genero, name="genero"),
    url(r'^editar/genero/(?P<id>\w+)/$', views.genero_editar, name="genero_editar"),
    url(r'^listar/generos/$', views.generos_listado, name="generos_listado"),
    url(r'^estado-civil/$', views.estado_civil, name="estado_civil"),
    url(r'^editar/estado-civil/(?P<id>\w+)/$', views.estado_civil_editar, name="estado_civil_editar"),
    url(r'^listar/estado-civil/$', views.estado_civil_listado, name="estado_civil_listado"),
    url(r'^parentesco/$', views.parentesco, name="parentesco"),
    url(r'^editar/parentesco/(?P<id>\w+)/$', views.parentesco_editar, name="parentesco_editar"),
    url(r'^listar/parentesco/$', views.parentesco_listado, name="parentesco_listado"),
    url(r'^funcion/$', views.funcion_trabajo, name="funcion_trabajo"),
    url(r'^editar/funcion/(?P<id>\w+)/$', views.funcion_trabajo_editar, name="funcion_trabajo_editar"),
    url(r'^listar/funciones/$', views.funcion_trab_listado, name="funcion_trab_listado"),
    url(r'^equipo/$', views.equipo_trabajo, name="equipo_trabajo"),
    url(r'^editar/equipo/(?P<id>\w+)/$', views.equipo_trabajo_editar, name="equipo_trabajo_editar"),
    url(r'^listar/equipos/$', views.equipo_trabajo_listado, name="equipo_trabajo_listado"),
    url(r'^estatus-empleado/$', views.estado_empleado, name="estado_empleado"),
    url(r'^editar/estatus-empleado/(?P<id>\w+)/$', views.estado_empleado_editar, name="estado_empleado_editar"),
    url(r'^listar/estatus-empleado/$', views.estado_empleado_listado, name="estado_empleado_listado"),
    url(r'^ausentismo/$', views.ausentismo, name="ausentismo"),
    url(r'^listar/ausentismo/$', views.ausentismo_listado, name="ausentismo_listado"),
    url(r'^editar/ausentismo/(?P<id>\w+)/$', views.ausentismo_editar, name="ausentismo_editar"),
    url(r'^motivo-ausencia/$', views.motivos_ausencia, name="motivos_ausencia"),
    url(r'^editar/motivo-ausencia/(?P<id>\w+)/$', views.motivos_ausencia_editar, name="motivos_ausencia_editar"),
    url(r'^listar/motivos-ausencia/$', views.motivos_ausencia_listado, name="motivos_ausencia_listado"),
    url(r'^motivo-despido/$', views.motivo_despido, name="motivo_despido"),
    url(r'^editar/motivo-despido/(?P<id>\w+)/$', views.motivo_despido_editar, name="motivo_despido_editar"),
    url(r'^listar/motivos-despido/$', views.motivos_despido_listado, name="motivos_despido_listado"),
    url(r'^motivo-renuncia/$', views.motivos_renuncia, name="motivos_renuncia"),
    url(r'^editar/motivo-renuncia/(?P<id>\w+)/$', views.motivos_renuncia_editar, name="motivos_renuncia_editar"),
    url(r'^listar/motivos-renuncia/$', views.motivos_renuncia_listado, name="motivos_renuncia_listado"),
    url(r'^clases-educacion/$', views.clase_educacion, name="clase_educacion"),
    url(r'^editar/clase-educacion/(?P<id>\w+)/$', views.clase_educacion_editar, name="clase_educacion_editar"),
    url(r'^listar/clase-educacion/$', views.clase_educacion_listado, name="clase_educacion_listado"),
    url(r'^educacion/$', views.educacion, name="educacion"),
    url(r'^editar/educacion/(?P<id>\w+)/$', views.educacion_editar, name="educacion_editar"),
    url(r'^listar/educacion/$', views.educacion_listar, name="educacion_listar"),
    url(r'^evaluacion/$', views.evaluacion, name="evaluacion"),
    url(r'^listar/evaluaciones/$', views.evaluacion_listar, name="evaluacion_listar"),
    url(r'^editar/evaluacion/(?P<id>\w+)/$', views.evaluacion_editar, name="evaluacion_editar"),
    url(r'^listar/motivos-aumento-sueldo/$', views.motivos_aumento_sueldo_listado,name="motivos_aumento_sueldo_listado"),
    url(r'^motivos-aumento-sueldo/$', views.motivos_aumento_sueldo,name="motivos_aumento_sueldo"),
    url(r'^editar/motivo-aumento-sueldo/(?P<id>\w+)/$',views.motivo_aumento_sueldo_editar, name="motivo_aumento_sueldo_editar"),
    url(r'^empleo-anterior/$', views.empleo_anterior_form, name="empleo_anterior_form"),
    url(r'^editar/empleo-anterior/(?P<id>\w+)/$', views.empleo_anterior_editar, name="empleo_anterior_editar"),
    url(r'^listar/empleo-anterior/$', views.empleo_anterior_listar,name="empleo_anterior_listar"),
    url(r'^grupo-comision/$', views.grupo_comision, name="grupo_comision"),
    url(r'^editar/grupo-comision/(?P<id>\w+)/$', views.grupo_comision_ditar, name="grupo_comision_ditar"),
    url(r'^listar/grupo-comision/$', views.grupo_comisiones_listar,name="grupo_comisiones_listar"),
    url(r'^form/vendedor/$', views.vendedor_form, name="vendedor_form"),
    url(r'^editar/vendedor/(?P<id>\w+)/$', views.vendedor_editar, name="vendedor_editar"),
    url(r'^listar/vendedor/$', views.vendedor_listar, name="vendedor_listar"),
    url(r'^form/feriado/$', views.feriado_form, name="feriado_form"),
    url(r'^editar/feriado/(?P<id>\w+)/$', views.feriado_editar, name="feriado_editar"),
    url(r'^listar/feriado/$', views.feriado_listar, name="feriado_listar"),
    url(r'^form/activo-asignado/$', views.articulo_asignado_form, name="articulo_asignado_form"),
    url(r'^editar/activo-asignado/(?P<id>\w+)/$', views.articulo_asignado_editar, name="articulo_asignado_editar"),
    url(r'^listar/activo-asignado/$', views.articulos_asignados_listar, name="articulos_asignados_listar"),
    url(r'^form/motivo-rescision-contrato/$', views.motivo_rescision_contrato_form, name="motivo_rescision_contrato_form"),
    url(r'^editar/motivo-rescision-contrato/(?P<id>\w+)/$', views.motivo_rescision_contrato_editar, name="motivo_rescision_contrato_editar"),
    url(r'^listar/motivo-rescision-contrato/$', views.motivo_rescicion_contrato_listar, name="motivo_rescicion_contrato_listar"),
    url(r'^form/tipo-salario/$', views.tipo_salario_form, name="tipo_salario_form"),
    url(r'^editar/tipo-salario/(?P<id>\w+)/$', views.tipo_salario_editar, name="tipo_salario_editar"),
    url(r'^listar/tipo-salario/$', views.tipo_salario_listar, name="tipo_salario_listar"),
    url(r'^form/costo-empleado/$', views.tipo_costo_empleado_form, name="tipo_costo_empleado_form"),
    url(r'^editar/costo-empleado/(?P<id>\w+)/$', views.tipo_costo_empleado_editar, name="tipo_costo_empleado_editar"),
    url(r'^listar/costo-empleado/$', views.tipo_costo_empleado_listar, name="tipo_costo_empleado_listar"),
    url(r'^form/banco/$', views.banco_form, name="banco_form"),
    url(r'^editar/banco/(?P<id>\w+)/$', views.banco_editar, name="banco_editar"),
    url(r'^listar/banco/$', views.banco_listado, name="banco_listado"),
    url(r'^form/empresa-usuario/$', views.usuario_empresa_form, name="emp_user_frm"),
    url(r'^listar/empresas-usuario/$', views.usuario_empresa_listar, name="emp_user"),
    url(r'^editar/empresa-usuario/(?P<id>\w+)/$', views.usuario_empresa_editar, name="usuario_empresa_editar"),

    url(r'^formulario/aumento-salario/$', views.aumento_salario_form, name="aumento_salario_form"),
    url(r'^formulario/deduccion-general/$', views.deduccion_general_form, name="deduccion_general_form"),
    url(r'^formulario/deduccion-general-detalle/$', views.deduccion_general_detalle_form, name="deduccion_general_detalle_form"),
    url(r'^formulario/deduccion-individual/$', views.deduccion_individual_form, name="deduccion_individual_form"),
    url(r'^formulario/deduccion-individual-detalle/$', views.deduccion_individual_detalle_form, name="deduccion_individual_detalle_form"),
    url(r'^formulario/deduccion-individual-planilla/$', views.deduccion_individual_planilla_form, name="deduccion_individual_planilla_form"),
    url(r'^formulario/encabezado-isr/$', views.isr_encabezado_form, name="isr_encabezado_form"),
    url(r'^formulario/he/$', views.horaextra_form, name="horaextra_form"),
    url(r'^formulario/ingreso-individual/$', views.ingreso_individual_form, name="ingreso_individual_form"),
    url(r'^formulario/ingreso-individual-detalle/$', views.ingreso_individual_detalle_form, name="ingreso_individual_detalle_form"),
    url(r'^formulario/ingreso-individual-planilla/$', views.ingreso_individual_planilla_form, name="ingreso_individual_planilla_form"),
    url(r'^formulario/ingreso-general/$', views.ingreso_general_form, name="ingreso_general_form"),
    url(r'^formulario/ingreso-general-detalle/$', views.ingreso_general_detalle_form, name="ingreso_general_detalle_form"),
    url(r'^formulario/isr/$', views.impuestosobrerenta_form, name="impuestosobrerenta_form"),
    url(r'^formulario/impuestovecinal/$', views.impuestovecinal_form, name="impuestovecinal_form"),
    url(r'^formulario/planilla/$', views.planilla_form, name="planilla_form"),
    url(r'^formulario/salariominimo/$', views.salariominimo_form, name="salariominimo_form"),
    url(r'^formulario/segurosocial/$', views.segurosocial_form, name="segurosocial_form"),
    url(r'^formulario/tipo-contrato/$', views.tipo_contrato_form, name="tipo_contrato_form"),
    url(r'^formulario/tipo-deduccion/$', views.tipo_deduccion_form, name="tipo_deduccion_form"),
    url(r'^formulario/tipo-ingreso/$', views.tipo_ingreso_form, name="tipo_ingreso_form"),
    url(r'^formulario/tipo-nomina/$', views.tipo_nomina_form, name="tipo_nomina_form"),

    url(r'^listar/aumento-salario/$', views.aumento_salario_listado, name="aumento_salario_listado"),
    url(r'^listar/deduccion-general/$', views.deduccion_general_listado, name="deduccion_general_listado"),
    url(r'^listar/deduccion-general-detalle/$', views.deduccion_general_detalle_listado, name="deduccion_general_detalle_listado"),
    url(r'^listar/deduccion-individual/$', views.deduccion_individual_listado, name="deduccion_individual_listado"),
    url(r'^listar/deduccion-individual-detalle/$', views.deduccion_individual_detalle_listado, name="deduccion_individual_detalle_listado"),
    url(r'^listar/deduccion-individual-planilla/$', views.deduccion_individual_planilla_listado, name="deduccion_individual_planilla_listado"),
    url(r'^listar/he/$', views.horaextra_listado, name="horaextra_listado"),
    url(r'^listar/isr/$', views.impuestosobrerenta_listado, name="impuestosobrerenta_listado"),
    url(r'^listar/impuesto-vecinal/$', views.impuestovecinal_listado, name="impuestovecinal_listado"),
    url(r'^listar/ingreso-individual/$', views.ingreso_individual_listado, name="ingreso_individual_listado"),
    url(r'^listar/ingreso-individual-detalle/$', views.ingreso_individual_detalle_listado,name="ingreso_individual_detalle_listado"),
    url(r'^listar/ingreso-individual-planilla/$', views.ingreso_individual_planilla_listado,name="ingreso_individual_planilla_listado"),
    url(r'^listar/ingreso-general/$', views.ingreso_general_listado, name="ingreso_general_listado"),
    url(r'^listar/ingreso-general-detalle/$', views.ingreso_general_detalle_listado,name="ingreso_general_detalle_listado"),
    url(r'^listar/planilla/$', views.planilla_listado, name="planilla_listado"),
    url(r'^listar/salario-minimo/$', views.salariominimo_listado, name="salariominimo_listado"),
    url(r'^listar/seguro-social/$', views.segurosocial_listado, name="segurosocial_listado"),
    url(r'^listar/tipo-contrato/$', views.tipo_contrato_listado, name="tipo_contrato_listado"),
    url(r'^listar/tipo-deduccion/$', views.tipo_deduccion_listado, name="tipo_deduccion_listado"),
    url(r'^listar/isr-encabezado/$', views.isr_encabezado, name="isr_encabezado"),
    url(r'^listar/tipo-ingreso/$', views.tipo_ingreso_listado, name="tipo_ingreso_listado"),
    url(r'^listar/tipo-nomina/$', views.tipo_nomina_listado, name="tipo_nomina_listar"),

    #----------------->>>AJAX<<<------------------
    url(r'^guardar/activo-asignado/$', views.guardar_activo_asignado, name='guardar_activo_asignado'),
    url(r'^guardar/ausentismo/$', views.guardar_ausentismo, name='guardar_ausentismo'),
    url(r'^guardar/banco/$', views.guardar_banco, name='guardar_banco'),
    url(r'^guardar/centro-costo/$', views.guardar_ccosto, name='guardar_ccosto'),
    url(r'^guardar/ciudad/$', views.guardar_ciudades, name='guardar_ciudades'),
    url(r'^guardar/clases-educacion/$', views.guardar_clase_educacion, name='guardar_clase_educacion'),
    url(r'^guardar/corporativo/$', views.guardar_corporativo, name='guardar_corporativo'),
    url(r'^guardar/costo-empleado-unidades/$', views.guardar_costo_empleado, name='guardar_costo_empleado'),
    url(r'^guardar/deduccion-empleado/$', views.guardar_deduccion_empleado, name='guardar_deduccion_empleado'),
    url(r'^guardar/deduccion-general/$', views.deduccion_general_guardar, name='deduccion_general_guardar'),
    url(r'^guardar/deduccion-general-detalle/$', views.deduccion_general_detalle_guardar, name='deduccion_general_detalle_guardar'),
    url(r'^guardar/deduccion-individual/$', views.deduccion_individual_guardar, name='deduccion_individual_guardar'),
    url(r'^guardar/deduccion-individual-detalle/$', views.deduccion_individual_detalle_guardar, name='deduccion_individual_detalle_guardar'),
    url(r'^guardar/deduccion-individual-planilla/$', views.deduccion_individual_planilla_guardar, name='deduccion_individual_planilla_guardar'),
    url(r'^guardar/departamento/$', views.guardar_departamento, name='guardar_departamento'),
    url(r'^guardar/depto-pais/$', views.guardar_deptos, name='guardar_deptos'),
    url(r'^guardar/division/$', views.guardar_division, name='guardar_division'),
    url(r'^guardar/educacion/$', views.guardar_educacion, name='guardar_educacion'),
    url(r'^guardar/empleado/$', views.guardar_empleado, name='guardar_empleado'),
    url(r'^guardar/empleo-anterior/$', views.guardar_empleo_anterior, name='guardar_empleo_anterior'),
    url(r'^guardar/empresa/$', views.guardar_empresa, name='guardar_empresa'),
    url(r'^guardar/empresa-usuario/$', views.guardar_empresa_usuario, name='guardar_empresa_usuario'),
    url(r'^guardar/equipo/$', views.guardar_equipos, name='guardar_equipos'),
    url(r'^guardar/estado-civil/$', views.guardar_estado_civil, name='guardar_estado_civil'),
    url(r'^guardar/estatus-empleado/$', views.guardar_estado_empleado, name='guardar_estado_empleado'),
    url(r'^guardar/evaluacion/$', views.guardar_evaluacion, name='guardar_evaluacion'),
    url(r'^guardar/feriado/$', views.guardar_feriado, name='guardar_feriado'),
    url(r'^guardar/foto-perfil/$', views.guardar_foto_perfil, name='guardar_foto_perfil'),
    url(r'^guardar/funcion/$', views.guardar_funciones, name='guardar_funciones'),
    url(r'^guardar/genero/$', views.guardar_genero, name='guardar_genero'),
    url(r'^guardar/grupo-comision/$', views.guardar_grupo_comision, name='guardar_grupo_comision'),
    url(r'^guardar/he/$', views.horaextra_guardar, name='horaextra_guardar'),
    url(r'^guardar/ingreso-individual/$', views.ingreso_individual_guardar, name='ingreso_individual_guardar'),
    url(r'^guardar/ingreso-individual-detalle/$', views.ingreso_indidvidual_detalle_guardar, name='ingreso_indidvidual_detalle_guardar'),
    url(r'^guardar/ingreso-individual-planilla/$', views.ingreso_individual_planilla_guardar, name='ingreso_indidvidual_planilla_guardar'),
    url(r'^guardar/ingreso-general/$', views.ingreso_general_guardar, name='ingreso_general_guardar'),
    url(r'^guardar/ingreso-general-detalle/$', views.ingreso_general_detalle_guardar, name='ingreso_general_detalle_guardar'),
    url(r'^guardar/isr-encabezado/$', views.isr_encabezado_guardar, name='isr_encabezado_guardar'),
    url(r'^guardar/isr-detalle/$', views.impuestosobrerenta_guardar, name='impuestosobrerenta_guardar'),
    url(r'^guardar/isr/$', views.impuestosobrerenta_guardar, name='impuestosobrerenta_guardar'),
    url(r'^guardar/impuesto-vecinal/$', views.impuestovecinal_guardar, name='impuestovecinal_guardar'),
    url(r'^guardar/motivo-ausencia/$', views.guardar_motivo_ausencia, name='guardar_motivo_ausencia'),
    url(r'^guardar/motivo-aumento-sueldo/$', views.guardar_motivo_aumento_sueldo, name='guardar_motivo_aumento_sueldo'),
    url(r'^guardar/motivo-despido/$', views.guardar_motivo_despido, name='guardar_motivo_despido'),
    url(r'^guardar/motivo-renuncia/$', views.guardar_motivo_renuncia, name='guardar_motivo_renuncia'),
    url(r'^guardar/motivo-rescision-contrato/$', views.guardar_motivo_rescision_contrato, name='guardar_motivo_rescision_contrato'),
    url(r'^guardar/pais/$', views.guardar_pais, name='guardar_pais'),
    url(r'^guardar/parentesco/$', views.guardar_parentesco, name='guardar_parentesco'),
    url(r'^guardar/planilla/$', views.planilla_guardar, name='planilla_guardar'),
    url(r'^guardar/puesto/$', views.guardar_puesto, name='guardar_puesto'),
    url(r'^guardar/salario-minimo/$', views.salariominimo_guardar, name='salariominimo_guardar'),
    url(r'^guardar/seguro-social/$', views.segurosocial_guardar, name='segurosocial_guardar'),
    url(r'^guardar/sucursal/$', views.guardar_sucursal, name='guardar_sucursal'),
    url(r'^guardar/tipo-contrato/$', views.tipo_contrato_guardar, name='tipo_contrato_guardar'),
    url(r'^guardar/tipo-deduccion/$', views.tipo_deduccion_guardar, name='tipo_deduccion_guardar'),
    url(r'^guardar/tipo-ingreso/$', views.tipo_ingreso_guardar, name='tipo_ingreso_guardar'),
    url(r'^guardar/tipo-nomina/$', views.tipo_nomina_guardar, name='tipo_nomina_guardar'),
    url(r'^guardar/tipo-salario/$', views.guardar_tipo_salario, name='guardar_tipo_salario'),
    url(r'^guardar/vendedor/$', views.guardar_vendedor, name='guardar_vendedor'),

    url(r'^generar/planilla/$', views.planilla_generar, name='planilla_generar'),
    url(r'^generar/planilla2/$', views.planilla_generar_calculos, name='planilla_generar_calculos'),
    url(r'^generar/reporte-general/planilla/$', views.generar_reporte_general, name='generar_reporte_general'),

    url(r'^actualizar/activo-asignado/$', views.actualizar_activo_asignado, name='actualizar_activo_asignado'),
    url(r'^actualizar/aumento-salario/$', views.aumento_salario_actualizar, name='aumento_salario_actualizar'),
    url(r'^actualizar/ausentismo/$', views.actualizar_ausentismo, name='actualizar_ausentismo'),
    url(r'^actualizar/banco/$', views.actualizar_banco, name='actualizar_banco'),
    url(r'^actualizar/centro-costo/$', views.actualizar_ccosto, name='actualizar_ccosto'),
    url(r'^actualizar/ciudad/$', views.actualizar_ciudad, name='actualizar_ciudad'),
    url(r'^actualizar/clase-educacion/$', views.actualizar_clase_educacion, name='actualizar_clase_educacion'),
    url(r'^actualizar/corporativo/$', views.actualizar_corporativo, name='actualizar_corporativo'),
    url(r'^actualizar/costo-empleado-unidades/$', views.actualizar_costo_empleado, name='actualizar_costo_empleado'),
    url(r'^actualizar/departamento/$', views.actualizar_departamento, name='actualizar_departamento'),
    url(r'^actualizar/deduccion-empleado/$', views.actualizar_deduccion_empleado, name='actualizar_deduccion_empleado'),
    url(r'^actualizar/deduccion-general/$', views.deduccion_general_actualizar, name='deduccion_general_actualizar'),
    url(r'^actualizar/deduccion-general-detalle/$', views.deduccion_general_detalle_actualizar, name='deduccion_general_detalle_actualizar'),
    url(r'^actualizar/deduccion-individual/$', views.deduccion_individual_actualizar, name='deduccion_individual_actualizar'),
    url(r'^actualizar/deduccion-individual-detalle/$', views.deduccion_individual_detalle_actualizar, name='deduccion_individual_detalle_actualizar'),
    url(r'^actualizar/deduccion-individual-planilla/$', views.deduccion_individual_planilla_actualizar, name='deduccion_individual_planilla_actualizar'),
    url(r'^actualizar/deptos-pais/$', views.actualizar_deptos, name='actualizar_deptos'),
    url(r'^actualizar/division/$', views.actualizar_division, name='actualizar_division'),
    url(r'^actualizar/educacion/$', views.actualizar_educacion, name='actualizar_educacion'),
    url(r'^actualizar/empleado/$', views.actualizar_empleado, name='actualizar_empleado'),
    url(r'^actualizar/empleo-anterior/$', views.actualizar_empleo_anterior, name='actualizar_empleo_anterior'),
    url(r'^actualizar/empresa/$', views.actualizar_empresa, name='actualizar_empresa'),
    url(r'^actualizar/empresa-usuario/$', views.actualizar_empresa_usuario, name='actualizar_empresa_usuario'),
    url(r'^actualizar/equipo/$', views.actualizar_equipos, name='actualizar_equipos'),
    url(r'^actualizar/estado-civil/$', views.actualizar_estado_civil, name='actualizar_estado_civil'),
    url(r'^actualizar/estatus-empleado/$', views.actualizar_estatus_empleado, name='actualizar_estatus_empleado'),
    url(r'^actualizar/evaluacion/$', views.actualizar_evaluacion, name='actualizar_evaluacion'),
    url(r'^actualizar/feriado/$', views.actualizar_feriado, name='actualizar_feriado'),
    url(r'^actualizar/funcion/$', views.actualizar_funcion, name='actualizar_funcion'),
    url(r'^actualizar/genero/$', views.actualizar_genero, name='actualizar_genero'),
    url(r'^actualizar/grupo-comision/$', views.actualizar_grupo_comision, name='actualizar_grupo_comision'),
    url(r'^actualizar/he/$', views.horaextra_actualizar, name='horaextra_actualizar'),
    url(r'^actualizar/ingreso-general/$', views.ingreso_general_actualizar, name='ingreso_general_actualizar'),
    url(r'^actualizar/ingreso-general-detalle/$', views.ingreso_general_detalle_actualizar, name='ingreso_general_detalle_actualizar'),
    url(r'^actualizar/ingreso-general-planilla/$', views.ingreso_individual_planilla_actualizar, name='ingreso_individual_planilla_actualizar'),
    url(r'^actualizar/ingreso-individual/$', views.ingreso_individual_actualizar, name='ingreso_individual_actualizar'),
    url(r'^actualizar/ingreso-individual-detalle/$', views.ingreso_individual_detalle_actualizar, name='ingreso_individual_detalle_actualizar'),
    url(r'^actualizar/ingreso-individual-planilla/$', views.ingreso_individual_planilla_actualizar, name='ingreso_individual_planilla_actualizar'),
    url(r'^actualizar/impuesto-vecinal/$', views.impuestovecinal_actualizar, name='impuestovecinal_actualizar'),
    url(r'^actualizar/isr/$', views.impuestosobrerenta_actualizar, name='impuestosobrerenta_actualizar'),
    url(r'^actualizar/motivo-aumento-sueldo/$', views.actualizar_motivo_aumento_sueldo, name='actualizar_motivo_aumento_sueldo'),
    url(r'^actualizar/motivo-ausencia/$', views.actualizar_motivo_ausencia, name='actualizar_motivo_ausencia'),
    url(r'^actualizar/motivo-despido/$', views.actualizar_motivo_despido, name='actualizar_motivo_despido'),
    url(r'^actualizar/motivo-renuncia/$', views.actualizar_motivo_renuncia, name='actualizar_motivo_renuncia'),
    url(r'^actualizar/motivo-rescision-contrato/$', views.actualizar_motivo_rescision_contrato, name='actualizar_motivo_rescision_contrato'),
    url(r'^actualizar/pais/$', views.actualizar_pais, name='actualizar_pais'),
    url(r'^actualizar/planilla/$', views.planilla_actualizar, name='planilla_actualizar'),
    url(r'^actualizar/parentesco/$', views.actualizar_parentesco, name='actualizar_parentesco'),
    url(r'^actualizar/puesto/$', views.actualizar_puesto, name='actualizar_puesto'),
    url(r'^actualizar/seguro-social/$', views.segurosocial_actualizar, name='segurosocial_actualizar'),
    url(r'^actualizar/sucursal/$', views.actualizar_sucursal, name='actualizar_sucursal'),
    url(r'^actualizar/tipo-contrato/$', views.tipo_contrato_actualizar, name='tipo_contrato_actualizar'),
    url(r'^actualizar/tipo-deduccion/$', views.tipo_deduccion_actualizar, name='tipo_deduccion_actualizar'),
    url(r'^actualizar/tipo-ingreso/$', views.tipo_ingreso_actualizar, name='tipo_ingreso_actualizar'),
    url(r'^actualizar/tipo-nomina/$', views.tipo_nomina_actualizar, name='tipo_nomina_actualizar'),
    url(r'^actualizar/tipo-salario/$', views.actualizar_tipo_salario, name='actualizar_tipo_salario'),
    url(r'^actualizar/vendedor/$', views.actualizar_vendedor, name='actualizar_vendedor'),

    url(r'^calcular/planilla-empleado/$', views.planilla_calculos_empleado, name='planilla_calculos_empleado'),
    url(r'^cerrar/planilla/$', views.planilla_cerrar, name='planilla_cerrar'),

    url(r'^editar/aumento-salario/(?P<id>\w+)/$', views.aumento_salario_editar, name="aumento_salario_editar"),
    url(r'^editar/deduccion-general/(?P<id>\w+)/$', views.deduccion_general_editar, name="deduccion_general_editar"),
    url(r'^editar/deduccion-general-detalle/(?P<id>\w+)/$', views.deduccion_general_detalle_editar, name="deduccion_general_detalle_editar"),
    url(r'^editar/deduccion-individual/(?P<id>\w+)/$', views.deduccion_individual_editar, name="deduccion_individual_editar"),
    url(r'^editar/deduccion-individual-detalle/(?P<id>\w+)/$', views.deduccion_indidvidual_detalle_editar, name="deduccion_indidvidual_detalle_editar"),
    url(r'^editar/deduccion-individual-planilla/(?P<id>\w+)/$', views.deduccion_indidvidual_planilla_editar, name="deduccion_indidvidual_planilla_editar"),
    url(r'^editar/he/(?P<id>\w+)/$', views.horaextra_editar, name="horaextra_editar"),
    url(r'^editar/ingreso-general/(?P<id>\w+)/$', views.ingreso_general_editar, name="ingreso_general_editar"),
    url(r'^editar/ingreso-general-detalle/(?P<id>\w+)/$', views.ingreso_general_detalle_editar, name="ingreso_general_detalle_editar"),
    url(r'^editar/ingreso-individual/(?P<id>\w+)/$', views.ingreso_individual_editar, name="ingreso_individual_editar"),
    url(r'^editar/ingreso-individual-detalle/(?P<id>\w+)/$', views.ingreso_indidvidual_detalle_editar, name="ingreso_indidvidual_detalle_editar"),
    url(r'^editar/ingreso-individual-planilla/(?P<id>\w+)/$', views.ingreso_individual_planilla_editar, name="ingreso_individual_planilla_editar"),
    url(r'^editar/isr/(?P<id>\w+)/$', views.impuestosobrerenta_editar, name="impuestosobrerenta_editar"),
    url(r'^editar/impuesto-vecinal/(?P<id>\w+)/$', views.impuestovecinal_editar, name="impuestovecinal_editar"),
    url(r'^editar/planilla/(?P<id>\w+)/$', views.planilla_editar, name="planilla_editar"),
    url(r'^editar/seguro-social/(?P<id>\w+)/$', views.segurosocial_editar, name="segurosocial_editar"),
    url(r'^editar/tipo-contrato/(?P<id>\w+)/$', views.tipo_contrato_editar, name="tipo_contrato_editar"),
    url(r'^editar/tipo-deduccion/(?P<id>\w+)/$', views.tipo_deduccion_editar, name="tipo_deduccion_editar"),
    url(r'^editar/tipo-ingreso/(?P<id>\w+)/$', views.tipo_ingreso_editar, name="tipo_ingreso_editar"),
    url(r'^editar/tipo-nomina/(?P<id>\w+)/$', views.tipo_nomina_editar, name="tipo_nomina_editar"),

    url(r'^eliminar/activo-asignado/$', views.eliminar_activo_asignado, name='eliminar_activo_asignado'),
    url(r'^eliminar/aumento-salario/$', views.aumento_salario_eliminar, name='aumento_salario_eliminar'),
    url(r'^eliminar/ausentismo/$', views.eliminar_ausentismo, name='eliminar_ausentismo'),
    url(r'^eliminar/banco/$', views.eliminar_banco, name='eliminar_banco'),
    url(r'^eliminar/centro-costo/$', views.eliminar_ccosto, name='eliminar_ccosto'),
    url(r'^eliminar/ciudad/$', views.eliminar_ciudad, name='eliminar_ciudad'),
    url(r'^eliminar/clase-educacion/$', views.eliminar_clase_educacion, name='eliminar_clase_educacion'),
    url(r'^eliminar/corporativo/$', views.eliminar_corporativo, name='eliminar_corporativo'),
    url(r'^eliminar/costo-empleado-unidades/$', views.eliminar_costo_empleado, name='eliminar_costo_empleado'),
    url(r'^eliminar/deduccion-empleado/$', views.eliminar_empleado_deduccion, name='eliminar_empleado_deduccion'),
    url(r'^eliminar/deduccion-general-detalle/$', views.deduccion_general_detalle_eliminar, name='deduccion_general_detalle_eliminar'),
    url(r'^eliminar/deduccion-individual/$', views.deduccion_individual_eliminar, name='deduccion_individual_eliminar'),
    url(r'^eliminar/deduccion-individual-detalle/$', views.deduccion_individual_detalle_eliminar, name='deduccion_individual_detalle_eliminar'),
    url(r'^eliminar/deduccion-individual-planilla/$', views.deduccion_individual_planilla_eliminar, name='deduccion_individual_planilla_eliminar'),
    url(r'^eliminar/departamento/$', views.eliminar_departamento, name='eliminar_departamento'),
    url(r'^eliminar/depto-pais/$', views.eliminar_depto, name='eliminar_depto'),
    url(r'^eliminar/division/$', views.eliminar_division, name='eliminar_division'),
    url(r'^eliminar/educacion/$', views.eliminar_educacion, name='eliminar_educacion'),
    url(r'^eliminar/empleado/$', views.eliminar_empleado, name='eliminar_empleado'),
    url(r'^eliminar/empleo-anterior/$', views.eliminar_empleo_anterior, name='eliminar_empleo_anterior'),
    url(r'^eliminar/empresa/$', views.eliminar_empresa, name='eliminar_empresa'),
    url(r'^eliminar/empresa-usuario/$', views.eliminar_empresa_usuario, name='eliminar_empresa_usuario'),
    url(r'^eliminar/equipo/$', views.eliminar_equipo_trabajo, name='eliminar_equipo_trabajo'),
    url(r'^eliminar/estado-civil/$', views.eliminar_estado_civil, name='eliminar_estado_civil'),
    url(r'^eliminar/estatus-empleado/$', views.eliminar_estatus_empleado, name='eliminar_estatus_empleado'),
    url(r'^eliminar/evaluacion/$', views.eliminar_evaluacion, name='eliminar_evaluacion'),
    url(r'^eliminar/feriado/$', views.eliminar_feriado, name='eliminar_feriado'),
    url(r'^eliminar/funcion/$', views.eliminar_funcion_trabajo, name='eliminar_funcion_trabajo'),
    url(r'^eliminar/genero/$', views.eliminar_genero, name='eliminar_genero'),
    url(r'^eliminar/grupo-comision/$', views.eliminar_grupo_comision, name='eliminar_grupo_comision'),
    url(r'^eliminar/grupo-comision/$', views.eliminar_grupo_comision, name='eliminar_grupo_comision'),
    url(r'^eliminar/he/$', views.horaextra_eliminar, name='horaextra_eliminar'),
    url(r'^eliminar/ingreso-general/$', views.ingreso_general_eliminar, name='ingreso_general_eliminar'),
    url(r'^eliminar/ingreso-general-detalle/$', views.ingreso_general_detalle_eliminar, name='ingreso_general_detalle_eliminar'),
    url(r'^eliminar/ingreso-individual/$', views.ingreso_individual_eliminar, name='ingreso_individual_eliminar'),
    url(r'^eliminar/ingreso-individual-detalle/$', views.ingreso_individual_detalle_eliminar, name='ingreso_individual_detalle_eliminar'),
    url(r'^eliminar/ingreso-individual-planilla/$', views.ingreso_individual_planilla_eliminar, name='ingreso_individual_planilla_eliminar'),
    url(r'^eliminar/isr/$', views.impuestosobrerenta_eliminar, name='impuestosobrerenta_eliminar'),
    url(r'^eliminar/impuesto-vecinal/$', views.impuestovecinal_eliminar, name='impuestovecinal_eliminar'),
    url(r'^eliminar/motivo-aumento-sueldo/$', views.eliminar_motivo_aumento_sueldo, name='eliminar_motivo_aumento_sueldo'),
    url(r'^eliminar/motivo-ausencia/$', views.eliminar_motivo_ausencia, name='eliminar_motivo_ausencia'),
    url(r'^eliminar/motivo-despido/$', views.eliminar_motivo_despido, name='eliminar_motivo_despido'),
    url(r'^eliminar/motivo-renuncia/$', views.eliminar_motivo_renuncia, name='eliminar_motivo_renuncia'),
    url(r'^eliminar/motivo-rescision-contrato/$', views.eliminar_motivo_rescision_contrato, name='eliminar_motivo_rescision_contrato'),
    url(r'^eliminar/pais/$', views.eliminar_pais, name='eliminar_pais'),
    url(r'^eliminar/parentesco/$', views.eliminar_parentesco, name='eliminar_parentesco'),
    url(r'^eliminar/puesto/$', views.eliminar_puesto, name='eliminar_puesto'),
    url(r'^eliminar/salario-minimo/$', views.salariominimo_eliminar, name='salariominimo_eliminar'),
    url(r'^eliminar/sucursal/$', views.eliminar_sucursal, name='eliminar_sucursal'),
    url(r'^eliminar/seguro-social/$', views.segurosocial_eliminar, name='segurosocial_eliminar'),
    url(r'^eliminar/tipo-contrato/$', views.tipo_contrato_eliminar, name='tipo_contrato_eliminar'),
    url(r'^eliminar/tipo-deduccion/$', views.tipo_deduccion_eliminar, name='tipo_deduccion_eliminar'),
    url(r'^eliminar/tipo-ingreso/$', views.tipo_ingreso_eliminar, name='tipo_ingreso_eliminar'),
    url(r'^eliminar/tipo-nomina/$', views.tipo_nomina_eliminar, name='tipo_nomina_eliminar'),
    url(r'^eliminar/tipo-salario/$', views.eliminar_tipo_salario, name='eliminar_tipo_salario'),
    url(r'^eliminar/vendedor/$', views.eliminar_vendedor, name='eliminar_vendedor'),

    url(r'^obtener/antiguedad/$', views.obtener_antiguedad, name="obtener_antiguedad"),
    url(r'^obtener/estados/$', views.lista_estados, name="lista_estados"),
    url(r'^obtener/deduccion-empleado/$', views.obtener_deduccion_empleado, name="obtener_deduccion_empleado"),
    url(r'^obtener/deducciones-empleado/$', views.obtener_deducciones, name="obtener_deducciones"),
    url(r'^obtener/dias-salario/$', views.obtener_dias_salario, name="obtener_dias_salario"),
    url(r'^obtener/empleados-planilla/$', views.obtener_empleados_planilla, name="obtener_empleados_planilla"),
    url(r'^obtener/grafico1/$', views.grafico1, name="grafico1"),
    url(r'^obtener/isr-encabezado/$', views.impuestosobrerenta_obtener, name="impuestosobrerenta_obtener"),
    url(r'^obtener/planilla-generada/$', views.planilla_generada, name="planilla_generada"),
    url(r'^obtener/puestos/$', views.obtenerPuestos, name="obtenerPuestos"),
    url(r'^obtener/salario-ultimo/$', views.obtener_ultimo_salario, name="obtener_ultimo_salario"),
    url(r'^obtener/sucursales/$', views.lista_sucursal, name="lista_sucursal"),

    url(r'^enviar/aumento-salario/$', views.aumento_salario_guardar, name="aumento_salario_guardar"),
    url(r'^enviar/sucursal/$', views.enviar_sucursal, name="enviar_sucursal"),

    url(r'^ver-registro/aumento-salario/$', views.aumento_salario_ver_registro, name="aumento_salario_ver_registro"),
    url(r'^ver-registro/planilla/$', views.planilla_ver_registro, name="planilla_ver_registro"),
    url(r'^ver/planilla/(?P<id>\w+)/$', views.planilla_ver, name="planilla_ver"),
    url(r'^reporte/planilla/$', views.planilla_reporte_general, name="planilla_reporte_general"),

    # ----------------->>>REPORTES<<<-------------------#
    url(r'reporte_personas_pdf/$', views.ReportePersonaPDF.as_view(), name="reporte_personas_pdf"),
    url(r'reporte/boleta-pago/$', views.boleta_pago_reporte, name='boleta_pago_reporte'),
    url(r'reporte/boleta-pago-prueba/$', views.reporte_probando, name='reporte_probando'),

    url(r'reporte-pdf/$', views.Pdf.as_view(), name='reporte-pdf'),


    url(r'email/boleta-pago/$', views.boleta_pago_email, name='boleta_pago_email'),



    #------------------>>>AJAX<<<-------------------

    #url(r'^seguridad/', include('django.contrib.auth.urls')),
    # url(r'^seguridad/logout/$', include('django.contrib.auth.views.login'), {'next_page': '/'}),
    # url(r'^seguridad/logout/$', include('django.contrib.auth.views.logout'), {'next_page': '/segurida/login/'}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
