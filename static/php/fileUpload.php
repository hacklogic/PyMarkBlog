<?php
session_start();

if (isset($_POST['type'])) {
    if (in_array($_FILES['file']['type'], array('image/jpeg', 'image/jpg', 'image/pjpeg', 'image/png', 'image/gif')) && $_POST['type'] !== 'image') {
        echo json_encode(array('name' => $_FILES['file']['name']));
    } elseif ($_POST['type'] !== 'file') {
        echo json_encode(array('name' => $_FILES['file']['name']));
    } else {
        echo 'error';
    }
} else {
    echo 'error';
}