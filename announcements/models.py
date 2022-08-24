from django.db           import models
from pymysql import NULL
from core.models         import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()


class FAQ(TimeStampedModel):
    user     = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.TextField()
    answer   = models.TextField()
    
    class Meta:
        db_table = 'FAQs'
        
    def __str__(self):
        return self.question


class QnA(TimeStampedModel):
    user    = models.ForeignKey(User,on_delete=models.CASCADE)
    title   = models.TextField()
    content = models.TextField()
    
    class Meta:
        db_table = 'QnAs'
        
    def __str__(self):
        return self.title


class QnAComment(TimeStampedModel):
    user    = models.ForeignKey(User,on_delete=models.CASCADE)
    qna     = models.ForeignKey('QnA',on_delete=models.CASCADE,related_name='qna_comments')
    content = models.TextField()
    
    class Meta:
        db_table = 'QnA_comments'
        
    def __str__(self):
        return self.content
    

class Notice(TimeStampedModel):
    user         = models.ForeignKey(User,on_delete=models.CASCADE)
    title        = models.TextField()
    content      = models.TextField()
    img1_url     = models.CharField(max_length=500)
    img1_s3_path = models.CharField(max_length=500)
    img2_url     = models.CharField(max_length=500,null=True)
    img2_s3_path = models.CharField(max_length=500,null=True)
    img3_url     = models.CharField(max_length=500,null=True)
    img3_s3_path = models.CharField(max_length=500,null=True)
    
    
    class Meta:
        db_table = 'notices'
        
    def __str__(self):
        return self.title