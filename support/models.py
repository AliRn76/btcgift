from django.db import models
from user.models import User


class Support(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    subject = models.CharField(db_column='Subject', max_length=63)
    issue = models.CharField(db_column='Issue', max_length=1024)
    date_created = models.DateTimeField(db_column='DateCreated', auto_now_add=True)
    user_id = models.ForeignKey(User, db_column='UserID', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Support'


class SupportMessages(models.Model):
    def support_files_path(self, file_name):
        return f'support/{self.support_id}/{file_name}'

    id = models.BigAutoField(db_column='ID', primary_key=True)
    is_answer = models.BooleanField(db_column='IsAnswer')
    message = models.CharField(db_column='Message', max_length=1024, blank=True, null=True)  # Required if file is None
    file = models.FileField(db_column='File', upload_to=support_files_path, blank=True, null=True)  # Required if message is None
    date_created = models.DateTimeField(db_column='DateCreated', auto_now_add=True)
    admin_id = models.ForeignKey(User, db_column='AdminID', on_delete=models.PROTECT)  # Required if is_answer is True
    support_id = models.ForeignKey(Support, db_column='SupportID', on_delete=models.CASCADE)

    class Meta:
        db_table = 'SupportMessage'
