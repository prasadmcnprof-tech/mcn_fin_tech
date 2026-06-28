from django.db import models
from django.contrib.auth.models import User

class ServiceCategory(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ["name"]
    def __str__(self): return self.name

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    short_description = models.TextField()
    overview = models.TextField()
    why_choose = models.TextField(blank=True)
    who_should_apply = models.TextField(blank=True)
    key_highlights = models.TextField(blank=True)
    documents_required = models.TextField(blank=True)
    process_steps = models.TextField(blank=True)
    timeline = models.TextField(blank=True)
    pricing_note = models.TextField(blank=True)
    faq = models.TextField(blank=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expected_timeline = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ["display_order", "title"]
    def __str__(self): return self.title
    def line_list(self, field_name):
        value = getattr(self, field_name, "") or ""
        return [x.strip() for x in value.splitlines() if x.strip()]
    def highlight_list(self): return self.line_list("key_highlights")
    def document_list(self): return self.line_list("documents_required")
    def process_step_list(self): return self.line_list("process_steps")
    def timeline_list(self): return self.line_list("timeline")
    def applicant_list(self): return self.line_list("who_should_apply")
    def faq_list(self):
        items = []
        for line in self.line_list("faq"):
            if "|" in line:
                q, a = line.split("|", 1)
                items.append({"question": q.strip(), "answer": a.strip()})
        return items

class CustomerRequest(models.Model):
    STATUS_CHOICES = [
        ("NEW", "New"), ("DOCS_PENDING", "Documents Pending"), ("UNDER_REVIEW", "Under Review"),
        ("SUBMITTED", "Submitted"), ("QUERY_RAISED", "Query Raised"), ("COMPLETED", "Completed"), ("CANCELLED", "Cancelled"),
    ]
    PAYMENT_STATUS_CHOICES = [("NOT_PAID", "Not Paid"), ("PARTIAL", "Partial"), ("PAID", "Paid")]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_requests")
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    request_number = models.CharField(max_length=30, unique=True, blank=True)
    customer_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100, blank=True)
    business_type = models.CharField(max_length=120, blank=True)
    customer_notes = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="NEW")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="NOT_PAID")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_customer_requests")
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Customer Request"
        verbose_name_plural = "Customer Requests"
        ordering = ["-created_at"]
    def save(self, *args, **kwargs):
        if not self.request_number:
            self.request_number = f"REQ-{CustomerRequest.objects.count()+1:05d}"
        super().save(*args, **kwargs)
    def __str__(self): return f"{self.request_number} - {self.customer_name}"

class RequestDocument(models.Model):
    customer_request = models.ForeignKey(CustomerRequest, on_delete=models.CASCADE, related_name="documents")
    document_name = models.CharField(max_length=150)
    file = models.FileField(upload_to="request_documents/")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    verified = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Request Document"
        verbose_name_plural = "Request Documents"
        ordering = ["-uploaded_at"]
    def __str__(self): return f"{self.customer_request.request_number} - {self.document_name}"
