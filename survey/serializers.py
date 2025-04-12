from rest_framework import serializers
from .models import Question, QuestionOption, QuestionFileProperty, Response, Certificate
from rest_framework.exceptions import ValidationError
import os

class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['value', 'text']

class QuestionFilePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionFileProperty
        fields = ['format', 'max_file_size', 'max_file_size_unit', 'multiple']

class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, read_only=True)
    file_properties = QuestionFilePropertySerializer(read_only=True)
    
    class Meta:
        model = Question
        fields = ['name', 'type', 'required', 'text', 'description', 'options', 'file_properties']

    def validate(self, data):
        """
        Custom validation to check specific logic for questions of type 'file'
        """
        if data.get('type') == 'file' and not data.get('file_properties'):
            raise ValidationError("File questions must have file properties defined.")
        return data

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'file']
        read_only_fields = ['id']

    def validate_file(self, value):
        """
        Custom validation to ensure that only PDF files are allowed for certificates
        """
        ext = os.path.splitext(value.name)[1]
        if ext.lower() != '.pdf':
            raise ValidationError("Only PDF files are allowed.")
        return value

class ResponseSerializer(serializers.ModelSerializer):
    certificates = serializers.ListField(
        child=serializers.FileField(), required=False, write_only=True
    )
    certificate_files = CertificateSerializer(source='certificate_set', many=True, read_only=True)

    class Meta:
        model = Response
        fields = ['id', 'full_name', 'email_address', 'description', 'gender', 
                  'programming_stack', 'certificates', 'certificate_files', 'date_responded']
        read_only_fields = ['id', 'date_responded', 'certificate_files']

    def validate_certificates(self, value):
        for file in value:
            ext = os.path.splitext(file.name)[1].lower()
            if ext != '.pdf':
                raise ValidationError("Only PDF files are allowed.")
        return value

    def create(self, validated_data):
        certificates = validated_data.pop('certificates', [])
        response = Response.objects.create(**validated_data)
        for cert in certificates:
            Certificate.objects.create(response=response, file=cert)
        return response

class CertificateUploadSerializer(serializers.Serializer):
    certificates = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False),
        required=True
    )
    
    def validate_certificates(self, value):
        """
        Validate that each certificate is a PDF
        """
        for cert in value:
            ext = os.path.splitext(cert.name)[1]
            if ext.lower() != '.pdf':
                raise ValidationError("Only PDF files are allowed")
        return value
