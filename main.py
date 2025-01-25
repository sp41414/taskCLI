import json
import os
from datetime import datetime
import argparse
import sys

class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.filename = 'tasks.json'
        self.next_id = 1
        self.init_json()
        self.load_tasks()
    
    def init_json(self):
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            self.save_tasks()
    
    def load_tasks(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.tasks = data.get('tasks', {})
                self.next_id = data.get('next_id', 1)
                if not self.tasks:
                    self.next_id = 1
        except (json.JSONDecodeError, FileNotFoundError):
            self.tasks = {}
            self.next_id = 1
            self.save_tasks()
    
    def save_tasks(self):
        data = {
            'tasks': self.tasks,
            'next_id': self.next_id
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def add_task(self, name, description):
        task_id = str(self.next_id)
        self.tasks[task_id] = {
            'id': task_id,
            'name': name,
            'description': description,
            'status': 'todo',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.next_id += 1
        self.save_tasks()
        return task_id

    def update_task(self, task_id, **kwargs):
        if task_id not in self.tasks:
            return False
        if 'status' in kwargs:
            if kwargs['status'] not in ['todo', 'in progress', 'done']:
                raise ValueError('invalid status')
        
        self.tasks[task_id].update(kwargs)
        self.tasks[task_id]['last_updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.save_tasks()
        return True
    
    def update_task_name(self, task_id, name):
        if task_id in self.tasks:
            self.tasks[task_id]['name'] = name
            self.tasks[task_id]['last_updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.save_tasks()

    def update_description(self, task_id, description):
        if task_id in self.tasks:
            self.tasks[task_id]['description'] = description
            self.tasks[task_id]['last_updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.save_tasks()

    def delete_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]
            if not self.tasks:
                self.next_id = 1
            self.save_tasks()
            return True
        return False
    
    def list_tasks(self, status=None):
        for task in self.tasks.values():
            if status is None or task['status'] == status:
                print(f"[ID: {task['id']}] {task['name']}\n{task['description']} - ({task['status']})")
                print(f"created: {task['created_at']}")
                print(f"updated: {task['last_updated_at']}\n")

def view_tasks_prompt():
    print("\nwould you like to:")
    print("1. view all tasks")
    print("2. continue without viewing")
    print("3. back to main menu")
    choice = input("enter choice: ")
    return choice

def main():
    manager = TaskManager()
    if len(sys.argv) > 1:
            parser = argparse.ArgumentParser(prog='task-cli')
            subparsers = parser.add_subparsers(dest='command')
            
            # Add task
            add_parser = subparsers.add_parser('add')
            add_parser.add_argument('name', help='Task name')
            add_parser.add_argument('--desc', help='Task description')
            
            # Update description
            update_parser = subparsers.add_parser('update-desc')
            update_parser.add_argument('id', help='Task ID')
            update_parser.add_argument('description', help='New description')
            
            # Update name
            name_parser = subparsers.add_parser('update-name')
            name_parser.add_argument('id', help='Task ID')
            name_parser.add_argument('name', help='New name')
            
            # Update status
            status_parser = subparsers.add_parser('update-status')
            status_parser.add_argument('id', help='Task ID')
            status_parser.add_argument('status', choices=['todo', 'in-progress', 'done'])
            
            # Delete task
            del_parser = subparsers.add_parser('delete')
            del_parser.add_argument('id', help='Task ID')
            
            # List tasks
            list_parser = subparsers.add_parser('list')
            list_parser.add_argument('--status', choices=['todo', 'in-progress', 'done'])
            
            args = parser.parse_args()
            
            try:
                if args.command == 'add':
                    task_id = manager.add_task(args.name, args.desc or "")
                    print(f"task added with id: {task_id}")
                    
                elif args.command == 'update-desc':
                    manager.update_description(args.id, args.description)
                    print("description updated")
                    
                elif args.command == 'update-name':
                    manager.update_task_name(args.id, args.name)
                    print("name updated")
                    
                elif args.command == 'update-status':
                    status = args.status.replace('-', ' ')
                    manager.update_task(args.id, status=status)
                    print("status updated")
                    
                elif args.command == 'delete':
                    if manager.delete_task(args.id):
                        print("task deleted")
                    else:
                        print("invalid task id")
                        
                elif args.command == 'list':
                    status = args.status.replace('-', ' ') if args.status else None
                    manager.list_tasks(status)
                    
            except Exception as e:
                print(f"Error: {e}")
            return
        

    while True:
        try:
            print("\n1. add task\n2. update description\n3. update name\n4. update status\n5. delete task\n6. list all tasks\n7. list todo\n8. list in progress\n9. list done\n10. exit")
            choice = input("enter choice: ")

            if choice in ['2', '3', '4', '5']: 
                view_choice = view_tasks_prompt()
                if view_choice == '1':
                    manager.list_tasks()
                elif view_choice == '3':
                    continue

            if choice == '1':
                naming = input("enter task name (or 'back' to return): ")
                if naming.lower() == 'back':
                    continue
                desc = input("enter task description (or 'back' to return): ")
                if desc.lower() == 'back':
                    continue
                task_id = manager.add_task(naming, desc)
                print(f"task added with id: {task_id}")
            elif choice == '2':
                task_id = input("enter task id (or 'back' to return): ")
                if task_id.lower() == 'back':
                    continue
                if task_id not in manager.tasks:
                    print("invalid task id")
                    continue
                descr = input("enter new description (or 'back' to return): ")
                if descr.lower() == 'back':
                    continue
                manager.update_description(task_id, descr)
                print("description updated")
            elif choice == '3':
                task_id = input("enter task id (or 'back' to return): ")
                if task_id.lower() == 'back':
                    continue
                if task_id not in manager.tasks:
                    print("invalid task id")
                    continue
                name = input("enter new name (or 'back' to return): ")
                if name.lower() == 'back':
                    continue
                manager.update_task_name(task_id, name)
                print("name updated")
            elif choice == '4':
                task_id = input("enter task id (or 'back' to return): ")
                if task_id.lower() == 'back':
                    continue
                if task_id not in manager.tasks:
                    print("invalid task id")
                    continue
                status = input("enter new status (todo/in progress/done) or 'back' to return: ").lower()
                if status == 'back':
                    continue
                if status not in ['todo', 'in progress', 'done']:
                    print("invalid status")
                    continue
                manager.update_task(task_id, status=status)
                print("status updated")
            elif choice == '5':
                task_id = input("enter task id (or 'back' to return): ")
                if task_id.lower() == 'back':
                    continue
                if task_id not in manager.tasks:
                    print("invalid task id")
                    continue
                confirm = input("are you sure you want to delete this task? (y/n): ")
                if confirm.lower() != 'y':
                    continue
                manager.delete_task(task_id)
                print("task deleted")
            elif choice == '6':
                manager.list_tasks()
            elif choice == '7':
                manager.list_tasks('todo')
            elif choice == '8':
                manager.list_tasks('in progress')
            elif choice == '9':
                manager.list_tasks('done')
            elif choice == '10':
                print('exiting...')
                break
            else:
                print('invalid choice')

            input("\npress enter to continue...")

        except KeyboardInterrupt:
            print('\nexiting...')
            break

if __name__ == '__main__':
    main()