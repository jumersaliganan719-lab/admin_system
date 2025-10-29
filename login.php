<?php
session_start();
if (isset($_SESSION['admin'])) {
    header("Location: admin/dashboard.php");
    exit;
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
<div class="container">
    <h2>Admin Login</h2>
    <?php if (isset($_GET['error'])): ?>
        <p class="error"><?= htmlspecialchars($_GET['error']); ?></p>
    <?php endif; ?>
    <form method="POST" action="process_login.php">
        <label>Username</label>
        <input type="text" name="username" required>

        <label>Password</label>
        <input type="password" name="password" required>

        <button type="submit">Login</button>
    </form>
</div>
</body>
</html>
