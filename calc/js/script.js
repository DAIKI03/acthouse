$(function(){
	var maxLength = 8;
	var memory = "";
	var lastCalc = "";
	$("#calc").on("click", ".num", function(){
		var current = $(".result").val();
		var pushed = $(this).text();
		var newValue;
		if (isOpeLastMemory()
			|| !hasMemory()) {
			newValue = pushed;
		} else {
			newValue = current + pushed;
			if (newValue.startsWith("0")) {
			newValue = newValue.substring(1);
			//"0123" = newValue.substrings(1) = "123"
			}
		}
		if (newValue.length <= maxLength) {
			$(".result").val(newValue);
		}
		memory = memory + pushed;
		$("#calc .clear").text("C");
	}).on("click", ".clear", function(){
		$(".result").val(0);
		memory = "";
		$("#last-answer").text("").fadeOut();

		var label = $(this).text()
		if (label == "AC") {
			$(".result").val(0);
			memory = "";
			lastCalc = "";
		} else {
			memory = memory.replace(/[\d]+$/, "");
			$(this).text("AC");
		}

	}).on("click", ".ope", function() {
		var lastLetter = getLastMemory();
			if (hasMemory() && isNumber(lastLetter)) {
				memory = memory + $(this).text();
			} else if (!hasMemory()) {
				memory = $(".result").val() + $(this).text();
			} 
				else {
				memory = memory.substring(0, memory.length - 1)//remove the last operater
				memory = memory + $(this).text();
			}
		
	}).on("click", ".eq", function() {
		console.log(memory);
		var result;
		if (memory.search(/[\+\-\*\%\/]/) == -1) {// -1 = No letter
			if (!lastCalc) {
				return;
			}
			
		}
		if (isNumber(getLastMemory())) {
			 result = checkOverFlow(eval(memory));//Get a number from letter
			if (result) {
				if (result.toString().length >= maxLength) {//greater than 8
					alert("おちんちーん！！！！！！");
					result = 0;
				}
			}
			var operaters = ["+", "-", "*", "/", "%"];
			var lastIndex;
			$.each(operaters, function(index, value) {
				var tmp = memory.lastIndexOf(value);
				if (tmp != -1) {
					lastIndex = tmp;
					return false;
				}
			});
			lastCalc = memory.substring(lastIndex);
			$(".result").val(result);
			memory = "";
		} else if (!hasMemory()) {
			var formula = $(".result").val() + lastCalc;
			var result = checkOverFlow(eval(formula));
			$(".result").val(eval(formula));
		}
		$("#last-answer").text(result).fadeIn(3000);
	});

	var hasMemory = function() { //function is always need ()
		return memory.length > 0;
	}

	var checkOverFlow = function(result) {
		if (result &&
				result.toString().length >+ maxLength) {
			var strResult = result.toString();
			if (result < 1) {
				result = strResult.
					substring(0, strResult.length -1);
			} else {
				alert("おちんちーん！！！！！！");
				return 0;
			}
			
		}
		return eval(result);

	};

	var isNumber = function(letter) {
		return letter && !isNaN(letter);
	}

	function isOpeLastMemory() {
		var lastLetter = getLastMemory();
		return lastLetter.endsWith("+")
				|| lastLetter.endsWith("-")
				|| lastLetter.endsWith("*")
				|| lastLetter.endsWith("/")
				|| lastLetter.endsWith("%");
	}

	function getLastMemory() {
		return memory.substring(memory.length - 1);
	}

	$(document).on("keyup", function(e){
		var key = e.key;
		$("#calc button:contains('" + key +"')")
			.trigger("click");
	});
	$("#calc").on("click", ".news", function() {
		var url = "http://ajax.googleapis.com/ajax/services/feed/load?v=1.0&q=https://goo.gl/qj6Xei";
		$.ajax({
			url: url, 
			dataType: "jsonp",
			jsonpClallback: "cb"
				}
			).done(function(response, textStatus, jpXHR){
				console.log(response);
				$("#news").fadeIn(3000).fadeOut();
			});	
	});
});