from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def index():
    blog_posts = read_file()

    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        blog_posts = read_file()

        blog_id = blog_posts[-1]['id'] + 1
        new_blog_post = {
            "id": blog_id,
            "author": author,
            "title": title,
            "content": content
        }
        blog_posts.append(new_blog_post)

        write_file(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    blog_posts = read_file()

    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    write_file(blog_posts)

    return redirect(url_for('index'))


def read_file():
    with open("blog_posts.json", "r") as f:
        blog_posts = json.load(f)
    return blog_posts


def write_file(blog_posts):
    with open("blog_posts.json", "w") as f:
        json.dump(blog_posts, f, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)