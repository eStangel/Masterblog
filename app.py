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


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = read_file()

    post, blog_post_index = get_post_by_id(blog_posts, post_id)
    if post is None:
        return "Post not found", 404
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        blog_posts.pop(blog_post_index)

        updated_blog_post = {
            "id": post['id'],
            "author": author,
            "title": title,
            "content": content
        }

        blog_posts.insert(blog_post_index, updated_blog_post)

        write_file(blog_posts)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


def get_post_by_id(posts, post_id):
    for i in range(len(posts)):
        if posts[i]['id'] == post_id:
          return posts[i], i
    return None, None


def read_file():
    with open("blog_posts.json", "r") as f:
        blog_posts = json.load(f)
    return blog_posts


def write_file(blog_posts):
    with open("blog_posts.json", "w") as f:
        json.dump(blog_posts, f, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)