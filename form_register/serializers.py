from rest_framework.fields import empty
from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined']

class ObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        if hasattr(user, 'profile'):
            token['middle_name'] = user.profile.middle_name
            token['email'] = user.email
            token['mobile'] = user.profile.mobile

        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'first_name', 'last_name', 'middle_name', 'mobile', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        user_data = {
            'email': validated_data['email'],
            'username': validated_data['email'],  # Use email as username
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
        }
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')
        try:
            user = User.objects.create(**user_data)
            user.set_password(password)
            user.save()

            user_account = UserAccount.objects.create(
                user=user,
                middle_name=validated_data['middle_name'],
                mobile=validated_data['mobile'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data['email']
            )
            return user_account
        except IntegrityError:
          raise serializers.ValidationError({"username": "Username already exists."})
        
# basic info serializer
class basicSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicInformation
        fields = ['id', 'user','NameOfTheIndustry', 'Telephone', 'WebsiteLink', 'ContactEmail']

# physical Adress srializer
class PhysicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalAddress
        fields = ["id", "user","District", "Constituency", "Sub_county", "Parish", "Village", "GPS_Points"]

# capacity serializer
class CapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Capacity
        fields = '__all__'


# education serializers
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationCount
        fields = '__all__'

# category serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeCategory
        fields = '__all__'

# hosting serializers
class WorkPlacementCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPlacementCourse
        fields = ['id', 'user','module_code', 'module_name', 'duration']

# trade serializer
class TradeSerializer(serializers.ModelSerializer):
    courses = WorkPlacementCourseSerializer(many=True)

    class Meta:
        model = Trade
        fields = ["id", "user", "targeted_trade","reason_for_partnership", "enterprise_size", "dev_stage", "track_record","expertise","staff_mentoring","infrastructure","sector_description", "courses"]

    def create(self, validated_data):
        courses_data = validated_data.pop('courses')
        trade = Trade.objects.create(**validated_data)
        for course_data in courses_data:
            WorkPlacementCourse.objects.create(trade=trade, **course_data)
        return trade
    
    
    def update(self, instance, validated_data):
        courses_data = validated_data.pop('courses')
        instance.targeted_trade = validated_data.get('targeted_trade', instance.targeted_trade)
        instance.reason_for_partnership = validated_data.get('reason_for_partnership', instance.reason_for_partnership)
        instance.enterprise_size = validated_data.get('enterprise_size', instance.enterprise_size)
        instance.dev_stage = validated_data.get('dev_stage', instance.dev_stage)
        instance.track_record = validated_data.get('track_record', instance.track_record)
        instance.expertise = validated_data.get('expertise', instance.expertise)
        instance.staff_mentoring= validated_data.get('staff_mentoring', instance.staff_mentoring)
        instance.infrastructure= validated_data.get('infrastructure', instance.infrastructure)
        instance.sector_description= validated_data.get('sector_description', instance.sector_description)
        instance.save()

        # Updating the courses
        existing_course_ids = [course.id for course in instance.courses.all()]
        new_course_ids = [course['id'] for course in courses_data if 'id' in course]

        # Delete courses that are not present in the new data
        for course_id in existing_course_ids:
            if course_id not in new_course_ids:
                WorkPlacementCourse.objects.get(id=course_id).delete()

        # Update or create courses
        for course_data in courses_data:
            course_id = course_data.get('id')
            if course_id:
                course = WorkPlacementCourse.objects.get(id=course_id)
                course.sn = course_data.get('sn', course.sn)
                course.course_name = course_data.get('course_name', course.course_name)
                course.duration = course_data.get('duration', course.duration)
                course.save()
            else:
                WorkPlacementCourse.objects.create(trade=instance, **course_data)

        return instance

class HostingExperienceSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = HostingExperience
        fields = '__all__'
# additional information
class AdditionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInformation
        fields = '__all__'

# change password
class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        # Check if the new password and its confirmation match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        # Verify that the provided old password matches the user's current password
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        # make sure user is only able to update their own password
        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You don't have permission for this user."})

        # Set the new password for the user instance
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UserInfoSerializer(serializers.ModelSerializer):
    physical_address = serializers.SerializerMethodField()
    capacities = serializers.SerializerMethodField()
    educations = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    trades = serializers.SerializerMethodField()
    hosting_experiences = serializers.SerializerMethodField()
    additional_info = serializers.SerializerMethodField()

    class Meta:
        model = BasicInformation
        fields = [
            'id', 'user', 'NameOfTheIndustry', 'Telephone', 'WebsiteLink', 'ContactEmail',
            'physical_address', 'capacities', 'educations', 
            'categories', 'trades', 'hosting_experiences', 'additional_info'
        ]

    def get_physical_address(self, obj):
        addresses = PhysicalAddress.objects.filter(user=obj.user)
        return PhysicalSerializer(addresses, many=True).data

    def get_capacities(self, obj):
        capacities = Capacity.objects.filter(user=obj.user)
        return CapacitySerializer(capacities, many=True).data

    def get_educations(self, obj):
        educations = EducationCount.objects.filter(user=obj.user)
        return EducationSerializer(educations, many=True).data

    def get_categories(self, obj):
        categories = EmployeeCategory.objects.filter(user=obj.user)
        return CategorySerializer(categories, many=True).data

    def get_trades(self, obj):
        trades = Trade.objects.filter(user=obj.user)
        return TradeSerializer(trades, many=True).data

    def get_hosting_experiences(self, obj):
        hosting_experiences = HostingExperience.objects.filter(user=obj.user)
        return HostingExperienceSerializer(hosting_experiences, many=True).data

    def get_additional_info(self, obj):
        additional_info = AdditionalInformation.objects.filter(user=obj.user)
        return AdditionalSerializer(additional_info, many=True).data