# comp-composition

> Compose components using children and render props instead of inheritance

## Why It Matters

Composition is more flexible than inheritance. Components composed through children and render props can be rearranged, wrapped, and combined without modifying the parent component. This keeps each component focused on a single responsibility while allowing consumers to assemble them freely.

Inheritance creates rigid hierarchies where changes to a base class ripple through every subclass. React's component model is explicitly designed around composition — the React team recommends never using inheritance for component reuse.

## Bad

```tsx
// Inheritance hierarchy — rigid, hard to extend
class Button extends React.Component<ButtonProps> {
  render() {
    return <button className="btn">{this.props.label}</button>;
  }
}

class IconButton extends Button {
  render() {
    return (
      <button className="btn">
        <Icon name={this.props.icon} />
        {this.props.label}
      </button>
    );
  }
}

class LoadingIconButton extends IconButton {
  render() {
    if (this.props.isLoading) {
      return <button className="btn" disabled><Spinner /></button>;
    }
    return super.render();
  }
}
```

## Good

```tsx
// Composition via children — flexible, each piece is independent
function Card({ children }: { children: React.ReactNode }) {
  return <div className="card">{children}</div>;
}

function CardHeader({ children }: { children: React.ReactNode }) {
  return <div className="card-header">{children}</div>;
}

function CardBody({ children }: { children: React.ReactNode }) {
  return <div className="card-body">{children}</div>;
}

// Consumers compose freely
function UserCard({ user }: { user: User }) {
  return (
    <Card>
      <CardHeader>
        <Avatar src={user.avatarUrl} />
        <h2>{user.name}</h2>
      </CardHeader>
      <CardBody>
        <p>{user.bio}</p>
      </CardBody>
    </Card>
  );
}
```

## See Also

- [comp-compound-pattern](comp-compound-pattern.md) - Use the compound component pattern for related UI elements
- [comp-custom-hooks](comp-custom-hooks.md) - Extract shared logic into custom hooks
