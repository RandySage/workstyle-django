var newTagTemplate = "ajp/TagListNewTag.html";
var tagTypeListTemplate = "ajp/TagListTagTypeList.html";

var newTagTypeTemplate = "ajp/TagTypeListNewTagType.html";

var tagListTemplate = "ajp/TaskDetailTagList.html";
var tagSelecterTemplate = "ajp/TaskDetailTagSelecter.html";
var commentListTemplate = "ajp/TaskDetailCommentList.html";
var linkedTaskListTemplate = "ajp/TaskDetailLinkedTaskList.html";
var linkedTaskTagSelecterTemplate = "ajp/TaskDetailLinkedTaskTagSelecter.html";
/**
 * タスク詳細閲覧用通常リクエストを作成する
 */
function buildViewUrl(taskId) {
	var url = 'TaskDetail.html';
	url += '?' + $H({taskId:taskId}).toQueryString();
	return url;
}
/// REST /////////////////////////////////////////////////////////
/**
 * タスク削除用RESTリクエストを作成する
 */
function buildDeleteTaskRequest(targetTaskId) {
	var req = Class.create();
	req.url = 'xml/SimpleResult.xml';
	req.param = $H({taskId:targetTaskId}).toQueryString();
	req.method = 'POST';
	return req;
}
/**
 * タスク状態更新用RESTリクエストを作成する
 */
function buildUpdateStatusRequest(targetTaskId, updateStatusId) {
	var req = Class.create();
	req.url = 'xml/Task.xml';
	req.param = $H({taskId:targetTaskId, statusId:updateStatusId}).toQueryString();
	req.method = 'POST';
	return req;
}
/**
 * タスク優先度更新用RESTリクエストを作成する
 */
function buildUpdatePriorityRequest(taskId, priority) {
	var req = Class.create();
	req.url = 'xml/Task.xml';
	req.param = $H({taskId:taskId, priority:priority}).toQueryString();
	req.method = 'POST';
	return req;
}
/**
 * タスクのタグ編集用RESTリクエストを作成する
 */
function buildEditTagListRequest(targetTaskId, tagList) {
	var req = Class.create();
	req.url = 'xml/Task.xml';
	req.param = $H({taskId:targetTaskId, tagList:tagList}).toQueryString();
	req.method = 'POST';
	return req;
}
/**
 * タスク内容編集用RESTリクエストを作成する
 */
function buildEditContentsRequest(targetTaskId, contents) {
	var req = Class.create();
	req.url = 'xml/Task.xml';
	req.param = $H({taskId:targetTaskId, contents:contents}).toQueryString();
	req.method = 'POST';
	return req;
}
/**
 * ファイル削除用RESTリクエストを作成する
 */
function buildDeleteFileRequest(targetFileId) {
	var req = Class.create();
	req.url = 'xml/SimpleResult.xml';
	req.param = $H({fileId:targetFileId}).toQueryString();
	req.method = 'POST';
	return req;
}
/**
 * コメント追加用RESTリクエストを作成する
 */
function buildAddCommentRequest(targetTaskId, commentator, comment) {
	var req = Class.create();
	req.url = 'xml/Task.xml';
	req.param = $H({
		taskId:targetTaskId,
		commentator:commentator,
		comment:comment}).toQueryString();
	req.method = 'POST';
	return req;
}
/**
 * プロパティ編集用RESTリクエストを作成する
 */
function buildEditPropertyRequest(property) {
	var req = Class.create();
	req.url = 'xml/Task.xml';
	req.param = $H({
		taskId: property.taskId,
		estimatedManHour: property.estimatedManHour,
		deadEndDate: property.deadEndDate}).toQueryString();
	req.method = 'POST';
	return req;
}
/**
 * タスク関連リンク削除用RESTリクエストを作成する
 */
function buildUnlinkTaskRequest(fromTaskId, toTaskId) {
	var req = Class.create();
	req.url = 'xml/SimpleResult.xml';
	req.param = $H({
		fromTaskId:fromTaskId,
		toTaskId: toTaskId}).toQueryString();
	req.method = 'POST';
	return req;
}
/**
 * 関連タスクリンク用RESTリクエストを作成する
 */
function buildLinkTaskRequest(fromTaskId, toTaskId) {
	var req = Class.create();
	req.url = 'xml/SimpleResult.xml';
	req.param = $H({
		fromTaskId:fromTaskId,
		toTaskId: toTaskId}).toQueryString();
	req.method = 'POST';
	return req;
}
/**
 * 関連タスク追加用RESTリクエストを作成する
 */
function buildAddLinkedTaskRequest(parentTaskId, contents, tagList) {
	var req = Class.create();
	req.url = 'xml/Task.xml';
	req.param = $H({
		parentTaskId:parentTaskId,
		contents:contents,
		tagList:tagList}).toQueryString();
	req.method = 'POST';
	return req;
}
/**
 * タグ状態更新用RESTリクエストを作成する
 */
function buildToggleTagActivityRequest(tagId) {
	var req = Class.create();
	req.url = 'xml/Tag.xml';
	req.param = $H({tagId:tagId}).toQueryString();
	req.method = 'POST';
	return req;
}
/**
 * タグ削除用RESTリクエストを作成する
 */
function buildDeleteTagRequest(tagId) {
	var req = Class.create();
	req.url = 'xml/SimpleResult.xml';
	req.param = $H({tagId:tagId}).toQueryString();
	req.method = 'POST';
	return req;
}
/**
 * タグの種別変更用RESTリクエストを作成する
 */
function buildChangeTypeOfTagRequest(tagId, tagTypeId) {
	var req = Class.create();
	req.url = 'xml/Tag.xml';
	req.param = $H({tagId:tagId, tagTypeId:tagTypeId}).toQueryString();
	req.method = 'POST';
	return req;
}
function buildDeleteTagTypeRequest(tagTypeId) {
	var req = Class.create();
	req.url = 'xml/SimpleResult.xml';
	req.param = $H({tagTypeId:tagTypeId}).toQueryString();
	req.method = 'POST';
	return req;
}
function buildChangeTagTypeStyleRequest(tagTypeId, styleClass) {
	var req = Class.create();
	req.url = 'xml/TagType.xml';
	req.param = $H({tagTypeId:tagTypeId, styleClass:styleClass}).toQueryString();
	req.method = 'POST';
	return req;
}
function buildEditTagType(tagTypeId, name, sortOrder) {
	var req = Class.create();
	req.url = 'xml/TagType.xml';
	req.param = $H({tagTypeId:tagTypeId, name:name, sortOrder:sortOrder}).toQueryString();
	req.method = 'POST';
	return req;
}
function buildAddTagType(name, sortOrder) {
	var req = Class.create();
	req.url = 'xml/TagType.xml';
	req.param = $H({name:name, sortOrder:sortOrder}).toQueryString();
	req.method = 'POST';
	return req;
}
function buildAddTag(name) {
	var req = Class.create();
	req.url = 'xml/Tag.xml';
	req.param = $H({name:name}).toQueryString();
	req.method = 'POST';
	return req;
}