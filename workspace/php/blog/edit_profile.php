<?php require 'utils.php';
	$page_title = "プロフィール作成";
	include 'header.php';

		$profile = get_profile();
		if (isset($_POST['name'])) {
			if ($profile) {
			$id = $profile['id'];
			$sql = "update profiles set name = ?, bio = ? where id = ?";
			$params = array($_POST['name'], $_POST['bio'], $id);
			} else {
				$sql = "insert into profiles (name, bio)values(?, ?)";
				$params = array($_POST['name'], $_POST['bio']);
			}
			$success = get_db()->prepare($sql)->execute($params);

			$profile = get_profile();//id を知る
			if (isset($_FILES['image'])) {//image file がアップロードされていれば
			$path = "uploads/profile";//保存場所
			@mkdir($path, 0777, true);
			$image = $_FILES['image'];
			$image_name = $image['name'];//名前取得
			$image_path = "${path}/${image_name}";//名前とpathを合体
			move_uploaded_file($image['tmp_name'], $image_path);

			$sql = "update profiles set image_path =?, updated_at = current_timestamp where id = ?";
			$params = array($image_path, $profile['id']);
			$success = get_db()->prepare($sql)->execute($params);
			}
		}
 ?>
	<div class="container">
		<form action="" method="post" enctype="multipart/form-data">
			<div class="to">
				<label for="name">名前
					<input type="text" name="name" value="<?php echo $profile['name']; ?>">
				</label>
			</div>
			<!-- control + option + enter -->
			<div>
				<label for="bio">
					<textarea name="bio" cols="30" rows="10"> <?php echo $profile['bio']; ?></textarea>
				</label>
			</div>
			<div>
				<img src="image.php?p" alt="image">
				<label for="images">写真
					<input type="file" name="image">
				</label>
			</div>
			<button>作成</button>
		</form>
	</div>

 <?php include 'footer.php'; ?>