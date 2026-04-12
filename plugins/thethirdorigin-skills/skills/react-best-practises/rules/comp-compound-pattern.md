# comp-compound-pattern

> Use the compound component pattern for related UI elements

## Why It Matters

Compound components give consumers full control over rendering order, styling, and conditional display of sub-elements. Instead of a single component with a complex configuration object, each sub-element is a standalone component that implicitly shares state through context.

Configuration-object APIs become unwieldy as features grow. Every new option requires a new prop, and consumers cannot insert custom elements between the built-in pieces. Compound components scale gracefully because adding a new sub-element is just a new component — no API changes needed.

## Bad

```tsx
// Config-object API — inflexible, hard to extend
interface TabConfig {
  label: string;
  content: React.ReactNode;
  icon?: React.ReactNode;
  disabled?: boolean;
}

function Tabs({ tabs, defaultIndex = 0 }: { tabs: TabConfig[]; defaultIndex?: number }) {
  const [activeIndex, setActiveIndex] = useState(defaultIndex);

  return (
    <div>
      <div className="tab-list" role="tablist">
        {tabs.map((tab, i) => (
          <button
            key={i}
            role="tab"
            disabled={tab.disabled}
            aria-selected={i === activeIndex}
            onClick={() => setActiveIndex(i)}
          >
            {tab.icon} {tab.label}
          </button>
        ))}
      </div>
      <div role="tabpanel">{tabs[activeIndex]?.content}</div>
    </div>
  );
}

// Consumer cannot reorder, wrap, or conditionally render individual tabs
<Tabs tabs={[{ label: "One", content: <PanelOne /> }, { label: "Two", content: <PanelTwo /> }]} />
```

## Good

```tsx
// Compound component API — consumers control structure
const TabsContext = createContext<{
  activeIndex: number;
  setActiveIndex: (index: number) => void;
}>({ activeIndex: 0, setActiveIndex: () => {} });

function Tabs({ defaultIndex = 0, children }: { defaultIndex?: number; children: React.ReactNode }) {
  const [activeIndex, setActiveIndex] = useState(defaultIndex);

  return (
    <TabsContext.Provider value={{ activeIndex, setActiveIndex }}>
      <div>{children}</div>
    </TabsContext.Provider>
  );
}

function TabList({ children }: { children: React.ReactNode }) {
  return <div role="tablist">{children}</div>;
}

function Tab({ index, children }: { index: number; children: React.ReactNode }) {
  const { activeIndex, setActiveIndex } = useContext(TabsContext);

  return (
    <button role="tab" aria-selected={activeIndex === index} onClick={() => setActiveIndex(index)}>
      {children}
    </button>
  );
}

function TabPanel({ index, children }: { index: number; children: React.ReactNode }) {
  const { activeIndex } = useContext(TabsContext);
  if (activeIndex !== index) return null;
  return <div role="tabpanel">{children}</div>;
}

// Consumer has full control
<Tabs defaultIndex={0}>
  <TabList>
    <Tab index={0}>Overview</Tab>
    <Tab index={1}>Details</Tab>
  </TabList>
  <TabPanel index={0}><OverviewContent /></TabPanel>
  <TabPanel index={1}><DetailsContent /></TabPanel>
</Tabs>
```

## See Also

- [comp-composition](comp-composition.md) - Compose components using children and render props
