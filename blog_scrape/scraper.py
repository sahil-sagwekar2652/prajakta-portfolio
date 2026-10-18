#!/usr/bin/env python3
"""
Verbatim scraper for https://yatrawithprajakta.blogspot.com
Fetches all posts word-for-word, downloads all images, scrapes comments.
"""

import json
import os
import re
import time
import urllib.request
import urllib.parse
from html.parser import HTMLParser

BLOG_URL = "https://yatrawithprajakta.blogspot.com"
FEED_URL = "https://yatrawithprajakta.blogspot.com/feeds/posts/default?alt=json&max-results=25&start-index=1"
OUTPUT_DIR = "/home/sahil/Desktop/my_work/prajakta-personal-website/blog_scrape"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

POST_URLS = [
    "https://yatrawithprajakta.blogspot.com/2026/03/kalsubai-trek-guide-from-mumbai-route.html",
    "https://yatrawithprajakta.blogspot.com/2025/11/childrens-day-vibe-in-20s.html",
    "https://yatrawithprajakta.blogspot.com/2025/09/tanzania-wildlife-safari-where.html",
    "https://yatrawithprajakta.blogspot.com/2025/09/nakhind-trek-ridge-walk-needle-hole.html",
    "https://yatrawithprajakta.blogspot.com/2025/08/gorakhgad-trek-complete-guide-route.html",
]


def fetch(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            print(f"  [!] Attempt {attempt+1} failed for {url}: {e}")
            time.sleep(2)
    return None


def upgrade_image_url(url):
    """Upgrade Blogger image URLs to highest resolution (/s1600/)."""
    if "bp.blogspot.com" in url or "blogger.com" in url:
        # Replace any /sNNN/ or /wNNN/ with /s1600/
        url = re.sub(r'/s\d+(-[a-z]+)?/', '/s1600/', url)
        url = re.sub(r'/w\d+-h\d+(-[a-z]+)?/', '/s1600/', url)
    return url


def extract_images_from_html(html):
    """Extract all image URLs from HTML content."""
    images = []
    # Find all img src attributes
    img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.IGNORECASE)
    for src in img_srcs:
        if src.startswith("http") and ("blogspot" in src or "bp.blogspot" in src or "blogger" in src or "google" not in src.lower() or "lh" in src):
            images.append(upgrade_image_url(src))
    # Also find any data-src or data-original attributes (lazy loading)
    lazy_srcs = re.findall(r'data-(?:src|original)=["\']([^"\']+)["\']', html, re.IGNORECASE)
    for src in lazy_srcs:
        if src.startswith("http"):
            images.append(upgrade_image_url(src))
    return list(dict.fromkeys(images))  # deduplicate preserving order


def html_to_text(html):
    """Convert HTML to plain text, preserving structure."""
    # Remove script and style blocks
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    # Replace block elements with newlines
    html = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'</p>', '\n\n', html, flags=re.IGNORECASE)
    html = re.sub(r'</div>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'<li[^>]*>', '• ', html, flags=re.IGNORECASE)
    html = re.sub(r'</li>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'<h[1-6][^>]*>', '\n\n### ', html, flags=re.IGNORECASE)
    html = re.sub(r'</h[1-6]>', '\n\n', html, flags=re.IGNORECASE)
    # Remove all remaining tags
    html = re.sub(r'<[^>]+>', '', html)
    # Decode HTML entities
    html = html.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>') \
               .replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ') \
               .replace('&mdash;', '—').replace('&ndash;', '–').replace('&rsquo;', "'") \
               .replace('&ldquo;', '"').replace('&rdquo;', '"').replace('&hellip;', '…') \
               .replace('&#160;', ' ')
    # Collapse excessive newlines
    html = re.sub(r'\n{4,}', '\n\n\n', html)
    return html.strip()


def extract_post_content_from_html(html):
    """Extract the main post content div from raw HTML."""
    # Try to get the post body
    match = re.search(r'<div class=["\']post-body["\'][^>]*>(.*?)</div>\s*</div>\s*<div class=["\']post-footer', html, re.DOTALL | re.IGNORECASE)
    if not match:
        match = re.search(r'<div class=["\']entry-content["\'][^>]*>(.*?)</div>\s*<div class=["\']post-footer', html, re.DOTALL | re.IGNORECASE)
    if not match:
        # More aggressive search
        match = re.search(r'class=["\'][^"\']*post-body[^"\']*["\'][^>]*>(.*?)(?=<div class=["\'][^"\']*post-footer)', html, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    return ""


def download_image(url, dest_dir, prefix="img"):
    """Download an image and return the local filename."""
    try:
        parsed = urllib.parse.urlparse(url)
        ext = os.path.splitext(parsed.path)[1]
        if not ext or len(ext) > 5:
            ext = ".jpg"
        # Create a clean filename
        fname_base = re.sub(r'[^a-zA-Z0-9_-]', '_', parsed.path.replace('/', '_'))[-50:]
        fname = f"{prefix}_{fname_base}{ext}" if not fname_base.endswith(ext) else f"{prefix}_{fname_base}"
        fname = fname.replace('__', '_')
        dest = os.path.join(dest_dir, fname)
        if os.path.exists(dest):
            print(f"    [=] Already exists: {fname}")
            return fname
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(dest, 'wb') as f:
            f.write(data)
        print(f"    [✓] Downloaded: {fname} ({len(data)//1024}KB)")
        return fname
    except Exception as e:
        print(f"    [✗] Failed to download {url}: {e}")
        return None


def fetch_comments(post_id):
    """Fetch all comments for a post via Blogger API."""
    comments = []
    url = f"https://yatrawithprajakta.blogspot.com/feeds/{post_id}/comments/default?alt=json&max-results=100"
    data = fetch(url)
    if not data:
        return comments
    try:
        j = json.loads(data)
        feed = j.get("feed", {})
        entries = feed.get("entry", [])
        for entry in entries:
            comment = {
                "author": entry.get("author", [{}])[0].get("name", {}).get("$t", "Unknown"),
                "date": entry.get("published", {}).get("$t", ""),
                "content": html_to_text(entry.get("content", {}).get("$t", ""))
            }
            comments.append(comment)
    except Exception as e:
        print(f"  [!] Failed to parse comments: {e}")
    return comments


def fetch_all_posts_from_api():
    """Fetch all posts from the Blogger JSON API."""
    print("[*] Fetching posts from Blogger JSON API...")
    data = fetch(FEED_URL)
    if not data:
        print("[!] Failed to fetch feed")
        return []

    j = json.loads(data)
    feed = j.get("feed", {})
    entries = feed.get("entry", [])
    print(f"[*] Found {len(entries)} posts in feed")

    posts = []
    for entry in entries:
        post = {}
        post["title"] = entry.get("title", {}).get("$t", "")
        post["published"] = entry.get("published", {}).get("$t", "")
        post["updated"] = entry.get("updated", {}).get("$t", "")
        post["author"] = entry.get("author", [{}])[0].get("name", {}).get("$t", "")

        # Get URL
        links = entry.get("link", [])
        for link in links:
            if link.get("rel") == "alternate":
                post["url"] = link.get("href", "")
                break

        # Get labels/tags
        post["labels"] = [cat.get("term", "") for cat in entry.get("category", [])]

        # Get post ID (for comments)
        post_id_raw = entry.get("id", {}).get("$t", "")
        id_match = re.search(r'post-(\d+)', post_id_raw)
        post["post_id"] = id_match.group(1) if id_match else ""

        # Get content from API (HTML)
        content_html = entry.get("content", {}).get("$t", "")
        if not content_html:
            content_html = entry.get("summary", {}).get("$t", "")

        post["content_html"] = content_html
        post["content_text"] = html_to_text(content_html)

        # Extract images from API content
        post["images_in_content"] = extract_images_from_html(content_html)

        posts.append(post)
        print(f"  [✓] Got post from API: {post['title'][:60]}")

    return posts


def fetch_post_full_html(url):
    """Fetch a post's full HTML page and extract additional content and images."""
    print(f"  [*] Fetching full HTML: {url}")
    html = fetch(url)
    if not html:
        return None, []

    # Extract all images from the full page
    all_images = extract_images_from_html(html)

    # Filter to just post-relevant images (exclude header/footer/sidebar images)
    post_content_html = extract_post_content_from_html(html)
    post_images = extract_images_from_html(post_content_html) if post_content_html else []

    # Fall back to all images if post extraction failed
    if not post_images:
        post_images = [img for img in all_images if "bp.blogspot.com" in img or "lh" in img]

    # Get comment count from HTML
    comment_count = 0
    count_match = re.search(r'(\d+)\s+[Cc]omments?', html)
    if count_match:
        comment_count = int(count_match.group(1))

    return post_images, comment_count


def main():
    os.makedirs(IMAGES_DIR, exist_ok=True)

    print("=" * 60)
    print("YatraWithPrajakta Blog Scraper")
    print("=" * 60)

    # Step 1: Fetch all posts from API
    posts = fetch_all_posts_from_api()

    if not posts:
        print("[!] No posts found from API. Aborting.")
        return

    # Step 2: For each post, fetch full HTML for images + comments
    print("\n[*] Fetching full post pages and downloading images...")
    for i, post in enumerate(posts):
        post_url = post.get("url", "")
        if not post_url:
            continue

        print(f"\n--- Post {i+1}/{len(posts)}: {post['title'][:55]}...")

        # Fetch full page for images
        page_images, comment_count = fetch_post_full_html(post_url)
        post["comment_count"] = comment_count

        # Merge images: API content images + page images
        all_img_urls = list(dict.fromkeys(post["images_in_content"] + (page_images or [])))
        post["image_urls"] = all_img_urls

        # Download images
        post["downloaded_images"] = []
        prefix = f"post{i+1}_{re.sub(r'[^a-z0-9]', '', post['title'].lower()[:20])}"
        for j, img_url in enumerate(all_img_urls):
            print(f"    Downloading image {j+1}/{len(all_img_urls)}: {img_url[:70]}...")
            fname = download_image(img_url, IMAGES_DIR, prefix=f"{prefix}_img{j+1}")
            if fname:
                post["downloaded_images"].append({
                    "url": img_url,
                    "local_file": f"images/{fname}"
                })
        time.sleep(1)

        # Fetch comments
        if post.get("post_id"):
            print(f"  [*] Fetching comments for post ID {post['post_id']}...")
            post["comments"] = fetch_comments(post["post_id"])
            print(f"  [✓] Got {len(post['comments'])} comments")
        else:
            post["comments"] = []

    # Step 3: Also fetch blog homepage for author bio / sidebar
    print("\n[*] Fetching blog homepage for sidebar info...")
    homepage_html = fetch(BLOG_URL)
    author_bio = ""
    blog_title = "YatraWithPrajakta"
    if homepage_html:
        bio_match = re.search(r'class=["\'][^"\']*profile-bio[^"\']*["\'][^>]*>(.*?)</div>', homepage_html, re.DOTALL | re.IGNORECASE)
        if bio_match:
            author_bio = html_to_text(bio_match.group(1))
        title_match = re.search(r'<title>(.*?)</title>', homepage_html, re.IGNORECASE)
        if title_match:
            blog_title = html_to_text(title_match.group(1))

    # Step 4: Build final output
    output = {
        "blog": {
            "title": blog_title,
            "url": BLOG_URL,
            "author": "Prajakta",
            "author_bio": author_bio,
            "total_posts": len(posts),
            "scrape_date": "2026-10-13"
        },
        "posts": []
    }

    for post in posts:
        output["posts"].append({
            "title": post.get("title", ""),
            "url": post.get("url", ""),
            "published": post.get("published", ""),
            "updated": post.get("updated", ""),
            "author": post.get("author", ""),
            "labels": post.get("labels", []),
            "post_id": post.get("post_id", ""),
            "comment_count": post.get("comment_count", 0),
            "content_verbatim": post.get("content_text", ""),
            "content_html": post.get("content_html", ""),
            "image_urls": post.get("image_urls", []),
            "downloaded_images": post.get("downloaded_images", []),
            "comments": post.get("comments", [])
        })

    # Save JSON
    json_path = os.path.join(OUTPUT_DIR, "scraped_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n[✓] Saved JSON: {json_path}")

    # Save Markdown
    md_lines = []
    md_lines.append(f"# {output['blog']['title']} — Complete Blog Scrape\n")
    md_lines.append(f"> Blog: {BLOG_URL}  \n> Scraped: 2026-10-13  \n> Total Posts: {len(posts)}\n")
    md_lines.append("---\n")
    md_lines.append(f"## Author Bio\n\n{author_bio}\n\n---\n")

    for i, post in enumerate(output["posts"]):
        md_lines.append(f"## Post {i+1}: {post['title']}\n")
        md_lines.append(f"- **URL:** {post['url']}")
        md_lines.append(f"- **Published:** {post['published']}")
        md_lines.append(f"- **Author:** {post['author']}")
        md_lines.append(f"- **Labels:** {', '.join(post['labels']) if post['labels'] else 'None'}")
        md_lines.append(f"- **Comments:** {post['comment_count']}\n")

        if post["downloaded_images"]:
            md_lines.append(f"### Images ({len(post['downloaded_images'])} downloaded)\n")
            for img in post["downloaded_images"]:
                md_lines.append(f"- [{img['local_file']}]({img['url']})")
            md_lines.append("")

        md_lines.append("### Full Content (Verbatim)\n")
        md_lines.append(post["content_verbatim"])
        md_lines.append("")

        if post["comments"]:
            md_lines.append(f"### Comments ({len(post['comments'])})\n")
            for c in post["comments"]:
                md_lines.append(f"**{c['author']}** _{c['date']}_:")
                md_lines.append(f"> {c['content']}\n")

        md_lines.append("\n---\n")

    md_path = os.path.join(OUTPUT_DIR, "scraped_data.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"[✓] Saved Markdown: {md_path}")

    # Print summary
    print("\n" + "=" * 60)
    print("SCRAPE COMPLETE")
    print("=" * 60)
    total_images = sum(len(p["downloaded_images"]) for p in output["posts"])
    total_comments = sum(len(p["comments"]) for p in output["posts"])
    print(f"Posts scraped:    {len(output['posts'])}")
    print(f"Images downloaded:{total_images}")
    print(f"Comments scraped: {total_comments}")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
