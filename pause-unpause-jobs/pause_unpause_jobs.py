from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import PauseStatus, JobSettings, CronSchedule, TriggerSettings
import argparse
import json
import os

default_file_name = "paused_jobs.json"


def find_jobs_with_schedule(wc: WorkspaceClient) -> dict[int, dict]:
    jobs_with_schedule_or_trigger = {}
    jobs = wc.jobs.list()
    for job in jobs:
        if job.settings.schedule and job.settings.schedule.pause_status == PauseStatus.UNPAUSED:
            # print(f"Job {job.settings.name} has a schedule. {job.settings.schedule.pause_status}")
            jobs_with_schedule_or_trigger[job.job_id] = {
                "name": job.settings.name,
                "type": "schedule",
                "data": job.settings.schedule.as_dict()
            }
        elif job.settings.trigger and job.settings.trigger.pause_status == PauseStatus.UNPAUSED:
            # print(f"Job {job.settings.name} has a trigger: {job.settings.trigger.pause_status}")
            jobs_with_schedule_or_trigger[job.job_id] = {
                "name": job.settings.name,
                "type": "trigger",
                "data": job.settings.trigger.as_dict()
            }

    return jobs_with_schedule_or_trigger


def switch_pause_status(wc: WorkspaceClient, jid:int, job_config: dict, pause: bool):
    new_settings = JobSettings()
    pause_status = PauseStatus.PAUSED if pause else PauseStatus.UNPAUSED
    if job_config['type'] == 'schedule':
        new_settings.schedule = CronSchedule.from_dict(job_config['data'])
        new_settings.schedule.pause_status = pause_status
    elif job_config['type'] == 'trigger':
        new_settings.trigger = TriggerSettings.from_dict(job_config['data'])
        new_settings.trigger.pause_status = pause_status
    else:
        print(f"Unknown job type {job_config['type']} for job {jid}")
        return
    wc.jobs.update(jid, new_settings=new_settings)


if __name__ == '__main__':
    # parse arguments for the script that supports three commands: list, pause, unpause
    parser = argparse.ArgumentParser(description='Pause or unpause Databricks jobs with schedules or triggers')
    supported_commands = ['scan', 'pause', 'unpause']
    parser.add_argument('command', choices=supported_commands)
    parser.add_argument('--file', default=default_file_name,
                        help=f'File to store paused jobs (default: {default_file_name})')
    args = parser.parse_args()
    if args.command not in supported_commands:
        print(f"Unknown command {args.command}")
        exit(1)
    wc = WorkspaceClient()
    if args.command == 'scan':
        jobs = find_jobs_with_schedule(wc)
        if jobs:
            print("Jobs with schedules or triggers:")
            for k, v in jobs.items():
                print(f"Job ID: {k}, Name: {v['name']}, Type: {v['type']}")
    elif args.command == 'pause':
        print("Pausing jobs...")
        jobs = find_jobs_with_schedule(wc)
        print(f"Found {len(jobs)} jobs with schedules or triggers. Pausing them...")
        for job_id, job in jobs.items():
            print(f"Pausing job '{job['name']}' with ID {job_id}")
            switch_pause_status(wc, job_id, job, True)
        with open(args.file, "w") as f:
            f.write(json.dumps(jobs))
        print(f"Jobs are paused. The list of paused jobs is saved in {args.file}")
    elif args.command == 'unpause':
        print(f"Unpausing jobs from {args.file}")
        with open(args.file, "r") as f:
            jobs = json.load(f)
            for job_id, job in jobs.items():
                print(f"Unpausing job '{job['name']}' with ID {job_id}")
                switch_pause_status(wc, int(job_id), job, False)
        print(f"Jobs are unpaused. Removing {args.file}...")
        os.remove(args.file)


