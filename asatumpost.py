#!/usr/bin/env python3

from datetime import datetime
import random
import sys

import asana
import pytumblr

import settings
from TaskScanner import TaskScanner
from AsanaOperations import AsanaOperations
from helper import user_select_option


def pick_task_for_publication(ts):

    general_bag_of_tasks = []
    today_tasks = []

    for i, val in enumerate(ts):
        tags_list = []
        if val["completed"] is False and val["assignee"] != "":

            if not val["tags"] and val["notes"] != "":
                for tag in val["tags"]:
                    tags_list.append(asana_client.tags.find_by_id(tag=tag["id"])["name"])

                val["tags"] = tags_list
                general_bag_of_tasks.append(val)

            if val["due_on"] is not None and val["due_on"] == datetime.today().strftime("%Y-%m-%d"):
                today_tasks.append(val)
                continue

    try:
        if not today_tasks:
            post = today_tasks[0]
        else:
            post = random.choice(general_bag_of_tasks)
        return post

    except IndexError:
        print("No tasks on Asana, that meet requirements to post on Tumblr!")
        exit(0)


def get_blog_name(client):

    client_info = client.info()
    if "meta" in client_info and "status" in client_info["meta"] and client_info["meta"]["status"] == 401:
        print("Your Tumblr credentials seem so fucked up!")
        exit(1)
    blogs = client_info["user"]["blogs"]
    blog_name = user_select_option("Please choose a blog", blogs)["name"]
    return blog_name

def scan_pc_and_update_asana(client):
    scanner = TaskScanner()
    print("Scanning folder for asana tasks...")
    scanner.get_file_list()
    tasks_to_post_on_asana = scanner.get_tasks_list()
    asana_operator = AsanaOperations(asana_client)
    asana_operator.load_tags()
    asana_operator.post_on_asana(tasks_to_post_on_asana)

def scan_asana_and_update_tumblr(as_client, tum_client):
    asana_operator = AsanaOperations(as_client)
    project_id = asana_operator.get_project("Pick project to upload tasks from Asana to Tumblr:")
    tasks = asana_operator.get_tasks(project_id)
    post_for_tumblr = pick_task_for_publication(tasks)
    blog_name = get_blog_name(tum_client)
    tum_client.create_video(blog_name, state="queue", tags=post_for_tumblr["tags"],
                            embed=post_for_tumblr["notes"])

    stripped_note = post_for_tumblr["notes"].strip()
    posts = tum_client.queue(blog_name)["posts"]
    last_post = posts[-1]
    scheduled_publish_time = last_post["scheduled_publish_time"]
    permalink = last_post["permalink_url"]
    if stripped_note in permalink:
        mark_as_done = user_select_option("Mark task as done?", [{"name": "No"}, {"name": "Yes"}])["name"]
        if "Yes" in mark_as_done:
            asana_client.tasks.update(post_for_tumblr["id"], {"completed": True})
            message = "and marked"
        elif "No" in mark_as_done:
            message = "without marking"
        scheduled_timestamp = datetime.fromtimestamp(int(scheduled_publish_time)).strftime("%Y-%m-%d %H:%M:%S")
        print(
            "Post scheduled for publication at %s on Tumblr %s as completed on Asana" % (scheduled_timestamp, message))
    else:
        print("Shit went wrong!")


if __name__ == "__main__":

    asana_client = asana.Client.access_token(settings.ASANA_PERSONAL_ACCESS_TOKEN)

    tum_client = pytumblr.TumblrRestClient(
        settings.TUMBLR_CONSUMER_KEY,
        settings.TUMBLR_SECRET_KEY,
        settings.TUMBLR_OAUTH_TOKEN,
        settings.TUMBLR_OAUTH_SECRET
    )

    options = ["Scan local path to update Asana tasks", "Scan Asana to add new Tumblr posts"]
    print("What would you like to do?")
    for i, val in enumerate(options):
        print(i, ': ', val)
    action = int(input("Enter choice (default 0): ") or 0)

    if action == 0:
        scan_pc_and_update_asana(asana_client)
    elif action == 1:
        scan_asana_and_update_tumblr(asana_client, tum_client)
    else:
        print("Wrong option!")
        sys.exit(1)
