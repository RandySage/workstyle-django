from django.db import models
from WorkStyle.settings import WORKSTYLE_JUNK_DIR

class TagType(models.Model) :
    name = models.CharField(_('Name'), maxlength=20, blank=False, unique=True)
    css  = models.CharField(_('css or image base name'), maxlength=50, blank=False)

    def __str__(self) :
        return self.name

    class Meta:
        ordering = ('name',)

    class Admin:
        pass

class Status(models.Model) :
    name = models.CharField(_('Name'), maxlength=20, blank=False, unique=True)
    css  = models.CharField(_('css or image base name'), maxlength=50, blank=False)

    def __str__(self) :
        return self.name

    class Meta:
        ordering = ('name',)

    class Admin:
        pass

class Task(models.Model):
    task = models.TextField(_('Task'), db_index=True, blank=False)
    create_date = models.DateTimeField(_('Create Date'), auto_now_add=True)
    update_date = models.DateTimeField(_('Update Date'))
    tag_searchable = models.CharField(_('Tag'), maxlength=800, db_index=True, blank=True)
    estimate = models.FloatField(_('Estimate'), max_digits=3, default=0, decimal_places=1, null=True)
    status = models.ForeignKey(Status)

    class Meta:
        ordering = ['-update_date']

    def get_absolute_url(self):
        return "/Task/%i/" % self.id

    def save(self):
        tag_type = TagType.objects.all().order_by('id')[:1]
        tag_list = tag_searchable.split(' ')
        for tag in tag_list :
            Tag.objects.get_or_create(name=tag[:50], defaults={'visible': True, 'tag_type_id': tag_type.id})
        super(Task, self).save()

class Tag(models.Model):
    name = models.CharField(_('Tag Name'), maxlength=50)
    visible = models.BooleanField(_('Visible'), default=True)
    tag_type = models.ForeignKey(TagType)
    class Meta:
        ordering = ['tag_type', 'id']
    def __repr__(self):
        return self.name

    def delete(self):
        taskList = Task.objects.filter(tag_searchable__contains=self.name)
        for task in taskList:
            task.tag_searchable = task.tag_searchable.replace(self.name, "").replace("  ", " ").strip()
            task.save()
        super(Tag, self).delete()


class Comment(models.Model):
    task        = models.ForeignKey(Task)
    comment    = models.TextField(_('Comment'), blank=False)
    commentator = models.CharField(_('Commentator'), maxlength=50, blank=False)
    create_date = models.DateTimeField(_('Comment Date'), auto_now_add=True)

class Attachment(models.Model):
    task        = models.ForeignKey(Task)
    file        = models.FileField(upload_to=WORKSTYLE_JUNK_DIR)
    create_date = models.DateTimeField(auto_now_add=True)
