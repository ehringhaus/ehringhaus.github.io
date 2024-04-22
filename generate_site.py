import os
import markdown

# Define your input and output directories
posts_directory = './posts'
output_directory = './docs'  # GitHub Pages looks for files in the 'docs' directory by default

# Load your HTML template
with open('./templates/template.html', 'r') as file:
    template = file.read()

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Generate the index page
index_content = "# About\n\n"
index_content += "Hello! We are the team behind 25-50, a social app for buddy matching and goal pursuing.\n\n"
index_content += "# Posts\n\n"
index_content += '''<script data-goatcounter="https://gc-98328744.goatcounter.com/count"
    async src="//gc.zgo.at/count.js"></script>'''

# Convert each Markdown file in the posts directory
for md_filename in os.listdir(posts_directory):
    if md_filename.endswith('.md'):
        # Read the Markdown file
        with open(os.path.join(posts_directory, md_filename), 'r') as md_file:
            md_content = md_file.read()

        # Convert to HTML
        html_content = markdown.markdown(md_content)

        # Create the full HTML page
        post_title = md_filename[:-3].replace('-', ' ').title()
        full_html = template.replace('{{ title }}', post_title).replace('{{ content }}', html_content)

        # Write to the output HTML file
        output_filename = md_filename[:-3] + '.html'
        with open(os.path.join(output_directory, output_filename), 'w') as html_file:
            html_file.write(full_html)

        # Add a link to the post on the index page
        index_content += f"- [{post_title}]({output_filename})\n"

# Write the index page
with open(os.path.join(output_directory, 'index.md'), 'w') as index_file:
    index_file.write(index_content)

print("Static site generated successfully!")