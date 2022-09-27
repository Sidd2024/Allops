from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField

#interest options
my_fields = (
            ('Internship','Internship'),
            ('Externship','Externship'),
            ('Student Program','Student Program'),
            ('Scholarship','Scholarship'),
            ('Apprenticeship','Apprenticeship'),
            ('Training','Training'),
            ('Language','Language'),
            ('Social Good','Social Good'),
            ('Open Ended', 'Open Ended'),
            ('Meet up', 'Meet up'),
            ('Conference', 'Conference'),
            ('Workshop', 'Workshop'),
            ('Machine Learning/AI','Machine Learning/AI'),
            ('Blockchain','Blockchain'),
            ('Design','Design'),
            ('Web','Web'),
            ('AR/VR','AR/VR'),
            ('Gaming','Gaming'),
            ('IoT','IoT'),
            ('DevOps','DevOps'),
            ('Cloud','Cloud'),
            ('Cybersecurity','Cybersecurity'),
            ('Mobile','Mobile'),
            ('Data', 'Data'),
            ('Music/Art','Music/Art'),
)

#type options
my_types = (
    ('Competitive','Competitive'),
    ('Event','Event'),
    ('Program','Program'),
    ('Course','Course')
)

class User(AbstractUser):
    pass

class opportunity(models.Model):
    head = models.CharField(max_length=64)
    desc = models.TextField()
    details = models.TextField(blank=False, default='head over to official link for more details!')
    image = models.URLField(blank=True)
    link = models.URLField(blank=False)
    start = models.DateField(blank=False)
    end = models.DateField(blank=True)
    interest = MultiSelectField(choices = my_fields)
    location = models.CharField(max_length=64, default='virtual')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices=my_types, blank=False,max_length=20, default='Program')
    featured = models.BooleanField(default=False)

    def __str__(self):
        return (f"{self.id}. {self.head}: {self.start}, {self.interest} by {self.user}")

class save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = False, related_name="prof_user")
    activity = models.ForeignKey(opportunity, on_delete=models.CASCADE, blank = False, related_name="item")

class mails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mail_user",blank=False)
    mail_id = models.EmailField(blank=False)
    fields = MultiSelectField(choices=my_fields)
    
    def __str__(self):
        return (f"{self.user}:  {self.mail_id}.")
    