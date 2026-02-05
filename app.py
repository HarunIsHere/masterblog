import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

POSTS_FILE = "posts.json"


def load_posts():
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_posts(posts):
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)


def next_id(posts):
    if not posts:
        return 1
    return max(post["id"] for post in posts) + 1


def fetch_post_by_id(posts, post_id):
    for p in posts:
        if p["id"] == post_id:
            return p
    return None


@app.route("/")
def index():
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        posts = load_posts()

        author = request.form.get("author", "").strip()
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        # minimal validation (no empty posts)
        if author and title and content:
            posts.append(
                {
                    "id": next_id(posts),
                    "author": author,
                    "title": title,
                    "content": content,
                }
            )
            save_posts(posts)

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:post_id>")
def delete(post_id):
    posts = load_posts()
    posts = [p for p in posts if p["id"] != post_id]
    save_posts(posts)
    return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    posts = load_posts()
    post = fetch_post_by_id(posts, post_id)
    if post is None:
        return "Post not found", 404

    if request.method == "POST":
        author = request.form.get("author", "").strip()
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if author and title and content:
            post["author"] = author
            post["title"] = title
            post["content"] = content
            save_posts(posts)

        return redirect(url_for("index"))

    return render_template("update.html", post=post)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

