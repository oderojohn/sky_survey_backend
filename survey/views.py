from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend

from .models import Question, Response as SurveyResponse, Certificate
from .serializers import (
    QuestionSerializer,
    ResponseSerializer,
    CertificateUploadSerializer,
    CertificateSerializer
)

import os


# 🟢 Read-only view for questions
class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.prefetch_related('options', 'file_properties').all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'questions': serializer.data})


# 🟡 Full CRUD for responses (mostly POST and GET with filtering by email)
class ResponseViewSet(viewsets.ModelViewSet):
    queryset = SurveyResponse.objects.prefetch_related('certificates').all()
    serializer_class = ResponseSerializer
    parser_classes = (MultiPartParser, FormParser)  # This is important for handling file uploads
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email_address']
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        """
        Custom list view that supports pagination and filters
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'question_responses': serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        return Response({'question_responses': serializer.data})

    def update(self, request, *args, **kwargs):
        """
        Custom update view to handle both updating SurveyResponse and related certificates
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()  # Get the instance by its primary key

        # Extract certificates data and remove it from the request data
        certificates_data = request.data.get('certificates', None)
        request.data.pop('certificates', None)  # Remove certificates to handle them separately

        # Update the SurveyResponse fields
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Handle certificates update if certificates_data exists
        if certificates_data is not None:
            instance.certificates.all().delete()  # Remove existing certificates (if updating)
            for cert_data in certificates_data:
                Certificate.objects.create(response=instance, **cert_data)

        return Response({'question_response': serializer.data}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """
        Handle partial updates (i.e., only update part of the resource)
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

# 🔵 Upload certificates linked to responses
class CertificateUploadView(generics.CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CertificateUploadSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_instance = serializer.validated_data['response']

        # Save each uploaded certificate
        uploaded_files = request.FILES.getlist('certificates')
        saved_files = []
        for file in uploaded_files:
            cert = Certificate.objects.create(response=response_instance, file=file)
            saved_files.append(cert.file.name)

        return Response(
            {'certificates_uploaded': saved_files},
            status=status.HTTP_201_CREATED
        )


# 🔻 Download a certificate by ID
class CertificateDownloadView(generics.RetrieveAPIView):
    queryset = Certificate.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CertificateSerializer

    def retrieve(self, request, *args, **kwargs):
        certificate = self.get_object()
        if not certificate.file.name.lower().endswith('.pdf'):
            return Response(
                {'error': 'Only PDF files are supported for download.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        file_handle = certificate.file.open()
        response = FileResponse(file_handle, content_type='application/pdf')
        response['Content-Length'] = certificate.file.size
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(certificate.file.name)}"'
        return response
