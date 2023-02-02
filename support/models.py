from django.db import models
from config.base_manager import BaseManager
from user.models import User


class Support(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    subject = models.CharField(db_column='Subject', max_length=63)
    date_created = models.DateTimeField(db_column='DateCreated', auto_now_add=True)
    user_id = models.ForeignKey(User, db_column='UserID', on_delete=models.CASCADE)

    objects = BaseManager()

    class Meta:
        db_table = 'Support'


class SupportMessages(models.Model):
    def support_files_path(self, file_name):
        return f'support/{self.support_id}/{file_name}'

    id = models.BigAutoField(db_column='ID', primary_key=True)
    is_answer = models.BooleanField(db_column='IsAnswer', default=True)
    message = models.CharField(db_column='Message', max_length=1023)
    file = models.FileField(db_column='File', upload_to=support_files_path, blank=True, null=True)
    date_created = models.DateTimeField(db_column='DateCreated', auto_now_add=True)
    support_id = models.ForeignKey(Support, db_column='SupportID', on_delete=models.CASCADE)

    class Meta:
        db_table = 'SupportMessage'
