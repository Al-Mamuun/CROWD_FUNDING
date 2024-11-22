from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    goalAmount = models.FloatField()
    collectedAmount = models.FloatField(default=0.0)
    createdAt = models.DateField(auto_now_add=True)
    startDate = models.DateField()
    endDate = models.DateField()
    status = models.CharField(max_length=50)
    image = models.ImageField(upload_to='Projectlist', default='Projectlist/donation.jpeg')  # Ensure this file exists in your media directory

    def __str__(self):
        return self.title

    
class Donation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation of ${self.amount} on {self.created_at}"


class Rating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    stars = models.IntegerField()
    ratingDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Rating of {self.stars} stars for {self.project.title}"


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    content = models.TextField()
    commentDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.project.title} - {self.content[:30]}"


class Report(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reportReason = models.TextField()
    reportDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.project.title} - {self.reportReason[:30]}"



class FeatureProject(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    goalAmount = models.FloatField(default=0.0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)  # Optional association
    createdAt = models.DateField(auto_now_add=True, blank=True, null=True)
    startDate = models.DateField(blank=True, null=True)
    endDate = models.DateField(blank=True, null=True)

    select_choice = (
        ('OnGoing', 'OnGoing'),
        ('Coming Soon', 'Coming Soon'),
    )
    status = models.CharField(max_length=50, choices=select_choice)

    def __str__(self):
        return self.title

