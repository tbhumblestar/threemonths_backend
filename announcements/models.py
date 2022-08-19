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


class QAndA(TimeStampedModel):
    user    = models.ForeignKey(User,on_delete=models.CASCADE)
    title   = models.TextField()
    content = models.TextField()
    
    class Meta:
        db_table = 'QAndAs'
        
    def __str__(self):
        return self.title


class QAndAComment(TimeStampedModel):
    user    = models.ForeignKey(User,on_delete=models.CASCADE)
    q_and_a = models.ForeignKey('QAndA',on_delete=models.CASCADE,related_name='q_and_a_comments')
    content = models.TextField()
    
    class Meta:
        db_table = 'Q_and_A_comments'
        
    def __str__(self):
        return self.content
    

# notyet
# class Notice(TimeStampedModel):
#     user    = models.ForeignKey(User,on_delete=models.CASCADE)
#     title   = models.TextField()
#     content = models.TextField()
    
#     class Meta:
#         db_table = 'notices'
        
#     def __str__(self):
#         return self.title


