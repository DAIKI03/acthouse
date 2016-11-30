<?php include 'utils.php'; ?>


	<?php 
		if (!isset($_GET['id'])) {
			$error = "idが指定されていません";
			$page_title = get_title("error");
		}	else {
			$id = $_GET['id'];
			$sql = "select * from posts where id = ${id}";
			$post = get_post($id);
			$page_title = get_title($post['title']);
		}
	?>
	 <?php include 'header.php'; ?>

	 <div class="container">
		 <ul class="breadcrumbs">
				<li><a href="index.php">Home</a></li>
				<li> > </li>
				<li>記事詳細</li>
			</ul>
		<?php if (isset($error)) :?> <!-- start if from : -->
			<?php echo $error; ?>
		<?php else :?>
		<div>
			<?php
				$prev_post_sql = "select * from posts where id < ${id} order by id desc limit 1";
				$prev_post = get_db()->query($prev_post_sql)->fetch();
				if ($prev_post) :?>
					<?php $prev_id = $prev_post['id']; ?>
					<a href="show.php?id=<?php echo $prev_id; ?>">前の記事</a>
			 	<?php endif; ?>

			 	<?php
			 		$next_post_sql ="select * from posts where id < ${id} order by id limit 1";
			 		$next_post = get_db()->query($next_post_sql)->fetch();
			 	if ($next_post) :?>
					<?php $next_id = $next_post['id']; ?>
					<a href="show.php?id=<?php echo $next_id; ?>">次の記事</a>
			 	<?php endif; ?>
			 	 
		</div>

		 <span class="cat">カテゴリー：<?php echo $post['category']; ?></span>
		 <h1><?php echo $post['title']; ?></h1>
		 <p><?php echo $post['content']; ?></p>
		 <div>
		 	<img src="image.php?id=<?php echo $id; ?>" alt="">
		 </div>
		 <a href="edit.php?id=<?php echo $post['id']; ?>" class="top-drafts btn">編集する</a>
		 <a href="delete.php?id=<?php echo $id; ?>" id="delete" class="top-drafts">削除する</a>
		<?php endif; ?> <!-- instead of {} = : endif -->
		<form action="comment.php" method="post">
			<label for="user_name">
				Username: <input type="text" name="user_name">
			</label>
			<label for="comment">
				Comment: <input type="text" name="comment">
			</label>
			<input type="hidden" name="post_id" value="<?php echo $id; ?>">
			<button>コメントする</button>
		</form>
		<?php
			$comment_sql = "select * from comments where post_id = ${id} ";
			foreach(get_db()->query($comment_sql) as $row) :
		 ?>
		<div>
				<span>Name: <?php echo $row['user_name']; ?></span>
				<span><?php echo $row['comment']; ?></span>
		</div>
			<?php endforeach ; ?>
		<a href="/php/blog/">Topに戻る</a>
	</div>
<?php include 'footer.php'; ?>