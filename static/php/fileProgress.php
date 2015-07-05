<?php
session_start();
$uploadId = ini_get('session.upload_progress.prefix') . $_POST['upload_id'];
echo json_encode(isset($_SESSION[$uploadId]) ? $_SESSION[$uploadId] : '');