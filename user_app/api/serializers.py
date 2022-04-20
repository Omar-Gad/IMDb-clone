from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    """Registration serializer"""
    
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    """Defining a new serializer field not in the model to check password equality"""
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password','password2']
        extra_kwargs = {
            'password': {
                'write_only':True
                }
        }
        
    def save(self):
        """Overriding save method to add the new user and check for validity"""
        
        password = self.validated_data.get('password')
        password2 = self.validated_data.get('password2')
        username = self.validated_data.get('username')
        email = self.validated_data.get('email')
        
        if password != password2:
            raise serializers.ValidationError({'error':'Password not the same!'})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error':'Email already in use!'})
        
        account = User(username=username, email=email)
        account.set_password(password)
        account.save()
        
        return account
            
        