	<?php 
		require 'utils.php';
		$page_title = get_title("新規記事作成"); ?>
	<?php include 'header.php'; ?>
		<div class="container">
			<ul class="breadcrumbs">
				<li><a href="index.php">Home</a></li>
				<li> > </li>
				<li>新規記事作成</li>
			</ul>
			<form action="post.php" name="form" method="post" enctype="multipart/form-data">
				<div class="insert title">
					<label for="title">タイトル
						<input type="text" name="title" placeholder="タイトルを挿入しなさい">
					</label>
				</div>
				内容
				<div class="insert content">
					<lable for="content">
						<textarea name="content" id="" cols="100" rows="50" placeholder="内容を挿入しなさい"></textarea>
					</lable>
				</div>
				<div class="cat">
					<label for="category">カテゴリー
						<input type="text" name="category" placeholder="ちんちんを挿入しなさい">
					</label>
				</div>
				<div class="images">
					<label for="image">画像
						<input type="file" name="image">
					</label>
				</div>
				<div class="images">
					<label for="draft">下書きにしちゃう？
						<input type="checkbox" name="draft" value="true">
					</label>
				</div>
				<button class="button submit">送信</button>
			</form>
		</div>
	<?php include 'footer.php'; ?>