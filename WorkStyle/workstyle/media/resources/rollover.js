/**
 * コンストラクタ
 */
function RollOverImage(img){
	this.img = img;
	this.originalPath = this.img.src;
}

/**
 * マウスオーバー・マウスアウト時処理
 */
RollOverImage.prototype.setMouseOverImage = function( filepath ){
	// 画像のロード
	this.mouseoverImg = new Image();
	this.mouseoverImg.src = filepath;
	var originalPath = this.originalPath;

	this.img.onmouseover = RollOverImage.createHandler(this.img, filepath);
	this.img.onmouseout = RollOverImage.createHandler(this.img, this.originalPath);
}

/**
 * マウスダウン・マウスアップ時処理
 */
RollOverImage.prototype.setMouseDownImage = function( filepath ){
	this.mousedownImg = new Image();
	this.mousedownImg.src = filepath;	//画像の先読み
	
	this.img.onmousedown = RollOverImage.createHandler(this.img, filepath);
	this.img.onmouseup = RollOverImage.createHandler(this.img, this.originalPath);
}

/**
 * 画像入れ替えを実行するクロージャ作成
 */
RollOverImage.createHandler = function(img, path){
	return function(){
		img.src = path;
	}
}
