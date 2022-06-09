from django.db import models


class CSVFile(models.Model):
    name = models.CharField(max_length=100)
    csvFile = models.FileField(upload_to='app1/csvs')

    def __str__(self):
        return self.name


# class Participant(models.Model):
#     name = models.CharField(max_length=10)
#     role = models.CharField(max_length=50)