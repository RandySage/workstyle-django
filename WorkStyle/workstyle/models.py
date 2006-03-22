from django.db import models
from WorkStyle.settings import WORKSTYLE_JUNK_DIR, TAG_TYPE_1, TAG_TYPE_2, TAG_TYPE_3, TAG_TYPE_4, TAG_TYPE_5, TAG_TYPE_6, TAG_TYPE_7, TAG_TYPE_8, TAG_TYPE_9, TAG_TYPE_10

# Create your models here.
TASK_STATUS = (
    (1, _('EXECUTING'),'on_going'),
    (2, _('ASAP'),'rapid'),
    (3, _('LATER'),'normal'),
    (4, _('PENDING'),'review'),
    (5, _('APPROVING'),'pending'),
    (6, _('DONE'),'finish'),
)

TASK_STATUS_CHOICES = (
    (1, _('EXECUTING')),
    (2, _('ASAP')),
    (3, _('LATER')),
    (4, _('PENDING')),
    (5, _('APPROVING')),
    (6, _('DONE')),
)

TAG_TYPE_CHOICES = (
    (1, TAG_TYPE_1),
    (2, TAG_TYPE_2),
    (3, TAG_TYPE_3),
    (4, TAG_TYPE_4),
    (5, TAG_TYPE_5),
    (6, TAG_TYPE_6),
    (7, TAG_TYPE_7),
    (8, TAG_TYPE_8),
    (9, TAG_TYPE_9),
    (10, TAG_TYPE_10),
)

class Task(models.Model):
    task = models.TextField(db_index=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField()
    tag_searchable = models.CharField(maxlength=800, db_index=True, null=True)
    estimate = models.FloatField(max_digits=3, default=0, decimal_places=1, null=True)
    status = models.IntegerField(maxlength=1, default=3, choices=TASK_STATUS_CHOICES, db_index=True)
    class Meta:
        ordering = ['-update_date']

class Tag(models.Model):
    name = models.CharField(maxlength=50)
    tag_type = models.IntegerField(maxlength=2, default=1, choices=TAG_TYPE_CHOICES)
    visible = models.BooleanField(default=True)
    class Meta:
        ordering = ['tag_type', 'id']
    def __repr__(self):
        return self.name

class TagList(models.Model):
    task = models.ForeignKey(Task)
    tag  = models.ForeignKey(Tag)

class Comment(models.Model):
    comment    = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    commentator = models.CharField(maxlength=50, null=True)
    task        = models.ForeignKey(Task)

class Attachment(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    name        = models.CharField(maxlength=200)
    file        = models.FileField(upload_to=WORKSTYLE_JUNK_DIR)
    size        = models.IntegerField(maxlength=12)
    task        = models.ForeignKey(Task)


