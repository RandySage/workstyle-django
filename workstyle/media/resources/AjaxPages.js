/**
 * Ajax Pages v0.51
 *
 * This software is licensed under the MIT License. 
 *
 * The MIT License
 * 
 * Copyright (c) 2005 Gustavo Ribeiro Amigo
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy of 
 * this software and associated documentation files (the "Software"), to deal in 
 * the Software without restriction, including without limitation the rights to use, 
 * copy, modify, merge, publish, distribute, sublicense, and/or sell copies of 
 * the Software, and to permit persons to whom the Software is furnished to do so, 
 * subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all 
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
 * CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
 * OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

/**  
 * Class responsable for processing Ajax Pages.
 * @constructor
 * @author Gustavo Amigo
 */
var AjaxPages = function() {
	this.onload = function() {};
	this.onerror = function() {};
	this.loader = new AjaxPagesLoader();
	if ( AjaxPages._cacheProcessor == undefined ) {
		AjaxPages._cacheProcessor = new Object();
	}
}

/**
 * Add a page template to be loaded
 * @param url The file to be loaded
 * @returns The template loaded
 */
AjaxPages.prototype.addPage = function ( url ) {
	this.loader.addPage (url);
}

/**
 * Loads pages template from files
 * @param url The file to be loaded
 * @returns The template loaded
 */
AjaxPages.prototype.loadPages = function () {
	this.loader.onload = this.onload;
	this.loader.onerror = this.onerror;
	this.loader.load();
}

/**
 * Get the page source
 * @param url The file to be loaded
 * @returns The template loaded
 */
AjaxPages.prototype.getPageSource = function (page) {
	return AjaxPagesLoader.getPreLoaded(page);
}

/** 
 * Parses the template
 * @param page The page template name, should be already loaded.
 * @returns The javascript code generated from the parsing
 */
AjaxPages.prototype.parse = function(page) {
	
    value = AjaxPagesLoader.getPreLoaded(page);
    
    if ( value == undefined ) value = "Error. Page '"+page+"' is not preloaded."; 
    
    var out = "";
    var lineNumber = 1;
    try {
    
        var betweenPerc = false;
        
        out = "function(context) { \n";
        
        out += "var __ajp = new AjaxPages();\n";
        
        out += "try {\n"
        
        out += "   if ( context == undefined ) { \n";
        out += "       context = '';\n";
        out += "   }\n";
        
        out += "var out= unescape('";
        
        var line = "";
        
        for (i = 0; i < value.length; i++ )
        {
            var nextTwo = "";
            if ( i <= value.length - 2 ) {
                nextTwo = value.charAt(i) + value.charAt( i + 1 );
            }
            
            var nextThree = "";
            if ( i <= value.length - 3 ) {
                nextThree = value.charAt(i) + value.charAt( i + 1 ) + value.charAt( i + 2 );
            }
            
            if ( nextTwo == "<%" && nextThree != "<%=" && nextThree != "<%@") {
                
                out += "');\n";
                betweenPerc = true;
                i += 1;
                
            } else if ( nextTwo == "<%" && nextThree == "<%=" && nextThree != "<%@") {
                
                out += escape(line) + "');\n";
                line = "";
                out += "    out+= ";
                
                betweenPerc = true;
                i += 2;
            } else if ( nextTwo == "<%" && nextThree != "<%=" && nextThree == "<%@" ) {
                
                i += 3;
                var directive = "";
                
                while ( nextTwo != "%>" ) {
                    directive += value.charAt(i); 
                    i++;
                        if ( i <= value.length - 2 ) {
                            nextTwo = value.charAt(i) + value.charAt( i + 1 );
                        }
                        
                }

                out += escape(line) + "');\n";
                line = "";
                

                out += this._processDirective( directive );
                out += "    out+= unescape('";
                i++;
            } else if ( nextTwo == "%>" ) {
                out += ";\n" + "    out+= unescape('";
    			if ( betweenPerc == false )  
        			throw new AjaxPagesException("Sintax error","Expecting %> as the of the tag.") ;                
                betweenPerc = false;
                i += 1;
            } else if ( value.charAt(i) == String.fromCharCode(10) )  { 
                if ( !betweenPerc ) {
                    out += escape(line) + "\\n');\n" + "    out+= unescape('";
                    line = "";
                    lineNumber ++;
                }               
                
            } else if ( value.charAt(i) == String.fromCharCode(13) )  {                 
            } else {  
                if ( betweenPerc ) {
                    out += value.charAt(i) ;
                } else {
                    line += value.charAt(i); 
                }   
            }
        }
        
        out += escape(line) + "');\n";
        
        out += "} catch (e) {"
        out += "return '"+"An exception occurred while excuting template. Error type: ' + e.name" 
               + "+ '. Error message: ' + e.message;";
        out += "}"
        out += "    return out;\n";
        out += "}\n";
   } catch (e) {
        
        out = "function(context) { \n";
        out += "return '"+"An exception occurred while parsing on line "+ lineNumber +". Error type: " + e.name 
               + ". Error message: " + e.message+"';";
        out += "}"     
   }
   
    return out;
}    

/** 
 * Private method. Should not be used externally.
 * @private
 */
AjaxPages.prototype._processDirective = function(directive) {
    var i = 0;
    
    var tolkenIndex = 0;
    var tolken = new Array();
    
    //Skip first spaces;    
    while ( directive.charAt(i) == ' ' ) {
        i++;
    }
    
    tolken[tolkenIndex] = "";
    while ( directive.charAt(i) != ' ' && i <= directive.length ) {
        tolken[tolkenIndex] += directive.charAt(i);
        i++;
    }
    
    tolkenIndex++;

    //Skip first spaces;    
    while ( directive.charAt(i) == ' ' ) {
        i++;
    }
    
    tolken[tolkenIndex] = "";
    while ( directive.charAt(i) != ' ' && directive.charAt(i) != '=' && i <= directive.length ) {
        tolken[tolkenIndex] += directive.charAt(i);
        i++;
    }
    
    tolkenIndex++;
    
    //Skip first spaces;    
    while ( directive.charAt(i) == ' ' ) {
        i++;
    }
    
    if( directive.charAt(i) != '=' ) 
        throw new AjaxPagesException("Sintax error", "Tolken = expected attribute");
    i++
    
    //Skip first spaces;    
    while ( directive.charAt(i) == ' ' ) {
        i++;
    }
    
    tolken[tolkenIndex] = "";
    while ( directive.charAt(i) != ' ' && i <= directive.length ) {
        tolken[tolkenIndex] += directive.charAt(i);
        i++;
    }   
    tolkenIndex++;
    
    //Skip first spaces;    
    while ( directive.charAt(i) == ' ' &&  i <= directive.length ) {
        i++;
    }
    
    tolken[tolkenIndex] = "";
    while ( directive.charAt(i) != ' ' && directive.charAt(i) != '=' && i <= directive.length && i <= directive.length ) {
        tolken[tolkenIndex] += directive.charAt(i);
        i++;
    }   
    
    tolkenIndex++;
    
    if( directive.charAt(i) != '='  && i <= directive.length  ) 
        throw  new AjaxPagesException("Sintax error", "Tolken = expected after attribute" );
    i++ 
    
    tolken[tolkenIndex] = "";
    while ( directive.charAt(i) != ' ' && i <= directive.length  && i <= directive.length ) {
        tolken[tolkenIndex] += directive.charAt(i);
        i++;
    }   

    var file = "";
    var context = "";

    if ( tolken[0] != "include" )  
        throw new AjaxPagesException("Sintax error","Directive " + tolken[0] + " unknown.") ;
        
    if ( tolken[1] != "file" )      
        throw new AjaxPagesException("Sintax error", "Attribute file expected after include." ); 
    else file = tolken[2];

        
    if ( tolken[3] != "context" && tolken[3] != "" )    
        throw new AjaxPagesException( "Sintax error", "Attribute context expected after file."); 
    else if ( tolken[3] == "context" ) 
        context = tolken[4]
    else 
        context = "context";
        
    var out = "    out+= __ajp.process(" + file + ", " + context + ");\n";
        
    return out;    
        
}

/** 
 * Processes the template
 * @param page The page template to be processed by Ajax Pages
 * @param context The context to be passed to the template 
 * @returns The output from processing the template
 */    
AjaxPages.prototype.process = function(page, context) {
	if ( AjaxPages._cacheProcessor[page] == undefined ) {
		eval ( "var processor =" + this.parse(page) );
		AjaxPages._cacheProcessor[page] = processor;
    	return processor(context);
	} else {
		var processor = AjaxPages._cacheProcessor[page];
		return processor(context);
	}
}  


/** 
 * Exception throwed by AjaxPages
 */
AjaxPagesException = function( name, message ) {
    this.name = name;
    this.message = message;
}

/**  
 * Class responsable for loading the template pages from the server. 
 * It is fully assyncronous and can load many pages at the same time. 
 * 
 * @constructor
 * @author Gustavo Amigo
 */
var AjaxPagesLoader = function() {

	this.onload = function () { };
	this.onerror = function () { };

		this._pagesUrl = new Array();
	if ( AjaxPagesLoader._preLoadedPages == undefined ) {
		 AjaxPagesLoader._preLoadedPages = new Object();
	}
}  

AjaxPagesLoader.prototype.addPage = function (url) {
    this._pagesUrl.push(url);
    if ( AjaxPagesLoader._preLoadedPages[url] == undefined ) {
    	AjaxPagesLoader._preLoadedPages[url] = null;
	}
} 

AjaxPagesLoader.prototype.load = function () {
	this._errorEvent = false;
	var ready = true;

    for( var  urlIndex=0; urlIndex<this._pagesUrl.length; urlIndex++ ) {
	    if ( AjaxPagesLoader._preLoadedPages[this._pagesUrl[urlIndex]] == null ) {
		    this._doRequest( this._pagesUrl[urlIndex], this._callBackRequestHandler );
		    ready = false;
	    }
	}
	if ( ready ) this.onload();
} 

AjaxPagesLoader.getPreLoaded = function ( url) {
	return AjaxPagesLoader._preLoadedPages[url];
}

AjaxPagesLoader.prototype._callBackRequestHandler = function ( url, req, onloadcallback, onerrorcallback ) {
	
	var ready = false;	
	var error = false;
	
	if ( req.readyState == 4 ) {
		ready = true;
		AjaxPagesLoader._preLoadedPages[url]=req.responseText;
		
		for ( key in AjaxPagesLoader._preLoadedPages ) {
			if ( AjaxPagesLoader._preLoadedPages[key] == null ) {
				ready = false;
			}
		}
		if ( req.status != 200 && req.status != 0 && req.status != 304 ) error = true;
	} else {
		AjaxPagesLoader._preLoadedPages[url]=null;
	}

	if( error && ready ) {
		onerrorcallback();
	} else if ( !error && ready) {
		onloadcallback();
	}

}

AjaxPagesLoader.prototype._doRequest = function (url, callback, index) {
	
	var onErrorEvent = this.onerror;
	var onLoadEvent = this.onload;
    var req;
    // branch for native XMLHttpRequest object
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
        
        req.onreadystatechange = function() {
	        
	        callback ( url, req, onLoadEvent , onErrorEvent );
        };

        req.open("GET", url, true);
        
           	try {
            	req.send(null);
        	} catch(e) {}
	    // branch for IE/Windows ActiveX version
	    } else {
			try{ //to get MS HTTP request object
	            req=new ActiveXObject("Msxml2.XMLHTTP.4.0");
	            }catch(e){
	                try{ //to get MS HTTP request object
	                    req=new ActiveXObject("Msxml2.XMLHTTP")
	                }catch(e){
	                    try{// to get the old MS HTTP request object
	                        req = new ActiveXObject("microsoft.XMLHTTP");
	                    } catch(e){
		                    throw "XMLHttpRequest not supported";
                    	}
                	}
            	}
        if (req) {
           	req.open("GET", url, true);
            req.onreadystatechange = function() {
	      	  	callback ( url, req, onLoadEvent , onErrorEvent  );
        	};
           	try {
            	req.send(null);
        	} catch(e) {}
        } 
    }
}