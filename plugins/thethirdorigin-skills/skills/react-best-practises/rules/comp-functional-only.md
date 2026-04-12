# comp-functional-only

> Use function declarations for components, not class components or arrow function assignments

## Why It Matters

Function declarations are hoisted, which means they can be referenced before their position in the file without causing a temporal dead zone error. They also produce named stack traces in error boundaries and React DevTools, making debugging straightforward.

Class components require understanding of `this` binding, lifecycle method ordering, and cannot use hooks. Arrow function assignments (`const MyComponent = () => {}`) lack hoisting and produce anonymous entries in stack traces unless explicitly named. Function declarations are the simplest, most readable form and align with how the React team designs the hooks API.

## Bad

```tsx
// Class component — verbose, no hooks, confusing `this` binding
class UserProfile extends React.Component<UserProfileProps> {
  state = { isEditing: false };

  handleEdit = () => {
    this.setState({ isEditing: true });
  };

  render() {
    return (
      <div>
        <h1>{this.props.user.name}</h1>
        {this.state.isEditing ? (
          <EditForm user={this.props.user} />
        ) : (
          <button onClick={this.handleEdit}>Edit</button>
        )}
      </div>
    );
  }
}

// Arrow assignment — not hoisted, anonymous in stack traces
const UserProfile = ({ user }: UserProfileProps) => {
  const [isEditing, setIsEditing] = useState(false);
  return (
    <div>
      <h1>{user.name}</h1>
      {isEditing ? <EditForm user={user} /> : <button onClick={() => setIsEditing(true)}>Edit</button>}
    </div>
  );
};
```

## Good

```tsx
function UserProfile({ user }: UserProfileProps) {
  const [isEditing, setIsEditing] = useState(false);

  return (
    <div>
      <h1>{user.name}</h1>
      {isEditing ? (
        <EditForm user={user} />
      ) : (
        <button onClick={() => setIsEditing(true)}>Edit</button>
      )}
    </div>
  );
}
```

## See Also

- [comp-one-per-file](comp-one-per-file.md) - Export one page-level component per file
