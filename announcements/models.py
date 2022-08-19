from django.db           import models
from core.models         import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()


class FAQ(TimeStampedModel):
    user     = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.TextField()
    awnser   = models.TextField()
    
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
    q_and_a = models.ForeignKey('QnA',on_delete=models.CASCADE,related_name='q_and_a_comments')
    content = models.TextField()
    
    class Meta:
        db_table = 'QnA_comments'
        
    def __str__(self):
        return self.content
    

# class Notice(TimeStampedModel):
#     user     = models.ForeignKey(User,on_delete=models.CASCADE)
#     title    = models.TextField()
#     content  = models.TextField()
#     img_src1 = models.CharField(max_length=500)
#     img_src2 = models.CharField(max_length=500)
#     img_src3 = models.CharField(max_length=500)
    
    
#     class Meta:
#         db_table = 'notices'
        
#     def __str__(self):
#         return self.title