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

    url(r'^actualizar/corporativo/$', views.actualizar_corporativo, name='actualizar_corporativo'),
    url(r'^actualizar/empresa/$', views.actualizar_empresa, name='actualizar_empresa'),
    url(r'^actualizar/sucursal/$', views.actualizar_sucursal, name='actualizar_sucursal'),
    url(r'^actualizar/division/$', views.actualizar_division, name='actualizar_division'),
    url(r'^actualizar/departamento/$', views.actualizar_departamento, name='actualizar_departamento'),
    url(r'^actualizar/puesto/$', views.actualizar_puesto, name='actualizar_puesto'),
    url(r'^actualizar/centro-costo/$', views.actualizar_ccosto, name='actualizar_ccosto'),
    url(r'^actualizar/pais/$', views.actualizar_pais, name='actualizar_pais'),

    url(r'^eliminar/corporativo/$', views.eliminar_corporativo, name='eliminar_corporativo'),
    url(r'^eliminar/empresa/$', views.eliminar_empresa, name='eliminar_empresa'),
    url(r'^eliminar/sucursal/$', views.eliminar_sucursal, name='eliminar_sucursal'),
    url(r'^eliminar/division/$', views.eliminar_division, name='eliminar_division'),
    url(r'^eliminar/departamento/$', views.eliminar_departamento, name='eliminar_departamento'),
    url(r'^eliminar/puesto/$', views.eliminar_puesto, name='eliminar_puesto'),
    url(r'^eliminar/centro-costo/$', views.eliminar_ccosto, name='eliminar_ccosto'),
    url(r'^eliminar/pais/$', views.eliminar_pais, name='eliminar_pais'),
    #------------------>>>AJAX<<<-------------------

    url(r'^seguridad/', include('django.contrib.auth.urls')),
    # url(r'^seguridad/logout/$', include('django.contrib.auth.views.login'), {'next_page': '/'}),
    # url(r'^seguridad/logout/$', include('django.contrib.auth.views.logout'), {'next_page': '/segurida/login/'}),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
