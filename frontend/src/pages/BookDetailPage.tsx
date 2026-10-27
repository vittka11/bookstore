import { useEffect, useState } from "react";
import {
  Alert,
  Button,
  CircularProgress,
  Container,
  Typography,
} from "@mui/material";
import { useParams } from "react-router-dom";

import api from "../services/api";
import { useCartStore } from "../store/cartStore";
import type { Book } from "../types/book";

export default function BookDetailPage() {
  const { id } = useParams();
  const [book, setBook] = useState<Book | null>(null);
  const [error, setError] = useState("");

  const addToCart = useCartStore((state) => state.addToCart);

  useEffect(() => {
    api
      .get(`books/${id}/`)
      .then((response) => setBook(response.data))
      .catch(() => setError("Could not load book."));
  }, [id]);

  if (error) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  if (!book) {
    return (
      <Container sx={{ mt: 5 }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h3">{book.title}</Typography>

      <Typography variant="h5" color="text.secondary" sx={{ mt: 1 }}>
        {book.author}
      </Typography>

      <Typography sx={{ mt: 3 }}>
        {book.description}
      </Typography>

      <Typography variant="h5" sx={{ mt: 3 }}>
        €{book.price}
      </Typography>

      <Typography sx={{ mt: 1 }}>
        In stock: {book.stock}
      </Typography>

      <Button
        variant="contained"
        sx={{ mt: 3 }}
        onClick={() => addToCart(book)}
      >
        Add to cart
      </Button>
    </Container>
  );
}