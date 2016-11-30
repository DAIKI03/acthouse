<?php
	require 'utils.php';
	if (isset($_GET['p'])) {
		$profile = get_profile();
		$image_type = "image/jpeg";
		$image_path = $profile['image_path'];
		$file_size = filesize($image_path);
	} else {
		$id = $_GET['id'];
		$post = get_post($id);

		$image_type = $post['image_type'];
		$image_path = $post['image_path'];
		$file_size = filesize($image_path);
	}
    //Response header
		header("Content-Length: ${file_size}");//サーバーからレスポンス
		header("Content-Type: ${image_type}");
		echo file_get_contents($image_path);
?>