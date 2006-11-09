"""
Copyright (c) 2006, www.everes.net
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, 
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, 
      this list of conditions and the following disclaimer in the documentation 
      and/or other materials provided with the distribution.
    * Neither the name of the everes nor the names of its contributors may be 
      used to endorse or promote products derived from this software without 
      specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF 
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import re, string
from django import forms
from django.core import validators
from WorkStyle.workstyle.models import TAG_TYPE_CHOICES, TASK_STATUS

alnum_re = re.compile(r'^[\w\.]+$')

class TaskManipulator(forms.Manipulator):
    def __init__(self):
        self.fields = (
            forms.LargeTextField(field_name="task", is_required=True),
            forms.LargeTextField(field_name="task_tag", maxlength=800, is_required=False, validator_list=[self.isValidTagName]),
            forms.FileUploadField(field_name="attachFile", is_required=False, validator_list=[self.isValidFileName]),
            forms.LargeTextField(field_name="comment", is_required=False),
            forms.TextField(field_name="commentator", maxlength=50, is_required=False),
            forms.FloatField(field_name="estimate", max_digits=3, decimal_places=1, is_required=False),
            forms.SelectField(field_name="status", choices=TASK_STATUS, is_required=True),
        )
    
    def isValidFileName(self, field_data, all_data):
        filename = field_data['filename']
        print "FILE_NAME:" + filename
        if not alnum_re.search(filename) :
            raise validators.ValidationError(_("Attach filename must contain only letters, numbers and underscores."))

    def isValidTagName(self, field_data, all_data):
        task_tag_list = string.split(field_data, " ")
        for task_tag in task_tag_list :
            task_tag = string.strip(task_tag)
            if len(task_tag) > 49 :
                raise validators.ValidationError(_("Tag's name is must be less than 50 characters."))

