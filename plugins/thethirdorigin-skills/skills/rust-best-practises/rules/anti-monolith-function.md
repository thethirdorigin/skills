# anti-monolith-function

> Split monolithic functions with multiple responsibilities into focused helpers

## Why It Matters

A 200-line function that validates input, queries the database, transforms data, and sends a response is hard to test, hard to review, and hard to modify. Testing the validation logic requires setting up a database. Changing the response format risks breaking the data transformation. Every modification touches the same function, increasing merge conflict risk.

Focused helper functions with a single responsibility can be tested in isolation, composed in different ways, and modified without side effects. Each function fits in a single screen, making code review efficient and bug localisation straightforward.

## Bad

```rust
pub async fn handle_create_order(req: Request) -> Response {
    // Validate input (30 lines)
    let body = req.body().await.unwrap();
    let order: CreateOrderRequest = serde_json::from_slice(&body).unwrap();
    if order.items.is_empty() {
        return Response::bad_request("No items");
    }
    for item in &order.items {
        if item.quantity == 0 {
            return Response::bad_request("Zero quantity");
        }
        if item.price < 0.0 {
            return Response::bad_request("Negative price");
        }
    }

    // Query database (40 lines)
    let pool = get_db_pool();
    let user = sqlx::query_as::<_, User>("SELECT * FROM users WHERE id = $1")
        .bind(order.user_id)
        .fetch_one(&pool)
        .await
        .unwrap();
    // ... more queries ...

    // Transform data (50 lines)
    let total = order.items.iter().map(|i| i.price * i.quantity as f64).sum::<f64>();
    let tax = total * 0.08;
    // ... more transformation ...

    // Build and send response (30 lines)
    let response_body = serde_json::to_vec(&OrderResponse {
        order_id: new_order.id,
        total: total + tax,
        // ...
    }).unwrap();
    Response::ok(response_body)
}
```

## Good

```rust
pub async fn handle_create_order(
    db: &PgPool,
    req: Request,
) -> Result<Response, AppError> {
    let order = parse_and_validate(req).await?;
    let user = fetch_user(db, order.user_id).await?;
    let priced_order = calculate_pricing(&order)?;
    let saved_order = save_order(db, &user, &priced_order).await?;
    Ok(build_response(&saved_order))
}

async fn parse_and_validate(req: Request) -> Result<CreateOrderRequest, AppError> {
    let body = req.body().await?;
    let order: CreateOrderRequest = serde_json::from_slice(&body)?;
    validate_items(&order.items)?;
    Ok(order)
}

fn validate_items(items: &[OrderItem]) -> Result<(), AppError> {
    if items.is_empty() {
        return Err(AppError::Validation("No items".into()));
    }
    for item in items {
        if item.quantity == 0 {
            return Err(AppError::Validation("Zero quantity".into()));
        }
    }
    Ok(())
}

fn calculate_pricing(order: &CreateOrderRequest) -> Result<PricedOrder, AppError> {
    let subtotal: Decimal = order.items.iter().map(|i| i.price * i.quantity).sum();
    let tax = subtotal * Decimal::new(8, 2);
    Ok(PricedOrder { subtotal, tax, total: subtotal + tax })
}

fn build_response(order: &SavedOrder) -> Response {
    Response::ok(serde_json::to_vec(&OrderResponse::from(order)).unwrap())
}
```

## See Also

- [anti-silence-clippy](anti-silence-clippy.md) - Fix warnings rather than suppress them
- [test-mockable-design](test-mockable-design.md) - Design for testability with traits
