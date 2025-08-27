import os
import click
import json
from datetime import datetime
from app import create_app, db
from app.models import Movie
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
