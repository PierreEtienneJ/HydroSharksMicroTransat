<nav>
    <ul>
        <li><a href="index.php"> Accueil</a></li>
        <li><a href="sponsor.php"> Sponsor</a></li>
        <li><a href="projet.php"> Le projet</a></li>
        <li><a href="association.php"> L'association</a></li>
        <?php 
        if(empty($_SESSION['id'])){
            ?>
            <li><a href="compte.php"> Connexion</a></li>
        <?php
        }else{?>
            <li><a href="profil.php"> Profil</a></li>
        <?php } ?>
    </ul>
</nav>