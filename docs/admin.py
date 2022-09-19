from django.contrib import admin
from .models import Document, DocumentRef, DocumentReceipt, DocumentReceiptRef

# Register your models here.
admin.site.register(Document)
admin.site.register(DocumentRef)
