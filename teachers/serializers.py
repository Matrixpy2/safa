from django.contrib.auth.hashers import check_password
from django.template.backends.django import reraise
from datetime import timezone
from rest_framework import serializers
from .admin import Teacher
from .models import teacher , News , Homework 
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from schools.models import Students , classes
from chat_app.models import ChatRoom ,Message



class SignUpSerializer(serializers.Serializer):
    username   = serializers.CharField()
    first_name = serializers.CharField()
    last_name  = serializers.CharField()
    number_id  = serializers.CharField()
    password1  = serializers.CharField(write_only=True )
    password2  = serializers.CharField(write_only=True)
    class Meta:
        model   = User
        fields  = ['username','first_name' , 'last_name' , 'number_id' , 'password1' , 'password2']

    def validate(self, data):
        print(data)
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({'password1 != password2'})
        # user = User.objects.get(username=data['username'])
        return data

    def validate_number_id(self , number_id):
        if number_id and teacher.objects.filter(number_id=number_id).exists():
            raise serializers.ValidationError('user was exists')
        return number_id

    def validate_first_name(self , first_name):
        if any(char.isdigit() for char in first_name):
            raise serializers.ValidationError('نمیتوانید از عدد داخل اسم استفاده کنید')
        if not first_name:
            raise serializers.ValidationError('first name is required')
        return first_name
    def validate_last_name(self , last_name):
        if any(char.isdigit() for char in last_name):
            raise serializers.ValidationError('نمیتوانید از عدد داخل اسم استفاده کنید')
        if not last_name:
            raise serializers.ValidationError('last name is required')
        return last_name

    def create(self , validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')


        username   = validated_data.pop('username')
        first_name = validated_data.pop('first_name')
        last_name  = validated_data.pop('last_name')
        number_id  = validated_data.pop('number_id')

        if not all([first_name , last_name , number_id]):
            raise serializers.ValidationError('fill all params')

        user = User(
            username = username,
        )
        user.set_password(password)

        user.save()
        teacher.objects.create(
            user       = user,
            first_name = first_name,
            last_name  = last_name,
            number_id  = number_id,
        )
        return user


class LoginSerializer(serializers.Serializer):
    username  =  serializers.CharField(max_length=100 , min_length=3)
    password  =  serializers.CharField(write_only=True)

    def validate(self, data):
        username = data['username']
        password = data['password']
        try:
            user = User.objects.get(username=username)
        except:
            raise serializers.ValidationError('user not found')
        if not teacher.objects.filter(user=user).exists():
            raise serializers.ValidationError('user is not teacher')
        if not check_password(password , user.password):
            raise serializers.ValidationError('username or password incorrect')
        
        return data



class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model  = teacher
        fields = '__all__'

class AddStudentSerializer(serializers.Serializer):
    number_id = serializers.CharField(max_length= 100)
    title =     serializers.CharField(max_length=100)
    def validate(self, data):
        number_id = data['number_id']
        class_name = data['title']
        try:
            Students.objects.get(number_id=number_id)
        except:
            print('1')
            raise serializers.ValidationError('student not found')
        if classes.objects.filter(students__number_id=number_id).exists():
            print('2')
            raise serializers.ValidationError('student is already in a class')
        if Students.objects.filter(classes__title=class_name , number_id=number_id).exists():
            raise serializers.ValidationError('student is already in this class')
        if not classes.objects.filter(title=class_name).exists():
            raise serializers.ValidationError(f'class {class_name} not found')
        
        return data
    
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
    
    def validate(self, data):
        title = data['title']
        if News.objects.filter(title=title).exists():
            raise serializers.ValidationError('new with this title already exists')
        return data
    
    def create(self, validated_data):
        author = validated_data.pop('author')
        classes = validated_data.pop('classes')
        title = validated_data.pop('title')
        content = validated_data.pop('content')

        news = News.objects.create(
            author=author,
            classes=classes,
            title=title,
            content=content
        )
        return news

class HomeworkSerializer(serializers.ModelSerializer):
    classes = serializers.CharField()   
    date = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"] )

    class Meta:
        model = Homework
        fields = ['title', 'content', 'classes' , 'date']
        read_only_fields = ['author']

    def validate_date(self, date):
        if date < timezone.now().date():
            raise serializers.ValidationError('date invalid')
        return date


    def validate_classes(self, value):
        try:
            return classes.objects.get(title=value)
        except classes.DoesNotExist:
            raise serializers.ValidationError("class not found")

    def validate(self, data):
        title = data['title']
        class_obj = data['classes']

        if Homework.objects.filter(title=title, classes=class_obj).exists():
            raise serializers.ValidationError("homework already exists for this class")

        return data
    
    def create(self, validated_data):
        author = self.context['request'].user
        title = validated_data.pop('title')
        content = validated_data.pop('content')
        classes = validated_data.pop('classes')
        date = validated_data.pop('date')

        homework = Homework.objects.create(
            author=author,
            title=title,
            content=content,
            classes=classes,
            date=date
        )
        return homework
        
class SendMessageSerializer(serializers.ModelSerializer):
        class Meta:
            model = Message
            fields = ['text']
        
        def validate(self, data):
            text = data['text']
            if len(text) > 500:
                raise serializers.ValidationError('text is too long')
            if len(text) <=3:
                raise serializers.ValidationError('text is too short')
            if text.isspace():
                raise serializers.ValidationError('text cannot be empty')
            return data
        def create(self, validated_data):
            sender = self.context['request'].user
            text = validated_data.pop('text')
            student_id = self.context['student_id']
            student = Students.objects.get(id=student_id)
            Teacher = teacher.objects.get(user=sender)
            chat_room= ChatRoom.objects.get_or_create(student=student, teacher=Teacher)
            message = Message.objects.create(
                room=chat_room[0],
                sender=sender,
                text=text
            )
            return message