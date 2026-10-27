import { useState } from "react";
import { Alert, Button, Container, TextField, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    try {
      await api.post("users/", { username, email, password });
      navigate("/login");
    } catch {
      setError("Registration failed.");
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Typography variant="h3">Register</Typography>

      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}

      <form onSubmit={handleSubmit}>
        <TextField fullWidth label="Username" margin="normal"
          value={username} onChange={(e) => setUsername(e.target.value)} />

        <TextField fullWidth label="Email" margin="normal"
          value={email} onChange={(e) => setEmail(e.target.value)} />

        <TextField fullWidth type="password" label="Password" margin="normal"
          value={password} onChange={(e) => setPassword(e.target.value)} />

        <Button type="submit" variant="contained" sx={{ mt: 2 }}>
          Register
        </Button>
      </form>
    </Container>
  );
}