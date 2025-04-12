from django.db import models
from django.core.validators import FileExtensionValidator

class Question(models.Model):
    QUESTION_TYPES = (
        ('short_text', 'Short Text'),
        ('long_text', 'Long Text'),
        ('email', 'Email'),
        ('choice', 'Choice'),
        ('file', 'File'),
    )
    
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    required = models.BooleanField(default=True)
    text = models.TextField()
    description = models.TextField(blank=True, null=True)
    multiple = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text

class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.question.text} - {self.text}"

class QuestionFileProperty(models.Model):
    FILE_FORMATS = (
        ('.pdf', 'PDF'),
        ('.doc', 'Word'),
        ('.docx', 'Word (new)'),
        ('.jpg', 'JPEG'),
        ('.png', 'PNG'),
    )
    
    SIZE_UNITS = (
        ('kb', 'Kilobytes'),
        ('mb', 'Megabytes'),
        ('gb', 'Gigabytes'),
    )
    
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='file_properties')
    format = models.CharField(max_length=10, choices=FILE_FORMATS)
    max_file_size = models.IntegerField()
    max_file_size_unit = models.CharField(max_length=2, choices=SIZE_UNITS)
    multiple = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.question.text} file properties"

class Response(models.Model):
    full_name = models.CharField(max_length=255)
    email_address = models.EmailField()
    description = models.TextField()
    gender = models.CharField(max_length=10)
    programming_stack = models.CharField(max_length=255)
    date_responded = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_responded']
    
    def __str__(self):
        return f"Response from {self.full_name}"

class Certificate(models.Model):
    response = models.ForeignKey(Response, related_name='certificates', on_delete=models.CASCADE)
    file = models.FileField(
        upload_to='certificates/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file.name.split('/')[-1]
    
