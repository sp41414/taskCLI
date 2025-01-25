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
                json.dump({}, f, indent=4)
    
    def load_tasks(self):
        with open(self.filename, 'r') as f:
            self.tasks = json.load(f)
    
    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=4)
    
    def add_task(self, description):
        task_id = str(len(self.tasks) + 1)
        self.tasks[task_id] = {
            'id': task_id,
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
    
    def delete_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.save_tasks()
    
    def list_tasks(self, status=None):
        for task in self.tasks.values():
            if status is None or task['status'] == status:
                print(f"[{task['id']}] {task['description']} - ({task['status']})")
                print(f"created: {task['created_at']}")
                print(f"updated: {task['last_updated_at']}\n")

def main():
    manager = TaskManager
    try: 
        while True:
            print("\n1. add task\n2. update status\n3. delete task\n4. list all tasks")
            print("5. list todo\n6. list in progress\n7. list done\n8. exit")

            choice = input("enter choice: ")

            if choice == '1':
                desc = input('enter task description: ')
                manager.add_task(desc)
            elif choice == '2':
                manager.list_tasks()
                task_id = input('enter task id: ')
                status = input('enter status: ')
                manager.update_task(task_id, status)
            elif choice == '3':
                task_id = input('enter task id: ')
                manager.delete_task(task_id)
            elif choice == '4':
                manager.list_tasks()
            elif choice == '5':
                manager.list_tasks('todo')
            elif choice == '6':
                manager.list_tasks('in progress')
            elif choice == '7':
                manager.list_tasks('done')
            elif choice == '8':
                break
            else:
                print('invalid choice')
                
    except KeyboardInterrupt:
        print('exiting...')
        exit(0)


if __name__ == '__main__':
    main()
