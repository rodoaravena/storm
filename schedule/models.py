from django.db import models
from django.contrib.auth.models import User


class ModuleTime(models.Model):
    module = models.IntegerField(primary_key=True)
    start = models.CharField(max_length=5)
    end = models.CharField(max_length=5)
    def __str__(self):
        return '{0}-{1}'.format(self.start, self.end)

class UserProfile(models.Model):
    rut = models.CharField(max_length=10, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)

    def create_user(self, email_user, password_user, name, lastname):
        try:
            user_data = User.objects.create_user(username=email_user,
                                            email=email_user, 
                                            first_name=name,
                                            last_name=lastname,
                                            password=password_user)
            self.user = user_data
            self.save()
            return True
        except:
            return False

class Schedule(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    date_schedule = models.DateField()
    module = models.ForeignKey(ModuleTime, on_delete=models.CASCADE)
    def __str__(self):
        return 'Registro: {0}'.format(self.id)