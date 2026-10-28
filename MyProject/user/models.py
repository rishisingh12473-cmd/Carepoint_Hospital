from django.db import models

# Create your models here.
class contactus(models.Model):
    name=models.CharField(max_length=50,null=True)
    mobile=models.CharField(max_length=20,null=True)
    email=models.CharField(max_length=40,null=True)
    message=models.TextField(null=True)


class igallery(models.Model):
    picture=models.ImageField(upload_to="static/gallery/",null=True,blank=True)
    title=models.CharField(max_length=30,null=True)
    details=models.CharField(max_length=300,null=True)

class team(models.Model):
    name=models.CharField(max_length=100,null=True)
    picture=models.ImageField(upload_to="static/team/",null=True,blank=True)
    details=models.CharField(max_length=300,null=True)
    flink=models.CharField(max_length=100,null=True)
    ilink=models.CharField(max_length=100,null=True)

class tblcity(models.Model):
    cityname=models.CharField(max_length=70,null=True)
    def __str__(self):
        return self.cityname

class tblblog(models.Model):
    title=models.CharField(max_length=300,null=True)
    description=models.TextField(null=True)
    picture=models.ImageField(upload_to="static/blog/",null=True,blank=True)
    city=models.ForeignKey(tblcity,on_delete=models.CASCADE)
    date=models.DateField(null=True)

class tblbooking(models.Model):
    name=models.CharField(max_length=60,null=True)
    plocation=models.CharField(max_length=200,null=True)
    mobile=models.CharField(max_length=20,null=True)
    email=models.EmailField(max_length=100,null=True)
    npeople=models.CharField(max_length=50,null=True)
    pkgname=models.CharField(max_length=200,null=True)
    date=models.CharField(max_length=100,null=True)
    days=models.CharField(max_length=20,null=True)

class tblpackage(models.Model):
    pkgname=models.CharField(max_length=100,null=True)
    title=models.TextField(null=True)
    description=models.TextField(null=True)
    picture=models.ImageField(upload_to="static/pkg/",null=True,blank=True)
    price=models.IntegerField(null=True)
    tdays=models.CharField(max_length=50,null=True)


class Appointment(models.Model):
    DEPARTMENT_CHOICES = [
        ("Cardiology", "Cardiology"),
        ("Neurology", "Neurology"),
        ("Orthopedics", "Orthopedics"),
        ("Pediatrics", "Pediatrics"),
        ("Womens Health", "Women's health"),
        ("Diagnostics", "Diagnostics"),
        ("General Medicine", "General medicine"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    patient_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    department = models.CharField(max_length=40, choices=DEPARTMENT_CHOICES)
    doctor = models.CharField(max_length=100, blank=True)
    appointment_date = models.DateField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["appointment_date", "created_at"]

    def __str__(self):
        return f"{self.patient_name} - {self.department} ({self.appointment_date})"