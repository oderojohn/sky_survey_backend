from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QuestionViewSet,
    ResponseViewSet,
    CertificateUploadView,
    CertificateDownloadView,
    CertificateBatchDownloadView
)

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'responses', ResponseViewSet, basename='response')

urlpatterns = [
    path('', include(router.urls)),
    path('upload-certificate/', CertificateUploadView.as_view(), name='upload-certificate'),
    path('download-certificate/<int:pk>/', CertificateDownloadView.as_view(), name='download-certificate'),
    path('certificates/download/', CertificateBatchDownloadView.as_view(), name='certificates-download'),

]
