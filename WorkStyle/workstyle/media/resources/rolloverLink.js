/**
 * コンストラクタ
 */
function RollOverLink(link, img){
	this.link = link;
	this.img = img;
	this.originalPath = this.img.src;
}

/**
 * マウスオーバー・マウスアウト時処理
 */
RollOverLink.prototype.setMouseOverImage = function( filepath ){
	// 画像のロード
	this.mouseoverImg = new Image();
	this.mouseoverImg.src = filepath;
	var originalPath = this.originalPath;

	this.link.onmouseover = RollOverLink.createHandler(this.img, filepath);
	this.link.onmouseout = RollOverLink.createHandler(this.img, this.originalPath);
}

/**
 * マウスダウン・マウスアップ時処理
 */
RollOverLink.prototype.setMouseDownImage = function( filepath ){
	this.mousedownImg = new Image();
	this.mousedownImg.src = filepath;	//画像の先読み
	
	this.img.onmousedown = RollOverLink.createHandler(this.img, filepath);
	this.img.onmouseup = RollOverLink.createHandler(this.img, this.originalPath);
}

/**
 * 画像入れ替えを実行するクロージャ作成
 */
RollOverLink.createHandler = function(img, path){
	return function(){
		img.src = path;
	}
}
