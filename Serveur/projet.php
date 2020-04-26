<?php session_start(); ?>
<!DOCTYPE html>
<html>
    <head>
        <title>Hydrosharks : projet</title>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="css/style.css"/>
    </head>
    <body>
        <?php include("php/entete.php"); ?>
        <?php include("php/menus.php"); ?>

        <p><?php echo "Ceci est du texte"; ?></p>
        
        <a href="compte.php?nom=Dupont&amp;prenom=Jean">Dis-moi bonjour !</a>

        <?php include("php/piedpage.php"); ?>
        
    </body>
</html>