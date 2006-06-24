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
    task = models.TextField(_('Task'), db_index=True, blank=False)
    create_date = models.DateTimeField(_('Create Date')auto_now_add=True)
    update_date = models.DateTimeField(_('Update Date'))
    tag_searchable = models.CharField(_('Tag')maxlength=800, db_index=True, blank=True)
    estimate = models.FloatField(_('Estimate')max_digits=3, default=0, decimal_places=1, null=True)
    status = models.IntegerField(_('Status')maxlength=1, default=3, choices=TASK_STATUS_CHOICES, db_index=True)
    class Meta:
        ordering = ['-update_date']

    def get_absolute_url(self):
        return "/Task/%i/" % self.id

    def save(self):
        tagList = tag_searchable.split(' ')
        existTag = Tag.objects.filter(name__in=tagList).values('name')
        for exist in existTag :
            tagList.remove(exist['name'])
        for tag in tagList :
            t = new Tag(name=tag)
            t.save()
        super(Task, self).save()

class Tag(models.Model):
    name = models.CharField(maxlength=50)
    tag_type = models.IntegerField(maxlength=2, default=1, choices=TAG_TYPE_CHOICES)
    visible = models.BooleanField(default=True)
    class Meta:
        ordering = ['tag_type', 'id']
    def __repr__(self):
        return self.name

    def delete(self):
        taskList = Task.objects.filter(tag_searchable__contains=self.name)
        for task in taskList:
            task.tag_searchable = task.tag_searchable.replace(self.name, "")replace("  ", " ").strip()
            task.save()
        super(Tag, self).delete()


class Comment(models.Model):
    task        = models.ForeignKey(Task)
    comment    = models.TextField(blank=False)
    commentator = models.CharField(maxlength=50, blank=False)
    create_date = models.DateTimeField(auto_now_add=True)

class Attachment(models.Model):
    task        = models.ForeignKey(Task)
    name        = models.CharField(maxlength=200)
    file        = models.FileField(upload_to=WORKSTYLE_JUNK_DIR)
    size        = models.IntegerField(maxlength=12)
    create_date = models.DateTimeField(auto_now_add=True)

class TaskRelation(models.Model):
    task_a = models.ForeignKey(Task)
    task_b = models.ForeignKey(Task)
