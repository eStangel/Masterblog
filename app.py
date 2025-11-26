from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def index():
    """Fetches all blog posts from the JSON file and renders the homepage."""
    blog_posts = read_file()

    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Displays a form to add a new blog post and saves it when submitted."""
    if request.method == 'POST':
        author = request.form.get('author', default='Guest')
        title = request.form.get('title', default='Title')
        content = request.form.get('content', default='Content')

        blog_posts = read_file()
        if blog_posts:
            blog_id = blog_posts[-1]['id'] + 1
        else:
            blog_id = 1
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
    """Deletes the blog post with the given ID and redirects to the homepage."""
    blog_posts = read_file()

    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    write_file(blog_posts)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Loads a blog post for editing and updates it when the form is submitted."""
    blog_posts = read_file()

    post, blog_post_index = get_post_by_id(blog_posts, post_id)
    if post is None:
        return "Post not found", 404
    if request.method == 'POST':
        author = request.form.get('author', default='Guest')
        title = request.form.get('title', default='Title')
        content = request.form.get('content', default='Content')

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
    """
    Returns the blog post and its index for the given ID,
    or (None, None) if not found.
    """
    for i in range(len(posts)):
        if posts[i]['id'] == post_id:
          return posts[i], i
    return None, None


def read_file():
    """Reads all blog posts from the JSON file and returns them as a list."""
    try:
        with open("blog_posts.json", "r") as f:
            blog_posts = json.load(f)
        return blog_posts
    except FileNotFoundError:
        return []


def write_file(blog_posts):
    """Writes the list of blog posts back to the JSON file with indentation."""
    with open("blog_posts.json", "w") as f:
        json.dump(blog_posts, f, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)