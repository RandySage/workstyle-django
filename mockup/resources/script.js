function normalize(value) {
	if (value == undefined) return "";
	return value;
}
var $AX = Array.fromEx = function(iterable) {
  if (!iterable) return [];
  if (iterable.toArray) {
    return iterable.toArray();
  } else if (!iterable.length) {
    var results = [];
    results.push(iterable);
    return results;
  } else {
    var results = [];
    for (var i = 0; i < iterable.length; i++)
      results.push(iterable[i]);
    return results;
  }
}

Object.extend(String.prototype, {
	formatSimpleHTML: function() {
		var tmp = this.escapeHTML();
		tmp = tmp.replace(/\n/g, '<br/>');
		tmp = tmp.replace(/(s?https?:\/\/[-_.!~*\'()a-zA-Z0-9;/?:@&=+$,%#]+)/g, '<a href="$1">$1</a>');
		return tmp;
	}, 
	formatWSTag: function() {
		return '[' + this + ']';
	},
	trim: function() {
		return this.replace(/^\s+|\s+$/g, "");
	}
});
function containsTag(tag, tagListValue) {
	tag = "["+tag+"]";
	return (tagListValue.indexOf(tag) >= 0);
}
function toggleAccordion(element, accordion) {
	Element.toggle(accordion);
	$(element).className = Element.visible(accordion) ? 'accordion-header-open' : 'accordion-header-close';
}
function activateForm(form) {
	$(form).className = 'active';
} 
/**
 * フォームのタグリスト欄に指定のタグを追加、またはタグリスト欄から指定のタグを削除する。
 */
function updateTagList(tagListId, tagId, tag, tagClass) {
	var tagLabel = document.getElementById(tagId);
	var tagList = document.getElementById(tagListId);
	if (containsTag(tag, tagList.value)) {
		tagList.value = tagList.value.replace("["+tag+"]", "");
		tagLabel.className = "";
	} else {
		tagList.value = tagList.value + "["+tag+"]";
		tagLabel.className = tagClass;
	}
	tagList.focus();
}

function processAjaxResult(callback) {
	return function(response, request) {
		var result = response.result;
		if (result && result.errors && result.errors.error.length > 0) {
			var error = response.result.errors.error.toString();
			alert(error);
			return;
		}
		callback(result, request);
	}
}

function processAjax(req, callback, result) {
	var xml = new JKL.ParseXML(req.url, req.param, req.method);
	xml.async(processAjaxResult(callback), result);
	xml.parse();
}

function ajaxDeleteTask(targetTaskId, elementId, callback) {
	if (!confirm('タスクを削除します。')) {
		return;
	}
	var req = buildDeleteTaskRequest(targetTaskId);
	processAjax(req, callback, {taskId:targetTaskId, element:elementId});
}
function ajaxUpdateStatus(targetTaskId, updateStatusId, callback) {
	var req = buildUpdateStatusRequest(targetTaskId, updateStatusId);
	processAjax(req, callback, {taskId:targetTaskId});
}
function ajaxUpdatePriority(taskId, priority, callback) {
	var req = buildUpdatePriorityRequest(taskId, priority);
	processAjax(req, callback, {taskId:taskId});
}
function ajaxEditTagList(targetTaskId, tagList, callback) {
	var req = buildEditTagListRequest(targetTaskId, tagList);
	processAjax(req, callback, {taskId:targetTaskId});
}
function ajaxEditContents(targetTaskId, contents, callback) {
	var req = buildEditContentsRequest(targetTaskId, contents);
	processAjax(req, callback, {taskId:targetTaskId});
}
function ajaxDeleteFile(fileId, elementId, callback) {
	if (!confirm('ファイルを削除します。')) {
		return;
	}
	var req = buildDeleteFileRequest(fileId);
	processAjax(req, callback, {fileId:fileId, element:elementId});
}
function ajaxAddComment(targetTaskId, commentator, comment, callback) {
	var req = buildAddCommentRequest(targetTaskId, commentator, comment);
	processAjax(req, callback, {});
}
function ajaxEditProperty(property, callback) {
	var req = buildEditPropertyRequest(property);
	processAjax(req, callback, {});
}
function ajaxUnlinkTask(fromTaskId, toTaskId, elementId, callback) {
	if (!confirm('タスクへのリンクを削除します。')) {
		return;
	}
	var req = buildUnlinkTaskRequest(fromTaskId, toTaskId);
	processAjax(req, callback, {fromTaskId:fromTaskId, toTaskId:toTaskId, element:elementId});
}
function ajaxLinkTask(fromTaskId, toTaskId, elementId, callback) {
	var req = buildLinkTaskRequest(fromTaskId, toTaskId);
	processAjax(req, callback, {fromTaskId:fromTaskId, toTaskId:toTaskId, element:elementId});
}
function ajaxAddLinkedTask(parentTaskId, contents, tagList, callback) {
	var req = buildAddLinkedTaskRequest(parentTaskId, contents, tagList);
	processAjax(req, callback, {parentTaskId:parentTaskId});
}
function ajaxToggleTagActivity(tagId, element, callback) {
	var req = buildToggleTagActivityRequest(tagId);
	processAjax(req, callback, {element:element});
}
function ajaxDeleteTag(tagId, elementId, callback) {
	if (!confirm('タグを削除します。既存のタスクからもタグが削除されます。')) {
		return;
	}
	var req = buildDeleteTagRequest(tagId);
	processAjax(req, callback, {element:elementId});
}
function ajaxChangeTypeOfTag(tagId, tagTypeId, callback) {
	var req = buildChangeTypeOfTagRequest(tagId, tagTypeId);
	processAjax(req, callback, {tagId:tagId});
}
function ajaxDeleteTagType(tagTypeId, elementId, callback) {
	if (!confirm('タグ種別を削除します。既存のタグはデフォルト状態に戻ります。')) {
		return;
	}
	var req = buildDeleteTagTypeRequest(tagTypeId);
	processAjax(req, callback, {element:elementId});
}
function ajaxChangeTagTypeStyle(tagTypeId, styleClass, callback) {
	var req = buildChangeTagTypeStyleRequest(tagTypeId, styleClass);
	processAjax(req, callback, {tagTypeId:tagTypeId});
}
function ajaxEditTagType(tagTypeId, name, sortOrder, callback) {
	var req = buildEditTagType(tagTypeId, name, sortOrder);
	processAjax(req, callback, {tagTypeId:tagTypeId});
}
function ajaxAddTagType(name, sortOrder, callback) {
	var req = buildAddTagType(name, sortOrder);
	processAjax(req, callback, {});
}
function ajaxAddTag(name, callback) {
	var req = buildAddTag(name);
	processAjax(req, callback, {});
}
/** 優先度 *******************************/
function updatePriorityIcon(elementId, newPriority) {
	Element.classNames(elementId).set('priority'+newPriority);
}
/**************************************/


