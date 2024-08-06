from django.contrib import admin
from .models import *

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'first_name', 'last_name', 'mobile','middle_name']

class userAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'email', 'first_name', 'middle_name', 'last_name', 'mobile']

class BasicAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','NameOfTheIndustry', 'Telephone', 'WebsiteLink', 'ContactEmail']

class PyhsicalAdmin(admin.ModelAdmin):
    list_display = ["id", "user","District", "Constituency", "Sub_county", "Parish", "Village", "GPS_Points"]

class CapacityAdmin(admin.ModelAdmin):
    list_display = ["id","reason","Date_Of_Registration","certificate", "Registration_Number", "Name_Of_The_Contact_Person", "TelNo_Of_The_Contact_Person", "Title_Of_The_Contact_Person"]

class educationAdmin(admin.ModelAdmin):
    list_display = ["id", "No_Formal_Education", "PLE", "UCE","UACE","Certificate","Diploma","Degree","Post_Graduate", "Total"]

class EmployeeCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'permanent_male', 'permanent_female',
                    'contract_male', 'contract_female',
                    'casual_male', 'casual_female',
                    'consultants_male', 'consultants_female',
                     'total')


class TradeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "targeted_trade","reason_for_partnership", "enterprise_size", "dev_stage", "track_record","expertise","staff_mentoring","infrastructure","sector_description"]

class HostingExperienceAdmin(admin.ModelAdmin):
    list_display =  ['id', 'user','has_hosted_apprentices', 'experience_details', 'max_apprentices', 'support_description']

class WorkAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','module_code', 'module_name', 'duration']

class AdditionalAdmin(admin.ModelAdmin):
    list_editable = ("verified",)
    list_display = ["id", "additionalComments", "fullName", "organizationName", "verified"]

class FileAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'user']

class EnvironmentAdmin(admin.ModelAdmin):
    list_display = ["user","Harrasment_Prevention",
                    "provided_PPES",
                    "Available_channels"]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserAccount, userAdmin)
admin.site.register(BasicInformation, BasicAdmin)
admin.site.register(PhysicalAddress, PyhsicalAdmin)
admin.site.register(Capacity, CapacityAdmin)
admin.site.register(EducationCount, educationAdmin)
admin.site.register(EmployeeCategory, EmployeeCategoryAdmin)
admin.site.register(Trade, TradeAdmin)
admin.site.register(HostingExperience, HostingExperienceAdmin)
admin.site.register(WorkPlacementCourse, WorkAdmin)
admin.site.register(AdditionalInformation, AdditionalAdmin)
admin.site.register(Files,FileAdmin)
admin.site.register(Environment, EnvironmentAdmin)