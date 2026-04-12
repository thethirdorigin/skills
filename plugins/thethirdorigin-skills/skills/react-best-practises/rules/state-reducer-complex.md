# state-reducer-complex

> Use useReducer for complex state with multiple interdependent fields

## Why It Matters

When a component manages several pieces of state that must change together — form fields with validation, wizard steps with progress tracking, or a data table with sorting, filtering, and pagination — separate `useState` calls make it easy to update one field while forgetting another. The component briefly renders with an inconsistent combination of old and new values.

A reducer centralises all state transitions into a single pure function. Each action describes what happened, and the reducer determines the complete new state. Transitions are atomic, testable in isolation, and impossible to leave half-finished.

## Bad

```tsx
function CheckoutWizard() {
  const [step, setStep] = useState(0);
  const [shippingAddress, setShippingAddress] = useState<Address | null>(null);
  const [paymentMethod, setPaymentMethod] = useState<Payment | null>(null);
  const [isValidating, setIsValidating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function handleNext() {
    setIsValidating(true);
    setError(null); // Forgetting this line leaves stale errors visible
    validateStep(step).then((valid) => {
      setIsValidating(false);
      if (valid) {
        setStep((s) => s + 1);
      }
    });
  }
}
```

## Good

```tsx
interface WizardState {
  step: number;
  shippingAddress: Address | null;
  paymentMethod: Payment | null;
  isValidating: boolean;
  error: string | null;
}

type WizardAction =
  | { type: "VALIDATE_START" }
  | { type: "VALIDATE_SUCCESS" }
  | { type: "VALIDATE_FAILURE"; error: string }
  | { type: "SET_SHIPPING"; address: Address }
  | { type: "SET_PAYMENT"; payment: Payment }
  | { type: "GO_BACK" };

function wizardReducer(state: WizardState, action: WizardAction): WizardState {
  switch (action.type) {
    case "VALIDATE_START":
      return { ...state, isValidating: true, error: null };
    case "VALIDATE_SUCCESS":
      return { ...state, isValidating: false, step: state.step + 1 };
    case "VALIDATE_FAILURE":
      return { ...state, isValidating: false, error: action.error };
    case "SET_SHIPPING":
      return { ...state, shippingAddress: action.address };
    case "SET_PAYMENT":
      return { ...state, paymentMethod: action.payment };
    case "GO_BACK":
      return { ...state, step: Math.max(0, state.step - 1), error: null };
  }
}

function CheckoutWizard() {
  const [state, dispatch] = useReducer(wizardReducer, {
    step: 0,
    shippingAddress: null,
    paymentMethod: null,
    isValidating: false,
    error: null,
  });

  async function handleNext() {
    dispatch({ type: "VALIDATE_START" });
    const result = await validateStep(state.step);
    dispatch(
      result.valid
        ? { type: "VALIDATE_SUCCESS" }
        : { type: "VALIDATE_FAILURE", error: result.message }
    );
  }
}
```

## See Also

- [state-local-simple](state-local-simple.md) - Use useState for simple isolated state
