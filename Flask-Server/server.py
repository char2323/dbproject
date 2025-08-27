import os
import click
from datetime import datetime
from app import create_app, db
from app.models import Movie
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

@app.cli.command("seed")
def seed():
    """向数据库中批量添加初始电影数据。"""
    movies_data = [
        {
            "name": "霸王别姬",
            "cover": "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2561716440.jpg",
            "description": "影片围绕两位京剧伶人半个世纪的悲欢离合，展现了对传统文化、人的生存状态及人性的思考与领悟。",
            "release_date": "1993-01-01",
            "duration_mins": 171
        },
        {
            "name": "盗梦空间",
            "cover": "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p513344864.jpg",
            "description": "多姆·柯布是一位经验老道的窃贼，他能够潜入人们精神最为脆弱的梦境中，窃取潜意识里的宝贵秘密。",
            "release_date": "2010-09-01",
            "duration_mins": 148
        }
    ]

    click.echo("Starting database seeding...")

    for movie_info in movies_data:
        existing_movie = Movie.query.filter_by(name=movie_info["name"]).first()
        if existing_movie:
            click.echo(f"Movie '{movie_info['name']}' already exists, skipping.")
            continue
        
        new_movie = Movie(
            name=movie_info["name"],
            cover=movie_info.get("cover"),
            description=movie_info.get("description"),
            release_date=datetime.strptime(movie_info["release_date"], "%Y-%m-%d").date(),
            duration_mins=movie_info.get("duration_mins")
        )
        db.session.add(new_movie)
        click.echo(f"Added movie: '{movie_info['name']}'")
    
    db.session.commit()
    click.echo("Database seeding completed.")
