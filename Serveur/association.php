<?php session_start(); ?>
<!DOCTYPE html>
<html>
    <head>
        <title>Hydrosharks : équipe</title>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="css/style.css"/>
    </head>
    <body>
        <?php include("php/entete.php"); ?>
        <?php include("php/menus.php"); ?>


        <?php 
            try{
                $bdd =new PDO('mysql:host=localhost;dbname=Hydroserv','superuser','123'); 
            }
            catch(Exception $e){
                die('Error :' . $e->getMessage());
            }   

            $reponse=$bdd->query('SELECT * FROM Equipe;');

            while($donnees=$reponse->fetch())
            { ?>
                <div class="equipe">
                <h2> <?php echo ucwords($donnees['nom']); ?> </h2>
                <p> <?php echo $donnees['commentaire']; ?> </p>

                <?php $reponseEtudiant=$bdd->query('SELECT nom,prenom, email, linkedin, commentaire FROM Etudiant WHERE id_equipe='.$donnees['id'].' ORDER BY promo;');
                while($donneesEtudiant=$reponseEtudiant->fetch())
                { ?>
                    <h3> <?php echo ucwords($donneesEtudiant['nom']).' '.ucwords($donneesEtudiant['prenom']); ?> 
                    <?php if($donneesEtudiant['linkedin'] != NULL){ ?>
                        <a href="<?php echo $donneesEtudiant['linkedin']; ?>" title="<?php echo $donneesEtudiant['nom'].' '.$donneesEtudiant['prenom']; ?>" target="_blank"a><img src="img/logo/linkedin.jpeg" alt="Linkedin" height="30"/> </a> 
                    <?php } ?>
                    </h3>
                    <?php if($donneesEtudiant['commentaire'] != NULL){ ?>
                        <p> <?php echo $donneesEtudiant['commentaire']; ?> </p>
                    <?php } ?>
            <? } 
            $reponseEtudiant->closeCursor();
        ?>
                </div>
        <?php } $reponse->closeCursor();?>


        <?php include("php/piedpage.php"); ?>

    </body>
</html>