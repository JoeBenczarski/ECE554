import asyncio

from scheduler import schedule_tasks

def main():
    asyncio.run(schedule_tasks())

if __name__ == '__main__':
    main()
