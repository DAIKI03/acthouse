<?php
		function get_db() {
			$db = new PDO('mysql:host=localhost;dbname=blog;charset=utf8mb4', 'root','');
			$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
			return $db;
		}

		function get_post($id) {
			$sql = "select * from posts where id = ${id}";
			$stm = get_db()->query($sql);
			foreach ($stm as $row) {
				$post = $row;
			}
			return $post;
		}

		function get_blogname() {
			return "おちんちんざむらい";
		}


		function get_title($title) {
			return get_blogname() . ' _ ' . $title;
		}

		function is_category() {
			return isset($_GET['cat']);
		}

		function is_search() {
			return isset($_GET['q']);
		}

		function is_draft() {
			return isset($_GET['st']);
		}

		function is_archive_by_month() {
			return isset($_GET['y']) and isset($_GET['m']);
		}

		function is_year() {
			return isset($_GET['y']);
		}
//リファクタリング
		function get_posts_by_category($cat) {
			$sql = "select * from posts where category = '${cat}' and status = 'published' order by created_at";
			return do_query($sql);
		}

		function get_posts_by_search($q) {
			$sql = "select * from posts where title like '%${q}%' or content like '%${q}%' and status = 'published' order by created_at desc";
			return do_query($sql);
		}

		function get_posts_by_status() {
			$sql = "select * from posts where status = 'draft' order by created_at desc";
			return do_query($sql);
		}

		function get_posts() {
			$sql = "select * from posts where status = 'published' order by created_at desc";
			return do_query($sql);
		}

		function get_posts_month() {
			$sql = "select count(*) as count, date_format(created_at, '%Y') as year, date_format(created_at, '%m') as month from posts group by date_format(created_at, '%Y'), date_format(created_at, '%m') order by year, month";
			return do_query($sql);
		}

		function get_posts_by_months($year, $month) {
			$sql = "select * from posts where created_at like '${year}-${month}%'";
			return do_query($sql);
		}

		function do_query($sql) {
			$stmt = get_db()->query($sql);
			$result = [];
			foreach ($stmt as $row) {
				$result[] = $row;
			}
			return $result;
		}

		function get_profile() {
			$select_sql = "select * from profiles limit 1";
			$profile = get_db()->query($select_sql)->fetch();
			return $profile;
		}

		function get_categories () {
			$category_sql = "select category, count(*) as count from posts group by category";
			return do_query($category_sql);
		}

		//-------------- View utilities------------------------

	function link_tag($url, $label) {
		$tag = "<a href='${url}'>$label</a>";
		echo $tag;
	}

	function to_english_month ($mon) {
		$months = ['01' => 'Jan', '02' => 'Feb', '03'=>'Mar',
			'04' => 'Apr', '05' => 'May', '06'=>'Jun',
			'07' => 'Jul', '08' => 'Aug', '09'=>'Sep',
			'10' => 'Oct', '11' => 'Nov', '12'=>'Dec',
		];
			return $months[$mon];
	}

	function breadcrumbs ($pages) {
		if (empty($delimiter)) {
			$delimiter = " > ";
		}
		$tag = "<ul class='breadcrumbs'>";
		foreach($pages as $index=>$page) {
			$url = $page['url'];//index.php
			$label = $page['label'];//Home
			$li = "<li>";
			if ($index + 1 == count($pages)) {
				$li = "${li}${label}</li>";
			} else {
				$li = "${li}<a href='${url}'>${label}</a></li>{$delimiter}</li>";
			}
			$tag = $tag . $li;
		}
		$tag = "${tag}</ul>";
		return $tag;
	}
?>