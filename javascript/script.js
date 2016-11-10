  var p1= document.getElementById("p1");
	console.log(p1);
	var clz = document.getElementsByClassName("p");
	console.log(clz[0].innerHTML);
	var tags = document.getElementsByTagName("p");
	console.log(tags[2].innerHTML);
	// p1.innerHTML = "変更後の段落文字列"
	// alert(p1.innerHTML);

	document.getElementById("remove-child")
		.addEventListener("click", function(){
			var container = document.getElementById("container");
			var children = container.children;
			// console.log(children);
			// container.removeChild(children[2]);
			var firstChild = container.firstChild;
			var lastChild = container.lastChild;
			if (lastChild) {
				container.removeChild(lastChild);
			}
			
		})

	document.getElementById("add-class")
		.addEventListener("click", function(){
			var e = document.createElement("div");
			e.setAttribute("class", "child");
			document.getElementById("container")
				.appendChild(e);
		});

	document.getElementById("add-child")
		.addEventListener("click", function() {
			var e = document.createElement("div");
			document.getElementById("container")
				.appendChild(e);
		});

	var timerId, time = 0;
	document.getElementById("start")
		.addEventListener('click', function(){
			if (!timerId) {
				timerId = setInterval(function(){
				document.getElementById("timer").innerHTML = time;
				time++;
				}, 10);
			}		
			
		});
	document.getElementById("stop")
		.addEventListener('click', function(){
			clearInterval(timerId);
			timerId = null;
		});

	document.getElementById("interval")
		.addEventListener('click', function(){
			setInterval(function(){
				var div = document.getElementById("div3");
				if (div.style.backgroundColor == "") {
					div.style.backgroundColor = "blue";
				} else {
					div.style.backgroundColor = "";
				}
			}, 100)
		});

	document.getElementById("delay")
		.addEventListener('click', function(){
			setTimeout(function(){
				alert("maayon buntag");
			}, 3000);
		});

	var imageIndex = 0;
	document.getElementById("image")
		.addEventListener('click', function(){
			var images = ["tintin1.jpg", "tintin2.jpg", "tintin3.jpg",
			 "tintin4.gif", "tintin5.jpg"];
			 this.src = images[imageIndex];
			if (imageIndex < 4 ) {
				imageIndex++;
			} else {
				imageIndex = 0;
			}
		});

	var oldColor;
	var div1 = document.getElementById("div1")
	// document.getElementById("div1")
		// .addEventListener('mouseover', function(){
		// 	// var div = document.getElementById("div1");
		// 	oldColor = this.style.backgroundColor;
		// 	this.style.backgroundColor = "#ffcccc";	
		// });
		// div1.addEventListener('mouseout', function(){
		// 	this.style.backgroundColor = oldColor;
		// });

		var div2 = document.getElementById("div2")
		.addEventListener('click', function(){
			if (this.style.width == "300px") {
				this.style.width = "100px";
			}	else {
				this.style.width = "300px";
			}
			if (this.style.fontSize == "50px") {
				this.style.fontSize = "10px"
			} else {
				this.style.fontSize = "50px"
			}
			if (!this.style.borderRadius) {
				this.style.borderRadius = "20px";
			} else {
				this.style.borderRadius = null;
			}
			if (this.style.backgroundColor == "") {
				this.style.backgroundColor = "pink";
			} else {
				this.stylebackgroundColor = "";
			}
			// this.style.fontSize = " 50px";
		});

	document.getElementById("open-self")
		.addEventListener('click', function(){
			location.href = "http://www.yahoo.com";
		});
	document.getElementById("open-new")
		.addEventListener('click', function(){
			window.open("http:www.apple.com/jp/")
		})

	document.getElementById("btn-while")
		.addEventListener('click', function(){
			var from = document.getElementById("from").value;
			var to = document.getElementById("to").value;
			if (from == "" || to =="") {
				alert("数値を入力してください");
				return; //stop processing
			}
			if (from > to) {
				var oldFrom = from;
				from = to;
				to = oldFrom;
			}
			var num = +from;
			var num2 = +to;
			while(num <= +to){	
				total = +from + +num;
				num++;
			}
			alert(from + "+" + to + "の合計は" + total + "です！");
		});

	document.getElementById("btn-array")
		.addEventListener('click', function(){
			var gender = new Array();
			gender[0] = "男";
			gender[1] = "女";
			gender[2] = "オカマ";
			document.getElementById("arai").innerHTML = gender[2];

			var month = ["Jan", "Feb", "Mar", "Apr", "May", "June",
				"July", "Aug", "Sep", "Oct", "Nov", "Dec"];
			document.getElementById("arai").innnerHTML = month[0];
			for(var i=0; i<month.length; i++) {
				console.log(month[i]);
			}	
		});
   
   document.getElementById("btn-array2")
   	.addEventListener('click', function(){
   		var slang = ["Dick", "Fuck", "Cock", "Shit", "Mother", "Penis",
				"Otin", "Tintin", "ppap"];
			document.getElementById("arai2").innnerHTML = slang[0];
			for(var i=0; i<slang.length; i++) {
				
				if (i == 0 ) {
					// break; //stop there
					continue; //skip the numbber
				}
				console.log(slang[i]);
			}	
   	});

	 document.getElementById("btn2")
	 	.addEventListener('click', function(){
	 		var val = document.getElementById("text1").value;
	 		switch(val) {
	 			case 'ちんこ':
	 				alert("ちんこです！");
	 				break;
	 			case 'おちんちん':
	 				alert("おちんちんが挿入されました！");
	 				break;
	 			case 'オティンティン':
	 				alert("オティンティンが挿入されました");
	 			  break;
	 			 case 'Penis':
	 			 	alert("Inserted your Penis");
	 			 	break;
	 			 	case 'Dick':
	 			 	alert("Inserted your Dick");
	 			 	break;
	 			 	case 'Cock':
	 			 	alert("Inserted your Cock");
	 			 	break;
	 			 default:
	 			 	alert("おちんちんを入力しなさい！"); 				
	 		}
	 	});
	 document.getElementById("btn1")
	 	.addEventListener('click', function(){
	 		var val = document.getElementById("text1").value;
	 		if (val == '') {
	 			alert('何か入力してください');
	 		}	else if (val == "1") {
	 			alert("１が入力されました");
	 		} else if (val == "おちんちん") {
	 			alert("おちんちんが挿入されました");
	 		}	else if (val == "ppap") {
	 			alert("ペンパイナップルアップルペン！")
	 		}	else {
	 			alert('１以外のものが入力されました');
	 		}
	 	});

	 document.getElementById("alert")
	 	.addEventListener('click', function(){
	 		alert("Hello Fuck you !")
	 	});
   document.getElementById("confirm")
	 	.addEventListener('click', function(){
      var result = confirm("あなたはおちんちんですか？");
      if (result == true) {
      	alert("嘘はやめましょう");
      } else {
      	alert("オチンチーン");
      }
	 	});
	 	document.getElementById("prompt")
	 	.addEventListener('click', function(){
	 		var response = prompt("あなたはのおちんちんの名前を教えてください？");
	 		alert("ようこそ" + response + "さん");
	 	});


	function showP1(message, message2) {
		var p1 = document.getElementById("p1");
		p1.innerHTML = message;
		document.getElementById("p2").innerHTML = message2;
  }

  function showP2() {
		var p1 = document.getElementById("p2");
		p1.innerHTML = "おちんちん";
	}

	function otinP4() {
		var p4 = document.getElementById("p4");
		p4.innerHTML = "おちんちーん";
	}

	document.getElementById("change-p1")
	.addEventListener('click', function(){
	 document.getElementById("p1").innerHTML = "イベントリスナから変更";
	});

	var btn = document.getElementById("change-p1");
	btn.addEventListener('click', function() {
		var paragragh1 = document.getElementById("p1");
		paragragh1.innerHTML = "イベントリスナからの変更２";
	});

	var btn = document.getElementById("change-p4");
	btn.addEventListener('click', function() {
		var paragragh1 = document.getElementById("p4");
		paragragh1.innerHTML = "おちんちーん";
	});