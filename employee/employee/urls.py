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
from worksheet import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^forms/empleado/$', views.empleado_form, name="empleados-form"),
    url(r'^perfil/empleado/$', views.empleado_perfil, name="empleado-perfil"),
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


    #----------------->>>AJAX<<<------------------
    url(r'^guardar/empleado/$', views.guardar_empleado, name='guardar_empleado'),
    url(r'^guardar/corporativo/$', views.guardar_corporativo, name='guardar_corporativo'),
    url(r'^guardar/empresa/$', views.guardar_empresa, name='guardar_empresa'),
    url(r'^guardar/sucursal/$', views.guardar_sucursal, name='guardar_sucursal'),
    url(r'^guardar/division/$', views.guardar_division, name='guardar_division'),
    url(r'^guardar/departamento/$', views.guardar_departamento, name='guardar_departamento'),
    url(r'^guardar/puesto/$', views.guardar_puesto, name='guardar_puesto'),
    url(r'^guardar/centro-costo/$', views.guardar_ccosto, name='guardar_ccosto'),
    url(r'^guardar/pais/$', views.guardar_pais, name='guardar_pais'),
    url(r'^guardar/depto-pais/$', views.guardar_deptos, name='guardar_deptos'),
    url(r'^guardar/ciudad/$', views.guardar_ciudades, name='guardar_ciudades'),
    url(r'^guardar/genero/$', views.guardar_genero, name='guardar_genero'),
    url(r'^guardar/estado-civil/$', views.guardar_estado_civil, name='guardar_estado_civil'),
    url(r'^guardar/parentesco/$', views.guardar_parentesco, name='guardar_parentesco'),
    url(r'^guardar/funcion/$', views.guardar_funciones, name='guardar_funciones'),
    url(r'^guardar/equipo/$', views.guardar_equipos, name='guardar_equipos'),
    url(r'^guardar/estatus-empleado/$', views.guardar_estado_empleado, name='guardar_estado_empleado'),
    url(r'^guardar/ausentismo/$', views.guardar_ausentismo, name='guardar_ausentismo'),
    url(r'^guardar/motivo-ausencia/$', views.guardar_motivo_ausencia, name='guardar_motivo_ausencia'),
    url(r'^guardar/motivo-despido/$', views.guardar_motivo_despido, name='guardar_motivo_despido'),

    url(r'^actualizar/corporativo/$', views.actualizar_corporativo, name='actualizar_corporativo'),
    url(r'^actualizar/empresa/$', views.actualizar_empresa, name='actualizar_empresa'),
    url(r'^actualizar/sucursal/$', views.actualizar_sucursal, name='actualizar_sucursal'),
    url(r'^actualizar/division/$', views.actualizar_division, name='actualizar_division'),
    url(r'^actualizar/departamento/$', views.actualizar_departamento, name='actualizar_departamento'),
    url(r'^actualizar/puesto/$', views.actualizar_puesto, name='actualizar_puesto'),
    url(r'^actualizar/centro-costo/$', views.actualizar_ccosto, name='actualizar_ccosto'),
    url(r'^actualizar/pais/$', views.actualizar_pais, name='actualizar_pais'),
    url(r'^actualizar/deptos-pais/$', views.actualizar_deptos, name='actualizar_deptos'),
    url(r'^actualizar/ciudad/$', views.actualizar_ciudad, name='actualizar_ciudad'),
    url(r'^actualizar/genero/$', views.actualizar_genero, name='actualizar_genero'),
    url(r'^actualizar/estado-civil/$', views.actualizar_estado_civil, name='actualizar_estado_civil'),
    url(r'^actualizar/parentesco/$', views.actualizar_parentesco, name='actualizar_parentesco'),
    url(r'^actualizar/funcion/$', views.actualizar_funcion, name='actualizar_funcion'),
    url(r'^actualizar/equipo/$', views.actualizar_equipos, name='actualizar_equipos'),
    url(r'^actualizar/estatus-empleado/$', views.actualizar_estatus_empleado, name='actualizar_estatus_empleado'),
    url(r'^actualizar/ausentismo/$', views.actualizar_ausentismo, name='actualizar_ausentismo'),
    url(r'^actualizar/motivo-ausencia/$', views.actualizar_motivo_ausencia, name='actualizar_motivo_ausencia'),
    url(r'^actualizar/motivo-despido/$', views.actualizar_motivo_despido, name='actualizar_motivo_despido'),

    url(r'^eliminar/corporativo/$', views.eliminar_corporativo, name='eliminar_corporativo'),
    url(r'^eliminar/empresa/$', views.eliminar_empresa, name='eliminar_empresa'),
    url(r'^eliminar/sucursal/$', views.eliminar_sucursal, name='eliminar_sucursal'),
    url(r'^eliminar/division/$', views.eliminar_division, name='eliminar_division'),
    url(r'^eliminar/departamento/$', views.eliminar_departamento, name='eliminar_departamento'),
    url(r'^eliminar/puesto/$', views.eliminar_puesto, name='eliminar_puesto'),
    url(r'^eliminar/centro-costo/$', views.eliminar_ccosto, name='eliminar_ccosto'),
    url(r'^eliminar/pais/$', views.eliminar_pais, name='eliminar_pais'),
    url(r'^eliminar/depto-pais/$', views.eliminar_depto, name='eliminar_depto'),
    url(r'^eliminar/ciudad/$', views.eliminar_ciudad, name='eliminar_ciudad'),
    url(r'^eliminar/genero/$', views.eliminar_genero, name='eliminar_genero'),
    url(r'^eliminar/estado-civil/$', views.eliminar_estado_civil, name='eliminar_estado_civil'),
    url(r'^eliminar/parentesco/$', views.eliminar_parentesco, name='eliminar_parentesco'),
    url(r'^eliminar/funcion/$', views.eliminar_funcion_trabajo, name='eliminar_funcion_trabajo'),
    url(r'^eliminar/equipo/$', views.eliminar_equipo_trabajo, name='eliminar_equipo_trabajo'),
    url(r'^eliminar/estatus-empleado/$', views.eliminar_estatus_empleado, name='eliminar_estatus_empleado'),
    url(r'^eliminar/ausentismo/$', views.eliminar_ausentismo, name='eliminar_ausentismo'),
    url(r'^eliminar/motivo-ausencia/$', views.eliminar_motivo_ausencia, name='eliminar_motivo_ausencia'),
    url(r'^eliminar/motivo-despido/$', views.eliminar_motivo_despido, name='eliminar_motivo_despido'),
    #------------------>>>AJAX<<<-------------------

    url(r'^seguridad/', include('django.contrib.auth.urls')),
    # url(r'^seguridad/logout/$', include('django.contrib.auth.views.login'), {'next_page': '/'}),
    # url(r'^seguridad/logout/$', include('django.contrib.auth.views.logout'), {'next_page': '/segurida/login/'}),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
