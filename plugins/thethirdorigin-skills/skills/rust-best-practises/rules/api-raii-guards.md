# api-raii-guards

> Use RAII guard objects that acquire resources on creation and release them on Drop

## Why It Matters

RAII (Resource Acquisition Is Initialization) ties resource lifetime to scope -- the resource is acquired when the guard is created and released when the guard is dropped. This guarantee holds whether the scope exits via normal return, early return with `?`, or panic unwinding. Manual acquire/release pairs are fragile because every error path and early return must remember to clean up, and forgetting creates resource leaks that are silent and hard to diagnose.

Rust's ownership system makes RAII especially powerful. The compiler enforces that a guard exists exactly once, cannot be copied accidentally, and is dropped at a deterministic point. This eliminates entire classes of bugs: dangling locks, leaked file handles, orphaned temporary files, and unbalanced reference counts. The standard library uses this pattern extensively -- `MutexGuard`, `RwLockWriteGuard`, `JoinHandle`, and `File` all rely on `Drop` for cleanup.

## Bad

```rust
use std::fs;
use std::path::{Path, PathBuf};

struct TempWorkspace {
    path: PathBuf,
}

impl TempWorkspace {
    fn create(base: &Path) -> Result<Self, std::io::Error> {
        let path = base.join(format!("workspace-{}", uuid::Uuid::new_v4()));
        fs::create_dir_all(&path)?;
        Ok(Self { path })
    }

    // Caller must remember to call cleanup -- easy to forget on error paths
    fn cleanup(&self) -> Result<(), std::io::Error> {
        fs::remove_dir_all(&self.path)
    }
}

fn run_analysis(base: &Path) -> Result<AnalysisResult> {
    let workspace = TempWorkspace::create(base)?;

    let data = load_data(&workspace.path)?;      // If this fails, workspace leaks
    let result = analyze(&data)?;                  // If this fails, workspace leaks
    export_report(&workspace.path, &result)?;      // If this fails, workspace leaks

    workspace.cleanup()?; // Only reached on the happy path
    Ok(result)
}
```

## Good

```rust
use std::fs;
use std::path::{Path, PathBuf};

struct TempWorkspace {
    path: PathBuf,
}

impl TempWorkspace {
    fn create(base: &Path) -> Result<Self, std::io::Error> {
        let path = base.join(format!("workspace-{}", uuid::Uuid::new_v4()));
        fs::create_dir_all(&path)?;
        Ok(Self { path })
    }

    fn path(&self) -> &Path {
        &self.path
    }
}

impl Drop for TempWorkspace {
    fn drop(&mut self) {
        // Cleanup runs automatically on all exit paths: normal, early return, panic
        if let Err(err) = fs::remove_dir_all(&self.path) {
            eprintln!("warning: failed to clean up {}: {err}", self.path.display());
        }
    }
}

fn run_analysis(base: &Path) -> Result<AnalysisResult> {
    let workspace = TempWorkspace::create(base)?;

    // If any of these fail, `workspace` is dropped and cleanup runs automatically
    let data = load_data(workspace.path())?;
    let result = analyze(&data)?;
    export_report(workspace.path(), &result)?;

    Ok(result)
    // workspace dropped here -- cleanup runs even on the happy path
}

// The same pattern works for any acquire/release pair:
struct MetricsTimer {
    name: String,
    start: std::time::Instant,
    recorder: Arc<MetricsRecorder>,
}

impl MetricsTimer {
    fn start(name: impl Into<String>, recorder: Arc<MetricsRecorder>) -> Self {
        Self {
            name: name.into(),
            start: std::time::Instant::now(),
            recorder,
        }
    }
}

impl Drop for MetricsTimer {
    fn drop(&mut self) {
        self.recorder.record_duration(&self.name, self.start.elapsed());
    }
}
```

## References

- [RAII guards pattern](https://rust-unofficial.github.io/patterns/patterns/behavioural/RAII.html)

## See Also

- [unsafe-soundness](unsafe-soundness.md) - Ensure unsafe code maintains soundness invariants
