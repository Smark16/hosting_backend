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

# trade serializer
class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'

# hosting serializers
class WorkPlacementCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPlacementCourse
        fields = ['id', 'user','sn', 'course_name', 'duration']

class HostingExperienceSerializer(serializers.ModelSerializer):
    courses = WorkPlacementCourseSerializer(many=True)

    class Meta:
        model = HostingExperience
        fields = ['id', 'user','has_hosted_apprentices', 'experience_details', 'max_apprentices', 'support_description', 'courses']

    def create(self, validated_data):
        courses_data = validated_data.pop('courses')
        hosting_experience = HostingExperience.objects.create(**validated_data)
        for course_data in courses_data:
            WorkPlacementCourse.objects.create(hosting_experience=hosting_experience, **course_data)
        return hosting_experience
    

    def update(self, instance, validated_data):
        courses_data = validated_data.pop('courses')
        instance.has_hosted_apprentices = validated_data.get('has_hosted_apprentices', instance.has_hosted_apprentices)
        instance.experience_details = validated_data.get('experience_details', instance.experience_details)
        instance.max_apprentices = validated_data.get('max_apprentices', instance.max_apprentices)
        instance.support_description = validated_data.get('support_description', instance.support_description)
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
                WorkPlacementCourse.objects.create(hosting_experience=instance, **course_data)

        return instance

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