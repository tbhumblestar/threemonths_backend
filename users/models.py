from django.db                  import models
from core.models                import TimeStampedModel
from django.contrib.auth.models import (
                                BaseUserManager,
                                AbstractBaseUser,
                                PermissionsMixin
)

class CustomUserManager(BaseUserManager):
    
    use_in_migrations = True
    
    def _create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('email must be set')
        if not password:
            raise ValueError('password must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
    def create_user(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email,password,**extra_fields)

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff',True)
        
        if extra_fields.get('is_superuser') is not True:
            return ValueError("Superuser must have is_superuser=True")
        
        if extra_fields.get('is_staff') is not True:
            return ValueError("Superuser must have is_staff=True")
                
        return self._create_user(email,password,**extra_fields)


class User(AbstractBaseUser,PermissionsMixin,TimeStampedModel):
    
    login_type = (
        ('KakaoLogin','KakaoLogin'),
        ('SiteLogin','SiteLogin')
    )

    email                      = models.EmailField('email adress',unique=True,max_length=100)
    login_type                 = models.CharField('login_type',max_length=30,choices=login_type)
    nickname                   = models.CharField('nickname',max_length=30,null=True)
    username                   = models.CharField('username',max_length=30,null=True,blank=True)
    contact_num                = models.CharField('contact_num',max_length=50,null=True,blank=True)
    location                   = models.CharField('location',max_length=50,null=True,blank=True)
    is_active                  = models.BooleanField('is_active',default=True)
    is_staff                   = models.BooleanField('is_staff',default=False)
    profile_image_url          = models.CharField('profile_image_url',max_length=200,null=True,blank=True)
    profile_image_storage_path = models.CharField('profile_image_storage_path',max_length=200,null=True,blank=True)
    kakao_id                   = models.PositiveIntegerField('kakao_id',null=True,blank=True)
    
    EMAIL_FIELD                = "email"
    USERNAME_FIELD             = 'email'
    REQUIRED_FIELDS            = ['nickname']
    
    objects                    = CustomUserManager()
    
    def __str__(self):
        return f"{self.email} (nickname : {self.nickname})"
    
    class Meta:
        db_table = 'users'
        
        
class SMSAuth(TimeStampedModel):

    sms_check_num = models.CharField(max_length=30)
    
    #번호 인덱스 추가해야 함
    contact_num   = models.CharField(max_length=100,db_index=True)

    def __str__(self):
        return f"{self.contact_num}:{self.sms_check_num}"

    class Meta:
        db_table = 'sms_auth'

        