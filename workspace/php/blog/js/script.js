var del = document.getElementById('delete');
if (del) {
	del.addEventListener("click", function(event){
		var result = confirm("削除してもよろしいですか？");
		if (result) {
			//nop
 		} else {
 			event.preventDefault();
 		}
	});
}