# task cli

a simple command-line interface for managing tasks

## features

- add new tasks with names and descriptions
- update task details (name, description, status)
- delete tasks
- list tasks by status
- persistent storage using json

## usage

run the program:

```bash
python main.py
```

available commands:

1. add task
2. update description
3. update name
4. update status
5. delete task
6. list all tasks
7. list todo tasks
8. list in-progress tasks
9. list done tasks
10. exit

## task status options

- todo
- in progress
- done

## data storage

tasks are stored in a local `tasks.json` file
