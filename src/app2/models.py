from django.db import models


class CSVFile(models.Model):
    name = models.CharField(max_length=100)
    csvFile = models.FileField(upload_to='app1/csvs')

    def __str__(self):
        return self.name


class Participant(models.Model):
    name = models.CharField(max_length=10)
    role = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    orgSize = models.IntegerField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    group = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Evidence(models.Model):
    text = models.CharField(max_length=200)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.text