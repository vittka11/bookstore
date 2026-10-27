import { useEffect, useState } from "react";
import {
  Alert,
  Button,
  Card,
  CardActions,
  CardContent,
  CircularProgress,
  Container,
  Grid,
  Typography,
} from "@mui/material";
import { Link } from "react-router-dom";

import api from "../services/api";
import { useCartStore } from "../store/cartStore";
import type { Book } from "../types/book";

export default function BookListPage() {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const addToCart = useCartStore((state) => state.addToCart);

  useEffect(() => {
    api
      .get("books/")
      .then((response) => {
        const data = response.data.results ?? response.data;
        setBooks(data);
      })
      .catch(() => {
        setError("Could not load books.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <Container sx={{ mt: 5 }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h3" gutterBottom>
        Bookstore
      </Typography>

      {error && <Alert severity="error">{error}</Alert>}

      <Grid container spacing={3}>
        {books.map((book) => (
          <Grid key={book.id} size={{ xs: 12, sm: 6, md: 4 }}>
            <Card>
              <CardContent>
                <Typography variant="h5">{book.title}</Typography>

                <Typography color="text.secondary">
                  {book.author}
                </Typography>

                <Typography sx={{ mt: 2 }}>
                  €{book.price}
                </Typography>
              </CardContent>

              <CardActions>
                <Button
                  component={Link}
                  to={`/books/${book.id}`}
                >
                  Details
                </Button>

                <Button
                  variant="contained"
                  onClick={() => addToCart(book)}
                >
                  Add to cart
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}