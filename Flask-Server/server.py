import os
import click
import json
import random
from datetime import datetime, timedelta
from app import create_app, db
from app.models import Movie, Screen
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

@app.cli.command("seed")
def seed():
    """
    从 seed_data.json 文件中读取并批量添加初始电影数据，增强了容错处理。
    """
    try:
        with open('seed_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            movies_data = data.get('movies', [])
    except FileNotFoundError:
        click.echo("错误: 未找到 seed_data.json 文件。")
        return
    except json.JSONDecodeError:
        click.echo("错误: seed_data.json 文件格式不正确。")
        return

    if not movies_data:
        click.echo("没有需要填充的电影数据。")
        return

    click.echo("正在从 JSON 文件开始填充数据库...")

    for movie_info in movies_data:
        # 检查关键字段是否存在
        if not movie_info.get("name"):
            click.echo("警告: 发现一条没有名称的电影记录，已跳过。")
            continue

        # 检查电影是否已存在
        existing_movie = Movie.query.filter_by(name=movie_info["name"]).first()
        if existing_movie:
            click.echo(f"电影 '{movie_info['name']}' 已存在，跳过。")
            continue

        # --- 👇 关键改动：更稳健的日期处理 ---
        release_date_str = movie_info.get("release_date")
        release_date_obj = None
        if release_date_str:
            try:
                # 尝试按标准格式解析，并只取日期部分
                release_date_obj = datetime.strptime(release_date_str.strip(), "%Y-%m-%d").date()
            except (ValueError, TypeError):
                # 如果失败（例如日期为空、格式错误或为“未知”），则忽略
                click.echo(f"警告: 无法解析电影 '{movie_info['name']}' 的日期 '{release_date_str}'。将设置为空值。")
        # --- 👆 改动结束 ---

        new_movie = Movie(
            name=movie_info["name"],
            cover=movie_info.get("cover"),
            description=movie_info.get("description"),
            release_date=release_date_obj, # 使用处理过的日期对象
            duration_mins=movie_info.get("duration_mins") or 0 # 如果时长为空则默认为0
        )
        db.session.add(new_movie)
        click.echo(f"已添加电影: '{movie_info['name']}'")
    
    db.session.commit()
    click.echo("数据库填充完成。")

@app.cli.command("seed-screens")
def seed_screens():
    """
    为数据库中的电影批量创建模拟场次。
    """
    click.echo("Starting to seed screens...")

    # 获取数据库中所有的电影
    movies = Movie.query.all()
    if not movies:
        click.echo("No movies found in the database. Please run 'flask seed' first.")
        return

    # 模拟的影院和影厅信息
    cinemas = [("万达影城", ["IMAX厅", "4号厅", "情侣厅"]), ("中影国际影城", ["1号厅", "激光厅"])]

    # 默认的座位图
    default_seat_layout = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    for movie in movies:
        # 为每部电影创建 3 个场次
        for i in range(3):
            cinema_name, hall_list = random.choice(cinemas)
            hall_name = random.choice(hall_list)

            # 生成一个未来随机时间点的场次 (未来1-3天内, 10:00 - 22:00 之间)
            start_day = datetime.now() + timedelta(days=random.randint(1, 3))
            start_hour = random.randint(10, 22)
            start_minute = random.choice([0, 15, 30, 45])
            start_time = start_day.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)

            # 随机生成一个票价
            price = random.choice([39.9, 45.0, 49.9, 55.0, 60.0])

            new_screen = Screen(
                movie_id=movie.id,
                cinema_name=cinema_name,
                hall_name=hall_name,
                start_time=start_time,
                price=price,
                seat_layout=default_seat_layout
            )
            db.session.add(new_screen)

    db.session.commit()
    click.echo(f"Successfully added screenings for {len(movies)} movies.")

