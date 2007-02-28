var ajp;
function init() {
    ajp = new AjaxPages();
    ajp.addPage(newTagTemplate);
    ajp.addPage(tagTypeListTemplate);
    ajp.loadPages();
}
function toggleTagActivity(tagId, element) {
	ajaxToggleTagActivity(tagId, element, handleToggleTagActivityResult);
}
function handleToggleTagActivityResult(result, request) {
	if (result.tag.active.trim().toUpperCase() == 'TRUE') {
		$(request.element).className = 'active';
	} else {
		$(request.element).className = 'inactive';
	}
}
function deleteTag(tagId, elementId) {
	ajaxDeleteTag(tagId, elementId, handleDeleteTagResult);
}
function handleDeleteTagResult(result, request) {
	Element.remove(request.element);
}
function changeTypeOfTag(tagId, tagTypeId) {
	ajaxChangeTypeOfTag(tagId, tagTypeId, handleChangeTypeOfTag);
}
function handleChangeTypeOfTag(result, request) {
	var element = 'tagTypeList-' + request.tagId;
	$(element).innerHTML = ajp.process(tagTypeListTemplate, {tag:result.tag, tagTypes:tagTypes});
}
/**
 * New tag
 */
function openTagForm() {
	Element.hide('newLink');
	Element.show('TagForm');
	$('name').value = "";
	$('name').focus();
}
function closeTagForm() {
	Element.hide('TagForm');
	Element.show('newLink');
}
function addTag() {
	ajaxAddTag($F('name'), handleAddTag);
	return false;
}
function handleAddTag(result, request) {
	var row = ajp.process(newTagTemplate, {tag:result.tag, tagTypes:tagTypes});
	new Insertion.Bottom($('tagList'), row);
	closeTagForm();
}
