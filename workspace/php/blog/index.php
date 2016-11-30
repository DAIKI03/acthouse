<?php require 'utils.php' ?>
<?php  $page_title = get_title("Home")?>
<?php include 'header.php'; ?>

		<div class="top">
				<video controls loop style="margin-left: 27%; margin-top: 21%; height: 21%;">
					<source src="video/dick-song.mp4">
				</video>
				<h1><span class="dick">おちんちん</span>ブログ
				<form action="index.php" class="form1">
						<input type="text" name="q" placeholder="🔍記事を検索" class="search">
						<button class="search-btn"></button>
				</form>
				</h1>
			</div>
		<div class="main">

		<div class="container">
			<div class="top-nav">
				<div class="category-section">

					 <ul>
					 		<li><a href="index.php">Home</a></li>
						 	<?php foreach(get_categories() as $row): ?>
						 		<li>
						 			<?php $category = $row['category'];
						 			link_tag("index.php?cat=${category}", $category); ?>
						 			(<?php echo $row['count']; ?>)
						 		</li>
					 		<?php endforeach; ?>
					 </ul>
				</div>
			</div>
			<div>
				<a href="new.php" class="button new">新規記事挿入</a>
				<a href="index.php?st=draft" class="top-drafts">下書き一覧</a>
			</div>
				<div class="archive">
				<?php
					//月別アーカイブ
				foreach(get_posts_month() as $row) :
					$year = $row['year'];
					$month = $row['month'];
					$show_month = to_english_month($month);
					$qs = "y=${year}&m=${month}";

					link_tag("index.php?${qs}", "${year}年${month}月");?>
					(<?php echo $row['count']; ?>)
				<?php endforeach; ?>
					</div>
				<?php
					if (is_category()) {
						$cat = $_GET['cat'];
						$results = get_posts_by_category($cat);
					} else if (is_search()) {
						$q = $_GET['q'];
						$results = get_posts_by_search($q);
					} else if (is_draft()) {
						$results = get_posts_by_status();
					} else if (is_archive_by_month()) {
						$year = $_GET['y'];
						$month = $_GET['m'];
						$results = get_posts_by_months($year, $month);
					} else {
						$results = get_posts();
					}
					// $stmt = get_db()->query($sql);
					// $count_sql = str_replace('*', 'count(*)', $sql);
					// $count_stmt = get_db()->query($count_sql);
					// $count = $count_stmt->fetch();
					if (is_category()) : ?>
						<p>カテゴリー<?php echo $_GET['cat'];?>の投稿一覧</p>
					<?php endif;
					if (is_year()) : ?>
						<p><?php echo $year; ?>年<?php echo $month; ?>月の投稿一覧</p>
					<?php endif;
					if (count($results) == 0) { ?>
						<p>検索結果がありませんでした</p>
					<?php } else {
						//記事表示開始
				 ?>
			<?php foreach($results as $row) { ?>
				<a href="show.php?id=<?php echo $row['id']; ?>">
				<div class="row">
					<div class="box">
						<?php if (empty($row['image_path'])): ?>
							<img src="img/no-image.gif" alt="">
						<?php else: ?>
						<img src="image.php?id=<?php echo $row['id'];?>" alt="<?php echo $row['title']; ?>">
						<div class="mask">
							<div class="caption">Read more ...</div>
						</div>
						<?php endif; ?>
						<div class="box-text">
							<div>カテゴリー: <?php echo $row['category']; ?></div>
							<h2><?php echo $row['title']; ?></h2>
							<span><?php echo $row['created_at']; ?></span>
							<div><?php echo $row['updated_at']; ?></div>
							<!-- <p><?php echo $row['content']; ?></p> -->
						</div>
					</div>
				</div>
			</a>
		<?php }} ?>
			<div id="profile">
			<aside>
				<a href="edit_profile.php">
					<h2>Profile</h2>
				<?php $profile = get_profile(); ?>
				<img src="image.php?p" alt="<?php echo $profile['name']; ?>">
				<h3 class="name"><?php echo $profile['name']; ?></h3>
				<p class="bio"><?php echo $profile['bio']; ?></p>
				</a>
			</aside>
		</div>
		</div>
	</div>
	<?php
		//print_r(get_posts_by_category('おちんちん'));
		//print_r(get_posts_by_search('おちんちん'));
	 ?>

<?php include 'footer.php'; ?>