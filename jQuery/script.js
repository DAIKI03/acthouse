jQuery(function($) {
	$("#traverse2 button").on("click", function(){
		$("#traverse2 .blue_border").removeClass("blue_border");
	});
	$("#traverse2 .prev").on("click", function(){
		$("#traverse2 .saburo").prev()
			.addClass("blue_border");
	});
	$("#traverse2 .prevAll").on("click", function(){
		$("#traverse2 .saburo").prevAll()
			.addClass("blue_border");
	});
	$("#traverse2 .next").on("click", function(){
		$("#traverse2 .saburo").next()
			.addClass("blue_border");
	});
	$("#traverse2 .nextAll").on("click", function(){
		$("#traverse2 .saburo").nextAll()
			.addClass("blue_border");
	});
	$("#traverse2 .parent").on("click", function(){
		$("#traverse2 .saburo").parent()
			.addClass("blue_border");
	});
	$("#traverse2 .parentAll").on("click", function(){
		$("#traverse2 .saburo").parents()
			.addClass("blue_border");
	});
	$("#traverse2 .children").on("click", function(){
		$("#traverse2 .saburo").children()
			.addClass("blue_border");
	});
	$("#traverse2 .siblings").on("click", function(){
		$("#traverse2 .saburo").siblings()
			.addClass("blue_border");
	});
	$("#traverse2 .closest").on("click", function(){
		$("#traverse2 .saburo").closest("div")
			.addClass("blue_border");
	});
	$("#traverse2 .find").on("click", function(){
		$("#traverse2 .saburo").find("ul > li ul > li")
			.addClass("blue_border");
	});
	$("#traverse2 .mago2").on("click", function(){
		$("#traverse2 .mago").parent().parent().next()
			.addClass("blue_border");
	});


	$("#traverse1 .first").on("click", function(){
		$("#traverse1 li")
			.css("font-weight", "bold")
			.first().css("color", "red");
	});
	$("#traverse1 .last").on("click", function(){
		$("#traverse1 li")
			.css("font-weight", "normal")
			.last().css("color", "blue");
	});
	$("#traverse1 .eq").on("click", function(){
		$("#traverse1 li")
			.css("font-style", "italic")
			.eq(2).css("color", "green");
	});

	$("#remove-elem").on("click", function(){
		$(".first").remove();
			});
	$("#empty-elem").on("click", function(){
		$(".second").empty();
	});
	$("#clone-elem").on("click", function(){
		$(".first, .second, .third").clone().appendTo("#remove ul");
	});

 	$("#append").on("click", function(){
 		$("#add ul").append("<li>漫湖</li>");
 	});
 	$("#prepend").on("click", function(){
 		$("#add ul").prepend("<li>珍子</li>")//.css("color", "red");
 	});
 	$("#before").on("click", function(){
 		$("#add ul").before("<p>子供の名前</p>");
 	});
 	$("#after").on("click", function(){
 		$("#add ul").after("<p>生年月日</p>");
 	});

	$(".get-check").on("click", function(){
		var val = $("#form input:checkbox:checked");
		var checked = [];
		// for(var i=0; i < val.length; i++) {
		// 	checked[i] = $(val[i]).val();
		// } 
		checked = val.map(function(){
			return $(this).val();
		}).toArray();
		alert(checked);
	});

	$(".get-radio").on("click", function(){
		var val = $("#form input:radio:checked").val();
		alert(val);
	});
	$(".set-radio").on("click", function(){
		$("#form input:radio").val(["0"]);
	});

	$(".get-value").on("click", function(){
		var val = $("#form .text").val();
		alert(val);
	});
	$(".set-value").on("click", function(){
		$("#form .text").val("デゥてるて");//val = value
	});

	$(".set-text").on("click", function(){
		$("#form li:first-child")
			.html("<span style='color:red'>のび太</span>");
		$("#form li:nth-child(2)")
			.text("<span style='color:blue'>ぢゃい子</span>");
	});
	$(".get-text").on("click", function(){
		var html = $("#form li").html();// get tag
		var text = $("#form li").text();// text
		alert(html + "\n" + text);
	});

	$("#offset").on("click", function(){
		// $("#offset-div > .box").offset({top: 50, left: 200});
		$("#offset-div > .box").css("position", "relative")
			// .animate({height: 100}, "slow");
			// .fadeToggle("slow");
			.animate({top: "+=50", left: "+=1000"}, 10);
	});

	$("#scroll-top").on("click", function(){
		$("html, body").animate({scrollTop: 0}, 50000);
	});

	$("#width").on("click", function(){
		$("#box").width(200);
		$("#box").addClass("change_box");
		var width = $("#box").width();
		var innerWidth = $("#box").innerWidth();//including padding
		var outerWidth = $("#box").outerWidth();//including padding and border
		console.log("width=" + width,
			"innerWidth =" + innerWidth,
			"outerWidth =" + outerWidth);
	});
	$("#height").on("click", function(){
		$("#box").height(200);
	});

	$("#add-class").on("click", function(){
		$("#hanako2").addClass("woman");
		$("#taro2, #jiro2").addClass("man");
		isWoman();
	});
	$("#remove-class").on("click", function(){
		$("#hanako2").removeClass("woman");
		$("#taro2, #jiro2").removeClass("man");
	});
	$("#toggle-class").on("click", function(){
		$("#hanako2").toggleClass("woman");
		$("#taro2, #jiro2").toggleClass("man");
		isWoman();
	})
	function isWoman(){
		var ret = $("#hanako2").hasClass("woman");
		var msg;
		if (ret) {
			msg = "花子は女性です";
		} else {
			msg = "花子は女性ではありません"
		}
		console.log(msg);
	}


	$("#remove-attr").on("click", function(){
		$("#remove > a").removeAttr("title");
	});

	$("#check-is").on("click", function(){
		var div = $("#is > div").is(".man");
		var chk1 = $("#is > #chk1").is(":checked");
		alert("manが含まれているのは" + div + "です"
			+ "chk1がチェックされているのは" + chk1 + "です");
	});

	$("#get-attr").on("click", function(){
		alert($("#yahoo").attr("href"));
	});
	$("#set-attr").on("click", function(){
		$("#apple").attr("href", "http://www.apple.co.jp/");
	});

	$("#check-value").on("click", function(){
		var checkedRadio = $("#form2 > input:checked").val();
		var selected = $("#form2 > select option:selected").val();
		alert(checkedRadio + "" + selected);
	});

	$("#check-form").on("click", function(){
		$("#form > input:text").css("background-color", "beige");
		$("#form > input:password").css("background-color", "olivedrab");
		$("#form > input:button").css("background-color", "indianred");
	});

	$("#empty").on("click", function(){
		$("#table td:empty").css("background-color", "cadetblue");
		$("#table td:parent").css("background-color", "lawngreen");
	});

	$("#has").on("click", function(){
		$("#filter li:has(span)").css("background-color", "moccasin");
	});
	$("#dofilter").on("click", function(){
		$("#filter li:contains('郎')").css("background-color", "lightpink");
	});

	$("#not").on("click", function(){
		$("a:not([href$='apple.co.jp'])").css("background-color","turquoise");
	});

	$("#point").on("click", function(){
		$(".list > li:eq(3)")
			.css("background-color", "deeppink");
		$(".list > li:gt(3)")
			.css("background-color", "burlywood");
		$(".list > li:lt(3)")
			.css("background-color", "seagreen");
	});

	$("#even2").on("click", function(){
		$(".list > li:even").css("background-color", "aquamarine");
	});
	$("#odd2").on("click", function(){
		$(".list > li:odd").css("background-color", "lightsalmon");
	});

	$("#alone").on("click", function(){
		$(".list > li:only-child").css("background-color", "gainsboro");
	});
	$("#span2").on("click", function(){
		$(".list > li:nth-child(3n+1)").css("background-color", "lavender");
	});
	$("#span").on("click", function(){
		$(".list > li:nth-child(3n)").css("background-color", "darkorange");
	});

	$("#odd").on("click", function(){
		$(".list > li:nth-child(odd)").css("background-color", "maroon");
	});
	$("#even").on("click", function(){
		$(".list > li:nth-child(even)").css("background-color", "bisque");
	});

	$("#nth-child").on("click",function(){
		$(".list > li:nth-child(3)").css("background-color", "plum");
	});
	
	$("#first-child").on("click", function(){
		$(".list > li:first-child").css("background-color", "thistle");
	});
	$("#first").on("click", function(){
		$(".list > li:first").css("background-color", "peachpuff");
	});
	$("#all-bro").on("click", function(){
		$("#sazaesan h2 ~ p").css("background-color", "firebrick");
	});
	$("#bro").on("click", function(){
		$("#sazaesan h2 + p").css("background-color", "chocolate");
	});
	$("#ko").on("click", function(){
		$("#child > p, #child > h2").css("background-color", "deeppink");
	});
	$("#shison").on("click",function(){
		$("#child p, #child h2").css("background-color", "turquoise");
	});

	$("#div1").on("click", function(){
		$("p", "#child-div2").css("background-color", "skyblue");
		// $("#child-div2 > p")
	});

	$("#back").on("click", function(){
		$("input[name$=rse]").css("background-color", "salmon");
	});
	$("#front").on("click", function(){
		$("input[name^=do]").css("background-color", "palegoldenrod");
	});
	$("#match").on("click", function(){
		$("input[name~=cat]").css("background-color", "lime");
	});
	$("#part").on("click", function(){
		$("input[name*=cat]").css("background-color", "khaki");
	});

	$("#not_equal").on("click", function(){
		$("a[target!=_blank]").css("color", "lightblue");
	});
	$("#att_sel").on("click", function(){
		$("a[target=_blank]").css("color", "pink");
		$("a[target=_self]").css("color", "blue");
		$("a[target=_parent]").css("color", "red");
		$("a[target=_top]").css("color", "green");
	});

	$("#uni").on("click", function(){
		$("*").css("color", "gold");
	});

	$("#list2").on("click", function(){
		$("#taro2, #jiro, #tin")
			.css("background-color", "pink");
	});

	$("#list1").on("click", function(){
		$(".man").css("background-color", "orange");
		$("#taro").css("background-color", "blue");
	});

	$("h2").on("click", function(){
		$(this).css("background-color", "red");
	});

		$("#add-link").on("click", function(){
			$("<a></a>", {
				href: "http://www.apple.com/ph",
				target: "_blank",
				"class": "myClass",
				text: "リンク"
			}).appendTo("#container");
		$("<div></div>", {
			width: 100,
			height: 100,
			css:{ border: "1px solid gray", float: "right"},
			addclass: "my-div",
			on:
				{
					mouseover: function(){
						$(this).css({backgroundColor: "red"});
					},
					mouseout: function() {
						$(this).css({backgroundColor: "blue"});
					}
				}
			}).appendTo("#container");	
		});

		$("#change-size").on("click", function(){
		$("<div></div>", {
			width: 400,
			css:{ 
			 fontSize: "30px",
			 backgroundColor: "green",
			 color: "white"},
			 text: "おちんちん！",
			on:
				{
					click: function(){
						$(this).css({
							color: "red", 
							backgroundColor: "black",
							fontSize : "90px"
						})
					}
				}
		}).appendTo("#container");
	});

		$("#change_color").on("click", function(){
			$("li")
				.css(
					{
						color: "red",
						backgroundColor: "yellow"
					}//object
				);
		});

		$("#console").on("click", function(){	
		var li = document.getElementsByTagName("li");
		console.log(li);// javascript
		console.log($("li"));// jQuery

	});
	// document.getElementById('change_border')
	$("#change_border").on("click", function(){
		$("#color_div").css("border", "50px dotted red");
	});
});