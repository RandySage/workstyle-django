var ajp;
function init() {
    ajp = new AjaxPages();
    ajp.addPage(tagListTemplate);
    ajp.addPage(tagSelecterTemplate);
    ajp.addPage(commentListTemplate);
    ajp.addPage(linkedTaskListTemplate);
    ajp.addPage(linkedTaskTagSelecterTemplate);
    ajp.loadPages();
}
/**
 * Refresh task data
 */
function update(varTask, varTagMasterList) {
	$('deadEndDateView').innerHTML = normalize(varTask.deadEndDate);
	$('estimatedManHourView').innerHTML = normalize(varTask.estimatedManHour);
	$('createDate').innerHTML = normalize(varTask.createDate);
	$('updateDate').innerHTML = normalize(varTask.updateDate);
	$('contents').value = normalize(varTask.contents);
	$('contents').defaultValue = normalize(varTask.contents);
	$('estimatedManHour').value = normalize(varTask.estimatedManHour);
	$('estimatedManHour').defaultValue = normalize(varTask.estimatedManHour);
	$('deadEndDate').value = normalize(varTask.deadEndDate);
	$('deadEndDate').defaultValue = normalize(varTask.deadEndDate);
	$('taskOriginalPriority').value = normalize(varTask.priority);
	updatePriorityIcon('taskPriority', normalize(varTask.priority));
	if (varTagMasterList) {
	    $('tagSelecter').innerHTML = ajp.process(tagSelecterTemplate, {task:varTask, tagMasterList:varTagMasterList});
	    updateLinkedTask(varTagMasterList);
	}
}

function updateLinkedTask(varTagMasterList) {
    $('linkedTaskTagSelecter').innerHTML = ajp.process(linkedTaskTagSelecterTemplate, {tagMasterList:varTagMasterList});
}
/**
 * Change task's status.
 */
function updateStatus(targetTaskId, updateStatusId) {
	ajaxUpdateStatus(targetTaskId, updateStatusId, handleUpdateStatusResult);
}
function handleUpdateStatusResult(result, request) {
	$('statusIcon').className = 'status' + result.task.status + '-iconLarge';
	update(result.task);
}
/**
 * Change task's priority
 */
function updatePriority(taskId, priority) {
	ajaxUpdatePriority(taskId, priority, handleUpdatePriorityResult);
}
function handleUpdatePriorityResult(result, request) {
	update(result.task);
}
/**
 * Open task's tag editor.
 */
function openTagListForm() {
	Element.hide('taskInfo');
	Element.hide('tagListViewContainer');
	Element.hide('tagListLink');
	Element.show('tagListFormContainer');
	$('tagList').focus();
}
function closeTagListForm() {
	Element.show('taskInfo');
	Element.show('tagListViewContainer');
	Element.show('tagListLink');
	Element.hide('tagListFormContainer');
}
function editTagList() {
	var taskId = $F('tagListTaskId');
	var tagList = $F('tagList');
	ajaxEditTagList(taskId, tagList, handleEditTagResult);
	closeTagListForm();
	return false;
}
function handleEditTagResult(result, request) {
    $('tagListView').innerHTML = ajp.process(tagListTemplate, {task:result.task});
	var tmpTags = $AX(result.task.tagList.tag);
	var tagList = tmpTags.collect(
				function (value, index) {
					return value.name.formatWSTag();
				});
	$('tagList').value = tagList.join('');
	$('tagList').defaultValue = tagList.join('');
	
	update(result.task, result.tagMasterList);
}
/**
 * Open task contents editor
 */
function openEditContentsForm() {
	Element.hide('taskInfo');
	Element.hide('contentsView');
	Element.hide('editContentsLink');
	Element.show('editContentsForm');
	$('contents').focus();
}
function closeEditContentsForm() {
	Element.show('taskInfo');
	Element.hide('editContentsForm');
	Element.show('contentsView');
	Element.show('editContentsLink');
}
function editContents() {
	ajaxEditContents($F('contentsTaskId'), $F('contents'), handleEditContentsResult);
	return false;
}
function handleEditContentsResult(result, request) {
	$('contentsView').innerHTML = result.task.contents.formatSimpleHTML();
	
	closeEditContentsForm();
	update(result.task);
}
function deleteFile(fileId, elementId) {
	ajaxDeleteFile(fileId, elementId, handleDeleteFileResult);
}
function handleDeleteFileResult(result, request) {
	Element.remove(request.element);
}
function openUploadFileForm() {
	Element.hide('uploadFileLink');
	Element.show('uploadFileForm');
}
function closeUploadFileForm() {
	Element.show('uploadFileLink');
	Element.hide('uploadFileForm');
}
/**
 * Open comment editor.
 */
function openCommentForm() {
	Element.hide('addCommentLink');
	Element.show('CommentForm');
	$('commentator').value = '';
	$('comment').value = '';
	$('comment').focus();
}
function closeCommentForm() {
	Element.show('addCommentLink');
	Element.hide('CommentForm');
}
function addComment() {
	ajaxAddComment($F('commentTaskId'), $F('commentator'), $F('comment'), handleAddCommentResult);
	return false;
}
function handleAddCommentResult(result, request) {
	Element.show('commentList');
    $('commentList').innerHTML = ajp.process(commentListTemplate, {task:result.task});
	update(result.task);
	
	closeCommentForm();
}
/**
 * Open property editor.
 */
function openPropertyForm() {
	Element.hide('deadEndDateContainer');
	Element.hide('estimatedManHourContainer');
	Element.hide('propertyLink');
	Element.show('deadEndDateForm');
	Element.show('estimatedManHourForm');
	Element.show('propertyFormButton');
	$('estimatedManHour').focus();
	$('estimatedManHour').select();
}
function closePropertyForm() {
	Element.show('deadEndDateContainer');
	Element.show('estimatedManHourContainer');
	Element.show('propertyLink');
	Element.hide('deadEndDateForm');
	Element.hide('estimatedManHourForm');
	Element.hide('propertyFormButton');
}
function editProperty() {
	ajaxEditProperty(
		{
			taskId: $F('estimatedManHourTaskId'),
			estimatedManHour: $F('estimatedManHour'),
			deadEndDate: $F('deadEndDate')
		 } , handlePropertyResult);
	return false;
}
function handlePropertyResult(result, request) {
	update(result.task);
	
	closePropertyForm();
}
/// Linked Task /////////////////////////////////////////////////
function updateLinkedTaskStatus(targetTaskId, updateStatusId) {
	ajaxUpdateStatus(targetTaskId, updateStatusId, handleUpdateLinkedTaskStatusResult);
}
function handleUpdateLinkedTaskStatusResult(result, request) {
	var elementId = 'linkedTaskStatusIcon-' + request.taskId;
	$(elementId).className = 'status' + result.task.status + '-icon';
	$('linkedTaskUpdateDate-' + request.taskId).innerHTML = result.task.updateDate;
}
/**
 * Change task's priority
 */
function updateLinkedTaskPriority(taskId, priority) {
	ajaxUpdatePriority(taskId, priority, handleUpdateLinkedTaskPriorityResult);
}
function handleUpdateLinkedTaskPriorityResult(result, request) {
	updatePriorityIcon('linkedTaskPriority-'+request.taskId, result.task.priority);
	$('linkedTaskOriginalPriority-'+request.taskId).value = result.task.priority;
	
	$('linkedTaskUpdateDate-' + request.taskId).innerHTML = result.task.updateDate;
}
function deleteLinkedTask(targetTaskId, elementId) {
	ajaxDeleteTask(targetTaskId, elementId, handleDeleteLinkedTaskResult);
}
function handleDeleteLinkedTaskResult(result, request) {
	Element.remove(request.element);
}
/**
 * Unlink task. This doesn't delete task, just unlink.
 */
function unlinkTask(fromTaskId, toTaskId, elementId) {
	ajaxUnlinkTask(fromTaskId, toTaskId, elementId, handleUnlinkTaskResult);
}
function handleUnlinkTaskResult(result, request) {
	Element.remove(request.element);
}
/**
 * open new linked task editor.
 */
function openLinkedTaskForm() {
	Element.hide('addLinkedTaskLink');
	Element.show('LinkedTaskForm');
	$('LinkedTaskForm').reset();
	$('linkedTaskTagList').value = $('tagList').value;
	$('linkedTaskContents').focus();
}
function closeLinkedTaskForm() {
	Element.show('addLinkedTaskLink');
	Element.hide('LinkedTaskForm');
}
function addLinkedTask() {
	ajaxAddLinkedTask(
		$F('parentTaskId'), 
		$F('linkedTaskContents'), 
		$F('linkedTaskTagList'), 
		handleAddLinkedTaskResult);
	return false;
}
function handleAddLinkedTaskResult(result, request) {
	var row = ajp.process(linkedTaskListTemplate, {task:result.task, parentTaskId:request.parentTaskId});
	new Insertion.Bottom($('linkedTaskList'), row);
	closeLinkedTaskForm();
	updateLinkedTask(result.tagMasterList);
	Element.show('linkedTaskList');
}
