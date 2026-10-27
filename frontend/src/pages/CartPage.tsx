import {
  Button,
  Container,
  Divider,
  List,
  ListItem,
  ListItemText,
  Typography,
} from "@mui/material";
import { Link } from "react-router-dom";

import { useCartStore } from "../store/cartStore";

export default function CartPage() {
  const items = useCartStore((state) => state.items);
  const removeFromCart = useCartStore((state) => state.removeFromCart);

  const total = items.reduce(
    (sum, item) => sum + Number(item.book.price) * item.quantity,
    0,
  );

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h3" gutterBottom>
        Shopping Cart
      </Typography>

      {items.length === 0 ? (
        <Typography>Your cart is empty.</Typography>
      ) : (
        <>
          <List>
            {items.map((item) => (
              <div key={item.book.id}>
                <ListItem
                  secondaryAction={
                    <Button
                      color="error"
                      onClick={() => removeFromCart(item.book.id)}
                    >
                      Remove
                    </Button>
                  }
                >
                  <ListItemText
                    primary={item.book.title}
                    secondary={`€${item.book.price} × ${item.quantity}`}
                  />
                </ListItem>

                <Divider />
              </div>
            ))}
          </List>

          <Typography variant="h5" sx={{ mt: 3 }}>
            Total: €{total.toFixed(2)}
          </Typography>

          <Button
            component={Link}
            to="/checkout"
            variant="contained"
            sx={{ mt: 2 }}
          >
            Checkout
          </Button>
        </>
      )}
    </Container>
  );
}