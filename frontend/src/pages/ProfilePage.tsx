import { Button, Container, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

export default function ProfilePage() {
  const navigate = useNavigate();
  const loggedIn = Boolean(localStorage.getItem("access_token"));

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    navigate("/login");
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h3">My Account</Typography>

      <Typography sx={{ mt: 2 }}>
        {loggedIn ? "You are logged in." : "You are not logged in."}
      </Typography>

      {loggedIn && (
        <Button variant="contained" onClick={logout} sx={{ mt: 2 }}>
          Logout
        </Button>
      )}
    </Container>
  );
}