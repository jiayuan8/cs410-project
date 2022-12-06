var uploader_index = 0;

$(document).ready(function(){
	// update author name
	$("#author-input").val(window.localStorage.getItem("username"));
});


$("#upload-btn").click(function(){
	$("#files").click();
});

//---------------------- new file ----------------------//
function new_file(){
	var filename = $(".curr-uploader input").val();
	$(".curr-uploader").append("<p>" + filename + "</p>");
	$(".curr-uploader").show();

	$(".curr-uploader").removeClass("curr-uploader");

	
	$(".files-container").append(
		"<div class='row'> \
			<div class='curr-uploader'> \
				<input type='file' name='file' onchange='new_file()'> \
			</div> \
		</div>"
	);
}


$("#files").change(function(){
	var files = $(this).prop("files");
	var html = "";
	for(var i = 0; i < files.length; i++){
		var file = files[i];
		html += "<tr><td>" + file.name + "</td></tr>";
	}
	$(".files-container table tbody").html(html);

});


$("#submit-btn").click(function(){	
	var formData = new FormData($("#files-form")[0]);

    $.ajax({
        url: "/upload",
        type: 'POST',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function(data) {
            console.log("Dataset is uploaded.")
            alert("Dataset is uploaded. It is accessible on the instructor home page.");
        }
    });
});
