import { Alert, Button, Container, Typography } from "@mui/material";
import { useState } from "react";
import { useCartStore } from "../store/cartStore";

export default function CheckoutPage() {
  const items = useCartStore((state) => state.items);
  const clearCart = useCartStore((state) => state.clearCart);
  const [success, setSuccess] = useState(false);

  const total = items.reduce(
    (sum, item) => sum + Number(item.book.price) * item.quantity,
    0,
  );

  const checkout = () => {
    setSuccess(true);
    clearCart();
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h3">Checkout</Typography>

      {success ? (
        <Alert severity="success" sx={{ mt: 3 }}>
          Order completed successfully.
        </Alert>
      ) : (
        <>
          <Typography variant="h5" sx={{ mt: 3 }}>
            Total: €{total.toFixed(2)}
          </Typography>

          <Button
            variant="contained"
            disabled={items.length === 0}
            onClick={checkout}
            sx={{ mt: 3 }}
          >
            Place Order
          </Button>
        </>
      )}
    </Container>
  );
}