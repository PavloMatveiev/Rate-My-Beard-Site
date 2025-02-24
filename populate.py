"""
populate.py

This script automatically populates the database with test data:
– Creates test users (and creates a profile for each with an avatar randomly selected from the test_images folder)
– Creates several posts for each user (with images randomly selected from test_images)
– Creates test comments for each post

Before running, make sure migrations are done:
python manage.py migrate

Run the script with the command:
python populate.py
"""

import os
import random
from datetime import timedelta
from django.utils import timezone
from django.core.files import File
from pathlib import Path

# Setting up the Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RateMyBeard.settings")
import django
django.setup()

from django.db.models import Avg
from django.contrib.auth.models import User
from beard_app.models import Post, Comment, Profile

# Define BASE_DIR (project root)
BASE_DIR = Path(__file__).resolve().parent

# === Configuration variables ===
NUM_USERS = 3                # Number of users to create
NUM_POSTS_PER_USER = 10      # Number of posts for each user
NUM_COMMENTS_PER_POST = 7    # Number of comments for each post

def get_random_image_file():
    """
    Picks a random image file from the test_images folder and returns a django.core.files.File object.
    Supported extensions are .jpg, .jpeg, .png.
    """
    image_dir = BASE_DIR / "test_images"
    valid_extensions = (".jpg", ".jpeg", ".png")
    # Get a list of files with the required extensions
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(valid_extensions)]
    if not image_files:
        raise Exception("No images found in test_images folder!")
    chosen_filename = random.choice(image_files)
    file_path = os.path.join(image_dir, chosen_filename)
    # Open the file in read mode in binary format
    # Each call returns a new file object
    f = open(file_path, "rb")
    return File(f, name=chosen_filename)

def clear_database():
    """
    Clears the database of test data.
    Deletes all comments, posts and profiles.
    Superusers are preserved.
    """
    print("Clearing existing data...")
    Comment.objects.all().delete()
    Post.objects.all().delete()
    Profile.objects.all().delete()
    # Delete all users except the superuser (if there is one)
    User.objects.exclude(is_superuser=True).delete()

def create_users(num_users=NUM_USERS):
    """
    Creates several test users.
    A random avatar is set for each user in the profile.
    Returns a list of created users.
    """
    users = []
    for i in range(num_users):
        username = f"user{i+1}"
        email = f"user{i+1}@example.com"
        password = "password123"
        # Create a user
        user = User.objects.create_user(username=username, email=email, password=password)
        # Create a profile with a random avatar
        avatar = get_random_image_file()
        Profile.objects.create(user=user, avatar=avatar)
        users.append(user)
    return users

def create_posts(users, num_posts_per_user=NUM_POSTS_PER_USER):
    """
    Creates posts for each user.
    For each post, a random image is set in the image field.
    After creating a post, update the created_at field to a random time (from 0 to 30 days ago).
    Returns a list of created posts.
    """
    posts = []
    for user in users:
        for i in range(num_posts_per_user):
            post = Post.objects.create(
                user=user,
                title=f"Post {i+1} by {user.username}",
                description=f"This is a sample description for post {i+1} by {user.username}. " * 5,
                image=get_random_image_file()
            )
            # Generate a random time offset (from 0 to 30 days ago)
            random_days = random.randint(0, 30)
            random_time = timezone.now() - timedelta(days=random_days)
            # Update the created_at field manually
            post.created_at = random_time
            post.save(update_fields=['created_at'])
            posts.append(post)
    return posts


def create_comments(posts, users, num_comments_per_post=NUM_COMMENTS_PER_POST):
    """
    Creates comments for each post.
    For each comment, a random author, text, and rating are selected.
    After comments are created, the comment_count and average_rating fields for the post are updated.
    Returns a list of created comments.
    """
    comments = []
    for post in posts:
        for i in range(num_comments_per_post):
            commenter = random.choice(users)
            comment = Comment.objects.create(
                user=commenter,
                post=post,
                comment=f"This is comment {i+1} on '{post.title}' by {commenter.username}. " * 3,
                rating=random.randint(0, 5),
                created_at=timezone.now() - timedelta(days=random.randint(0, 30))
            )
            comments.append(comment)
        post.comment_count = post.comments.count()
        avg_rating = post.comments.aggregate(avg=Avg('rating'))['avg'] or 0
        post.average_rating = avg_rating
        post.save()
    return comments

if __name__ == "__main__":
    print("Starting filling the database with test data...")

    clear_database()
    users = create_users()
    print(f"{len(users)} users created.")

    posts = create_posts(users)
    print(f"Created {len(posts)} posts.")

    comments = create_comments(posts, users)
    print(f"{len(comments)} comments created.")

    print("Database filling completed!")
