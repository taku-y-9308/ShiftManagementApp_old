from django.urls import path
from . import views

app_name = 'ShiftManagementApp'
urlpatterns = [
    path('',views.home,name = 'index'),
    path('home/',views.home,name = 'index'),
    path('login/',views.Login,name = 'Login'),
    path('logout/',views.Logout,name ='Logout'),
    path('create-newaccount/',views.create_newaccount,name='create-newaccount'),
    path('<int:pk>/',views.Detaildate.as_view(),name='detaildate'),
    #path('<slug:id>/',views.Detailuser.as_view(),name='detailuser'),
    path('SubmitShift/',views.SubmitShift.as_view(),name = 'SubmitShift'),
    path('SubmitShift-Ajax/',views.submitshift,name='SubmitShift-Ajax'),
    path('edit-shift/',views.editshift,name='edit-shift'),
    path('edit-shift-Ajax/',views.editshift_ajax,name='edit-shift-Ajax'),
    path('edit-shift-Ajax/post-shiftdata/',views.editshift_ajax_post_shiftdata,name='edit-shift-Ajax-post-shiftdata'),
    path('edit-shift-Ajax/delete-shiftdata/',views.editshift_ajax_delete_shiftdata,name='edit-shift-Ajax-delete-shiftdata'),
    path('edit/<int:pk>/',views.EditShift.as_view(),name = 'EditShift'),
    path('delete/<int:pk>/',views.DeleteShift.as_view(),name = 'DeleteShift'),
    path('test/',views.ListViewTest.as_view(),name = 'ListViewTest'),
]