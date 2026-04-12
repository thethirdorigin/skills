# list-stable-keys

> Always provide unique, stable keys from entity IDs

## Why It Matters

React uses keys to track element identity across renders. When you provide stable keys derived from your data (such as database IDs or UUIDs), React can accurately determine which items were added, removed, or moved. This allows it to preserve component state correctly and perform minimal DOM updates.

When keys are unstable or non-unique, React loses track of which component belongs to which data item. This leads to subtle bugs where form inputs retain stale values, animations fire on the wrong elements, and controlled components display incorrect state after list mutations.

## Bad

```tsx
interface Task {
  id: string;
  title: string;
  completed: boolean;
}

function TaskList({ tasks }: { tasks: Task[] }) {
  return (
    <ul>
      {tasks.map((task, index) => (
        <li key={index}>
          <input
            type="checkbox"
            defaultChecked={task.completed}
          />
          {task.title}
        </li>
      ))}
    </ul>
  );
}
```

## Good

```tsx
interface Task {
  id: string;
  title: string;
  completed: boolean;
}

function TaskList({ tasks }: { tasks: Task[] }) {
  return (
    <ul>
      {tasks.map((task) => (
        <li key={task.id}>
          <input
            type="checkbox"
            defaultChecked={task.completed}
          />
          {task.title}
        </li>
      ))}
    </ul>
  );
}
```

## See Also

- [list-extract-items](list-extract-items.md) - Extract list items into separate components for readability and memoization
