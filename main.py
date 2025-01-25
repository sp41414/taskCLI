import json
import os
from datetime import datetime

class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.filename = 'tasks.json'
        self.init_json()
        self.load_tasks()
    
    def init_json(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({'tasks': {}}, f, indent=4)
        elif os.path.getsize(self.filename) == 0:
            with open(self.filename, 'w') as f:
                json.dump({'tasks': {}}, f, indent=4)
    
    def load_tasks(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.tasks = data.get('tasks', {})
        except json.JSONDecodeError:
            self.tasks = {}
            self.save_tasks()
    
    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump({'tasks': self.tasks}, f, indent=4)
    
    def add_task(self, name, description):
        task_id = str(len(self.tasks) + 1)
        self.tasks[task_id] = {
            'id': task_id,
            'name': name,
            'description': description,
            'status': 'todo',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.save_tasks()
        return task_id

    def update_task(self, task_id, status):
        if task_id in self.tasks:
            self.tasks[task_id]['status'] = status
            self.tasks[task_id]['last_updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.save_tasks()
    
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
            self.save_tasks()
    
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
                manager.update_task(task_id, status)
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
