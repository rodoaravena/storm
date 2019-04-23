from django.conf.urls import url
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view
from api import views
from api.apiviews import InfoSchedules, RegisterUser, InfoUser, InfoAvailableRoomHours, InfoRangeRoomHours

schema_view = get_swagger_view(title='Storm Api')

urlpatterns = [

    # auth
    path('auth/', include('rest_framework.urls'), name='rest_framework'),
    path('auth/rest/', include('rest_auth.urls'), name='rest_auth'),

    # schedules
    path('schedule/available/<year>/<month>/<day>/', InfoAvailableRoomHours.as_view(), name='available_schedules'),
    path('schedule/range/<year>/<month>/<day>/<hour>/<min>/', InfoRangeRoomHours.as_view(), name='range_schedules'),
    path('schedule/info/', InfoSchedules.as_view(), name='info_schedules'),
    path('schedule/info/<year>/', InfoSchedules.as_view(), name='year_schedules'),
    path('schedule/info/<year>/<month>/', InfoSchedules.as_view(), name='month_schedules'),
    path('schedule/info/<year>/<month>/<day>/', InfoSchedules.as_view(), name='day_schedules'),

    #user
    path('user/create/', RegisterUser.as_view(), name='register_user'),
    path('user/info/<rut_user>', InfoUser.as_view(), name='info_user'),

    # swagger docs
    path('docs/', schema_view),

]

router = routers.DefaultRouter()
#router.register(r'schedule/create', ScheduleViewSet)

urlpatterns += router.urls

