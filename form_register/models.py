from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator

# Create your models here.
class UserAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile = models.PositiveBigIntegerField(validators=[MaxValueValidator(999999999999)])

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.PositiveBigIntegerField(null=True, blank=True, validators=[MaxValueValidator(999999999999)])

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            email=instance.email,
            first_name=instance.first_name,
            last_name=instance.last_name
        )

def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

post_save.connect(create_profile, sender=User)
post_save.connect(save_profile, sender=User)

class BasicInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    NameOfTheIndustry = models.CharField(max_length=200)
    Telephone = models.PositiveBigIntegerField(validators=[MaxValueValidator(999999999999)])
    WebsiteLink = models.URLField(max_length=200, null=True, blank=True, default='No Website Link')
    ContactEmail = models.EmailField(max_length=200)

    def __str__(self):
        return self.NameOfTheIndustry
    
class PhysicalAddress(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     District = models.CharField(max_length=100)
     Constituency = models.CharField(max_length=100)
     Sub_county = models.CharField(max_length=200)
     Parish = models.CharField(max_length=200)
     Village = models.CharField(max_length=100)
     GPS_Points = models.CharField(max_length=100, null=True, blank=True)

class Capacity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Date_Of_Registration = models.DateField(null=True, blank=True)
    certificate = models.FileField(upload_to='files/')
    Registration_Number = models.CharField(max_length=200, null=True, blank=True)
    Name_Of_The_Contact_Person = models.CharField(max_length=200, null=True, blank=True)
    TelNo_Of_The_Contact_Person = models.PositiveBigIntegerField(validators=[MaxValueValidator(999999999999)], null=True, blank=True)
    Title_Of_The_Contact_Person = models.CharField(max_length=100, null=True, blank=True)
    reason = models.CharField(max_length=300, default='No Reason')

class EducationCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    No_Formal_Education = models.PositiveIntegerField()
    PLE = models.PositiveIntegerField()
    UCE = models.PositiveIntegerField()
    UACE = models.PositiveIntegerField()
    Certificate = models.PositiveIntegerField()
    Diploma = models.PositiveIntegerField()
    Degree = models.PositiveIntegerField()
    Post_Graduate = models.PositiveIntegerField()
    Total = models.PositiveIntegerField()

class EmployeeCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permanent_male = models.PositiveIntegerField(default=0)
    permanent_female = models.PositiveIntegerField(default=0)
    contract_male = models.PositiveIntegerField(default=0)
    contract_female = models.PositiveIntegerField(default=0)
    casual_male = models.PositiveIntegerField(default=0)
    casual_female = models.PositiveIntegerField(default=0)
    consultants_male = models.PositiveIntegerField(default=0)
    consultants_female = models.PositiveIntegerField(default=0)

    @property
    def total(self):
        return (self.permanent_male + self.permanent_female +
                self.contract_male + self.contract_female +
                self.casual_male + self.casual_female +
                self.self_employed_male + self.self_employed_female +
                self.other_male + self.other_female)

    def __str__(self):
        return f"User {self.user.id} - Total Employees: {self.total}"

class Trade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    targeted_trade = models.CharField(max_length=255)
    reason_for_partnership = models.TextField()
    enterprise_size = models.CharField(max_length=255)
    dev_stage = models.CharField(max_length=255)
    track_record = models.TextField()
    expertise = models.TextField()
    staff_mentoring = models.TextField()
    infrastructure = models.TextField()
    sector_description = models.TextField()

    def __str__(self):
        return self.targeted_trade
    
class HostingExperience(models.Model):
    YES_NO_CHOICES = [
        ('YES', 'Yes'),
        ('NO', 'No'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    has_hosted_apprentices = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    experience_details = models.TextField(blank=True, null=True)
    max_apprentices = models.IntegerField()
    support_description = models.TextField()

    def __str__(self):
        return f"Hosting Experience: {self.has_hosted_apprentices}"

class WorkPlacementCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trade = models.ForeignKey(Trade, related_name='courses', on_delete=models.CASCADE)
    module_code = models.CharField(max_length=100)
    module_name = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.module_code} - {self.module_name} ({self.duration})"

class AdditionalInformation(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   additionalComments= models.TextField()
   fullName = models.CharField(max_length=255)
   verified = models.BooleanField(default=False)
   organizationName= models.CharField(max_length=255)

   def __str__(self):
        return f'{self.fullName } - {self.organizationName}'
