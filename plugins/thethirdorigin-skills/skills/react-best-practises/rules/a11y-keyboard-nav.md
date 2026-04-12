# a11y-keyboard-nav

> Ensure keyboard navigation works for all interactive elements

## Why It Matters

Many users navigate exclusively with a keyboard: people using screen readers, users with motor disabilities who rely on switch devices, power users who prefer keyboard shortcuts, and anyone with a temporarily broken mouse. If an interactive element only responds to mouse clicks, these users are completely locked out.

Custom widgets like dropdowns, menus, tabs, and modals need explicit keyboard handling to match the interaction patterns users expect. The WAI-ARIA Authoring Practices define standard key bindings for each widget type. Following these patterns means your custom components behave like native browser controls, which every user already knows how to operate.

## Bad

```tsx
interface Option {
  value: string;
  label: string;
}

function CustomDropdown({ options, onSelect }: {
  options: Option[];
  onSelect: (value: string) => void;
}) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="dropdown">
      {/* No keyboard support — only works with mouse */}
      <div className="dropdown-trigger" onClick={() => setIsOpen(!isOpen)}>
        Select an option
      </div>
      {isOpen && (
        <div className="dropdown-menu">
          {options.map((option) => (
            <div
              key={option.value}
              className="dropdown-item"
              onClick={() => {
                onSelect(option.value);
                setIsOpen(false);
              }}
            >
              {option.label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

## Good

```tsx
interface Option {
  value: string;
  label: string;
}

function CustomDropdown({ options, onSelect, label }: {
  options: Option[];
  onSelect: (value: string) => void;
  label: string;
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const optionRefs = useRef<(HTMLLIElement | null)[]>([]);

  const handleTriggerKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case "Enter":
      case " ":
      case "ArrowDown":
        e.preventDefault();
        setIsOpen(true);
        setActiveIndex(0);
        break;
      case "Escape":
        setIsOpen(false);
        break;
    }
  };

  const handleOptionKeyDown = (e: React.KeyboardEvent, index: number) => {
    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        setActiveIndex(Math.min(index + 1, options.length - 1));
        break;
      case "ArrowUp":
        e.preventDefault();
        setActiveIndex(Math.max(index - 1, 0));
        break;
      case "Enter":
      case " ":
        e.preventDefault();
        onSelect(options[index].value);
        setIsOpen(false);
        break;
      case "Escape":
        setIsOpen(false);
        break;
    }
  };

  useEffect(() => {
    if (isOpen && activeIndex >= 0) {
      optionRefs.current[activeIndex]?.focus();
    }
  }, [isOpen, activeIndex]);

  return (
    <div className="dropdown">
      <button
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        aria-label={label}
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={handleTriggerKeyDown}
      >
        {label}
      </button>
      {isOpen && (
        <ul role="listbox" aria-label={label}>
          {options.map((option, index) => (
            <li
              key={option.value}
              ref={(el) => { optionRefs.current[index] = el; }}
              role="option"
              tabIndex={-1}
              aria-selected={index === activeIndex}
              onClick={() => {
                onSelect(option.value);
                setIsOpen(false);
              }}
              onKeyDown={(e) => handleOptionKeyDown(e, index)}
            >
              {option.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

## See Also

- [a11y-focus-management](a11y-focus-management.md) - Maintain visible focus indicators and logical tab order
