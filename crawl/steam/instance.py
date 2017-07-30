import os

broker_url = "redis://redis/0"

instance_path = os.path.abspath(__file__)
current_dir = os.path.dirname(instance_path)
application_dir = os.path.dirname(current_dir)
project_dir = os.path.dirname(application_dir)
logs_dir = "/data/logs/steam"
crawl_logs_dir = os.path.join(logs_dir, "crawl")
