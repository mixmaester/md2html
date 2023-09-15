# md2website: markdown to static website builder

import os
import re
import shutil
import markdown
from datetime import datetime

DIST_PATH = "../michaelsjoberg.com/dist"
ASSETS = ["main.css", "main.js", "highlight.min.js", "fav.png"]
AUTHOR = "Michael Sjöberg"
DESCRIPTION = "My projects, posts, and programming notes."
APP_NAME = "Michael Sjöberg"
APP_THEME = "#161716"
SHOW_RECENT_POSTS = True

# for listing all posts on index page
GLOBAL_POSTS = [] # [ { title, date, url } ]

def sort_by_date_and_title(item):
    return (item["date"], item["title"])

def write_header(file, title="Static website built with md2website", root=0):
    file.write("<!DOCTYPE html>\n")
    file.write("""
    <!--
    ████████████████████████████████████████████████████████████████
    █▄─▀█▀─▄█▄─▄▄▀█▀▄▄▀█▄─█▀▀▀█─▄█▄─▄▄─█▄─▄─▀█─▄▄▄▄█▄─▄█─▄─▄─█▄─▄▄─█
    ██─█▄█─███─██─██▀▄███─█─█─█─███─▄█▀██─▄─▀█▄▄▄▄─██─████─████─▄█▀█
    █▄▄▄█▄▄▄█▄▄▄▄██▄▄▄▄██▄▄▄█▄▄▄██▄▄▄▄▄█▄▄▄▄██▄▄▄▄▄█▄▄▄██▄▄▄██▄▄▄▄▄█
    This static website was built by github.com/mrsjoberg/md2website
    -->
    """.replace("    ", ""))
    file.write("<html lang='en'>")
    file.write("<head>")
    # favicon
    # file.write("<link rel='icon' href='fav.png'>")
    # title
    file.write(f"<title>{title}</title>")
    # meta
    file.write("<meta charset='utf-8'>")
    file.write("<meta name='viewport' content='width=device-width, initial-scale=1'>")
    file.write(f"<meta name='author' content='{AUTHOR}'>")
    file.write(f"<meta name='description' content='{DESCRIPTION}'>")
    file.write(f"<meta name='theme-color' content='{APP_THEME}'>")
    file.write(f"<meta name='application-name' content='{APP_NAME}'>")
    file.write(f"<meta name='apple-mobile-web-app-title' content='{title}'>")
    file.write("<meta name='apple-mobile-web-app-capable' content='yes'>")
    file.write("<meta name='mobile-web-app-capable' content='yes'>")
    file.write(f"<meta name='apple-mobile-web-app-status-bar-style' content='{APP_THEME}'>")
    # css
    # file.write(f"<link rel='stylesheet' href='{'../'*root}main.min.css'>")
    file.write("<style>")
    css_file = open(f"{DIST_PATH}/main.min.css", "r")
    css_content = css_file.read()
    css_file.close()
    file.write(css_content)
    file.write("</style>")
    # js
    # file.write(f"<script src='{'../'*root}main.min.js'></script>")
    file.write("</head>")
    # -------------------------------------------
    file.write("<body>")
    # fixed nav
    file.write("<div class='nav'>")
    try:
        nav_file = open("nav.md", "r")
        nav_content = nav_file.read()
        nav_file.close()
        if nav_content != "":
            file.write(markdown.markdown(nav_content))
        else:
            raise
    except:
        file.write(f"<p><a href='{'../'*root}index.html'>home</a></p>")
    file.write("</div>")
    file.write("<div class='page'>")

def write_footer(file):
    file.write("</div>")
    file.write("<div id='footer'>")
    file.write("<p>[<a id='invert'>light|dark</a>]</p>")
    file.write(f"<p class='small'>This static website was built by <a href='https://github.com/mrsjoberg/md2website'>md2website</a> on {datetime.now().strftime('%B %d, %Y')}. DOM loaded in <span id='dom_time'></span> and page loaded in <span id='load_time'></span>.</p>")
    file.write("</div>")
    file.write("<script>")
    js_file = open(f"{DIST_PATH}/main.min.js", "r")
    js_content = js_file.read()
    js_file.close()
    file.write(js_content)
    file.write("</script>")
    file.write("</body>")
    file.write("</html>")

# create dist folder
if os.path.isdir(DIST_PATH): shutil.rmtree(DIST_PATH)
os.mkdir(DIST_PATH)

# minimize css
with open(f"{DIST_PATH}/main.min.css", "w+") as file:
    css_content = ""
    for css in [asset for asset in ASSETS if asset.split(".")[-1] == "css"]:
        tmp_file = open(css, "r")
        css_content += tmp_file.read()
        tmp_file.close()
    css_content = css_content.replace("\n", "")
    css_content = css_content.replace("\t", "")
    css_content = css_content.replace("  ", "")
    file.write(css_content)

# minimize js
with open(f"{DIST_PATH}/main.min.js", "w+") as file:
    js_content = ""
    for js in [asset for asset in ASSETS if asset.split(".")[-1] == "js"]:
        tmp_file = open(js, "r")
        js_content += tmp_file.read()
        tmp_file.close()
    js_content = js_content.replace("  ", "")
    js_content = "\n".join([line for line in js_content.split("\n") if not line.startswith("//")])
    js_content = js_content.replace("\n", "")
    js_content = js_content.replace("\t", "")
    # write
    file.write(js_content)

# copy non-css and non-js assets
# for asset in [asset for asset in ASSETS if asset.split(".")[-1] not in ["css", "js"]]:
#     os.system(f"cp {asset} {DIST_PATH}/{asset}")

# for each folder in root dir, create list page with content
for dir_ in os.listdir("."):
    if "." not in dir_ and dir_ != "dist" and dir_ != "pages":
        with open(f"{DIST_PATH}/{dir_}.html", "w+") as dir_page:
            write_header(dir_page, title=dir_.title())
            posts_lst = [] # [ { title, date, url } ]
            posts_dict = {} # { category: { subcategory: [ { title, date, url } ] } }
            # for each md file in dir_, create html page and append to posts_lst or posts_dict
            for root, dirs, posts in os.walk(dir_):
                for post in posts:
                    if post.split(".")[1] == "md":
                        post_name = post.split(".")[0]
                        # create page
                        with open(f"{DIST_PATH}/{post_name}.html", "w+") as tmp_file:
                            post_file = open(f"{root}/{post}")
                            post_content = post_file.read()
                            # title
                            title = post_content.split("\n")[0].split("# ")[1]
                            # date
                            date = post_content.split("\n")[2].split("*")[1]
                            # categories
                            category = None
                            subcategory = None
                            try:
                                category = post_content.split("\n")[2].split("*")[2].strip().split(" ", 1)[0].split("]")[0][1:].lower()
                                subcategory = post_content.split("\n")[2].split("*")[2].strip().split(" ", 1)[1].split("]")[0][1:].lower()
                            except:
                                pass
                            # category and subcategory
                            if category and subcategory:
                                if not category in posts_dict: posts_dict[category] = {}
                                if not subcategory in posts_dict[category]: posts_dict[category][subcategory] = []
                                # append
                                posts_dict[category][subcategory].append({ "title": title, "date": datetime.strptime(date, "%B %Y"), "url": post_name })
                            # category
                            elif category:
                                if not category in posts_dict: posts_dict[category] = []
                                # append
                                posts_dict[category].append({ "title": title, "date": datetime.strptime(date, "%B %Y"), "url": post_name })
                            else:
                                # append to posts_lst
                                posts_lst.append({ "title": title, "date": datetime.strptime(date, "%B %Y"), "url": post_name })
                            # finally, append to global
                            GLOBAL_POSTS.append({ "title": title, "date": datetime.strptime(date, "%B %Y"), "url": post_name })
                            # write
                            write_header(tmp_file, title=title)
                            tmp_file.write(markdown.markdown(post_content, extensions=["fenced_code", "tables"]))
                            write_footer(tmp_file)
                            post_file.close()
            # sort posts_lst by date then by name
            sorted_posts_lst = sorted(posts_lst, key=sort_by_date_and_title, reverse=True)
            # write posts_lst (list by date)
            current_date = None
            for post in sorted_posts_lst:
                if current_date != post['date'].year:
                    if current_date != None:
                        dir_page.write("</ul>")
                    dir_page.write(f"<h1>{post['date'].year}</h1>")
                    current_date = post['date'].year
                    dir_page.write("<ul>")
                dir_page.write(f"<li><a href='{post['url']}.html'>{post['title']}</a></li>")
            # create list with categories for ordering
            category_list = sorted(posts_dict.keys())
            # list newest posts on top
            all_posts = [post for category in category_list for subcategory in posts_dict[category] for post in posts_dict[category][subcategory]]
            sorted_all_posts = sorted(all_posts, key=sort_by_date_and_title, reverse=True)
            for post in sorted_all_posts:
                # if date is current or last month
                if post['date'].year == datetime.now().year and post['date'].month == datetime.now().month or post['date'].year == datetime.now().year and post['date'].month == datetime.now().month - 1:
                    dir_page.write(f"<p><mark>new</mark> <a href='{post['url']}.html'>{post['title']}</a></p>")
            # write posts in posts_dict (list by category and subcategory)
            for category in category_list:
                # write category
                dir_page.write(f"<h1 id='{category}'>{category.title()}</h1>")
                for subcategory in posts_dict[category]:
                    if len(posts_dict[category].keys()) > 1:
                        dir_page.write(f"<p id='{category}-{subcategory.replace(' ', '-')}'>{subcategory.title()}</p>")
                    sorted_posts_dict = sorted(posts_dict[category][subcategory], key=sort_by_date_and_title, reverse=True)
                    dir_page.write("<ul>")
                    for post in sorted_posts_dict:
                        # if date is current or last month
                        if post['date'].year == datetime.now().year and post['date'].month == datetime.now().month or post['date'].year == datetime.now().year and post['date'].month == datetime.now().month - 1:
                            dir_page.write(f"<li><mark>new</mark> <a href='{post['url']}.html'>{post['title']}</a></li>")
                        else:    
                            dir_page.write(f"<li><a href='{post['url']}.html'>{post['title']}</a></li>")
                    dir_page.write("</ul>")
            write_footer(dir_page)

# for each md file in pages, create html page
for root, dirs, files in os.walk("pages"):
    for file in files:
        if file.split(".")[1] == "md":
            file_name = file.split(".")[0]
            # create page
            with open(f"{DIST_PATH}/{file_name}.html", "w+") as tmp_file:
                file = open(f"{root}/{file}", "r")
                file_content = file.read()
                title = file_content.split("\n")[0].split("# ")[1]
                # generate anchors
                file_content = re.sub(r"## (.*)", r"## <a name='\1' class='anchor'></a> [\1](#\1)", file_content)
                # write
                write_header(tmp_file, title)
                tmp_file.write(markdown.markdown(file_content, extensions=["fenced_code", "tables"]))
                # list recent posts
                if SHOW_RECENT_POSTS and file_name == "index":
                    # tmp_file.write("<h1>Recent</h1>")
                    # list newest posts on top
                    sorted_global_posts = sorted(GLOBAL_POSTS, key=sort_by_date_and_title, reverse=True)
                    for post in sorted_global_posts:
                        # if date is current or last month
                        if post['date'].year == datetime.now().year and post['date'].month == datetime.now().month or post['date'].year == datetime.now().year and post['date'].month == datetime.now().month - 1:
                            tmp_file.write(f"<p><mark>new</mark> <a href='{post['url']}.html'>{post['title']}</a></p>")
                write_footer(tmp_file)
                file.close()
