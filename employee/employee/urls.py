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
from django.conf.urls import url
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
    url(r'^listar/corporativos/$', views.listadoCorporativo, name="listado_corporativos"),
    url(r'^empresa/$', views.empresa, name="empresa"),
    url(r'^listar/empresas/$', views.listadoEmpresa, name="listado_empresas"),
    url(r'^sucursal/$', views.sucursal, name="sucursal"),
    url(r'^listar/sucursales/$', views.listadoSucursal, name="listado_sucursal"),
    url(r'^divisiones/$', views.divisiones, name="divisiones"),
    url(r'^listar/divisiones/$', views.listadoDivisiones, name="listado_divisiones"),
    url(r'^departamentos/$', views.departamentos, name="departamentos"),
    url(r'^listar/departamentos/$', views.listadoDepartamentos, name="listado_departamentos"),


    #----------------->>>AJAX<<<------------------
    url(r'^guardar/empleado/$', views.guardar_empleado, name='guardar_empleado'),
    url(r'^guardar/corporativo/$', views.guardar_corporativo, name='guardar_corporativo'),
    url(r'^guardar/empresa/$', views.guardar_empresa, name='guardar_empresa'),
    url(r'^guardar/sucursal/$', views.guardar_sucursal, name='guardar_sucursal'),
    url(r'^guardar/division/$', views.guardar_division, name='guardar_division'),
    url(r'^guardar/departamento/$', views.guardar_departamento, name='guardar_departamento'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
