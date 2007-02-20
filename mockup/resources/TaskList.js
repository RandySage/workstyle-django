function updateStatus(targetTaskId, updateStatusId) {
	ajaxUpdateStatus(targetTaskId, updateStatusId, handleUpdateStatusResult);
}
function handleUpdateStatusResult(result, request) {
	var iconId = 'statusIcon-' + request.taskId;
	$(iconId).className = 'status' + result.task.status + '-icon';
	
	var updateDateId = 'updateDate-' + request.taskId;
	$(updateDateId).innerHTML = result.task.updateDate;
}
function updatePriority(taskId, priority) {
	ajaxUpdatePriority(taskId, priority, handleUpdatePriorityResult);
}
function handleUpdatePriorityResult(result, request) {
	updatePriorityIcon('taskPriority-'+request.taskId, result.task.priority);
	$('taskOriginalPriority-'+request.taskId).value = result.task.priority;
	
	var updateDateId = 'updateDate-' + request.taskId;
	$(updateDateId).innerHTML = result.task.updateDate;
}
function deleteTask(targetTaskId, elementId) {
	ajaxDeleteTask(targetTaskId, elementId, handleDeleteTaskResult);
}
function handleDeleteTaskResult(result, request) {
	Element.remove(request.element);
}
