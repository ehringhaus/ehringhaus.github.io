import os
import datetime
import markdown
import frontmatter
import shutil
import platform

# Define your input and output directories
posts_directory = './posts'
output_directory = './docs'  # GitHub Pages looks for files in the 'docs' directory by default

# Load the index template
with open('./templates/index-template.html', 'r') as file:
    index_template = file.read()

# Load the post template
with open('./templates/post-template.html', 'r') as file:
    post_template = file.read()

# Remove all existing files in the output directory
if os.path.exists(output_directory):
    shutil.rmtree(output_directory)
os.makedirs(output_directory, exist_ok=True)

# Get the list of post directories
post_dirs = [d for d in os.listdir(posts_directory) if os.path.isdir(os.path.join(posts_directory, d))]
sorted_posts = sorted(post_dirs, key=lambda x: os.path.getctime(os.path.join(posts_directory, x)), reverse=True)

grouped_posts = {}

# Convert each Markdown file in the post directories
for post_dir in sorted_posts:
    md_files = [f for f in os.listdir(os.path.join(posts_directory, post_dir)) if f.endswith('.md')]
    for md_filename in md_files:
        # Read the Markdown file
        with open(os.path.join(posts_directory, post_dir, md_filename), 'r') as md_file:
            post = frontmatter.load(md_file)

        # Get the creation time of the markdown file
        creation_time = os.stat(os.path.join(posts_directory, post_dir, md_filename)).st_birthtime
        creation_datetime = datetime.datetime.fromtimestamp(creation_time)
        year = creation_datetime.year
        month = creation_datetime.month

        # Convert the content to HTML
        html_content = markdown.markdown(post.content)

        # Extract the front matter
        post_title = post['title']
        post_subtitle = post.get('subtitle', '')

        # Create the full HTML page for individual posts
        post_html = post_template.replace('{{ title }}', post_title)
        post_html = post_html.replace('{{ subtitle }}', post_subtitle)
        post_html = post_html.replace('{{ content }}', html_content)
        post_html = post_html.replace('{% if is_post %}', '').replace('{% endif %}', '')

        # Write to the output HTML file for individual posts
        output_dir = os.path.join(output_directory, post_dir)
        os.makedirs(output_dir, exist_ok=True)
        output_filename = md_filename[:-3] + '.html'
        with open(os.path.join(output_dir, output_filename), 'w') as html_file:
            html_file.write(post_html)

        # Copy the associated images to the output directory
        for filename in os.listdir(os.path.join(posts_directory, post_dir)):
            if filename != md_filename:
                shutil.copy(os.path.join(posts_directory, post_dir, filename), output_dir)

        # Group posts by year and month
        year_month = f"{year}-{month:02d}"
        if year_month not in grouped_posts:
            grouped_posts[year_month] = []
        grouped_posts[year_month].append(f"<a href='{post_dir}/{output_filename}'>{post_title}</a>")

# Generate the grouped_posts content
grouped_posts_content = ""
for year_month, posts in sorted(grouped_posts.items(), reverse=True):
    grouped_posts_content += f"\n<h2>{datetime.datetime.strptime(year_month, '%Y-%m').strftime('%B %Y')}</h2>\n"
    for post_link in posts:
        grouped_posts_content += f"<div class='post-link'>{post_link}</div>\n"

# Generate the index HTML
index_html = index_template.replace('{{ grouped_posts }}', grouped_posts_content)

# Write the index page
with open(os.path.join(output_directory, 'index.html'), 'w') as index_file:
    index_file.write(index_html)

print("Static site generated successfully!")