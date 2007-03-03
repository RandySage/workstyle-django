# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _ #_は辞めようという方向だけどさ


# Create your models here.

class Status(models.Model):
    status_id  = models.AutoField(primary_key=True)
    name       = models.CharField(_('Name'), maxlength=20)
    sort_order = models.IntegerField(_('Sort Order'), default=0)
    image      = models.CharField(_('Image Path'), maxlength=256)
    
    class Meta:
        verbose_name = _('Status')
  
class TagType(models.Model):
    tag_type_id  = models.AutoField(primary_key=True)
    name         = models.CharField(_('Name'), maxlength=20)
    style_class  = models.CharField(maxlength=10)
    sort_order   = models.IntegerField(_('Sort Order'), default=0)

    class Meta:
        verbose_name = _('Tag Type')
        ordering = ('sort_order',)


class Task(models.Model):
    task_id              = models.AutoField(primary_key=True)
    contents             = models.TextField(_('Contents'))
    estimated_man_hour   = models.FloatField(_('Estimate by man'), max_digits=5, decimal_places=2, default=0.0)
    tag_list             = models.CharField(maxlength=200, db_index=True)
    create_date          = models.DateTimeField(_('Create Date'), auto_now_add=True, db_index=True)
    update_date          = models.DateTimeField(_('Update Date'), auto_now=True, db_index=True)
    deadend_date          = models.DateTimeField(_('Limit Date'), db_index=True, null=True, blank=True)
    status               = models.ForeignKey(Status, verbose_name=_('Status'), default=7)
    related_task         = models.ManyToManyField('self', null=True, blank=True, verbose_name=_('Task'))
    priority             = models.IntegerField(_('priority'), default=3)
    
    def save(self):
        super(Task, self).save()
        for tag in self.tag_list.strip().replace('[', '').split(']'):
            #処理は冗長だけど…
            if tag:
                Tag.objects.get_or_create(name=tag.strip(), defaults={'active': True, 'tag_type_id': 1})
    
    def get_tag_list(self):
        return self.tag_list.strip().replace('[', '').split(']')
    
    class Meta:
         verbose_name=_('Task')
         
    def get_absolute_url(self):
        return '/task/%d/' % (self.task_id,)

class FileInfo(models.Model):
    file_id    = models.AutoField(primary_key=True)
    #ここはoriginalから変更したので注意
    file       = models.FileField(_('File'), upload_to=settings.FILE_STORE)
    task       = models.ForeignKey(Task, verbose_name=_('Task'))
    
    class Meta:
        verbose_name=_('File')

class TaskComment(models.Model):
    comment_id           = models.AutoField(primary_key=True)
    contents             = models.TextField(_('Comment'))
    commentator          = models.CharField(_('Commentator'), maxlength=50)
    update_date          = models.DateTimeField(auto_now=True)
    task                 = models.ForeignKey(Task)
    
    class Meta:
        verbose_name=_('Comment')

class TagManager(models.Manager):
    def get_query_set(self):
        return super(TagManager, self).get_query_set().filter(active=True)

class Tag(models.Model):
    tag_id           = models.AutoField(primary_key=True)
    name             = models.CharField(_('Name'), maxlength=50)
    active           = models.BooleanField(_('Active'), default=True)
    tag_type         = models.ForeignKey(TagType)

    objects = models.Manager()
    public_objects = TagManager()

    class Meta:
        verbose_name=_('Tag')
        #order_with_respect_to = 'tag_type'
