# hook-useReducer-complex

> Switch from useState to useReducer when a component has 4+ related state variables

## Why It Matters

When multiple `useState` calls manage related data, updating one piece of state without the others creates inconsistent intermediate states. For example, setting `isSubmitting` to true while forgetting to clear `error` leaves the component in an impossible state. Each `setState` call triggers a separate re-render, and between those renders the component displays a combination of old and new values.

A reducer updates all related fields atomically in response to a single dispatched action. State transitions are explicit and testable — you can unit test the reducer function in isolation, and every valid state is defined by the action handlers.

## Bad

```tsx
function RegistrationForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  async function handleSubmit() {
    setIsSubmitting(true);
    setSubmitError(null); // Easy to forget this line
    setErrors({});        // ...or this one
    try {
      await registerUser({ name, email });
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : "Unknown error");
      setIsSubmitting(false); // Must remember to reset in every branch
    }
  }
}
```

## Good

```tsx
interface FormState {
  name: string;
  email: string;
  errors: Record<string, string>;
  isSubmitting: boolean;
  submitError: string | null;
}

type FormAction =
  | { type: "SET_FIELD"; field: string; value: string }
  | { type: "SUBMIT_START" }
  | { type: "SUBMIT_SUCCESS" }
  | { type: "SUBMIT_FAILURE"; error: string }
  | { type: "RESET" };

const initialState: FormState = {
  name: "",
  email: "",
  errors: {},
  isSubmitting: false,
  submitError: null,
};

function formReducer(state: FormState, action: FormAction): FormState {
  switch (action.type) {
    case "SET_FIELD":
      return { ...state, [action.field]: action.value, errors: {} };
    case "SUBMIT_START":
      return { ...state, isSubmitting: true, submitError: null, errors: {} };
    case "SUBMIT_SUCCESS":
      return { ...initialState };
    case "SUBMIT_FAILURE":
      return { ...state, isSubmitting: false, submitError: action.error };
    case "RESET":
      return initialState;
  }
}

function RegistrationForm() {
  const [state, dispatch] = useReducer(formReducer, initialState);

  async function handleSubmit() {
    dispatch({ type: "SUBMIT_START" });
    try {
      await registerUser({ name: state.name, email: state.email });
      dispatch({ type: "SUBMIT_SUCCESS" });
    } catch (err) {
      dispatch({
        type: "SUBMIT_FAILURE",
        error: err instanceof Error ? err.message : "Unknown error",
      });
    }
  }
}
```

## See Also

- [state-local-simple](state-local-simple.md) - Use useState for simple, isolated state
