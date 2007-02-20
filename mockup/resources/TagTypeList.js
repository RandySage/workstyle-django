var tagTypeStyles = ['tag1','tag2','tag3','tag4','tag5','tag6','tag7','tag8','tag9','tag10'];
var ajp;
function init() {
    ajp = new AjaxPages();
    ajp.addPage(newTagTypeTemplate);
    ajp.loadPages();
}
function deleteTagType(tagTypeId, elementId) {
	ajaxDeleteTagType(tagTypeId, elementId, handleDeleteTagTypeResult);
}
function handleDeleteTagTypeResult(result, request) {
	Element.remove(request.element);
}
/**
 * Tag type STYLE
 */
function update(tagTypeId, result) {
	var elementTagType = 'tagTypeStyle-' + tagTypeId;
	$(elementTagType).className = result.tagType.styleClass;
	
	var elementName = $('nameView-' + tagTypeId);
//	var elementOrder = $('orderView-' + tagTypeId);
	var nameForm = $('name-' + tagTypeId);
//	var orderForm = $('order-' + tagTypeId);
	
	elementName.innerHTML = result.tagType.name;
//	elementOrder.innerHTML = result.tagType.sortOrder;
	nameForm.value = result.tagType.name;
	nameForm.defaultValue = result.tagType.name;
//	orderForm.value = result.tagType.sortOrder;
//	orderForm.defaultValue = result.tagType.sortOrder;

	updateOrder(result.sortOrderList);
}
function updateOrder(sortOrderList) {
	var sortTagTypes = $AX(sortOrderList.tagType);
	for (var i=0; i<sortTagTypes.length; i++) {
		var order = $('orderView-' + sortTagTypes[i].tagTypeId);
		var orderForm = $('order-' + sortTagTypes[i].tagTypeId);
		if (order && orderForm) {
			order.innerHTML = sortTagTypes[i].sortOrder;
			orderForm.value = sortTagTypes[i].sortOrder;
			orderForm.defaultValue = sortTagTypes[i].sortOrder;
		}
	}
}
function openChangeTagTypeStyleForm(tagTypeId) {
	var elementLink = 'tagTypeStyleLink-' + tagTypeId;
	var elementForm = 'tagTypeStyleForm-' + tagTypeId;
	Element.hide(elementLink);
	Element.show(elementForm);
}
function closeChangeTagTypeStyleForm(tagTypeId) {
	var elementLink = 'tagTypeStyleLink-' + tagTypeId;
	var elementForm = 'tagTypeStyleForm-' + tagTypeId;
	Element.show(elementLink);
	Element.hide(elementForm);
}
function changeTagTypeStyle(tagTypeId, styleClass) {
	ajaxChangeTagTypeStyle(tagTypeId, styleClass, handleChangeTagTypeStyle);
}
function handleChangeTagTypeStyle(result, request) {
	update(request.tagTypeId, result);
	closeChangeTagTypeStyleForm(request.tagTypeId);
}

/**
 * Tag type EDIT
 */
function _openEditForm(tagTypeId) {
	var elementLink = 'editLink-' + tagTypeId;
	var elementName = 'nameView-' + tagTypeId;
	var elementOrder = 'orderView-' + tagTypeId;
	var elementButton = 'editButton-' + tagTypeId;
	var elementNameForm = 'editName-' + tagTypeId;
	var elementOrderForm = 'editOrder-' + tagTypeId;
	Element.hide(elementLink);
	Element.hide(elementName);
	Element.hide(elementOrder);
	Element.show(elementButton);
	Element.show(elementNameForm);
	Element.show(elementOrderForm);
}
function openEditForm(tagTypeId) {
	_openEditForm(tagTypeId);
	var nameForm = 'name-' + tagTypeId;
	$(nameForm).select();
	$(nameForm).focus();
}
function openEditFormOrder(tagTypeId) {
	_openEditForm(tagTypeId);
	var orderForm = 'order-' + tagTypeId;
	$(orderForm).select();
	$(orderForm).focus();
}
function closeEditForm(tagTypeId) {
	var elementLink = 'editLink-' + tagTypeId;
	var elementName = 'nameView-' + tagTypeId;
	var elementOrder = 'orderView-' + tagTypeId;
	var elementButton = 'editButton-' + tagTypeId;
	var elementNameForm = 'editName-' + tagTypeId;
	var elementOrderForm = 'editOrder-' + tagTypeId;
	Element.show(elementLink);
	Element.show(elementName);
	Element.show(elementOrder);
	Element.hide(elementButton);
	Element.hide(elementNameForm);
	Element.hide(elementOrderForm);
}
function setTarget(targetId) {
	$('tagTypeId').value= targetId;
}
function editTagType() {
	return _editTagType($F('tagTypeId'));
}
function _editTagType(tagTypeId) {
	var _name = $F('name-' + tagTypeId);
	var _order = $F('order-' + tagTypeId);
	ajaxEditTagType(tagTypeId, _name, _order, handleEditTagType);
	return false;
}
function handleEditTagType(result, request) {
	update(request.tagTypeId, result);
	closeEditForm(request.tagTypeId);
}

/**
 * New tag type
 */
function openTagTypeForm() {
	Element.hide('newLink');
	Element.show('TagTypeForm');
	
	$('name').focus();
}
function closeTagTypeForm() {
	Element.hide('TagTypeForm');
	Element.show('newLink');
}
function addTagType() {
	ajaxAddTagType($F('name'), $F('order'), handleAddTagType);
	return false;
}
function handleAddTagType(result, request) {
	var row = ajp.process(newTagTypeTemplate, {tagType:result.tagType, tagTypeStyles:tagTypeStyles});
	new Insertion.Bottom($('tagTypeList'), row);
	updateOrder(result.sortOrderList);
	closeTagTypeForm();
}
