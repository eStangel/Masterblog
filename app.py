from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def index():
    with open("blog_posts.json", "r") as f:
        blog_posts = json.load(f)

    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        with open("blog_posts.json", "r") as f:
            blog_posts = json.load(f)

        blog_id = blog_posts[-1]['id'] + 1
        new_blog_post = {
            "id": blog_id,
            "author": author,
            "title": title,
            "content": content
        }
        blog_posts.append(new_blog_post)

        with open("blog_posts.json", "w") as f:
            json.dump(blog_posts, f, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)