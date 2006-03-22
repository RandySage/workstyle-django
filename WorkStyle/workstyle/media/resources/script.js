function containsTag(tag, tagListValue) {
	tag = "["+tag+"]";
	return (tagListValue.indexOf(tag) >= 0);
}
function setRollOver(imgId, src) {
    var rollover = new RollOverImage(document.getElementById(imgId));
    rollover.setMouseOverImage(src);
}
function setRollOverLink(linkId, imgId, src) {
    var rollover = 
    	new RollOverLink(document.getElementById(linkId), document.getElementById(imgId));
    rollover.setMouseOverImage(src);
}
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
}
