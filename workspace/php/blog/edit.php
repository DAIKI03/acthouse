	<?php include 'utils.php'; ?>

	<?php
		if(!isset($_GET['id'])) {
			$error = 'idが指定されていません';
			$page_title = "error";
		} else {
			$id = $_GET['id'];
			$post = get_post($id);
			$title = '記事' .$post['title'].'の編集';
			$page_title = get_title($title);
		}
	 ?>
	 <?php include 'header.php'; ?>
	 <?php if(isset($error)) : ?>
	 		<?php echo $error; ?>
	 	<?php else : ?>

		<div class="container">
			<!-- <ul class="breadcrumbs">
				<li><a href="index.php">Home</a></li>
				<li> > </li>
				<li><a href="show.php?id=<?php echo $id; ?>"><?php echo $post['title']; ?></a></li>
				<li> > </li>
				<li>記事編集</li>
			</ul> -->
			<?php $pages =
				[
					['url' => 'index.php', 'label' => 'Home'],//foreachs1週目
					['url' => 'show..php?id=${id}', 'label' => $post['title']],//２週目
					['url' => '', 'label' => '記事編集'],//３週目
				];
					echo breadcrumbs($pages);
			 ?>
			<form action="post.php" name="form" method="post" enctype="multipart/form-data">
				<div class="edit title">
					<label for="title">タイトル
						<input type="text" name="title" value="<?php echo $post['title']; ?>">
					</label>
				</div>
				内容
				<div class="edit content">
					<lable for="content">
						<textarea name="content" id="" cols="100" rows="50"
						><?php echo $post['content']; ?>
						</textarea>
					</lable>
				</div>
				<div class="cat">
					<label for="category">カテゴリー
						<input type="text" name="category" value="<?php echo $post['category']; ?>">
					</label>
				</div>
				<div class="images">
					<label for="image">
						<input type="file" name="image">
					</label>
				</div>
				<div class="drafts">
					<label for="draft">下書きにしちゃう？
						<?php
							$draft = $post['status'] == 'draft';
						?>
						<input type="checkbox" name="draft" value="true" <?php if ($draft) echo 'checked'; ?>>
					</label>
				</div>
				<button class="button">送信</button>
				<input type="hidden" name="mode" value="edit">
				<input type="hidden" name="id" value="<?php echo $post['id']; ?>">
			</form>
		</div>
	<?php endif; ?>
	<?php include 'footer.php'; ?>